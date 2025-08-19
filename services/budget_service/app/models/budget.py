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
    
    # Financial fields
    total_purchase_value = Column(Float, default=0.0)
    total_sale_value = Column(Float, default=0.0)
    total_commission = Column(Float, default=0.0)
    markup_percentage = Column(Float, default=0.0)
    profitability_percentage = Column(Float, default=0.0)
    
    # Status and metadata
    status = Column(String, nullable=False, default=BudgetStatus.DRAFT.value)
    notes = Column(Text, nullable=True)
    created_by = Column(String, nullable=False)  # Username who created
    
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
    quantity = Column(Float, nullable=False)
    weight = Column(Float, nullable=True)
    
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
    commission_value = Column(Float, default=0.0)
    
    # Cost reference for external system (Dunamis)
    dunamis_cost = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    budget = relationship("Budget", back_populates="items")