"""Add provider capability evidence and explicit manual ledger provenance."""

from alembic import op
import sqlalchemy as sa

revision = "20261028_05"
down_revision = "20261027_04"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("pair_ledger_records", sa.Column("provenance", sa.Text(), nullable=False, server_default='{"kind":"manual-source"}'))
    op.create_table(
        "provider_capability_evidence",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("provider", sa.String(100), nullable=False),
        sa.Column("sport", sa.String(100), nullable=False),
        sa.Column("market", sa.String(100), nullable=False),
        sa.Column("region", sa.String(32), nullable=False),
        sa.Column("book", sa.String(180)),
        sa.Column("source_timestamp", sa.DateTime(timezone=True)),
        sa.Column("received_timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("quota_remaining", sa.Integer()),
        sa.Column("outcome", sa.String(32), nullable=False),
        sa.Column("failure_reason", sa.Text()),
        sa.Column("unknowns", sa.Text(), nullable=False, server_default=""),
        sa.Column("details", sa.Text(), nullable=False, server_default="{}"),
    )
    op.create_index("ix_provider_capability_evidence_received", "provider_capability_evidence", ["received_timestamp"])


def downgrade() -> None:
    op.drop_index("ix_provider_capability_evidence_received", table_name="provider_capability_evidence")
    op.drop_table("provider_capability_evidence")
    op.drop_column("pair_ledger_records", "provenance")
