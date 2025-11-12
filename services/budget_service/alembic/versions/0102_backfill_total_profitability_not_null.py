"""Backfill total_profitability and set NOT NULL

Revision ID: 0102
Revises: 0101
Create Date: 2025-11-12 00:10:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0102"
down_revision = "0101"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Backfill total_profitability for existing rows where it is NULL
    op.execute(
        """
        UPDATE budget_items
        SET total_profitability = 
            CASE
                WHEN total_purchase > 0 THEN ((total_sale / total_purchase) - 1) * 100
                ELSE 0
            END
        WHERE total_profitability IS NULL;
        """
    )

    # Set default and NOT NULL at DB level
    op.alter_column(
        "budget_items",
        "total_profitability",
        existing_type=sa.Float(),
        nullable=False,
        server_default=sa.text("0")
    )


def downgrade() -> None:
    # Revert NOT NULL and drop server default
    op.alter_column(
        "budget_items",
        "total_profitability",
        existing_type=sa.Float(),
        nullable=True,
        server_default=None
    )