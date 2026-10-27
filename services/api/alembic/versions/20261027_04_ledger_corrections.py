"""Add immutable manual ledger corrections."""

from alembic import op
import sqlalchemy as sa

revision = "20261027_04"
down_revision = "20261027_03"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("pair_ledger_corrections", sa.Column("id", sa.String(36), primary_key=True), sa.Column("record_id", sa.String(36), sa.ForeignKey("pair_ledger_records.id"), nullable=False), sa.Column("reason", sa.String(300), nullable=False), sa.Column("status", sa.String(16), nullable=False), sa.Column("total_stake_minor", sa.Integer, nullable=False), sa.Column("returned_minor", sa.Integer, nullable=False), sa.Column("fees_minor", sa.Integer, nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_pair_ledger_corrections_record_created", "pair_ledger_corrections", ["record_id", "created_at"])


def downgrade() -> None:
    op.drop_index("ix_pair_ledger_corrections_record_created", table_name="pair_ledger_corrections")
    op.drop_table("pair_ledger_corrections")
