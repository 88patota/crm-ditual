"""Convert budget status from enum to string

Revision ID: 003
Revises: 002
Create Date: 2025-08-15 12:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Convert enum column to string
    connection = op.get_bind()
    
    # Check if the budgets table exists
    inspector = sa.inspect(connection)
    if 'budgets' in inspector.get_table_names():
        # First, alter the column to be a string type
        op.alter_column('budgets', 'status',
                       type_=sa.String(),
                       nullable=False,
                       existing_nullable=False)
    
    # Drop the enum type if it exists (it might not exist if migration 002 wasn't run)
    connection.execute(sa.text("DROP TYPE IF EXISTS budgetstatus CASCADE;"))


def downgrade() -> None:
    # This would recreate the enum, but we'll keep it simple for now
    # and just ensure the column exists as string
    pass
