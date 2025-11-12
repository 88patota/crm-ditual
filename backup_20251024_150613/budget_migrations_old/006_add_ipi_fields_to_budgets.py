"""Add IPI fields to budgets table

Revision ID: 006
Revises: 005
Create Date: 2025-09-03 22:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add IPI fields to budgets table"""
    
    # Check if tables exist
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    tables = inspector.get_table_names()
    
    # Add new fields to budgets table
    if 'budgets' in tables:
        columns = [col['name'] for col in inspector.get_columns('budgets')]
        
        # Add total_ipi_value if not exists
        if 'total_ipi_value' not in columns:
            op.add_column('budgets', sa.Column('total_ipi_value', sa.Float(), nullable=True))
        
        # Add total_final_value if not exists
        if 'total_final_value' not in columns:
            op.add_column('budgets', sa.Column('total_final_value', sa.Float(), nullable=True))


def downgrade() -> None:
    """Remove IPI fields from budgets table"""
    
    # Check if tables exist
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    tables = inspector.get_table_names()
    
    # Remove columns from budgets
    if 'budgets' in tables:
        columns = [col['name'] for col in inspector.get_columns('budgets')]
        
        if 'total_final_value' in columns:
            op.drop_column('budgets', 'total_final_value')
        
        if 'total_ipi_value' in columns:
            op.drop_column('budgets', 'total_ipi_value')