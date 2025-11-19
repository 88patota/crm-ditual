"""Update statuses and rename prazo_medio to origem

Revision ID: 0103
Revises: 0102
Create Date: 2025-11-17 00:00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0103"
down_revision = "0102"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Update existing status values
    op.execute("UPDATE budgets SET status = 'sent' WHERE status = 'expired'")
    op.execute("UPDATE budgets SET status = 'lost' WHERE status = 'rejected'")

    # Rename prazo_medio -> origem and change type to VARCHAR(20)
    # Use direct SQL for safe type conversion in PostgreSQL
    op.execute("ALTER TABLE budgets RENAME COLUMN prazo_medio TO origem")
    op.execute("ALTER TABLE budgets ALTER COLUMN origem TYPE VARCHAR(20) USING origem::text")
    # Normalize values: set origem to NULL if not one of allowed values
    op.execute("UPDATE budgets SET origem = NULL WHERE origem NOT IN ('Orpen','Email','Google','Telefone')")


def downgrade() -> None:
    # Revert statuses
    op.execute("UPDATE budgets SET status = 'expired' WHERE status = 'sent'")
    op.execute("UPDATE budgets SET status = 'rejected' WHERE status = 'lost'")

    # Change origem back to INTEGER and rename to prazo_medio
    op.execute(
        "ALTER TABLE budgets ALTER COLUMN origem TYPE INTEGER USING CASE WHEN origem ~ '^[0-9]+' THEN origem::integer ELSE NULL END"
    )
    op.execute("ALTER TABLE budgets RENAME COLUMN origem TO prazo_medio")