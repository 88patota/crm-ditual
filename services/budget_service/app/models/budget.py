from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class BudgetStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True, index=True, nullable=False)
    client_name = Column(String, nullable=False)
    client_id = Column(Integer, nullable=True)  # Future FK to client service
    
    # Calculated values
    total_purchase_value = Column(Float, default=0.0)
    total_sale_value = Column(Float, default=0.0)  # SEM impostos - valor que muda quando ICMS muda
    total_sale_with_icms = Column(Float, default=0.0)  # COM ICMS - valor real sem IPI
    total_commission = Column(Float, default=0.0)
    commission_percentage_actual = Column(Float, default=0.0)  # Percentual de comissão real calculado
    markup_percentage = Column(Float, default=0.0)
    profitability_percentage = Column(Float, default=0.0)
    
    # IPI totals
    total_ipi_value = Column(Float, nullable=True)  # Total do IPI de todos os itens
    total_final_value = Column(Float, nullable=True)  # Valor final incluindo IPI (valor que o cliente paga)
    
    # Weight difference
    total_weight_difference_percentage = Column(Float, default=0.0)  # Diferença total de peso em porcentagem
    
    # Status and metadata
    status = Column(String, nullable=False, default=BudgetStatus.DRAFT.value)
    notes = Column(Text, nullable=True)
    created_by = Column(String, nullable=False)  # Username who created
    
    # Business fields
    prazo_medio = Column(Integer, nullable=True, comment='Prazo médio em dias')
    outras_despesas_totais = Column(Float, nullable=True, comment='Outras despesas do pedido')
    freight_type = Column(String(10), nullable=False, default='FOB')
    freight_value_total = Column(Float, nullable=True, comment='Valor total do frete')
    payment_condition = Column(String(50), nullable=True, comment='Condições de pagamento')
    valor_frete_compra = Column(Float, nullable=True, comment='Valor do frete por kg (Valor Frete Total / Peso Total)')
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    items = relationship("BudgetItem", back_populates="budget", cascade="all, delete-orphan")


class BudgetItem(Base):
    __tablename__ = "budget_items"

    id = Column(Integer, primary_key=True, index=True)
    budget_id = Column(Integer, ForeignKey("budgets.id"), nullable=False)
    
    # Product information
    description = Column(String, nullable=False)
    weight = Column(Float, nullable=True)
    delivery_time = Column(String, nullable=True)  # Prazo de entrega por item (ex: "5 dias", "Imediato", "15 dias úteis")
    
    # Purchase data
    purchase_value_with_icms = Column(Float, nullable=False)
    purchase_icms_percentage = Column(Float, default=0.0)
    purchase_other_expenses = Column(Float, default=0.0)
    purchase_value_without_taxes = Column(Float, nullable=False)
    purchase_value_with_weight_diff = Column(Float, nullable=True)
    
    # Sale data
    sale_weight = Column(Float, nullable=True)
    sale_value_with_icms = Column(Float, nullable=False)
    sale_icms_percentage = Column(Float, default=0.0)
    sale_value_without_taxes = Column(Float, nullable=False)
    weight_difference = Column(Float, nullable=True)
    
    # Calculated fields
    profitability = Column(Float, default=0.0)
    total_purchase = Column(Float, nullable=False)
    total_sale = Column(Float, nullable=False)
    unit_value = Column(Float, nullable=False)
    total_value = Column(Float, nullable=False)
    
    # Commission
    commission_percentage = Column(Float, default=0.0)
    commission_percentage_actual = Column(Float, default=0.0)  # Actual percentage used by backend
    commission_value = Column(Float, default=0.0)
    
    # IPI (Imposto sobre Produtos Industrializados)
    ipi_percentage = Column(Float, default=0.0)  # Percentual IPI (formato decimal: 0.0, 0.0325, 0.05)
    ipi_value = Column(Float, nullable=True)  # Valor do IPI calculado
    total_value_with_ipi = Column(Float, nullable=True)  # Valor total incluindo IPI
    
    # Weight difference display (JSON field for formatted display)
    weight_difference_display = Column(Text, nullable=True)  # JSON string with weight difference display info
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    budget = relationship("Budget", back_populates="items")
