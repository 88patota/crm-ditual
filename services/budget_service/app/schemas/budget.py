from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime
from app.models.budget import BudgetStatus


# Schema simplificado - APENAS campos que o vendedor deve preencher
class BudgetItemSimplified(BaseModel):
    """Schema com apenas os campos obrigatórios conforme especificado"""
    # Campos obrigatórios
    description: str
    quantity: float
    weight: Optional[float] = None
    purchase_value_with_icms: float
    purchase_icms_percentage: float = 17.0
    purchase_other_expenses: Optional[float] = 0.0  # Opcional
    sale_value_with_icms: float
    sale_icms_percentage: float = 17.0

    @validator('quantity')
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError('Quantidade deve ser maior que zero')
        return v

    @validator('purchase_value_with_icms', 'sale_value_with_icms')
    def validate_positive_values(cls, v):
        if v <= 0:
            raise ValueError('Valores devem ser maiores que zero')
        return v

    @validator('purchase_icms_percentage', 'sale_icms_percentage')
    def validate_icms_percentage(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Porcentagem de ICMS deve estar entre 0 e 100')
        return v


class BudgetSimplifiedCreate(BaseModel):
    """Schema para criação simplificada"""
    # Número do pedido será gerado automaticamente se não fornecido
    order_number: Optional[str] = None
    client_name: str
    status: Optional[str] = "draft"
    expires_at: Optional[datetime] = None
    notes: Optional[str] = None
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
    quantity: float
    weight: Optional[float] = None
    
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
    
    # Commission
    commission_percentage: float = 0.0
    dunamis_cost: Optional[float] = None

    @validator('quantity')
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError('Quantidade deve ser maior que zero')
        return v

    @validator('purchase_value_with_icms', 'sale_value_with_icms')
    def validate_positive_values(cls, v):
        if v < 0:
            raise ValueError('Valores não podem ser negativos')
        return v


class BudgetItemCreate(BudgetItemBase):
    pass


class BudgetItemUpdate(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    weight: Optional[float] = None
    purchase_value_with_icms: Optional[float] = None
    purchase_icms_percentage: Optional[float] = None
    purchase_other_expenses: Optional[float] = None
    purchase_value_without_taxes: Optional[float] = None
    sale_value_with_icms: Optional[float] = None
    sale_icms_percentage: Optional[float] = None
    sale_value_without_taxes: Optional[float] = None
    commission_percentage: Optional[float] = None
    dunamis_cost: Optional[float] = None


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
    
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BudgetBase(BaseModel):
    order_number: str
    client_name: str
    client_id: Optional[int] = None
    markup_percentage: float = 0.0
    notes: Optional[str] = None
    expires_at: Optional[datetime] = None

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


class BudgetResponse(BudgetBase):
    id: int
    status: BudgetStatus
    
    # Financial totals
    total_purchase_value: float
    total_sale_value: float
    total_commission: float
    profitability_percentage: float
    
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
    total_sale_value: float
    total_commission: float
    profitability_percentage: float
    items_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class BudgetCalculation(BaseModel):
    """Response model for budget calculations"""
    total_purchase_value: float
    total_sale_value: float
    total_commission: float
    profitability_percentage: float
    markup_percentage: float
    items_calculations: List[dict]


class BudgetPreviewCalculation(BaseModel):
    """Response para cálculo de preview com entrada simplificada"""
    total_purchase_value: float
    total_sale_value: float
    total_commission: float
    profitability_percentage: float
    markup_percentage: float  # CALCULADO AUTOMATICAMENTE
    items_preview: List[dict]
    
    # Configurações utilizadas no cálculo
    commission_percentage_default: float = 1.5  # Padrão 1,5%
    sale_icms_percentage_default: float = 17.0  # Padrão ICMS venda
    other_expenses_default: float = 0.0  # Outras despesas padrão
    # NOVOS CAMPOS
    minimum_markup_applied: float = 20.0
    maximum_markup_applied: float = 200.0