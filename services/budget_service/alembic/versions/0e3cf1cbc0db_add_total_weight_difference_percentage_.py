"""Add total_weight_difference_percentage to budgets table

Revision ID: 0e3cf1cbc0db
Revises: 002
Create Date: 2025-10-28 17:11:38.161702

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e3cf1cbc0db'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Check if column exists before adding it
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('budgets')]
    
    # Add total_weight_difference_percentage column if it doesn't exist
    if 'total_weight_difference_percentage' not in columns:
        op.add_column('budgets', sa.Column('total_weight_difference_percentage', sa.Float(), nullable=True, default=0.0))


def downgrade() -> None:
    # Remove the column if it exists
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('budgets')]
    
    if 'total_weight_difference_percentage' in columns:
        op.drop_column('budgets', 'total_weight_difference_percentage')
