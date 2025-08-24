from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from app.models.budget import Budget, BudgetItem, BudgetStatus
from app.schemas.budget import BudgetCreate, BudgetUpdate, BudgetItemCreate, BudgetItemUpdate
from app.services.budget_calculator import BudgetCalculatorService


class BudgetService:
    
    @staticmethod
    async def create_budget(db: AsyncSession, budget_data: BudgetCreate, created_by: str) -> Budget:
        """Create a new budget with items"""
        
        # Validate budget data
        budget_dict = budget_data.dict()
        errors = BudgetCalculatorService.validate_budget_data(budget_dict)
        if errors:
            raise ValueError(f"Dados inválidos: {'; '.join(errors)}")
        
        # Calculate totals
        items_data = [item.dict() for item in budget_data.items]
        totals = BudgetCalculatorService.calculate_budget_totals(items_data)
        
        # Create budget
        budget = Budget(
            order_number=budget_data.order_number,
            client_name=budget_data.client_name,
            client_id=budget_data.client_id,
            markup_percentage=budget_data.markup_percentage,
            notes=budget_data.notes,
            expires_at=budget_data.expires_at,
            created_by=created_by,
            total_purchase_value=totals['total_purchase_value'],
            total_sale_value=totals['total_sale_value'],
            total_commission=totals['total_commission'],
            profitability_percentage=totals['profitability_percentage']
        )
        
        db.add(budget)
        await db.flush()  # Get the budget ID
        
        # Create items with calculations
        for item_data in items_data:
            calculations = BudgetCalculatorService.calculate_item_totals(item_data)
            
            budget_item = BudgetItem(
                budget_id=budget.id,
                description=item_data['description'],
                                weight=item_data.get('weight'),
                purchase_value_with_icms=item_data['purchase_value_with_icms'],
                purchase_icms_percentage=item_data['purchase_icms_percentage'],
                purchase_other_expenses=item_data.get('purchase_other_expenses', 0),
                purchase_value_without_taxes=calculations['purchase_value_without_taxes'],
                purchase_value_with_weight_diff=item_data.get('purchase_value_with_weight_diff'),
                sale_weight=item_data.get('sale_weight'),
                sale_value_with_icms=item_data['sale_value_with_icms'],
                sale_icms_percentage=item_data['sale_icms_percentage'],
                sale_value_without_taxes=calculations['sale_value_without_taxes'],
                weight_difference=calculations['weight_difference'],
                profitability=calculations['profitability'],
                total_purchase=calculations['total_purchase'],
                total_sale=calculations['total_sale'],
                unit_value=calculations['unit_value'],
                total_value=calculations['total_value'],
                commission_percentage=item_data.get('commission_percentage', 0),
                commission_value=calculations['commission_value'],
                dunamis_cost=item_data.get('dunamis_cost')
            )
            db.add(budget_item)
        
        await db.commit()
        await db.refresh(budget)
        
        return budget
    
    @staticmethod
    async def get_budget_by_id(db: AsyncSession, budget_id: int) -> Optional[Budget]:
        """Get budget by ID with items"""
        query = select(Budget).options(selectinload(Budget.items)).where(Budget.id == budget_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_budget_by_order_number(db: AsyncSession, order_number: str) -> Optional[Budget]:
        """Get budget by order number"""
        query = select(Budget).options(selectinload(Budget.items)).where(Budget.order_number == order_number)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_budgets(
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[BudgetStatus] = None,
        client_name: Optional[str] = None,
        created_by: Optional[str] = None
    ) -> List[Budget]:
        """Get budgets with filtering"""
        query = select(Budget).options(selectinload(Budget.items))
        
        # Apply filters
        conditions = []
        if status:
            conditions.append(Budget.status == status)
        if client_name:
            conditions.append(Budget.client_name.ilike(f"%{client_name}%"))
        if created_by:
            conditions.append(Budget.created_by == created_by)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        query = query.offset(skip).limit(limit).order_by(Budget.created_at.desc())
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def update_budget(db: AsyncSession, budget_id: int, budget_data: BudgetUpdate) -> Optional[Budget]:
        """Update budget"""
        budget = await BudgetService.get_budget_by_id(db, budget_id)
        if not budget:
            return None
        
        # Update fields
        for field, value in budget_data.dict(exclude_unset=True).items():
            setattr(budget, field, value)
        
        await db.commit()
        await db.refresh(budget)
        return budget
    
    @staticmethod
    async def delete_budget(db: AsyncSession, budget_id: int) -> bool:
        """Delete budget"""
        budget = await BudgetService.get_budget_by_id(db, budget_id)
        if not budget:
            return False
        
        await db.delete(budget)
        await db.commit()
        return True
    
    @staticmethod
    async def recalculate_budget(db: AsyncSession, budget_id: int) -> Optional[Budget]:
        """Recalculate budget totals"""
        budget = await BudgetService.get_budget_by_id(db, budget_id)
        if not budget:
            return None
        
        # Get items data
        items_data = []
        for item in budget.items:
            items_data.append({
                                'purchase_value_with_icms': item.purchase_value_with_icms,
                'purchase_icms_percentage': item.purchase_icms_percentage,
                'purchase_other_expenses': item.purchase_other_expenses,
                'sale_value_with_icms': item.sale_value_with_icms,
                'sale_icms_percentage': item.sale_icms_percentage,
                'commission_percentage': item.commission_percentage,
                'weight': item.weight,
                'sale_weight': item.sale_weight
            })
        
        # Recalculate totals
        totals = BudgetCalculatorService.calculate_budget_totals(items_data)
        
        # Update budget totals
        budget.total_purchase_value = totals['total_purchase_value']
        budget.total_sale_value = totals['total_sale_value']
        budget.total_commission = totals['total_commission']
        budget.profitability_percentage = totals['profitability_percentage']
        budget.markup_percentage = totals['markup_percentage']
        
        # Recalculate each item
        for i, item in enumerate(budget.items):
            calculations = BudgetCalculatorService.calculate_item_totals(items_data[i])
            
            item.purchase_value_without_taxes = calculations['purchase_value_without_taxes']
            item.sale_value_without_taxes = calculations['sale_value_without_taxes']
            item.total_purchase = calculations['total_purchase']
            item.total_sale = calculations['total_sale']
            item.unit_value = calculations['unit_value']
            item.total_value = calculations['total_value']
            item.profitability = calculations['profitability']
            item.commission_value = calculations['commission_value']
            item.weight_difference = calculations['weight_difference']
        
        await db.commit()
        await db.refresh(budget)
        return budget
    
    @staticmethod
    async def apply_markup_to_budget(db: AsyncSession, budget_id: int, markup_percentage: float) -> Optional[Budget]:
        """Apply markup percentage to budget and adjust prices"""
        budget = await BudgetService.get_budget_by_id(db, budget_id)
        if not budget:
            return None
        
        # Get items data
        items_data = []
        for item in budget.items:
            items_data.append({
                                'purchase_value_with_icms': item.purchase_value_with_icms,
                'purchase_icms_percentage': item.purchase_icms_percentage,
                'purchase_other_expenses': item.purchase_other_expenses,
                'sale_value_with_icms': item.sale_value_with_icms,
                'sale_icms_percentage': item.sale_icms_percentage,
                'commission_percentage': item.commission_percentage,
                'weight': item.weight,
                'sale_weight': item.sale_weight
            })
        
        # Calculate with desired markup
        result = BudgetCalculatorService.calculate_with_markup(items_data, markup_percentage)
        
        # Update budget and items
        budget.markup_percentage = markup_percentage
        budget.total_purchase_value = result['totals']['total_purchase_value']
        budget.total_sale_value = result['totals']['total_sale_value']
        budget.total_commission = result['totals']['total_commission']
        budget.profitability_percentage = result['totals']['profitability_percentage']
        
        # Update items with adjusted prices
        for i, item in enumerate(budget.items):
            adjusted_item = result['adjusted_items'][i]
            
            item.sale_value_with_icms = adjusted_item['sale_value_with_icms']
            item.sale_value_without_taxes = adjusted_item['sale_value_without_taxes']
            item.total_sale = adjusted_item['total_sale']
            item.unit_value = adjusted_item['unit_value']
            item.total_value = adjusted_item['total_value']
            item.profitability = adjusted_item['profitability']
            item.commission_value = adjusted_item['commission_value']
        
        await db.commit()
        await db.refresh(budget)
        return budget
