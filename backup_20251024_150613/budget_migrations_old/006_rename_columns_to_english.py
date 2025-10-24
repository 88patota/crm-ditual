"""Rename Portuguese column names to English for model compatibility

Revision ID: 006_rename_columns_to_english
Revises: 005_remove_quantity_column
Create Date: 2025-08-19 22:17:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '006_rename_columns_to_english'
down_revision = '005_remove_quantity_column'
branch_labels = None
depends_on = None

def upgrade() -> None:
    """Rename Portuguese column names to English"""
    
    # Check if tables exist
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    tables = inspector.get_table_names()
    
    if 'budget_items' in tables:
        columns = [col['name'] for col in inspector.get_columns('budget_items')]
        
        # Rename Portuguese columns to English names
        column_mappings = {
            'valor_com_icms_compra': 'purchase_value_with_icms',
            'peso_compra': 'purchase_weight', 
            'percentual_icms_compra': 'purchase_icms_percentage',
            'outras_despesas_item': 'purchase_other_expenses',
            'valor_sem_impostos_compra': 'purchase_value_without_taxes',
            'valor_corrigido_peso': 'purchase_value_with_weight_diff',
            'peso_venda': 'sale_weight',
            'valor_com_icms_venda': 'sale_value_with_icms', 
            'percentual_icms_venda': 'sale_icms_percentage',
            'valor_sem_impostos_venda': 'sale_value_without_taxes',
            'diferenca_peso': 'weight_difference',
            'valor_unitario_venda': 'unit_sale_value',
            'rentabilidade_item': 'profitability',
            'total_compra_item': 'total_purchase',
            'total_venda_item': 'total_sale',
            'percentual_comissao': 'commission_percentage',
            'valor_comissao': 'commission_value',
            'custo_dunamis': 'dunamis_cost'
        }
        
        for old_name, new_name in column_mappings.items():
            if old_name in columns:
                op.alter_column('budget_items', old_name, new_column_name=new_name)

def downgrade() -> None:
    """Rename English column names back to Portuguese"""
    
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    tables = inspector.get_table_names()
    
    if 'budget_items' in tables:
        columns = [col['name'] for col in inspector.get_columns('budget_items')]
        
        # Reverse mappings
        column_mappings = {
            'purchase_value_with_icms': 'valor_com_icms_compra',
            'purchase_weight': 'peso_compra',
            'purchase_icms_percentage': 'percentual_icms_compra',
            'purchase_other_expenses': 'outras_despesas_item',
            'purchase_value_without_taxes': 'valor_sem_impostos_compra',
            'purchase_value_with_weight_diff': 'valor_corrigido_peso',
            'sale_weight': 'peso_venda',
            'sale_value_with_icms': 'valor_com_icms_venda',
            'sale_icms_percentage': 'percentual_icms_venda',
            'sale_value_without_taxes': 'valor_sem_impostos_venda',
            'weight_difference': 'diferenca_peso',
            'unit_sale_value': 'valor_unitario_venda',
            'profitability': 'rentabilidade_item',
            'total_purchase': 'total_compra_item',
            'total_sale': 'total_venda_item',
            'commission_percentage': 'percentual_comissao',
            'commission_value': 'valor_comissao',
            'dunamis_cost': 'custo_dunamis'
        }
        
        for old_name, new_name in column_mappings.items():
            if old_name in columns:
                op.alter_column('budget_items', old_name, new_column_name=new_name)
