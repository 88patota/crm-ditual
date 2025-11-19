"""Baseline full schema for budget_service

Revision ID: 0100
Revises: None
Create Date: 2025-11-06 12:00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0100"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create budgets table
    op.create_table(
        "budgets",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("order_number", sa.String(), nullable=False),
        sa.Column("client_name", sa.String(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=True),

        # Calculated values
        sa.Column("total_purchase_value", sa.Float(), nullable=True),
        sa.Column("total_sale_value", sa.Float(), nullable=True),
        sa.Column("total_sale_with_icms", sa.Float(), nullable=True),
        sa.Column("total_commission", sa.Float(), nullable=True),
        sa.Column("commission_percentage_actual", sa.Float(), nullable=True),
        sa.Column("profitability_percentage", sa.Float(), nullable=True),

        # IPI totals
        sa.Column("total_ipi_value", sa.Float(), nullable=True),
        sa.Column("total_final_value", sa.Float(), nullable=True),

        # Weight difference
        sa.Column("total_weight_difference_percentage", sa.Float(), nullable=True),

        # Status and metadata
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_by", sa.String(), nullable=False),

        # Business fields
        sa.Column("prazo_medio", sa.Integer(), nullable=True),
        sa.Column("outras_despesas_totais", sa.Float(), nullable=True),
        sa.Column("freight_type", sa.String(length=10), nullable=False),
        sa.Column("freight_value_total", sa.Float(), nullable=True),
        sa.Column("payment_condition", sa.String(length=50), nullable=True),
        sa.Column("valor_frete_compra", sa.Float(), nullable=True),

        # Timestamps
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Indexes for budgets
    op.create_index("ix_budgets_id", "budgets", ["id"], unique=False)
    op.create_index("ix_budgets_order_number", "budgets", ["order_number"], unique=True)

    # Create budget_items table
    op.create_table(
        "budget_items",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("budget_id", sa.Integer(), nullable=False),

        # Product information
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("weight", sa.Float(), nullable=True),
        sa.Column("delivery_time", sa.String(), nullable=True),

        # Purchase data
        sa.Column("purchase_value_with_icms", sa.Float(), nullable=False),
        sa.Column("purchase_icms_percentage", sa.Float(), nullable=True),
        sa.Column("purchase_other_expenses", sa.Float(), nullable=True),
        sa.Column("purchase_value_without_taxes", sa.Float(), nullable=False),
        sa.Column("purchase_value_with_weight_diff", sa.Float(), nullable=True),

        # Sale data
        sa.Column("sale_weight", sa.Float(), nullable=True),
        sa.Column("sale_value_with_icms", sa.Float(), nullable=False),
        sa.Column("sale_icms_percentage", sa.Float(), nullable=True),
        sa.Column("sale_value_without_taxes", sa.Float(), nullable=False),
        sa.Column("weight_difference", sa.Float(), nullable=True),

        # Calculated fields
        sa.Column("profitability", sa.Float(), nullable=True),
        sa.Column("total_purchase", sa.Float(), nullable=False),
        sa.Column("total_sale", sa.Float(), nullable=False),
        sa.Column("unit_value", sa.Float(), nullable=False),
        sa.Column("total_value", sa.Float(), nullable=False),

        # Commission
        sa.Column("commission_percentage", sa.Float(), nullable=True),
        sa.Column("commission_percentage_actual", sa.Float(), nullable=True),
        sa.Column("commission_value", sa.Float(), nullable=True),

        # IPI
        sa.Column("ipi_percentage", sa.Float(), nullable=True),
        sa.Column("ipi_value", sa.Float(), nullable=True),
        sa.Column("total_value_with_ipi", sa.Float(), nullable=True),

        # Weight difference display
        sa.Column("weight_difference_display", sa.Text(), nullable=True),

        # Timestamps
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    # FK and indexes for budget_items
    op.create_foreign_key(
        "fk_budget_items_budget_id",
        source_table="budget_items",
        referent_table="budgets",
        local_cols=["budget_id"],
        remote_cols=["id"],
        ondelete=None,
    )
    op.create_index("ix_budget_items_id", "budget_items", ["id"], unique=False)


def downgrade() -> None:
    # Drop indexes and tables in reverse order
    op.drop_index("ix_budget_items_id", table_name="budget_items")
    op.drop_constraint("fk_budget_items_budget_id", "budget_items", type_="foreignkey")
    op.drop_table("budget_items")

    op.drop_index("ix_budgets_order_number", table_name="budgets")
    op.drop_index("ix_budgets_id", table_name="budgets")
    op.drop_table("budgets")