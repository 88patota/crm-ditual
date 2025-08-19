"""Create BudgetStatus enum in database

Revision ID: 002
Revises: 001
Create Date: 2025-08-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Em vez de criar enum, vamos apenas garantir que a coluna existe como STRING
    connection = op.get_bind()
    
    # Drop enum se existir
    connection.execute(sa.text("DROP TYPE IF EXISTS budgetstatus CASCADE;"))
    
    # Verificar se a tabela budgets existe e tem a coluna status
    inspector = sa.inspect(connection)
    if 'budgets' in inspector.get_table_names():
        columns = inspector.get_columns('budgets')
        status_column_exists = any(col['name'] == 'status' for col in columns)
        
        if status_column_exists:
            # Alterar coluna para VARCHAR se necessário
            connection.execute(sa.text("ALTER TABLE budgets ALTER COLUMN status DROP DEFAULT;"))
            connection.execute(sa.text("ALTER TABLE budgets ALTER COLUMN status TYPE VARCHAR(20);"))
            connection.execute(sa.text("ALTER TABLE budgets ALTER COLUMN status SET DEFAULT 'draft';"))
        else:
            # Adicionar coluna se não existir
            op.add_column('budgets', sa.Column('status', sa.String(20), nullable=False, default='draft'))
        
        # Garantir que valores são válidos
        connection.execute(sa.text("""
            UPDATE budgets 
            SET status = 'draft' 
            WHERE status NOT IN ('draft', 'pending', 'approved', 'rejected', 'expired')
               OR status IS NULL;
        """))


def downgrade() -> None:
    # Convert enum back to text
    op.alter_column('budgets', 'status',
                   type_=sa.String(),
                   nullable=False,
                   existing_nullable=False)
    
    # Drop the enum type
    connection = op.get_bind()
    connection.execute(sa.text("DROP TYPE IF EXISTS budgetstatus CASCADE;"))
