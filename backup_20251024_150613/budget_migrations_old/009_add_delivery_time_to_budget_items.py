"""Add delivery_time field to budget_items

Revision ID: 009_add_delivery_time
Revises: 008_add_ipi_fields_to_budget_items
Create Date: 2025-09-15 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '009_add_delivery_time'
down_revision: Union[str, None] = '008'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add delivery_time field to budget_items table"""
    op.add_column('budget_items', sa.Column('delivery_time', sa.String(), nullable=True))


def downgrade() -> None:
    """Remove delivery_time field from budget_items table"""
    op.drop_column('budget_items', 'delivery_time')
