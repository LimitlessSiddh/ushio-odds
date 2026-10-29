from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
import json
from os import getenv
from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
from pydantic import BaseModel, Field

from .domain import CalculationError, calculate_hedge
from .fixtures import fixture_board
from .opportunities import detect_two_way_opportunities
from .persistence import Book, CanonicalEvent, Market, Outcome, PairLedgerCorrection, PairLedgerRecord, ProviderCapabilityEvidence, Quote, QuoteVersion, SavedCalculation, WatchlistEntry, create_schema, new_id, session
from .provider import OddsApiAdapter
from .quote_lifecycle import expire_current_quotes, ingest_market_observations, is_active

app = FastAPI(title="Ushio Odds API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?", allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["*"])


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
    provenance: dict | None = None


class LedgerCorrectionRequest(BaseModel):
    reason: str = Field(min_length=3, max_length=300)
    status: Literal["settled", "open", "void"]
    total_stake: str
    returned: str
    fees: str = "0"


class ProviderRefreshRequest(BaseModel):
    sport: str = Field(min_length=1, max_length=100)
    market: str = Field(min_length=1, max_length=100)


class WatchlistRequest(BaseModel):
    event_id: str = Field(min_length=1, max_length=180)


@app.get("/v1/health")
def health() -> dict:
    provider = OddsApiAdapter().status()
    return {"status": "ok", "data_mode": provider.mode, "provider_key_configured": provider.configured, "provider_message": provider.message}


@app.get("/v1/odds")
def odds(sport: str = Query("icehockey_nhl"), market: str = Query("h2h")) -> dict:
    return fixture_board(sport, market)


@app.get("/v1/opportunities")
def opportunities(sport: str = Query("all"), market: str = Query("all")) -> dict:
    board = fixture_board(sport, market)
    received_at = datetime.now(timezone.utc)
    with session() as database:
        for game in board["games"]:
            for quote in game["quotes"]:
                observations = [{"provider": "deterministic-fixture", "region": board["region"], "book": quote["book"], "event_id": game["id"], "sport": game["sport"], "league": game["league"], "away": game["away"], "home": game["home"], "commence_time": game["commence_time"], "market": game["market"], "period": game["period"], "line": game.get("line"), "settlement_assumptions": "fixture-defined", "outcome": outcome, "position": position, "price": quote["prices"][position], "source_timestamp": board["as_of"], "status": "active", "raw_reference": f"fixture:{game['id']}:{quote['book']}"} for position, outcome in enumerate(game["outcomes"])]
                ingest_market_observations(database, observations, received_at=received_at, ttl_seconds=300)
        expire_current_quotes(database, now=received_at)
        database.commit()
        games = lifecycle_games(database, now=received_at)
    return {"mode": board["mode"], "provider": board["provider"], "opportunities": detect_two_way_opportunities(games)}


def lifecycle_games(database, *, now: datetime) -> list[dict]:
    """Rebuild the comparison shape only from active, exact, versioned quotes."""
    rows = (database.query(QuoteVersion, Book, Outcome, Market, CanonicalEvent).join(Quote, Quote.id == QuoteVersion.quote_id).join(Book, Book.id == Quote.book_id).join(Outcome, Outcome.id == Quote.outcome_id).join(Market, Market.id == Outcome.market_id).join(CanonicalEvent, CanonicalEvent.id == Market.event_id).filter(QuoteVersion.is_current.is_(True), QuoteVersion.status == "active").all())
    grouped: dict[str, dict] = {}
    for version, book, outcome, market, event in rows:
        if not is_active(version, now=now):
            continue
        game = grouped.setdefault(market.id, {"id": event.source_event_id, "away": event.away, "home": event.home, "market": market.key, "period": market.period, "line": market.line, "outcomes": {}, "quotes": {}})
        game["outcomes"][outcome.position] = outcome.label
        quote = game["quotes"].setdefault(book.name, {"book": book.name, "prices": {}, "quote_version_ids": {}})
        quote["prices"][outcome.position] = version.american_price
        quote["quote_version_ids"][outcome.position] = version.id
    result = []
    for game in grouped.values():
        if sorted(game["outcomes"]) != [0, 1]:
            continue
        quotes = [{"book": quote["book"], "prices": [quote["prices"][0], quote["prices"][1]], "quote_version_ids": [quote["quote_version_ids"][0], quote["quote_version_ids"][1]]} for quote in game["quotes"].values() if sorted(quote["prices"]) == [0, 1]]
        if len(quotes) >= 2:
            result.append({**game, "outcomes": [game["outcomes"][0], game["outcomes"][1]], "quotes": quotes})
    return result


