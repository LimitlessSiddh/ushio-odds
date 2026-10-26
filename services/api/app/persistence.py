from __future__ import annotations

from datetime import datetime, timezone
from os import getenv
from uuid import uuid4

from sqlalchemy import DateTime, Integer, Numeric, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker


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


DATABASE_URL = getenv("USHIO_DATABASE_URL", "sqlite:///./ushio-local.db")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False)


def create_schema() -> None:
    Base.metadata.create_all(engine)


def session() -> Session:
    return SessionLocal()


def new_id() -> str:
    return str(uuid4())
