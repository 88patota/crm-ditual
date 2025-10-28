"""Add weight difference fields to budget_items

Revision ID: 002
Revises: 001
Create Date: 2024-12-27 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Check if columns exist before adding them
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('budget_items')]
    
    # Add weight_difference column if it doesn't exist
    if 'weight_difference' not in columns:
        op.add_column('budget_items', sa.Column('weight_difference', sa.Float(), nullable=True))
    
    # Add weight_difference_display column if it doesn't exist
    if 'weight_difference_display' not in columns:
        op.add_column('budget_items', sa.Column('weight_difference_display', sa.Text(), nullable=True))


def downgrade() -> None:
    # Remove the columns if they exist
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('budget_items')]
    
    if 'weight_difference_display' in columns:
        op.drop_column('budget_items', 'weight_difference_display')
    
    if 'weight_difference' in columns:
        op.drop_column('budget_items', 'weight_difference')