@app.get("/v1/capabilities")
def capabilities() -> dict:
    provider = OddsApiAdapter().status()
    return fixture_board("all", "all")["capabilities"] | {"mode": provider.mode, "region": provider.region, "credit_floor": provider.credit_floor, "message": provider.message}


@app.post("/v1/provider/refresh")
def refresh_provider(request: ProviderRefreshRequest) -> dict:
    """Run one explicit selected-market refresh; fixture mode never polls providers."""
    received = datetime.now(timezone.utc)
    adapter = OddsApiAdapter()
    status = adapter.status()
    try:
        board = adapter.fetch_selected_market(request.sport, request.market)
    except RuntimeError as error:
        record_capability_evidence(provider="the-odds-api", sport=request.sport, market=request.market, region=status.region, received=received, quota=None, outcome="deferred" if not status.configured else "rejected", failure=str(error), unknowns="No provider observation was requested or accepted; coverage, display rights, limits, and Quebec eligibility remain unknown.")
        raise HTTPException(status_code=409, detail=str(error)) from error
    except httpx.HTTPError as error:
        record_capability_evidence(provider="the-odds-api", sport=request.sport, market=request.market, region=status.region, received=received, quota=None, outcome="failed", failure="Provider request failed", unknowns="No observation was accepted; source availability and coverage remain unknown.")
        raise HTTPException(status_code=502, detail="Provider request failed; fixture mode remains available.") from error
    board["as_of"] = received.isoformat()
    summary = board["coverage_summary"]
    outcome = "observed" if board["games"] else "observed-empty"
    evidence = record_capability_evidence(provider="the-odds-api", sport=request.sport, market=request.market, region=status.region, received=received, quota=board["credit_state"]["remaining"], outcome=outcome, unknowns="Period, settlement assumptions, exact source status, limits, fees, FX, display rights, and Quebec eligibility were not supplied by this bounded board response.", details={"coverage_summary": summary})
    return board | {"observation_state": "provider-observed-not-revalidated", "revalidation_reason": "Exact period, settlement assumptions, and source-specific status are required before lifecycle ingestion.", "evidence": evidence}


def record_capability_evidence(*, provider: str, sport: str, market: str, region: str, received: datetime, quota: int | None, outcome: str, failure: str | None = None, unknowns: str = "", book: str | None = None, source_time: str | None = None, details: dict | None = None) -> dict:
    source = None
    if source_time:
        try:
            source = datetime.fromisoformat(source_time.replace("Z", "+00:00"))
        except ValueError:
            pass
    with session() as database:
        row = ProviderCapabilityEvidence(id=new_id(), provider=provider, sport=sport, market=market, region=region, book=book, source_timestamp=source, received_timestamp=received, quota_remaining=quota, outcome=outcome, failure_reason=failure, unknowns=unknowns, details=json.dumps(details or {}, separators=(",", ":")))
        database.add(row)
        database.commit()
        return evidence_row(row)


def evidence_row(row: ProviderCapabilityEvidence) -> dict:
    return {"id": row.id, "provider": row.provider, "sport": row.sport, "market": row.market, "region": row.region, "book": row.book, "source_timestamp": row.source_timestamp.isoformat() if row.source_timestamp else None, "received_timestamp": row.received_timestamp.isoformat(), "quota_remaining": row.quota_remaining, "outcome": row.outcome, "failure_reason": row.failure_reason, "unknowns": row.unknowns, "details": json.loads(row.details)}


