from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime
from app.models.budget import BudgetStatus
from app.utils.json_utils import safe_json_loads


# Schema simplificado - APENAS campos que o vendedor deve preencher
class BudgetItemSimplified(BaseModel):
    """Schema com apenas os campos obrigatórios conforme especificado (nomes em português)"""
    # Campos obrigatórios
    description: str
    peso_compra: Optional[float] = 1.0  # Peso de compra, padrão 1.0
    peso_venda: Optional[float] = None  # Se não fornecido, usa peso_compra
    valor_com_icms_compra: float  # Valor de compra com ICMS
    percentual_icms_compra: float = 0.18  # Percentual ICMS compra (formato decimal 0.18 = 18%)
    outras_despesas_item: Optional[float] = 0.0  # Outras despesas do item
    valor_com_icms_venda: float  # Valor de venda com ICMS
    percentual_icms_venda: float = 0.18  # Percentual ICMS venda (formato decimal 0.18 = 18%)
    percentual_ipi: float = 0.0  # Percentual IPI (formato decimal: 0.0, 0.0325, 0.05)
    delivery_time: Optional[str] = "0"  # Prazo de entrega em dias (0 = imediato)

    @validator('peso_venda', always=True)
    def validate_peso_venda(cls, v, values):
        # Se peso_venda não fornecido, usa peso_compra
        if v is None:
            return values.get('peso_compra', 1.0)
        return v

    @validator('valor_com_icms_compra', 'valor_com_icms_venda')
    def validate_positive_values(cls, v):
        if v <= 0:
            raise ValueError('Valores devem ser maiores que zero')
        return v

    @validator('percentual_icms_compra', 'percentual_icms_venda')
    def validate_icms_percentage(cls, v):
        if v < 0 or v > 1:
            raise ValueError('Percentual de ICMS deve estar entre 0 e 1 (formato decimal)')
        return v

    @validator('percentual_ipi')
    def validate_ipi_percentage(cls, v):
        # IPI aceita apenas 0%, 3.25% ou 5% (em formato decimal)
        valid_ipi_values = [0.0, 0.0325, 0.05]
        if v not in valid_ipi_values:
            raise ValueError('Percentual de IPI deve ser 0%, 3.25% ou 5% (formato decimal: 0.0, 0.0325, 0.05)')
        return v

    @validator('peso_compra')
    def validate_peso_compra(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Peso de compra deve ser maior que zero')
        return v


class BudgetSimplifiedCreate(BaseModel):
    """Schema para criação simplificada"""
    # Número do pedido será gerado automaticamente se não fornecido
    order_number: Optional[str] = None
    client_name: str
    status: Optional[str] = "draft"
    expires_at: Optional[datetime] = None
    notes: Optional[str] = None
    
    # Campos de negócio
    prazo_medio: Optional[int] = None  # Prazo médio em dias
    outras_despesas_totais: Optional[float] = None  # Outras despesas do pedido
    freight_type: str = "FOB"
    freight_value_total: Optional[float] = None  # Valor total do frete
    payment_condition: Optional[str] = None  # Condições de pagamento
    valor_frete_compra: Optional[float] = None  # Valor do frete por kg
    
    items: List[BudgetItemSimplified]

    @validator('items')
    def validate_items(cls, v):
        if not v:
            raise ValueError('Orçamento deve ter pelo menos um item')
        return v

    @validator('client_name')
    def validate_client_name(cls, v):
        if not v or len(v) < 2:
            raise ValueError('Nome do cliente deve ter pelo menos 2 caracteres')
        return v


class MarkupConfiguration(BaseModel):
    """Configurações do sistema para cálculo de markup"""
    minimum_markup_percentage: float = 20.0
    maximum_markup_percentage: float = 200.0
    default_market_position: str = "competitive"
    icms_sale_default: float = 17.0
    commission_default: float = 1.5
    other_expenses_default: float = 0.0


class BudgetItemBase(BaseModel):
    description: str
    weight: Optional[float] = None
    delivery_time: Optional[str] = None  # Prazo de entrega por item
    
    # Purchase data
    purchase_value_with_icms: float
    purchase_icms_percentage: float = 0.0
    purchase_other_expenses: float = 0.0
    purchase_value_without_taxes: float
    purchase_value_with_weight_diff: Optional[float] = None
    
    # Sale data
    sale_weight: Optional[float] = None
    sale_value_with_icms: float
    sale_icms_percentage: float = 0.0
    sale_value_without_taxes: float
    weight_difference: Optional[float] = None
    
    # IPI (Imposto sobre Produtos Industrializados)
    ipi_percentage: float = 0.0  # Percentual IPI (formato decimal: 0.0, 0.0325, 0.05)
    
    # Comissão
    commission_percentage: float = 0.0
    
    # Weight difference display info
    weight_difference_display: Optional[dict] = None


    @validator('purchase_value_with_icms', 'sale_value_with_icms')
    def validate_positive_values(cls, v):
        if v < 0:
            raise ValueError('Valores não podem ser negativos')
        return v

    @validator('ipi_percentage')
    def validate_ipi_percentage(cls, v):
        # IPI aceita apenas 0%, 3.25% ou 5% (em formato decimal)
        valid_ipi_values = [0.0, 0.0325, 0.05]
        if v not in valid_ipi_values:
            raise ValueError('Percentual de IPI deve ser 0%, 3.25% ou 5% (formato decimal: 0.0, 0.0325, 0.05)')
        return v


class BudgetItemCreate(BudgetItemBase):
    pass


class BudgetItemUpdate(BaseModel):
    description: Optional[str] = None
    weight: Optional[float] = None
    purchase_value_with_icms: Optional[float] = None
    purchase_icms_percentage: Optional[float] = None
    purchase_other_expenses: Optional[float] = None
    purchase_value_without_taxes: Optional[float] = None
    sale_value_with_icms: Optional[float] = None
    sale_icms_percentage: Optional[float] = None
    sale_value_without_taxes: Optional[float] = None
    ipi_percentage: Optional[float] = None  # IPI percentual
    commission_percentage: Optional[float] = None


class BudgetItemResponse(BudgetItemBase):
    id: int
    budget_id: int
    
    # Calculated fields
    profitability: float
    total_purchase: float
    total_sale: float
    unit_value: float
    total_value: float
    commission_value: float
    commission_percentage_actual: float  # Actual commission percentage used (for display)
    rentabilidade_comissao: Optional[float] = None  # Rentabilidade usada para comissão (SEM ICMS)
    
    # IPI calculated values
    ipi_value: Optional[float] = None  # Valor do IPI calculado
    total_value_with_ipi: Optional[float] = None  # Valor total incluindo IPI
    
    # Weight difference display info
    weight_difference_display: Optional[dict] = None  # Weight difference display info
    
    created_at: datetime
    updated_at: datetime

    @validator('weight_difference_display', pre=True)
    def parse_weight_difference_display(cls, v):
        """Convert JSON string to dict if needed"""
        if isinstance(v, str):
            return safe_json_loads(v)
        return v

    class Config:
        from_attributes = True


class BudgetBase(BaseModel):
    order_number: str
    client_name: str
    client_id: Optional[int] = None
    markup_percentage: float = 0.0
    notes: Optional[str] = None
    expires_at: Optional[datetime] = None
    
    # Campos de negócio
    prazo_medio: Optional[int] = None  # Prazo médio em dias
    outras_despesas_totais: Optional[float] = None  # Outras despesas do pedido
    freight_type: str = "FOB"
    freight_value_total: Optional[float] = None  # Valor total do frete
    payment_condition: Optional[str] = None  # Condições de pagamento
    valor_frete_compra: Optional[float] = None  # Valor do frete por kg

    @validator('order_number')
    def validate_order_number(cls, v):
        if not v or len(v) < 3:
            raise ValueError('Número do pedido deve ter pelo menos 3 caracteres')
        return v

    @validator('client_name')
    def validate_client_name(cls, v):
        if not v or len(v) < 2:
            raise ValueError('Nome do cliente deve ter pelo menos 2 caracteres')
        return v


class BudgetCreate(BudgetBase):
    items: List[BudgetItemCreate] = []


class BudgetUpdate(BaseModel):
    client_name: Optional[str] = None
    client_id: Optional[int] = None
    markup_percentage: Optional[float] = None
    status: Optional[BudgetStatus] = None
    notes: Optional[str] = None
    expires_at: Optional[datetime] = None
    items: Optional[List[BudgetItemCreate]] = None
    freight_type: Optional[str] = None  # Remove default value to properly handle updates
    freight_value_total: Optional[float] = None  # Valor total do frete
    payment_condition: Optional[str] = None  # Condições de pagamento
    valor_frete_compra: Optional[float] = None  # Valor do frete por kg


class BudgetResponse(BudgetBase):
    id: int
    status: BudgetStatus
    
    # Financial totals
    total_purchase_value: float
    total_sale_value: float  # SEM impostos - valor que muda quando ICMS muda
    total_sale_with_icms: float  # COM ICMS - valor real sem IPI
    total_commission: float
    commission_percentage_actual: float  # Percentual de comissão real calculado
    profitability_percentage: float
    
    # IPI totals
    total_ipi_value: Optional[float] = None  # Total do IPI de todos os itens
    total_final_value: Optional[float] = None  # Valor final incluindo IPI (valor que o cliente paga)
    
    # Weight difference
    total_weight_difference_percentage: Optional[float] = None  # Diferença total de peso em porcentagem
    
    created_by: str
    created_at: datetime
    updated_at: datetime
    
    items: List[BudgetItemResponse] = []

    class Config:
        from_attributes = True


class BudgetSummary(BaseModel):
    id: int
    order_number: str
    client_name: str
    status: BudgetStatus
    total_sale_value: float  # SEM impostos - valor que muda quando ICMS muda
    total_sale_with_icms: float  # COM ICMS - valor real sem IPI
    total_commission: float
    commission_percentage_actual: Optional[float] = 0.0  # Percentual de comissão real calculado
    profitability_percentage: float
    items_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class BudgetCalculation(BaseModel):
    # Valores principais
    total_purchase_value: float
    total_sale_value: float  # COM ICMS - valor real pago pelo cliente
    total_net_revenue: float  # SEM impostos - receita líquida após impostos
    total_taxes: float  # Impostos totais = total_sale_value - total_net_revenue
    total_commission: float
    commission_percentage_actual: float  # Percentual de comissão real calculado
    profitability_percentage: float
    rentabilidade_comissao_total: float  # Rentabilidade total usada para comissão (SEM ICMS)
    markup_percentage: float
    items_calculations: List[dict]
    
    # IPI calculations
    total_ipi_value: float = 0.0  # Total do IPI de todos os itens
    total_final_value: float = 0.0  # Valor final incluindo IPI
    
    # Total weight difference
    total_weight_difference_percentage: float = 0.0  # Diferença total de peso em porcentagem


class BudgetPreviewCalculation(BaseModel):
    """Response para cálculo de preview com entrada simplificada"""
    total_purchase_value: float
    total_sale_value: float  # SEM impostos - valor que muda quando ICMS muda
    total_sale_with_icms: float  # COM ICMS - valor real sem IPI
    total_commission: float
    commission_percentage_actual: float  # Percentual de comissão real calculado
    profitability_percentage: float
    rentabilidade_comissao_total: float  # Rentabilidade total usada para comissão (SEM ICMS)
    markup_percentage: float  # CALCULADO AUTOMATICAMENTE
    items_preview: List[dict]
    
    # Configurações utilizadas no cálculo
    commission_percentage_default: float = 1.5  # Padrão 1,5%
    sale_icms_percentage_default: float = 17.0  # Padrão ICMS venda
    other_expenses_default: float = 0.0  # Outras despesas padrão
    # NOVOS CAMPOS
    minimum_markup_applied: float = 20.0
    maximum_markup_applied: float = 200.0
    
    # IPI preview calculations
    total_ipi_value: float = 0.0  # Total do IPI de todos os itens
    total_final_value: float = 0.0  # Valor final incluindo IPI
    
    # Total weight difference
    total_weight_difference_percentage: float = 0.0  # Diferença total de peso em porcentagem
