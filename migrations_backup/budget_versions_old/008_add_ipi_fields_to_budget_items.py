"""Add IPI fields to budget_items table

Revision ID: 008
Revises: 007_fonte_da_verdade_inicial
Create Date: 2025-09-03 22:35:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '008'
down_revision = '007_fonte_da_verdade_inicial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add IPI fields to budget_items table"""
    
    # Check if tables exist
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    tables = inspector.get_table_names()
    
    # Add new IPI fields to budget_items table
    if 'budget_items' in tables:
        columns = [col['name'] for col in inspector.get_columns('budget_items')]
        
        # Add ipi_percentage if not exists
        if 'ipi_percentage' not in columns:
            op.add_column('budget_items', sa.Column('ipi_percentage', sa.Float(), nullable=True))
        
        # Add ipi_value if not exists
        if 'ipi_value' not in columns:
            op.add_column('budget_items', sa.Column('ipi_value', sa.Float(), nullable=True))
        
        # Add total_value_with_ipi if not exists
        if 'total_value_with_ipi' not in columns:
            op.add_column('budget_items', sa.Column('total_value_with_ipi', sa.Float(), nullable=True))


def downgrade() -> None:
    """Remove IPI fields from budget_items table"""
    
    # Check if tables exist
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    tables = inspector.get_table_names()
    
    # Remove IPI columns from budget_items
    if 'budget_items' in tables:
        columns = [col['name'] for col in inspector.get_columns('budget_items')]
        
        if 'total_value_with_ipi' in columns:
            op.drop_column('budget_items', 'total_value_with_ipi')
        
        if 'ipi_value' in columns:
            op.drop_column('budget_items', 'ipi_value')
        
        if 'ipi_percentage' in columns:
            op.drop_column('budget_items', 'ipi_percentage')