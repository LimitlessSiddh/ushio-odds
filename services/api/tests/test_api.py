from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.persistence import Base
from app.provider import OddsApiAdapter, normalise_odds_payload, persist_validated_provider_market
from app.quote_lifecycle import QuoteLifecycleError


@pytest.fixture
def database():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with sessionmaker(engine)() as runtime:
        yield runtime

def test_fixture_odds_and_calculator_contracts() -> None:
    with TestClient(app) as client:
        board = client.get("/v1/odds?sport=icehockey_nhl&market=h2h")
        assert board.status_code == 200
        assert board.json()["mode"] == "fixture"
        assert board.json()["games"]

        response = client.post("/v1/calculators/hedge", json={"odds": [-110, 115], "amount": "250", "mode": "budget"})
        assert response.status_code == 200
        assert response.json()["is_theoretical_arb"] is True

        prop_board = client.get("/v1/odds?sport=basketball_nba&market=player_points")
        assert prop_board.status_code == 200
        assert prop_board.json()["games"][0]["outcomes"][0].endswith("points")
        assert prop_board.json()["capabilities"]["books"][-1] == "Rainbet"
        assert len(prop_board.json()["games"][0]["quotes"]) == 11
        assert next(quote for quote in prop_board.json()["games"][0]["quotes"] if quote["book"] == "ToonieBet")["region_status"] == "excluded"

        opportunities = client.get("/v1/opportunities?sport=icehockey_nhl&market=h2h")
        assert opportunities.status_code == 200
        assert opportunities.json()["opportunities"][0]["books"][0] != opportunities.json()["opportunities"][0]["books"][1]
        assert "ToonieBet" not in opportunities.json()["opportunities"][0]["books"]
        assert float(opportunities.json()["opportunities"][0]["minimum_profit"]) > 0
        candidate = opportunities.json()["opportunities"][0]
        assert len(candidate["selected_quote_version_ids"]) == 2
        assert candidate["period"] == "full_game"
        assert candidate["mode"] == "indicative"


def test_invalid_calculator_request_is_explicit() -> None:
    with TestClient(app) as client:
        response = client.post("/v1/calculators/hedge", json={"odds": [0, -110], "amount": "250"})
        assert response.status_code == 422


def test_local_dev_cors_allows_vite_fallback_port() -> None:
    with TestClient(app) as client:
        response = client.options("/v1/health", headers={"Origin": "http://127.0.0.1:5175", "Access-Control-Request-Method": "GET"})
        assert response.status_code == 200
        assert response.headers["access-control-allow-origin"] == "http://127.0.0.1:5175"


def test_manual_ledger_contract_persists_a_record() -> None:
    with TestClient(app) as runtime:
        response = runtime.post("/v1/ledger", json={"occurred_on": "2026-10-26", "event_name": "Fixture matchup", "books": "Book A / Book B", "status": "settled", "total_stake": "250.00", "returned": "252.80", "fees": "0.00"})
        assert response.status_code == 201
        records = runtime.get("/v1/ledger")
        assert records.status_code == 200
        assert any(row["id"] == response.json()["id"] for row in records.json())


def test_ledger_provenance_requires_complete_sourced_legs() -> None:
    with TestClient(app) as runtime:
        base = {"occurred_on": "2026-10-28", "event_name": "Provenance", "books": "A / B", "status": "settled", "total_stake": "100", "returned": "102"}
        rejected = runtime.post("/v1/ledger", json=base | {"provenance": {"kind": "sourced-pair", "legs": [{"book": "A"}]}})
        assert rejected.status_code == 422
        accepted = runtime.post("/v1/ledger", json=base | {"provenance": {"kind": "sourced-pair", "legs": [{"book": "A", "quote_version_id": "quote-a", "stake": "50", "returned": "51", "status": "settled", "settlement_context": "full-game"}, {"book": "B", "manual_source_marker": "manual receipt", "stake": "50", "returned": "51", "status": "settled", "settlement_context": "full-game"}]}})
        assert accepted.status_code == 201
        saved = next(row for row in runtime.get("/v1/ledger").json() if row["id"] == accepted.json()["id"])
        assert saved["provenance"]["kind"] == "sourced-pair"
        assert saved["provenance"]["legs"][0]["stake_minor"] == 5000


