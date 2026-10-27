from __future__ import annotations

from datetime import datetime, timezone
from os import getenv
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker


class Base(DeclarativeBase):
    pass


class SavedCalculation(Base):
    __tablename__ = "saved_calculations"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(180))
    payload: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class PairLedgerRecord(Base):
    __tablename__ = "pair_ledger_records"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    occurred_on: Mapped[str] = mapped_column(String(10))
    event_name: Mapped[str] = mapped_column(String(180))
    books: Mapped[str] = mapped_column(String(240))
    status: Mapped[str] = mapped_column(String(16))
    total_stake_minor: Mapped[int] = mapped_column(Integer)
    returned_minor: Mapped[int] = mapped_column(Integer)
    fees_minor: Mapped[int] = mapped_column(Integer)
    source: Mapped[str] = mapped_column(String(32), default="manual")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class PairLedgerCorrection(Base):
    __tablename__ = "pair_ledger_corrections"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    record_id: Mapped[str] = mapped_column(ForeignKey("pair_ledger_records.id"), nullable=False)
    reason: Mapped[str] = mapped_column(String(300), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    total_stake_minor: Mapped[int] = mapped_column(Integer, nullable=False)
    returned_minor: Mapped[int] = mapped_column(Integer, nullable=False)
    fees_minor: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class WatchlistEntry(Base):
    __tablename__ = "watchlist_entries"
    event_id: Mapped[str] = mapped_column(String(180), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class Provider(Base):
    __tablename__ = "providers"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    key: Mapped[str] = mapped_column(String(100), unique=True)
    name: Mapped[str] = mapped_column(String(180))


class RegionalFeed(Base):
    __tablename__ = "regional_feeds"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    provider_id: Mapped[str] = mapped_column(ForeignKey("providers.id"), nullable=False)
    region: Mapped[str] = mapped_column(String(32), nullable=False)
    provider: Mapped[Provider] = relationship()
    __table_args__ = (UniqueConstraint("provider_id", "region", name="uq_regional_feeds_provider_region"),)


class Book(Base):
    __tablename__ = "books"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    key: Mapped[str] = mapped_column(String(180), unique=True)
    name: Mapped[str] = mapped_column(String(180))


class CanonicalEvent(Base):
    __tablename__ = "canonical_events"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    feed_id: Mapped[str] = mapped_column(ForeignKey("regional_feeds.id"), nullable=False)
    source_event_id: Mapped[str] = mapped_column(String(240), nullable=False)
    sport: Mapped[str] = mapped_column(String(100), nullable=False)
    league: Mapped[str] = mapped_column(String(180), nullable=False)
    away: Mapped[str] = mapped_column(String(180), nullable=False)
    home: Mapped[str] = mapped_column(String(180), nullable=False)
    commence_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    __table_args__ = (UniqueConstraint("feed_id", "source_event_id", name="uq_canonical_events_feed_source"),)


class Market(Base):
    __tablename__ = "markets"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    event_id: Mapped[str] = mapped_column(ForeignKey("canonical_events.id"), nullable=False)
    key: Mapped[str] = mapped_column(String(100), nullable=False)
    period: Mapped[str] = mapped_column(String(100), nullable=False)
    line: Mapped[str | None] = mapped_column(String(64))
    settlement_assumptions: Mapped[str] = mapped_column(Text, default="")
    __table_args__ = (UniqueConstraint("event_id", "key", "period", "line", "settlement_assumptions", name="uq_markets_identity"),)


class Outcome(Base):
    __tablename__ = "outcomes"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    market_id: Mapped[str] = mapped_column(ForeignKey("markets.id"), nullable=False)
    label: Mapped[str] = mapped_column(String(240), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    __table_args__ = (UniqueConstraint("market_id", "position", name="uq_outcomes_market_position"), UniqueConstraint("market_id", "label", name="uq_outcomes_market_label"))


class Quote(Base):
    __tablename__ = "quotes"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    feed_id: Mapped[str] = mapped_column(ForeignKey("regional_feeds.id"), nullable=False)
    book_id: Mapped[str] = mapped_column(ForeignKey("books.id"), nullable=False)
    outcome_id: Mapped[str] = mapped_column(ForeignKey("outcomes.id"), nullable=False)
    __table_args__ = (UniqueConstraint("feed_id", "book_id", "outcome_id", name="uq_quotes_identity"),)


class QuoteVersion(Base):
    __tablename__ = "quote_versions"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    quote_id: Mapped[str] = mapped_column(ForeignKey("quotes.id"), nullable=False)
    observation_key: Mapped[str] = mapped_column(String(128), unique=True)
    american_price: Mapped[int] = mapped_column(Integer, nullable=False)
    source_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    received_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(24), nullable=False)
    invalidation_reason: Mapped[str | None] = mapped_column(String(120))
    is_current: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    raw_reference: Mapped[str | None] = mapped_column(Text)


DATABASE_URL = getenv("USHIO_DATABASE_URL", "sqlite:///./ushio-local.db")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False)


def create_schema() -> None:
    Base.metadata.create_all(engine)


def session() -> Session:
    return SessionLocal()


def new_id() -> str:
    return str(uuid4())
