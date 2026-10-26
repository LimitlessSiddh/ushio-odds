from decimal import Decimal, ROUND_HALF_UP
import json
from os import getenv
from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .domain import CalculationError, calculate_hedge
from .fixtures import fixture_board
from .persistence import PairLedgerRecord, SavedCalculation, create_schema, new_id, session
from .provider import OddsApiAdapter

app = FastAPI(title="Ushio Odds API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["*"])


@app.on_event("startup")
def startup() -> None:
    create_schema()


class HedgeRequest(BaseModel):
    odds: list[int] = Field(min_length=2)
    amount: str
    mode: Literal["budget", "fixed_first"] = "budget"


class SavedCalculationRequest(BaseModel):
    title: str = Field(min_length=1, max_length=180)
    payload: dict


class LedgerRecordRequest(BaseModel):
    occurred_on: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    event_name: str = Field(min_length=1, max_length=180)
    books: str = Field(min_length=3, max_length=240)
    status: Literal["settled", "open", "void"]
    total_stake: str
    returned: str
    fees: str = "0"


@app.get("/v1/health")
def health() -> dict:
    provider = OddsApiAdapter().status()
    return {"status": "ok", "data_mode": provider.mode, "provider_key_configured": provider.configured, "provider_message": provider.message}


@app.get("/v1/odds")
def odds(sport: str = Query("icehockey_nhl"), market: str = Query("h2h")) -> dict:
    return fixture_board(sport, market)


@app.get("/v1/capabilities")
def capabilities() -> dict:
    provider = OddsApiAdapter().status()
    return fixture_board("all", "all")["capabilities"] | {"mode": provider.mode, "region": provider.region, "credit_floor": provider.credit_floor, "message": provider.message}


@app.post("/v1/calculators/hedge")
def hedge(request: HedgeRequest) -> dict:
    try:
        return calculate_hedge(request.odds, Decimal(request.amount), request.mode)
    except (CalculationError, ValueError) as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


def cents(value: str) -> int:
    amount = Decimal(value)
    if amount < 0:
        raise ValueError("Money values cannot be negative.")
    return int((amount * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


@app.get("/v1/saved-calculations")
def list_saved_calculations() -> list[dict]:
    with session() as database:
        rows = database.query(SavedCalculation).order_by(SavedCalculation.created_at.desc()).all()
        return [{"id": row.id, "title": row.title, "payload": json.loads(row.payload), "created_at": row.created_at.isoformat()} for row in rows]


@app.post("/v1/saved-calculations", status_code=201)
def save_calculation(request: SavedCalculationRequest) -> dict:
    row = SavedCalculation(id=new_id(), title=request.title, payload=json.dumps(request.payload, separators=(",", ":")))
    with session() as database:
        database.add(row)
        database.commit()
        database.refresh(row)
    return {"id": row.id, "title": row.title, "created_at": row.created_at.isoformat()}


@app.get("/v1/ledger")
def list_ledger() -> list[dict]:
    with session() as database:
        rows = database.query(PairLedgerRecord).order_by(PairLedgerRecord.occurred_on.desc()).all()
        return [{"id": row.id, "occurred_on": row.occurred_on, "event_name": row.event_name, "books": row.books, "status": row.status, "total_stake": f"{row.total_stake_minor / 100:.2f}", "returned": f"{row.returned_minor / 100:.2f}", "fees": f"{row.fees_minor / 100:.2f}", "source": row.source} for row in rows]


@app.post("/v1/ledger", status_code=201)
def create_ledger_record(request: LedgerRecordRequest) -> dict:
    try:
        stake, returned, fees = cents(request.total_stake), cents(request.returned), cents(request.fees)
    except Exception as error:
        raise HTTPException(status_code=422, detail="Ledger money values must be non-negative decimal strings.") from error
    if stake == 0:
        raise HTTPException(status_code=422, detail="Total stake must be greater than zero.")
    if request.status == "open" and (returned != 0 or fees != 0):
        raise HTTPException(status_code=422, detail="Open records must have zero returned amount and fees.")
    if request.status == "void" and fees != 0:
        raise HTTPException(status_code=422, detail="Voided records must have zero fees.")
    row = PairLedgerRecord(id=new_id(), occurred_on=request.occurred_on, event_name=request.event_name, books=request.books, status=request.status, total_stake_minor=stake, returned_minor=returned, fees_minor=fees)
    with session() as database:
        database.add(row)
        database.commit()
        database.refresh(row)
    return {"id": row.id}