def test_saved_calculation_survives_a_new_app_client() -> None:
    payload = {"title": "Fixture hedge", "payload": {"odds": [-110, 115], "result": {"minimum_profit": "1.00"}}}
    with TestClient(app) as first:
        created = first.post("/v1/saved-calculations", json=payload)
        assert created.status_code == 201
    with TestClient(app) as restarted:
        rows = restarted.get("/v1/saved-calculations")
        assert any(row["id"] == created.json()["id"] and row["payload"] == payload["payload"] for row in rows.json())


def test_ledger_correction_is_immutable_and_changes_the_projection() -> None:
    with TestClient(app) as runtime:
        created = runtime.post("/v1/ledger", json={"occurred_on": "2026-10-27", "event_name": "Fixture correction", "books": "Book A / Book B", "status": "open", "total_stake": "100.00", "returned": "0", "fees": "0"})
        corrected = runtime.post(f"/v1/ledger/{created.json()['id']}/corrections", json={"reason": "Result settled", "status": "settled", "total_stake": "100.00", "returned": "108.50", "fees": "0.50"})
        assert corrected.status_code == 201
        record = next(row for row in runtime.get("/v1/ledger").json() if row["id"] == created.json()["id"])
        assert record["status"] == "settled"
        assert record["returned"] == "108.50"
        assert record["fees"] == "0.50"
        assert record["correction_count"] == 1
        assert record["original"] == {"status": "open", "total_stake": "100.00", "returned": "0.00", "fees": "0.00", "created_at": record["original"]["created_at"]}
        audit = runtime.get(f"/v1/ledger/{created.json()['id']}/corrections")
        assert audit.status_code == 200
        assert audit.json()[0]["reason"] == "Result settled"


def test_ledger_correction_rejects_an_invalid_open_projection() -> None:
    with TestClient(app) as runtime:
        created = runtime.post("/v1/ledger", json={"occurred_on": "2026-10-27", "event_name": "Fixture correction validation", "books": "Book A / Book B", "status": "settled", "total_stake": "100.00", "returned": "108.50", "fees": "0"})
        correction = runtime.post(f"/v1/ledger/{created.json()['id']}/corrections", json={"reason": "Incorrect open amount", "status": "open", "total_stake": "100.00", "returned": "1.00", "fees": "0"})
        assert correction.status_code == 422
        assert correction.json()["detail"] == "Open records must have zero returned amount and fees."


def test_ledger_summary_uses_effective_projection_without_open_or_void_double_counting() -> None:
    with TestClient(app) as runtime:
        settled = runtime.post("/v1/ledger", json={"occurred_on": "2026-10-28", "event_name": "Summary settled", "books": "A / B", "status": "settled", "total_stake": "100", "returned": "110", "fees": "1"}).json()["id"]
        runtime.post(f"/v1/ledger/{settled}/corrections", json={"reason": "Correct return", "status": "settled", "total_stake": "100", "returned": "108", "fees": "1"})
        runtime.post("/v1/ledger", json={"occurred_on": "2026-10-28", "event_name": "Summary open", "books": "A / B", "status": "open", "total_stake": "50", "returned": "0", "fees": "0"})
        runtime.post("/v1/ledger", json={"occurred_on": "2026-10-28", "event_name": "Summary void", "books": "A / B", "status": "void", "total_stake": "25", "returned": "25", "fees": "0"})
        summary = runtime.get("/v1/ledger/summary")
        assert summary.status_code == 200
        totals = summary.json()
        assert totals["settled_stake_minor"] >= 10000
        assert totals["open_stake_minor"] >= 5000
        assert totals["method"].startswith("effective projection")


