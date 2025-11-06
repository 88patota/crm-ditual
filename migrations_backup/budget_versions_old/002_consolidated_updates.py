"""Consolidated updates: add weight difference fields and total percentage, remove dunamis_cost

Revision ID: 002
Revises: 001
Create Date: 2024-12-27 16:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Get connection and inspector
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    # Check existing columns in budget_items table
    budget_items_columns = [col['name'] for col in inspector.get_columns('budget_items')]
    
    # Add weight_difference column to budget_items if it doesn't exist
    if 'weight_difference' not in budget_items_columns:
        op.add_column('budget_items', sa.Column('weight_difference', sa.Float(), nullable=True))
    
    # Add weight_difference_display column to budget_items if it doesn't exist
    if 'weight_difference_display' not in budget_items_columns:
        op.add_column('budget_items', sa.Column('weight_difference_display', sa.Text(), nullable=True))
    
    # Remove dunamis_cost column from budget_items if it exists
    if 'dunamis_cost' in budget_items_columns:
        op.drop_column('budget_items', 'dunamis_cost')
    
    # Check existing columns in budgets table
    budgets_columns = [col['name'] for col in inspector.get_columns('budgets')]
    
    # Add total_weight_difference_percentage column to budgets if it doesn't exist
    if 'total_weight_difference_percentage' not in budgets_columns:
        op.add_column('budgets', sa.Column('total_weight_difference_percentage', sa.Float(), nullable=True, default=0.0))


def downgrade() -> None:
    # Get connection and inspector
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    # Check existing columns in budgets table
    budgets_columns = [col['name'] for col in inspector.get_columns('budgets')]
    
    # Remove total_weight_difference_percentage column from budgets if it exists
    if 'total_weight_difference_percentage' in budgets_columns:
        op.drop_column('budgets', 'total_weight_difference_percentage')
    
    # Check existing columns in budget_items table
    budget_items_columns = [col['name'] for col in inspector.get_columns('budget_items')]
    
    # Add dunamis_cost column back to budget_items if it doesn't exist
    if 'dunamis_cost' not in budget_items_columns:
        op.add_column('budget_items', sa.Column('dunamis_cost', sa.Float(), nullable=True))
    
    # Remove weight_difference_display column from budget_items if it exists
    if 'weight_difference_display' in budget_items_columns:
        op.drop_column('budget_items', 'weight_difference_display')
    
    # Remove weight_difference column from budget_items if it exists
    if 'weight_difference' in budget_items_columns:
        op.drop_column('budget_items', 'weight_difference')