from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.persistence import Base, QuoteVersion
from app.quote_lifecycle import QuoteLifecycleError, expire_current_quotes, ingest_market_observations, ingest_observation, is_active


NOW = datetime(2026, 10, 27, 12, 0, tzinfo=timezone.utc)


@pytest.fixture
def database():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with sessionmaker(engine)() as session:
        yield session


def observation(**overrides):
    data = {
        "provider": "deterministic-fixture", "region": "ca", "book": "Stake", "event_id": "nhl-mtl-tor",
        "sport": "icehockey_nhl", "league": "NHL", "away": "Montreal", "home": "Toronto",
        "market": "h2h", "period": "full_game", "line": None, "settlement_assumptions": "regulation-included",
        "outcome": "Montreal", "position": 0, "price": -110, "source_timestamp": NOW.isoformat(),
    }
    data.update(overrides)
    return data


def test_duplicate_observation_is_idempotent_and_has_traceable_identity(database) -> None:
    first = ingest_observation(database, observation(), received_at=NOW)
    second = ingest_observation(database, observation(), received_at=NOW)
    assert first.id == second.id
    assert database.query(QuoteVersion).count() == 1
    assert first.source_timestamp == NOW
    assert first.received_timestamp == NOW
    assert first.status == "active"
    assert is_active(first, now=NOW + timedelta(seconds=1))


def test_future_and_stale_observations_are_not_active(database) -> None:
    with pytest.raises(QuoteLifecycleError, match="later than receipt"):
        ingest_observation(database, observation(source_timestamp=(NOW + timedelta(seconds=1)).isoformat()), received_at=NOW)
    stale = ingest_observation(database, observation(source_timestamp=(NOW - timedelta(seconds=91)).isoformat()), received_at=NOW, ttl_seconds=90)
    assert stale.status == "stale"
    assert stale.invalidation_reason == "expired_on_receipt"
    assert not is_active(stale, now=NOW)


def test_out_of_order_quote_cannot_replace_current_price(database) -> None:
    current = ingest_observation(database, observation(price=-110), received_at=NOW)
    older = ingest_observation(database, observation(price=-105, source_timestamp=(NOW - timedelta(seconds=1)).isoformat()), received_at=NOW)
    assert current.is_current is True
    assert older.is_current is False
    assert older.invalidation_reason == "out_of_order"


def test_new_observation_repairs_legacy_multiple_current_versions(database) -> None:
    first = ingest_observation(database, observation(price=-110), received_at=NOW)
    second = ingest_observation(database, observation(price=-105, source_timestamp=(NOW + timedelta(seconds=1)).isoformat()), received_at=NOW + timedelta(seconds=1))
    first.is_current = True  # Simulate a pre-constraint persisted legacy state.
    repaired = ingest_observation(database, observation(price=-108, source_timestamp=(NOW + timedelta(seconds=2)).isoformat()), received_at=NOW + timedelta(seconds=2))
    current = database.query(QuoteVersion).filter_by(is_current=True).all()
    assert [row.id for row in current] == [repaired.id]
    assert second.invalidation_reason == "superseded"


def test_suspended_and_expired_current_quotes_are_invalidated(database) -> None:
    active = ingest_observation(database, observation(), received_at=NOW, ttl_seconds=30)
    suspended = ingest_observation(database, observation(status="suspended", source_timestamp=(NOW + timedelta(seconds=1)).isoformat()), received_at=NOW + timedelta(seconds=1), ttl_seconds=30)
    assert active.is_current is False
    assert active.invalidation_reason == "suspended"
    assert suspended.is_current is True
    assert not is_active(suspended, now=NOW + timedelta(seconds=2))
    later = ingest_observation(database, observation(price=110, source_timestamp=(NOW + timedelta(seconds=2)).isoformat()), received_at=NOW + timedelta(seconds=2), ttl_seconds=1)
    assert expire_current_quotes(database, now=NOW + timedelta(seconds=4)) == 1
    assert later.status == "stale"
    assert later.invalidation_reason == "expired"


def test_two_way_ingestion_rejects_mismatched_identity_and_missing_outcomes(database) -> None:
    first = observation(outcome="Montreal", position=0)
    second = observation(outcome="Toronto", position=1, price=115, line="1.5")
    with pytest.raises(QuoteLifecycleError, match="exact market identity"):
        ingest_market_observations(database, [first, second], received_at=NOW)
    with pytest.raises(QuoteLifecycleError, match="exactly two"):
        ingest_market_observations(database, [first], received_at=NOW)
