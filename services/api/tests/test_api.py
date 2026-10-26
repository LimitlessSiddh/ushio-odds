from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_fixture_odds_and_calculator_contracts() -> None:
    board = client.get("/v1/odds?sport=icehockey_nhl&market=h2h")
    assert board.status_code == 200
    assert board.json()["mode"] == "fixture"
    assert board.json()["games"]

    response = client.post("/v1/calculators/hedge", json={"odds": [-110, 115], "amount": "250", "mode": "budget"})
    assert response.status_code == 200
    assert response.json()["is_theoretical_arb"] is True


def test_invalid_calculator_request_is_explicit() -> None:
    response = client.post("/v1/calculators/hedge", json={"odds": [0, -110], "amount": "250"})
    assert response.status_code == 422


def test_manual_ledger_contract_persists_a_record() -> None:
    with TestClient(app) as runtime:
        response = runtime.post("/v1/ledger", json={"occurred_on": "2026-10-26", "event_name": "Fixture matchup", "books": "Book A / Book B", "status": "settled", "total_stake": "250.00", "returned": "252.80", "fees": "0.00"})
        assert response.status_code == 201
        records = runtime.get("/v1/ledger")
        assert records.status_code == 200
        assert any(row["id"] == response.json()["id"] for row in records.json())
