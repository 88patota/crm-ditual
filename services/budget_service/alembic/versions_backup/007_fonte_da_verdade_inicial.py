"""Initial migration - fonte da verdade baseada nos campos utilizados na aplicação

Revision ID: 007_fonte_da_verdade_inicial
Revises: 006_rename_columns_to_english
Create Date: 2025-08-19 22:25:00.000000

Esta migration contém TODOS os campos que estão sendo utilizados na aplicação:
- Modelos SQLAlchemy (Budget, BudgetItem)
- Schemas Pydantic (BudgetSimplified, BudgetItemSimplified)
- Frontend TypeScript (budgetService.ts)
- Formulários React (BudgetForm, SimplifiedBudgetForm)
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '007_fonte_da_verdade_inicial'
down_revision = '006_rename_columns_to_english'
branch_labels = None
depends_on = None

def upgrade() -> None:
    """Criar tabelas com estrutura fonte da verdade"""
    
    # Criar enum para status do orçamento
    budget_status_enum = postgresql.ENUM(
        'draft', 'pending', 'approved', 'rejected', 'expired',
        name='budgetstatus',
        create_type=False
    )
    budget_status_enum.create(op.get_bind(), checkfirst=True)
    
    # Tabela principal de orçamentos
    op.create_table(
        'budgets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_number', sa.String(), nullable=False),
        sa.Column('client_name', sa.String(), nullable=False),
        sa.Column('client_id', sa.Integer(), nullable=True),
        
        # Campos financeiros calculados
        sa.Column('total_purchase_value', sa.Float(), default=0.0, nullable=True),
        sa.Column('total_sale_value', sa.Float(), default=0.0, nullable=True),
        sa.Column('total_commission', sa.Float(), default=0.0, nullable=True),
        sa.Column('markup_percentage', sa.Float(), default=0.0, nullable=True),
        sa.Column('profitability_percentage', sa.Float(), default=0.0, nullable=True),
        
        # Status e metadados
        sa.Column('status', sa.String(), nullable=False, default='draft'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_by', sa.String(), nullable=False),
        
        # Timestamps
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        
        # Campos adicionais utilizados nos schemas
        sa.Column('prazo_medio', sa.Integer(), nullable=True, comment='Prazo médio em dias'),
        sa.Column('outras_despesas_totais', sa.Float(), nullable=True, comment='Outras despesas do pedido'),
        
        # Constraints
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('order_number')
    )
    
    # Índices para performance
    op.create_index('ix_budgets_id', 'budgets', ['id'])
    op.create_index('ix_budgets_order_number', 'budgets', ['order_number'])
    op.create_index('ix_budgets_client_name', 'budgets', ['client_name'])
    op.create_index('ix_budgets_status', 'budgets', ['status'])
    op.create_index('ix_budgets_created_by', 'budgets', ['created_by'])
    op.create_index('ix_budgets_created_at', 'budgets', ['created_at'])
    
    # Tabela de itens do orçamento
    op.create_table(
        'budget_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('budget_id', sa.Integer(), nullable=False),
        
        # Informações do produto
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('weight', sa.Float(), nullable=True, comment='Peso original do item'),
        
        # Campos de entrada do frontend simplificado (formato português)
        sa.Column('peso_compra', sa.Float(), nullable=True, comment='Peso na compra'),
        sa.Column('valor_com_icms_compra', sa.Float(), nullable=True, comment='Valor com ICMS na compra'),
        sa.Column('percentual_icms_compra', sa.Float(), nullable=True, comment='Percentual ICMS na compra'),
        sa.Column('outras_despesas_item', sa.Float(), default=0.0, nullable=True, comment='Outras despesas do item'),
        sa.Column('peso_venda', sa.Float(), nullable=True, comment='Peso na venda'),
        sa.Column('valor_com_icms_venda', sa.Float(), nullable=True, comment='Valor com ICMS na venda'),
        sa.Column('percentual_icms_venda', sa.Float(), nullable=True, comment='Percentual ICMS na venda'),
        
        # Campos de compra (formato inglês para modelo SQLAlchemy)
        sa.Column('purchase_icms_percentage', sa.Float(), default=0.0, nullable=True),
        sa.Column('purchase_other_expenses', sa.Float(), default=0.0, nullable=True),
        sa.Column('purchase_value_without_taxes', sa.Float(), nullable=True),
        sa.Column('purchase_value_with_weight_diff', sa.Float(), nullable=True),
        
        # Campos de venda (formato inglês para modelo SQLAlchemy)
        sa.Column('sale_weight', sa.Float(), nullable=True),
        sa.Column('sale_icms_percentage', sa.Float(), default=0.0, nullable=True),
        sa.Column('sale_value_without_taxes', sa.Float(), nullable=True),
        sa.Column('weight_difference', sa.Float(), nullable=True),
        
        # Campos calculados pelo sistema
        sa.Column('profitability', sa.Float(), default=0.0, nullable=True),
        sa.Column('total_purchase', sa.Float(), nullable=True),
        sa.Column('total_sale', sa.Float(), nullable=True),
        sa.Column('unit_value', sa.Float(), nullable=True),
        sa.Column('total_value', sa.Float(), nullable=True),
        
        # Comissão
        sa.Column('commission_percentage', sa.Float(), default=0.0, nullable=True),
        sa.Column('commission_value', sa.Float(), default=0.0, nullable=True),
        
        # Referência de custo para sistema externo (Dunamis)
        sa.Column('dunamis_cost', sa.Float(), nullable=True),
        
        # Campos adicionais do frontend antigo (para compatibilidade)
        sa.Column('quantity', sa.Float(), default=1.0, nullable=True, comment='Quantidade - compatibilidade'),
        sa.Column('purchase_value_with_icms', sa.Float(), nullable=True, comment='Valor compra com ICMS - compatibilidade'),
        sa.Column('sale_value_with_icms', sa.Float(), nullable=True, comment='Valor venda com ICMS - compatibilidade'),
        
        # Timestamps
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        
        # Constraints
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['budget_id'], ['budgets.id'], ondelete='CASCADE')
    )
    
    # Índices para performance da tabela budget_items
    op.create_index('ix_budget_items_id', 'budget_items', ['id'])
    op.create_index('ix_budget_items_budget_id', 'budget_items', ['budget_id'])
    op.create_index('ix_budget_items_description', 'budget_items', ['description'])

def downgrade() -> None:
    """Remover todas as tabelas"""
    
    # Remover índices
    op.drop_index('ix_budget_items_description', 'budget_items')
    op.drop_index('ix_budget_items_budget_id', 'budget_items')
    op.drop_index('ix_budget_items_id', 'budget_items')
    
    op.drop_index('ix_budgets_created_at', 'budgets')
    op.drop_index('ix_budgets_created_by', 'budgets')
    op.drop_index('ix_budgets_status', 'budgets')
    op.drop_index('ix_budgets_client_name', 'budgets')
    op.drop_index('ix_budgets_order_number', 'budgets')
    op.drop_index('ix_budgets_id', 'budgets')
    
    # Remover tabelas
    op.drop_table('budget_items')
    op.drop_table('budgets')
    
    # Remover enum
    budget_status_enum = postgresql.ENUM(
        'draft', 'pending', 'approved', 'rejected', 'expired',
        name='budgetstatus'
    )
    budget_status_enum.drop(op.get_bind())
