"""Persist the single-local-profile watchlist."""

from alembic import op
import sqlalchemy as sa

revision = "20261026_02"
down_revision = "20261026_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "watchlist_entries",
        sa.Column("event_id", sa.String(length=180), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("watchlist_entries")
