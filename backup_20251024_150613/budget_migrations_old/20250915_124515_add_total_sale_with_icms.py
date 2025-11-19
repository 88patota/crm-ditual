"""add_total_sale_with_icms

Revision ID: 20250915_124515
Revises: 007_fonte_da_verdade_inicial
Create Date: 2025-09-15 12:45:15.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250915_124515'
down_revision = '007_fonte_da_verdade_inicial'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add the new column to budgets table
    op.add_column('budgets', sa.Column('total_sale_with_icms', sa.Float(), default=0.0))
    
    # Update existing records to calculate total_sale_with_icms from items
    # This SQL calculates the sum of (sale_value_with_icms * sale_weight) for each budget
    op.execute("""
        UPDATE budgets 
        SET total_sale_with_icms = (
            SELECT COALESCE(SUM(
                bi.sale_value_with_icms * COALESCE(bi.sale_weight, bi.weight, 1.0)
            ), 0.0)
            FROM budget_items bi 
            WHERE bi.budget_id = budgets.id
        )
        WHERE total_sale_with_icms IS NULL;
    """)

def downgrade() -> None:
    # Remove the column
    op.drop_column('budgets', 'total_sale_with_icms')
