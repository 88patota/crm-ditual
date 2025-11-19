"""Remove quantity column from budget_items

Revision ID: 005_remove_quantity_column
Revises: 004_add_business_rules_fields
Create Date: 2025-08-19 15:54:45.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '005_remove_quantity_column'
down_revision = '004_add_business_rules_fields'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Remove quantity column from budget_items table"""
    # Drop the quantity column
    op.drop_column('budget_items', 'quantity')


def downgrade() -> None:
    """Add back quantity column to budget_items table"""
    # Add the quantity column back with NOT NULL constraint and default value
    op.add_column('budget_items', sa.Column('quantity', sa.Float(), nullable=False, server_default='1.0'))