def test_watchlist_toggle_persists_and_removes() -> None:
    with TestClient(app) as runtime:
        first = runtime.post("/v1/watchlist", json={"event_id": "fixture-event"})
        assert first.status_code == 200
        assert first.json()["watched"] is True
        assert "fixture-event" in runtime.get("/v1/watchlist").json()
        second = runtime.post("/v1/watchlist", json={"event_id": "fixture-event"})
        assert second.json()["watched"] is False


def test_provider_normaliser_excludes_incomplete_or_three_way_groups() -> None:
    payload = [{"id": "fixture-event", "sport_key": "basketball_nba", "sport_title": "NBA", "away_team": "Away", "home_team": "Home", "commence_time": "2026-10-26T00:00:00Z", "bookmakers": [{"title": "Stake", "last_update": "2026-10-26T00:00:00Z", "markets": [{"key": "player_points", "outcomes": [{"name": "Over", "description": "Sample Player", "point": 20.5, "price": 110}, {"name": "Under", "description": "Sample Player", "point": 20.5, "price": -130}]}]}, {"title": "Betway", "last_update": "2026-10-26T00:00:00Z", "markets": [{"key": "player_points", "outcomes": [{"name": "Over", "description": "Sample Player", "point": 20.5, "price": 105}, {"name": "Under", "description": "Sample Player", "point": 20.5, "price": -125}]}, {"key": "h2h", "outcomes": [{"name": "Away", "price": 200}, {"name": "Home", "price": 150}, {"name": "Draw", "price": 220}]}]}, {"title": "Unselected Book", "last_update": "2026-10-26T00:00:00Z", "markets": [{"key": "player_points", "outcomes": [{"name": "Over", "description": "Sample Player", "point": 20.5, "price": 130}, {"name": "Under", "description": "Sample Player", "point": 20.5, "price": -150}]}]}]}]
    board = normalise_odds_payload(payload, region="ca", remaining=100)
    assert len(board["games"]) == 1
    assert board["games"][0]["market"] == "player_points"
    assert board["games"][0]["outcomes"] == ["Sample Player Over 20.5", "Sample Player Under 20.5"]
    assert [quote["book"] for quote in board["games"][0]["quotes"]] == ["Stake", "Betway"]


def test_provider_coverage_summary_explains_empty_and_never_retains_a_key() -> None:
    payload = [{"id": "coverage-event", "sport_key": "icehockey_nhl", "sport_title": "NHL", "away_team": "Away", "home_team": "Home", "bookmakers": [
        {"title": "Unknown CA", "last_update": "2026-10-29T12:00:00Z", "markets": [{"key": "h2h", "outcomes": [{"name": "Away", "price": 110}, {"name": "Home", "price": -120}]}]},
        {"title": "Stake", "markets": [{"key": "h2h", "outcomes": [{"name": "Away", "price": 110}, {"name": "Home", "price": -120}]}]},
        {"title": "ToonieBet", "markets": [{"key": "h2h", "outcomes": [{"name": "Away", "price": 110}, {"name": "Home", "price": -120}]}]},
        {"title": "Betway", "markets": [{"key": "h2h", "outcomes": [{"name": "Away", "price": 200}, {"name": "Home", "price": 150}, {"name": "Draw", "price": 220}]}]},
    ]}]
    board = normalise_odds_payload(payload, region="ca", remaining=99)
    summary = board["coverage_summary"]
    assert board["games"] == []
    assert summary["raw_event_count"] == 1
    assert summary["raw_bookmaker_count"] == 4
    assert summary["raw_market_keys"] == ["h2h"]
    assert summary["selected_book_title_matches"] == {"Betway": ["Betway"], "Stake": ["Stake"]}
    assert summary["rejection_counts"]["unknown_book"] == 1
    assert summary["rejection_counts"]["excluded_book"] == 1
    assert summary["rejection_counts"]["invalid_two_way_market"] >= 1
    assert summary["rejection_counts"]["one_eligible_book"] >= 1
    assert summary["source_timing"]["available"] is True
    assert "apiKey" not in str(summary)
    assert "secret" not in str(summary).lower()


