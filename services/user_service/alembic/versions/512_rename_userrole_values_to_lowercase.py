from alembic import op
import sqlalchemy as sa

revision = "512"
down_revision = "511c1d92e466"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM pg_enum e JOIN pg_type t ON e.enumtypid=t.oid
                WHERE t.typname='userrole' AND e.enumlabel='ADMIN'
            ) THEN
                ALTER TYPE userrole RENAME VALUE 'ADMIN' TO 'admin';
            END IF;
            IF EXISTS (
                SELECT 1 FROM pg_enum e JOIN pg_type t ON e.enumtypid=t.oid
                WHERE t.typname='userrole' AND e.enumlabel='VENDAS'
            ) THEN
                ALTER TYPE userrole RENAME VALUE 'VENDAS' TO 'vendas';
            END IF;
        END$$;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM pg_enum e JOIN pg_type t ON e.enumtypid=t.oid
                WHERE t.typname='userrole' AND e.enumlabel='admin'
            ) THEN
                ALTER TYPE userrole RENAME VALUE 'admin' TO 'ADMIN';
            END IF;
            IF EXISTS (
                SELECT 1 FROM pg_enum e JOIN pg_type t ON e.enumtypid=t.oid
                WHERE t.typname='userrole' AND e.enumlabel='vendas'
            ) THEN
                ALTER TYPE userrole RENAME VALUE 'vendas' TO 'VENDAS';
            END IF;
        END$$;
        """
    )