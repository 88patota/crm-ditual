from alembic import op
import sqlalchemy as sa

revision = "0104"
down_revision = "0103"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "budgets",
        "origem",
        type_=sa.String(length=50),
        existing_type=sa.String(length=20),
        existing_nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "budgets",
        "origem",
        type_=sa.String(length=20),
        existing_type=sa.String(length=50),
        existing_nullable=True,
    )