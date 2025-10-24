"""add_weight_difference_display_to_budget_items

Revision ID: 1f4f4176aeb7
Revises: c0eefe7ade9c
Create Date: 2025-10-23 11:28:14.350447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f4f4176aeb7'
down_revision = 'c0eefe7ade9c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add weight_difference_display column to budget_items table
    op.add_column('budget_items', sa.Column('weight_difference_display', sa.Text(), nullable=True))


def downgrade() -> None:
    # Remove weight_difference_display column from budget_items table
    op.drop_column('budget_items', 'weight_difference_display')
