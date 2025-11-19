"""add timestamps server default

Revision ID: 511c1d92e466
Revises: 001
Create Date: 2025-11-17 22:42:54.622797

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '511c1d92e466'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('users', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               server_default=sa.text('now()'),
               nullable=False)
    op.alter_column('users', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               server_default=sa.text('now()'),
               nullable=False)


def downgrade() -> None:
    op.alter_column('users', 'updated_at',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               server_default=None,
               nullable=False)
    op.alter_column('users', 'created_at',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               server_default=None,
               nullable=False)