@app.get("/v1/provider/evidence")
def provider_evidence() -> list[dict]:
    with session() as database:
        rows = database.query(ProviderCapabilityEvidence).order_by(ProviderCapabilityEvidence.received_timestamp.desc()).all()
        return [evidence_row(row) for row in rows]


@app.get("/v1/watchlist")
def list_watchlist() -> list[str]:
    with session() as database:
        return [row.event_id for row in database.query(WatchlistEntry).order_by(WatchlistEntry.created_at.desc()).all()]


@app.post("/v1/watchlist")
def toggle_watchlist(request: WatchlistRequest) -> dict:
    with session() as database:
        existing = database.get(WatchlistEntry, request.event_id)
        if existing is not None:
            database.delete(existing)
            database.commit()
            return {"event_id": request.event_id, "watched": False}
        database.add(WatchlistEntry(event_id=request.event_id))
        database.commit()
        return {"event_id": request.event_id, "watched": True}


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
        return [ledger_projection(database, row) for row in rows]


@app.get("/v1/ledger/summary")
def ledger_summary() -> dict:
    """Return research-ledger totals from integer minor units, never browser math."""
    with session() as database:
        records = [ledger_projection(database, row) for row in database.query(PairLedgerRecord).all()]
    settled_stake = settled_net = open_stake = 0
    for row in records:
        stake = cents(row["total_stake"])
        returned = cents(row["returned"])
        fees = cents(row["fees"])
        if row["status"] == "settled":
            settled_stake += stake
            settled_net += returned - stake - fees
        elif row["status"] == "open":
            open_stake += stake
    roi_basis_points = (settled_net * 10000 // settled_stake) if settled_stake else 0
    return {"settled_stake_minor": settled_stake, "realised_net_minor": settled_net, "open_stake_minor": open_stake, "settled_count": sum(row["status"] == "settled" for row in records), "roi_basis_points": roi_basis_points, "method": "effective projection only; open and void records are excluded from realised ROI"}


@app.get("/v1/ledger/{record_id}/corrections")
def list_ledger_corrections(record_id: str) -> list[dict]:
    with session() as database:
        if database.get(PairLedgerRecord, record_id) is None:
            raise HTTPException(status_code=404, detail="Ledger record was not found.")
        rows = database.query(PairLedgerCorrection).filter_by(record_id=record_id).order_by(PairLedgerCorrection.created_at.asc()).all()
        return [{"id": row.id, "reason": row.reason, "status": row.status, "total_stake": f"{row.total_stake_minor / 100:.2f}", "returned": f"{row.returned_minor / 100:.2f}", "fees": f"{row.fees_minor / 100:.2f}", "created_at": row.created_at.isoformat()} for row in rows]


def validate_ledger_money(status: str, total_stake: str, returned: str, fees: str) -> tuple[int, int, int]:
    try:
        stake, returned_minor, fees_minor = cents(total_stake), cents(returned), cents(fees)
    except Exception as error:
        raise HTTPException(status_code=422, detail="Ledger money values must be non-negative decimal strings.") from error
    if stake == 0:
        raise HTTPException(status_code=422, detail="Total stake must be greater than zero.")
    if status == "open" and (returned_minor != 0 or fees_minor != 0):
        raise HTTPException(status_code=422, detail="Open records must have zero returned amount and fees.")
    if status == "void" and fees_minor != 0:
        raise HTTPException(status_code=422, detail="Voided records must have zero fees.")
    return stake, returned_minor, fees_minor


def ledger_projection(database, row: PairLedgerRecord) -> dict:
    correction = database.query(PairLedgerCorrection).filter_by(record_id=row.id).order_by(PairLedgerCorrection.created_at.desc()).first()
    status = correction.status if correction else row.status
    stake = correction.total_stake_minor if correction else row.total_stake_minor
    returned = correction.returned_minor if correction else row.returned_minor
    fees = correction.fees_minor if correction else row.fees_minor
    original = {"status": row.status, "total_stake": f"{row.total_stake_minor / 100:.2f}", "returned": f"{row.returned_minor / 100:.2f}", "fees": f"{row.fees_minor / 100:.2f}", "created_at": row.created_at.isoformat()}
    return {"id": row.id, "occurred_on": row.occurred_on, "event_name": row.event_name, "books": row.books, "status": status, "total_stake": f"{stake / 100:.2f}", "returned": f"{returned / 100:.2f}", "fees": f"{fees / 100:.2f}", "source": row.source, "provenance": json.loads(row.provenance), "original": original, "correction_count": database.query(PairLedgerCorrection).filter_by(record_id=row.id).count()}


@app.post("/v1/ledger", status_code=201)
def create_ledger_record(request: LedgerRecordRequest) -> dict:
    stake, returned, fees = validate_ledger_money(request.status, request.total_stake, request.returned, request.fees)
    provenance = validate_ledger_provenance(request.provenance)
    row = PairLedgerRecord(id=new_id(), occurred_on=request.occurred_on, event_name=request.event_name, books=request.books, status=request.status, total_stake_minor=stake, returned_minor=returned, fees_minor=fees, provenance=json.dumps(provenance, separators=(",", ":")))
    with session() as database:
        database.add(row)
        database.commit()
        database.refresh(row)
    return {"id": row.id}


def validate_ledger_provenance(value: dict | None) -> dict:
    if value is None:
        return {"kind": "manual-source", "note": "Book labels are user-entered research context, not verified sportsbook execution data."}
    kind = value.get("kind")
    if kind == "manual-source":
        return {"kind": "manual-source", "note": str(value.get("note") or "Manual research entry.")}
    if kind != "sourced-pair":
        raise HTTPException(status_code=422, detail="Ledger provenance must be manual-source or sourced-pair.")
    legs = value.get("legs")
    if not isinstance(legs, list) or len(legs) != 2:
        raise HTTPException(status_code=422, detail="Sourced-pair provenance requires exactly two legs.")
    normalized = []
    for leg in legs:
        required = ("book", "stake", "returned", "status", "settlement_context")
        if not isinstance(leg, dict) or any(leg.get(field) in (None, "") for field in required):
            raise HTTPException(status_code=422, detail="Each sourced leg requires book, stake, returned, status, and settlement context.")
        if leg.get("quote_version_id") in (None, "") and leg.get("manual_source_marker") in (None, ""):
            raise HTTPException(status_code=422, detail="Each sourced leg requires a quote version ID or explicit manual-source marker.")
        try:
            stake = cents(str(leg["stake"]))
            returned = cents(str(leg["returned"]))
        except Exception as error:
            raise HTTPException(status_code=422, detail="Sourced leg amounts must be non-negative decimal strings.") from error
        normalized.append({"book": str(leg["book"]), "quote_version_id": leg.get("quote_version_id"), "manual_source_marker": leg.get("manual_source_marker"), "stake_minor": stake, "returned_minor": returned, "status": str(leg["status"]), "settlement_context": str(leg["settlement_context"])})
    return {"kind": "sourced-pair", "legs": normalized}


@app.post("/v1/ledger/{record_id}/corrections", status_code=201)
def correct_ledger_record(record_id: str, request: LedgerCorrectionRequest) -> dict:
    stake, returned, fees = validate_ledger_money(request.status, request.total_stake, request.returned, request.fees)
    with session() as database:
        if database.get(PairLedgerRecord, record_id) is None:
            raise HTTPException(status_code=404, detail="Ledger record was not found.")
        correction = PairLedgerCorrection(id=new_id(), record_id=record_id, reason=request.reason, status=request.status, total_stake_minor=stake, returned_minor=returned, fees_minor=fees)
        database.add(correction)
        database.commit()
        database.refresh(correction)
    return {"id": correction.id, "record_id": record_id}