def test_provider_coverage_summary_accepts_two_selected_books_with_missing_source_times() -> None:
    payload = [{"id": "eligible-event", "sport_key": "icehockey_nhl", "sport_title": "NHL", "away_team": "Away", "home_team": "Home", "bookmakers": [
        {"title": "Stake", "markets": [{"key": "h2h", "outcomes": [{"name": "Away", "price": 110}, {"name": "Home", "price": -120}]}]},
        {"title": "Betway", "markets": [{"key": "h2h", "outcomes": [{"name": "Away", "price": 105}, {"name": "Home", "price": -125}]}]},
    ]}]
    board = normalise_odds_payload(payload, region="ca", remaining=99)
    assert len(board["games"]) == 1
    assert board["coverage_summary"]["accepted_market_count"] == 1
    assert board["coverage_summary"]["source_timing"] == {"available": False, "timestamp_count": 0, "earliest": None, "latest": None}


def test_successful_empty_refresh_persists_one_request_level_observation(monkeypatch) -> None:
    empty_board = normalise_odds_payload([], region="ca", remaining=98)
    monkeypatch.setattr(OddsApiAdapter, "fetch_selected_market", lambda self, sport, market: empty_board)
    monkeypatch.setattr(OddsApiAdapter, "status", lambda self: type("Status", (), {"configured": True, "region": "ca", "credit_floor": 25})())
    with TestClient(app) as runtime:
        response = runtime.post("/v1/provider/refresh", json={"sport": "icehockey_nhl", "market": "h2h"})
        assert response.status_code == 200
        body = response.json()
        assert body["observation_state"] == "provider-observed-not-revalidated"
        assert body["evidence"]["outcome"] == "observed-empty"
        assert body["coverage_summary"]["raw_event_count"] == 0
        evidence = runtime.get("/v1/provider/evidence").json()
        row = next(item for item in evidence if item["id"] == body["evidence"]["id"])
        assert row["details"]["coverage_summary"] == body["coverage_summary"]
        assert "apiKey" not in str(row)


def test_missing_key_creates_deferred_capability_evidence() -> None:
    with TestClient(app) as runtime:
        response = runtime.post("/v1/provider/refresh", json={"sport": "icehockey_nhl", "market": "h2h"})
        assert response.status_code == 409
        evidence = runtime.get("/v1/provider/evidence")
        assert evidence.status_code == 200
        assert any(row["outcome"] == "deferred" and row["sport"] == "icehockey_nhl" for row in evidence.json())


def test_provider_lifecycle_contract_rejects_missing_period_and_unsupported_fx(database) -> None:
    base = {"provider": "permitted-sample", "region": "ca", "book": "Stake", "event_id": "provider-sample", "sport": "icehockey_nhl", "league": "NHL", "away": "Away", "home": "Home", "market": "h2h", "period": "full_game", "settlement_assumptions": "regulation-included", "source_timestamp": "2026-10-28T12:00:00Z", "quote_status": "active", "fx": "CAD"}
    first = base | {"outcome": "Away", "position": 0, "price": 110}
    second = base | {"outcome": "Home", "position": 1, "price": -120}
    versions = persist_validated_provider_market(database, [first, second], received_at="2026-10-28T12:00:01Z")
    assert len(versions) == 2
    missing_period = dict(first)
    missing_period["period"] = ""
    with pytest.raises(QuoteLifecycleError, match="period"):
        persist_validated_provider_market(database, [missing_period, second], received_at="2026-10-28T12:00:01Z")
    with pytest.raises(QuoteLifecycleError, match="fees or FX"):
        persist_validated_provider_market(database, [first | {"fx": "USD"}, second | {"fx": "USD"}], received_at="2026-10-28T12:00:01Z")
