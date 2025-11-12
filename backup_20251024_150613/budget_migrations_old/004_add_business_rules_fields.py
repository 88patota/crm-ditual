"""Add business rules fields to budget and budget_item tables

Revision ID: 004
Revises: 003
Create Date: 2025-08-19 14:02:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '004_add_business_rules_fields'
down_revision = '003'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Check if tables exist
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    tables = inspector.get_table_names()
    
    # Add new fields to budgets table
    if 'budgets' in tables:
        columns = [col['name'] for col in inspector.get_columns('budgets')]
        
        # Add prazo_medio if not exists
        if 'prazo_medio' not in columns:
            op.add_column('budgets', sa.Column('prazo_medio', sa.Integer(), nullable=True))
        
        # Add outras_despesas_totais if not exists  
        if 'outras_despesas_totais' not in columns:
            op.add_column('budgets', sa.Column('outras_despesas_totais', sa.Float(), server_default='0.0'))
    
    # Add new fields to budget_items table
    if 'budget_items' in tables:
        columns = [col['name'] for col in inspector.get_columns('budget_items')]
        
        # Bloco Compras - Purchase fields
        if 'peso_compra' not in columns:
            op.add_column('budget_items', sa.Column('peso_compra', sa.Float(), nullable=True))
        
        if 'valor_com_icms_compra' not in columns:
            op.add_column('budget_items', sa.Column('valor_com_icms_compra', sa.Float(), nullable=True))
        
        if 'percentual_icms_compra' not in columns:
            op.add_column('budget_items', sa.Column('percentual_icms_compra', sa.Float(), server_default='0.18'))
        
        if 'outras_despesas_item' not in columns:
            op.add_column('budget_items', sa.Column('outras_despesas_item', sa.Float(), server_default='0.0'))
        
        if 'valor_sem_impostos_compra' not in columns:
            op.add_column('budget_items', sa.Column('valor_sem_impostos_compra', sa.Float(), nullable=True))
        
        if 'valor_corrigido_peso' not in columns:
            op.add_column('budget_items', sa.Column('valor_corrigido_peso', sa.Float(), nullable=True))
        
        # Bloco Vendas - Sale fields
        if 'peso_venda' not in columns:
            op.add_column('budget_items', sa.Column('peso_venda', sa.Float(), nullable=True))
        
        if 'valor_com_icms_venda' not in columns:
            op.add_column('budget_items', sa.Column('valor_com_icms_venda', sa.Float(), nullable=True))
        
        if 'percentual_icms_venda' not in columns:
            op.add_column('budget_items', sa.Column('percentual_icms_venda', sa.Float(), server_default='0.18'))
        
        if 'valor_sem_impostos_venda' not in columns:
            op.add_column('budget_items', sa.Column('valor_sem_impostos_venda', sa.Float(), nullable=True))
        
        if 'diferenca_peso' not in columns:
            op.add_column('budget_items', sa.Column('diferenca_peso', sa.Float(), nullable=True))
        
        if 'valor_unitario_venda' not in columns:
            op.add_column('budget_items', sa.Column('valor_unitario_venda', sa.Float(), nullable=True))
        
        # Bloco Rentabilidade - Profitability fields
        if 'rentabilidade_item' not in columns:
            op.add_column('budget_items', sa.Column('rentabilidade_item', sa.Float(), server_default='0.0'))
        
        if 'total_compra_item' not in columns:
            op.add_column('budget_items', sa.Column('total_compra_item', sa.Float(), nullable=True))
        
        if 'total_venda_item' not in columns:
            op.add_column('budget_items', sa.Column('total_venda_item', sa.Float(), nullable=True))
        
        # Bloco Comissões - Commission fields
        if 'percentual_comissao' not in columns:
            op.add_column('budget_items', sa.Column('percentual_comissao', sa.Float(), server_default='0.0'))
        
        if 'valor_comissao' not in columns:
            op.add_column('budget_items', sa.Column('valor_comissao', sa.Float(), server_default='0.0'))
        
        # Bloco Dunamis - Integration fields
        if 'custo_dunamis' not in columns:
            op.add_column('budget_items', sa.Column('custo_dunamis', sa.Float(), nullable=True))

def downgrade() -> None:
    # Remove added columns in reverse order
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    tables = inspector.get_table_names()
    
    # Remove columns from budget_items
    if 'budget_items' in tables:
        columns = [col['name'] for col in inspector.get_columns('budget_items')]
        
        columns_to_remove = [
            'custo_dunamis', 'valor_comissao', 'percentual_comissao',
            'total_venda_item', 'total_compra_item', 'rentabilidade_item',
            'valor_unitario_venda', 'diferenca_peso', 'valor_sem_impostos_venda',
            'percentual_icms_venda', 'valor_com_icms_venda', 'peso_venda',
            'valor_corrigido_peso', 'valor_sem_impostos_compra',
            'outras_despesas_item', 'percentual_icms_compra',
            'valor_com_icms_compra', 'peso_compra'
        ]
        
        for column in columns_to_remove:
            if column in columns:
                op.drop_column('budget_items', column)
    
    # Remove columns from budgets
    if 'budgets' in tables:
        columns = [col['name'] for col in inspector.get_columns('budgets')]
        
        if 'outras_despesas_totais' in columns:
            op.drop_column('budgets', 'outras_despesas_totais')
        
        if 'prazo_medio' in columns:
            op.drop_column('budgets', 'prazo_medio')
