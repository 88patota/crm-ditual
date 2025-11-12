"""Convert Float fields to Numeric for monetary precision

Revision ID: 001
Revises: 
Create Date: 2024-12-19 13:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Alterar campos da tabela budgets
    op.alter_column('budgets', 'total_purchase_value',
                    type_=sa.Numeric(15, 2),
                    existing_type=sa.Float(),
                    existing_nullable=True)
    
    op.alter_column('budgets', 'total_sale_value',
                    type_=sa.Numeric(15, 2),
                    existing_type=sa.Float(),
                    existing_nullable=True)
    
    op.alter_column('budgets', 'total_commission',
                    type_=sa.Numeric(15, 2),
                    existing_type=sa.Float(),
                    existing_nullable=True)
    
    op.alter_column('budgets', 'markup_percentage',
                    type_=sa.Numeric(8, 2),
                    existing_type=sa.Float(),
                    existing_nullable=True)
    
    op.alter_column('budgets', 'profitability_percentage',
                    type_=sa.Numeric(8, 2),
                    existing_type=sa.Float(),
                    existing_nullable=True)
    
    # Alterar campos da tabela budget_items
    op.alter_column('budget_items', 'quantity',
                    type_=sa.Numeric(10, 3),
                    existing_type=sa.Float(),
                    existing_nullable=False)
    
    op.alter_column('budget_items', 'weight',
                    type_=sa.Numeric(10, 3),
                    existing_type=sa.Float(),
                    existing_nullable=True)
    
    op.alter_column('budget_items', 'purchase_value_with_icms',
                    type_=sa.Numeric(15, 2),
                    existing_type=sa.Float(),
                    existing_nullable=False)
    
    op.alter_column('budget_items', 'purchase_icms_percentage',
                    type_=sa.Numeric(5, 2),
                    existing_type=sa.Float(),
                    existing_nullable=True)
    
    op.alter_column('budget_items', 'purchase_other_expenses',
                    type_=sa.Numeric(15, 2),
                    existing_type=sa.Float(),
                    existing_nullable=True)
    
    op.alter_column('budget_items', 'purchase_value_without_taxes',
                    type_=sa.Numeric(15, 2),
                    existing_type=sa.Float(),
                    existing_nullable=False)
    
    op.alter_column('budget_items', 'purchase_value_with_weight_diff',
                    type_=sa.Numeric(15, 2),
                    existing_type=sa.Float(),
                    existing_nullable=True)
    
    op.alter_column('budget_items', 'sale_weight',
                    type_=sa.Numeric(10, 3),
                    existing_type=sa.Float(),
                    existing_nullable=True)
    
    op.alter_column('budget_items', 'sale_value_with_icms',
                    type_=sa.Numeric(15, 2),
                    existing_type=sa.Float(),
                    existing_nullable=False)
    
    op.alter_column('budget_items', 'sale_icms_percentage',
                    type_=sa.Numeric(5, 2),
                    existing_type=sa.Float(),
                    existing_nullable=True)
    
    op.alter_column('budget_items', 'sale_value_without_taxes',
                    type_=sa.Numeric(15, 2),
                    existing_type=sa.Float(),
                    existing_nullable=False)
    
    op.alter_column('budget_items', 'weight_difference',
                    type_=sa.Numeric(10, 3),
                    existing_type=sa.Float(),
                    existing_nullable=True)
    
    op.alter_column('budget_items', 'profitability',
                    type_=sa.Numeric(8, 2),
                    existing_type=sa.Float(),
                    existing_nullable=True)
    
    op.alter_column('budget_items', 'total_purchase',
                    type_=sa.Numeric(15, 2),
                    existing_type=sa.Float(),
                    existing_nullable=False)
    
    op.alter_column('budget_items', 'total_sale',
                    type_=sa.Numeric(15, 2),
                    existing_type=sa.Float(),
                    existing_nullable=False)
    
    op.alter_column('budget_items', 'unit_value',
                    type_=sa.Numeric(15, 2),
                    existing_type=sa.Float(),
                    existing_nullable=False)
    
    op.alter_column('budget_items', 'total_value',
                    type_=sa.Numeric(15, 2),
                    existing_type=sa.Float(),
                    existing_nullable=False)
    
    op.alter_column('budget_items', 'commission_percentage',
                    type_=sa.Numeric(5, 2),
                    existing_type=sa.Float(),
                    existing_nullable=True)
    
    op.alter_column('budget_items', 'commission_value',
                    type_=sa.Numeric(15, 2),
                    existing_type=sa.Float(),
                    existing_nullable=True)
    
    op.alter_column('budget_items', 'dunamis_cost',
                    type_=sa.Numeric(15, 2),
                    existing_type=sa.Float(),
                    existing_nullable=True)


def downgrade() -> None:
    # Reverter campos da tabela budgets
    op.alter_column('budgets', 'total_purchase_value',
                    type_=sa.Float(),
                    existing_type=sa.Numeric(15, 2),
                    existing_nullable=True)
    
    op.alter_column('budgets', 'total_sale_value',
                    type_=sa.Float(),
                    existing_type=sa.Numeric(15, 2),
                    existing_nullable=True)
    
    op.alter_column('budgets', 'total_commission',
                    type_=sa.Float(),
                    existing_type=sa.Numeric(15, 2),
                    existing_nullable=True)
    
    op.alter_column('budgets', 'markup_percentage',
                    type_=sa.Float(),
                    existing_type=sa.Numeric(8, 2),
                    existing_nullable=True)
    
    op.alter_column('budgets', 'profitability_percentage',
                    type_=sa.Float(),
                    existing_type=sa.Numeric(8, 2),
                    existing_nullable=True)
    
    # Reverter campos da tabela budget_items
    op.alter_column('budget_items', 'quantity',
                    type_=sa.Float(),
                    existing_type=sa.Numeric(10, 3),
                    existing_nullable=False)
    
    op.alter_column('budget_items', 'weight',
                    type_=sa.Float(),
                    existing_type=sa.Numeric(10, 3),
                    existing_nullable=True)
    
    op.alter_column('budget_items', 'purchase_value_with_icms',
                    type_=sa.Float(),
                    existing_type=sa.Numeric(15, 2),
                    existing_nullable=False)
    
    op.alter_column('budget_items', 'purchase_icms_percentage',
                    type_=sa.Float(),
                    existing_type=sa.Numeric(5, 2),
                    existing_nullable=True)
    
    op.alter_column('budget_items', 'purchase_other_expenses',
                    type_=sa.Float(),
                    existing_type=sa.Numeric(15, 2),
                    existing_nullable=True)
    
    op.alter_column('budget_items', 'purchase_value_without_taxes',
                    type_=sa.Float(),
                    existing_type=sa.Numeric(15, 2),
                    existing_nullable=False)
    
    op.alter_column('budget_items', 'purchase_value_with_weight_diff',
                    type_=sa.Float(),
                    existing_type=sa.Numeric(15, 2),
                    existing_nullable=True)
    
    op.alter_column('budget_items', 'sale_weight',
                    type_=sa.Float(),
                    existing_type=sa.Numeric(10, 3),
                    existing_nullable=True)
    
    op.alter_column('budget_items', 'sale_value_with_icms',
                    type_=sa.Float(),
                    existing_type=sa.Numeric(15, 2),
                    existing_nullable=False)
    
    op.alter_column('budget_items', 'sale_icms_percentage',
                    type_=sa.Float(),
                    existing_type=sa.Numeric(5, 2),
                    existing_nullable=True)
    
    op.alter_column('budget_items', 'sale_value_without_taxes',
                    type_=sa.Float(),
                    existing_type=sa.Numeric(15, 2),
                    existing_nullable=False)
    
    op.alter_column('budget_items', 'weight_difference',
                    type_=sa.Float(),
                    existing_type=sa.Numeric(10, 3),
                    existing_nullable=True)
    
    op.alter_column('budget_items', 'profitability',
                    type_=sa.Float(),
                    existing_type=sa.Numeric(8, 2),
                    existing_nullable=True)
    
    op.alter_column('budget_items', 'total_purchase',
                    type_=sa.Float(),
                    existing_type=sa.Numeric(15, 2),
                    existing_nullable=False)
    
    op.alter_column('budget_items', 'total_sale',
                    type_=sa.Float(),
                    existing_type=sa.Numeric(15, 2),
                    existing_nullable=False)
    
    op.alter_column('budget_items', 'unit_value',
                    type_=sa.Float(),
                    existing_type=sa.Numeric(15, 2),
                    existing_nullable=False)
    
    op.alter_column('budget_items', 'total_value',
                    type_=sa.Float(),
                    existing_type=sa.Numeric(15, 2),
                    existing_nullable=False)
    
    op.alter_column('budget_items', 'commission_percentage',
                    type_=sa.Float(),
                    existing_type=sa.Numeric(5, 2),
                    existing_nullable=True)
    
    op.alter_column('budget_items', 'commission_value',
                    type_=sa.Float(),
                    existing_type=sa.Numeric(15, 2),
                    existing_nullable=True)
    
    op.alter_column('budget_items', 'dunamis_cost',
                    type_=sa.Float(),
                    existing_type=sa.Numeric(15, 2),
                    existing_nullable=True)
