"""Durable, provider-neutral quote lifecycle rules.

This module deliberately does not call external providers.  It records a received
observation and makes its freshness and identity testable before any live source
is allowed to influence a product claim.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from hashlib import sha256
from typing import Any

from sqlalchemy.orm import Session

from .persistence import Book, CanonicalEvent, Market, Outcome, Provider, Quote, QuoteVersion, RegionalFeed, new_id

ACTIVE = "active"
INACTIVE_STATUSES = {"suspended", "missing", "stale", "invalid"}


class QuoteLifecycleError(ValueError):
    pass


def utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def parse_timestamp(value: datetime | str | None, field: str) -> datetime:
    if isinstance(value, datetime):
        return utc(value)
    if isinstance(value, str):
        try:
            return utc(datetime.fromisoformat(value.replace("Z", "+00:00")))
        except ValueError as error:
            raise QuoteLifecycleError(f"{field} must be an ISO-8601 timestamp.") from error
    raise QuoteLifecycleError(f"{field} is required.")


def canonical_line(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    return text


def observation_key(data: dict[str, Any], source_at: datetime, received_at: datetime) -> str:
    fields = ("provider", "region", "book", "event_id", "market", "period", "line", "outcome", "position", "price", "status")
    raw = "|".join(str(data.get(field, "")) for field in fields) + f"|{source_at.isoformat()}|{received_at.isoformat()}"
    return sha256(raw.encode()).hexdigest()


def get_or_create(session: Session, model: type, defaults: dict[str, Any], **where: Any) -> Any:
    value = session.query(model).filter_by(**where).one_or_none()
    if value is not None:
        return value
    value = model(id=new_id(), **where, **defaults)
    session.add(value)
    session.flush()
    return value


def validate_observation(data: dict[str, Any], *, received_at: datetime) -> tuple[datetime, str, str]:
    required = ("provider", "region", "book", "event_id", "sport", "league", "away", "home", "market", "period", "outcome", "position", "price", "source_timestamp")
    missing = [field for field in required if data.get(field) in (None, "")]
    if missing:
        raise QuoteLifecycleError(f"Quote identity is incomplete: {', '.join(missing)}.")
    try:
        price = int(data["price"])
        position = int(data["position"])
    except (TypeError, ValueError) as error:
        raise QuoteLifecycleError("Quote price and position must be integers.") from error
    if price == 0 or abs(price) < 100:
        raise QuoteLifecycleError("American quote price must have an absolute magnitude of at least 100.")
    if position < 0:
        raise QuoteLifecycleError("Outcome position cannot be negative.")
    source_at = parse_timestamp(data["source_timestamp"], "source_timestamp")
    if source_at > received_at:
        raise QuoteLifecycleError("Source timestamp cannot be later than receipt timestamp.")
    status = str(data.get("status", ACTIVE)).lower()
    if status not in {ACTIVE, *INACTIVE_STATUSES}:
        raise QuoteLifecycleError("Quote status must be active, suspended, missing, stale, or invalid.")
    return source_at, status, str(price)


def ingest_observation(session: Session, data: dict[str, Any], *, received_at: datetime | str | None = None, ttl_seconds: int = 90) -> QuoteVersion:
    """Store a single observation; older data never displaces a newer current state."""
    if ttl_seconds <= 0:
        raise QuoteLifecycleError("Freshness TTL must be positive.")
    received = parse_timestamp(received_at or datetime.now(timezone.utc), "received_timestamp")
    source_at, status, _ = validate_observation(data, received_at=received)
    key = observation_key(data, source_at, received)
    duplicate = session.query(QuoteVersion).filter_by(observation_key=key).one_or_none()
    if duplicate is not None:
        return duplicate

    provider = get_or_create(session, Provider, {"name": str(data.get("provider_name") or data["provider"])}, key=str(data["provider"]))
    feed = get_or_create(session, RegionalFeed, {}, provider_id=provider.id, region=str(data["region"]))
    book_key = str(data["book"])
    book = get_or_create(session, Book, {"name": str(data.get("book_name") or book_key)}, key=book_key)
    commence = parse_timestamp(data["commence_time"], "commence_time") if data.get("commence_time") else None
    event = get_or_create(session, CanonicalEvent, {"sport": str(data["sport"]), "league": str(data["league"]), "away": str(data["away"]), "home": str(data["home"]), "commence_time": commence}, feed_id=feed.id, source_event_id=str(data["event_id"]))
    line = canonical_line(data.get("line"))
    settlement = str(data.get("settlement_assumptions") or "")
    market = session.query(Market).filter_by(event_id=event.id, key=str(data["market"]), period=str(data["period"]), line=line, settlement_assumptions=settlement).one_or_none()
    if market is None:
        market = Market(id=new_id(), event_id=event.id, key=str(data["market"]), period=str(data["period"]), line=line, settlement_assumptions=settlement)
        session.add(market)
        session.flush()
    outcome = get_or_create(session, Outcome, {"label": str(data["outcome"])}, market_id=market.id, position=int(data["position"]))
    if outcome.label != str(data["outcome"]):
        raise QuoteLifecycleError("Outcome position conflicts with existing market identity.")
    quote = get_or_create(session, Quote, {}, feed_id=feed.id, book_id=book.id, outcome_id=outcome.id)

    currents = session.query(QuoteVersion).filter_by(quote_id=quote.id, is_current=True).order_by(QuoteVersion.source_timestamp.desc(), QuoteVersion.received_timestamp.desc()).all()
    current = currents[0] if currents else None
    expired_on_receipt = source_at + timedelta(seconds=ttl_seconds) <= received
    reason: str | None = "expired_on_receipt" if expired_on_receipt and status == ACTIVE else None
    if expired_on_receipt and status == ACTIVE:
        status = "stale"
    is_current = current is None or source_at >= utc(current.source_timestamp)
    if not is_current:
        reason = "out_of_order"
    elif current is not None:
        for prior in currents:
            prior.is_current = False
            prior.invalidation_reason = "superseded" if status == ACTIVE else status
    version = QuoteVersion(
        id=new_id(), quote_id=quote.id, observation_key=key, american_price=int(data["price"]), source_timestamp=source_at,
        received_timestamp=received, expires_at=source_at + timedelta(seconds=ttl_seconds), status=status,
        invalidation_reason=reason, is_current=is_current, raw_reference=data.get("raw_reference"),
    )
    session.add(version)
    session.flush()
    return version


def ingest_market_observations(session: Session, observations: list[dict[str, Any]], *, received_at: datetime | str | None = None, ttl_seconds: int = 90) -> list[QuoteVersion]:
    """Accept only an exact two-outcome market group; never pair mismatched lines."""
    if len(observations) != 2:
        raise QuoteLifecycleError("Only exactly two mutually exclusive outcomes can form a quote market.")
    identities = {tuple(str(item.get(field, "")) for field in ("provider", "region", "event_id", "market", "period", "line", "settlement_assumptions")) for item in observations}
    if len(identities) != 1:
        raise QuoteLifecycleError("Quote outcomes do not share an exact market identity.")
    labels = [str(item.get("outcome", "")) for item in observations]
    positions = [item.get("position") for item in observations]
    if len(set(labels)) != 2 or sorted(positions) != [0, 1]:
        raise QuoteLifecycleError("A two-outcome market requires distinct outcomes at positions zero and one.")
    return [ingest_observation(session, item, received_at=received_at, ttl_seconds=ttl_seconds) for item in observations]


def expire_current_quotes(session: Session, *, now: datetime | str | None = None) -> int:
    instant = parse_timestamp(now or datetime.now(timezone.utc), "now")
    rows = session.query(QuoteVersion).filter_by(is_current=True, status=ACTIVE).all()
    expired = 0
    for row in rows:
        if utc(row.expires_at) <= instant:
            row.status = "stale"
            row.invalidation_reason = "expired"
            expired += 1
    session.flush()
    return expired


def is_active(version: QuoteVersion, *, now: datetime | str | None = None) -> bool:
    instant = parse_timestamp(now or datetime.now(timezone.utc), "now")
    return version.is_current and version.status == ACTIVE and utc(version.expires_at) > instant
