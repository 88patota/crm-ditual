"""add commission_percentage_actual field

Revision ID: 005_add_commission_percentage_actual
Revises: 004_add_business_rules_fields
Create Date: 2025-08-26 15:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '005'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add commission_percentage_actual field to budget_items table"""
    
    # Add the commission_percentage_actual column
    op.add_column('budget_items', sa.Column('commission_percentage_actual', sa.Float(), default=0.0))


def downgrade() -> None:
    """Remove commission_percentage_actual field from budget_items table"""
    
    # Remove the commission_percentage_actual column
    op.drop_column('budget_items', 'commission_percentage_actual')