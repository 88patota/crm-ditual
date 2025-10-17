"""add_freight_type_to_budgets

Revision ID: 010_add_freight_type_to_budgets
Revises: 20250915_124515
Create Date: 2025-09-23 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '010_add_freight_type_to_budgets'
down_revision = '009_add_delivery_time'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add freight_type column to budgets table
    op.add_column('budgets', sa.Column('freight_type', sa.String(10), nullable=True))
    
    # Set default value for existing records
    op.execute("UPDATE budgets SET freight_type = 'FOB' WHERE freight_type IS NULL")
    
    # Make the column non-nullable after setting default values
    op.alter_column('budgets', 'freight_type', nullable=False)

def downgrade() -> None:
    # Remove the column
    op.drop_column('budgets', 'freight_type')