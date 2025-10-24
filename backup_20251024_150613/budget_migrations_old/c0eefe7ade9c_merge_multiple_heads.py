"""merge_multiple_heads

Revision ID: c0eefe7ade9c
Revises: 006, 011_add_freight_value_total, 20250915_124515
Create Date: 2025-10-23 11:27:51.778732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0eefe7ade9c'
down_revision = ('006', '011_add_freight_value_total', '20250915_124515')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
