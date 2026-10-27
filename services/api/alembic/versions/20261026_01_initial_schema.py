"""Create saved-calculation and manual ledger tables."""

from alembic import op
import sqlalchemy as sa

revision = "20261026_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "saved_calculations",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("title", sa.String(length=180), nullable=False),
        sa.Column("payload", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "pair_ledger_records",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("occurred_on", sa.String(length=10), nullable=False),
        sa.Column("event_name", sa.String(length=180), nullable=False),
        sa.Column("books", sa.String(length=240), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("total_stake_minor", sa.Integer(), nullable=False),
        sa.Column("returned_minor", sa.Integer(), nullable=False),
        sa.Column("fees_minor", sa.Integer(), nullable=False),
        sa.Column("source", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("pair_ledger_records")
    op.drop_table("saved_calculations")
