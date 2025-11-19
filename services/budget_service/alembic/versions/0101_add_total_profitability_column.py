"""Add total_profitability column to budget_items

Revision ID: 0101
Revises: 0100
Create Date: 2025-11-12 00:00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0101"
down_revision = "0100"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "budget_items",
        sa.Column("total_profitability", sa.Float(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("budget_items", "total_profitability")