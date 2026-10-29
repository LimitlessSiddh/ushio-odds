"""Add durable provider quote lifecycle tables."""

from alembic import op
import sqlalchemy as sa

revision = "20261027_03"
down_revision = "20261026_02"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("providers", sa.Column("id", sa.String(36), primary_key=True), sa.Column("key", sa.String(100), nullable=False, unique=True), sa.Column("name", sa.String(180), nullable=False))
    op.create_table("regional_feeds", sa.Column("id", sa.String(36), primary_key=True), sa.Column("provider_id", sa.String(36), sa.ForeignKey("providers.id"), nullable=False), sa.Column("region", sa.String(32), nullable=False), sa.UniqueConstraint("provider_id", "region", name="uq_regional_feeds_provider_region"))
    op.create_table("books", sa.Column("id", sa.String(36), primary_key=True), sa.Column("key", sa.String(180), nullable=False, unique=True), sa.Column("name", sa.String(180), nullable=False))
    op.create_table("canonical_events", sa.Column("id", sa.String(36), primary_key=True), sa.Column("feed_id", sa.String(36), sa.ForeignKey("regional_feeds.id"), nullable=False), sa.Column("source_event_id", sa.String(240), nullable=False), sa.Column("sport", sa.String(100), nullable=False), sa.Column("league", sa.String(180), nullable=False), sa.Column("away", sa.String(180), nullable=False), sa.Column("home", sa.String(180), nullable=False), sa.Column("commence_time", sa.DateTime(timezone=True)), sa.UniqueConstraint("feed_id", "source_event_id", name="uq_canonical_events_feed_source"))
    op.create_table("markets", sa.Column("id", sa.String(36), primary_key=True), sa.Column("event_id", sa.String(36), sa.ForeignKey("canonical_events.id"), nullable=False), sa.Column("key", sa.String(100), nullable=False), sa.Column("period", sa.String(100), nullable=False), sa.Column("line", sa.String(64)), sa.Column("settlement_assumptions", sa.Text, nullable=False), sa.UniqueConstraint("event_id", "key", "period", "line", "settlement_assumptions", name="uq_markets_identity"))
    op.create_table("outcomes", sa.Column("id", sa.String(36), primary_key=True), sa.Column("market_id", sa.String(36), sa.ForeignKey("markets.id"), nullable=False), sa.Column("label", sa.String(240), nullable=False), sa.Column("position", sa.Integer, nullable=False), sa.UniqueConstraint("market_id", "position", name="uq_outcomes_market_position"), sa.UniqueConstraint("market_id", "label", name="uq_outcomes_market_label"))
    op.create_table("quotes", sa.Column("id", sa.String(36), primary_key=True), sa.Column("feed_id", sa.String(36), sa.ForeignKey("regional_feeds.id"), nullable=False), sa.Column("book_id", sa.String(36), sa.ForeignKey("books.id"), nullable=False), sa.Column("outcome_id", sa.String(36), sa.ForeignKey("outcomes.id"), nullable=False), sa.UniqueConstraint("feed_id", "book_id", "outcome_id", name="uq_quotes_identity"))
    op.create_table("quote_versions", sa.Column("id", sa.String(36), primary_key=True), sa.Column("quote_id", sa.String(36), sa.ForeignKey("quotes.id"), nullable=False), sa.Column("observation_key", sa.String(128), nullable=False, unique=True), sa.Column("american_price", sa.Integer, nullable=False), sa.Column("source_timestamp", sa.DateTime(timezone=True), nullable=False), sa.Column("received_timestamp", sa.DateTime(timezone=True), nullable=False), sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False), sa.Column("status", sa.String(24), nullable=False), sa.Column("invalidation_reason", sa.String(120)), sa.Column("is_current", sa.Boolean, nullable=False), sa.Column("raw_reference", sa.Text))
    op.create_index("ix_quote_versions_quote_current", "quote_versions", ["quote_id", "is_current"])


def downgrade() -> None:
    op.drop_index("ix_quote_versions_quote_current", table_name="quote_versions")
    for table in ("quote_versions", "quotes", "outcomes", "markets", "canonical_events", "books", "regional_feeds", "providers"):
        op.drop_table(table)
