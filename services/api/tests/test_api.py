from fastapi.testclient import TestClient

from app.main import app
from app.provider import normalise_odds_payload

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


def test_manual_ledger_contract_persists_a_record() -> None:
    with TestClient(app) as runtime:
        response = runtime.post("/v1/ledger", json={"occurred_on": "2026-10-26", "event_name": "Fixture matchup", "books": "Book A / Book B", "status": "settled", "total_stake": "250.00", "returned": "252.80", "fees": "0.00"})
        assert response.status_code == 201
        records = runtime.get("/v1/ledger")
        assert records.status_code == 200
        assert any(row["id"] == response.json()["id"] for row in records.json())


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
