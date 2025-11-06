"""Remove markup_percentage from budgets table

Revision ID: 004
Revises: 003
Create Date: 2025-11-05 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade():
    # Use batch operations for SQLite compatibility and safer schema changes
    with op.batch_alter_table('budgets') as batch_op:
        batch_op.drop_column('markup_percentage')


def downgrade():
    with op.batch_alter_table('budgets') as batch_op:
        batch_op.add_column(sa.Column('markup_percentage', sa.Float(), nullable=True))