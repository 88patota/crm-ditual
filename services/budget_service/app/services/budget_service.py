from typing import List, Optional, cast
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from app.models.budget import Budget, BudgetItem, BudgetStatus
from app.schemas.budget import BudgetCreate, BudgetUpdate, BudgetItemCreate, BudgetItemUpdate
from app.services.business_rules_calculator import BusinessRulesCalculator


class BudgetService:
    
    @staticmethod
    async def create_budget(db: AsyncSession, budget_data: BudgetCreate, created_by: str) -> Budget:
        """Create a new budget with items"""
        
        # Validate budget data
        budget_dict = budget_data.dict()
        items_data = [item.dict() for item in budget_data.items]
        
        # Transform from English schema format to Portuguese BusinessRulesCalculator format if needed
        transformed_items = []
        for item_data in items_data:
            # Check if already in Portuguese format (for backwards compatibility)
            if 'peso_compra' in item_data:
                transformed_items.append(item_data)
            else:
                # Transform from English to Portuguese format
                transformed_item = {
                    'description': item_data.get('description', ''),
                    'peso_compra': item_data.get('weight', 1.0),
                    'peso_venda': item_data.get('sale_weight') or item_data.get('weight', 1.0),
                    'valor_com_icms_compra': item_data.get('purchase_value_with_icms', 0),
                    'percentual_icms_compra': item_data.get('purchase_icms_percentage', 0.18),
                    'outras_despesas_item': item_data.get('purchase_other_expenses', 0),
                    'valor_com_icms_venda': item_data.get('sale_value_with_icms', 0),
                    'percentual_icms_venda': item_data.get('sale_icms_percentage', 0.18),
                    'dunamis_cost': item_data.get('dunamis_cost')
                }
                transformed_items.append(transformed_item)
        
        # Validate items using business rules
        for item_data in transformed_items:
            errors = BusinessRulesCalculator.validate_item_data(item_data)
            if errors:
                raise ValueError(f"Dados inválidos: {'; '.join(errors)}")
        
        # Calculate totals using business rules calculator
        soma_pesos_pedido = sum(item.get('peso_compra', 0) for item in transformed_items)
        outras_despesas_totais = sum(item.get('outras_despesas_item', 0) for item in transformed_items)
        
        budget_result = BusinessRulesCalculator.calculate_complete_budget(
            transformed_items, outras_despesas_totais, soma_pesos_pedido
        )
        
        totals = {
            'total_purchase_value': budget_result['totals']['soma_total_compra'],
            'total_sale_value': budget_result['totals']['soma_total_venda'],
            'total_commission': sum(item['valor_comissao'] for item in budget_result['items']),
            'profitability_percentage': budget_result['totals']['markup_pedido']
        }
        
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
        
        # Create items with calculations from business rules
        for i, item_data in enumerate(transformed_items):
            calculated_item = budget_result['items'][i]
            
            budget_item = BudgetItem(
                budget_id=budget.id,
                description=calculated_item['description'],
                weight=calculated_item['peso_compra'],
                purchase_value_with_icms=calculated_item['valor_com_icms_compra'],
                purchase_icms_percentage=calculated_item['percentual_icms_compra'],
                purchase_other_expenses=calculated_item['outras_despesas_distribuidas'],
                purchase_value_without_taxes=calculated_item['valor_sem_impostos_compra'],
                purchase_value_with_weight_diff=calculated_item['valor_corrigido_peso'],
                sale_weight=calculated_item['peso_venda'],
                sale_value_with_icms=calculated_item['valor_com_icms_venda'],
                sale_icms_percentage=calculated_item['percentual_icms_venda'],
                sale_value_without_taxes=calculated_item['valor_sem_impostos_venda'],
                weight_difference=calculated_item['diferenca_peso'],
                profitability=calculated_item['rentabilidade_item'] * 100,  # Convert to percentage
                total_purchase=calculated_item['total_compra_item'],
                total_sale=calculated_item['total_venda_item'],
                unit_value=calculated_item['valor_unitario_venda'],
                total_value=calculated_item['total_venda_item'],
                commission_value=calculated_item['valor_comissao'],
                commission_percentage=calculated_item.get('percentual_comissao', 0.0),
                commission_percentage_actual=calculated_item.get('commission_percentage_actual', 0.0),
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
        return list(result.scalars().all())
    
    @staticmethod
    async def update_budget(db: AsyncSession, budget_id: int, budget_data: BudgetUpdate) -> Optional[Budget]:
        """Update budget"""
        budget = await BudgetService.get_budget_by_id(db, budget_id)
        if not budget:
            return None
        
        budget_dict = budget_data.dict(exclude_unset=True)
        
        # Handle items update separately if provided
        items_data = budget_dict.pop('items', None)
        
        # Update budget fields (excluding items)
        for field, value in budget_dict.items():
            setattr(budget, field, value)
        
        # Update items if provided
        if items_data is not None:
            # Convert items to list of dicts if needed
            items_list = [item.dict() if hasattr(item, 'dict') else item for item in items_data]
            
            # Transform from English schema format to Portuguese BusinessRulesCalculator format
            transformed_items = []
            for item_data in items_list:
                transformed_item = {
                    'description': item_data.get('description', ''),
                    'peso_compra': item_data.get('weight', 1.0),
                    'peso_venda': item_data.get('sale_weight') or item_data.get('weight', 1.0),
                    'valor_com_icms_compra': item_data.get('purchase_value_with_icms', 0),
                    'percentual_icms_compra': item_data.get('purchase_icms_percentage', 0.18),
                    'outras_despesas_item': item_data.get('purchase_other_expenses', 0),
                    'valor_com_icms_venda': item_data.get('sale_value_with_icms', 0),
                    'percentual_icms_venda': item_data.get('sale_icms_percentage', 0.18),
                    'dunamis_cost': item_data.get('dunamis_cost')
                }
                transformed_items.append(transformed_item)
            
            # Validate items using business rules
            for item_data in transformed_items:
                errors = BusinessRulesCalculator.validate_item_data(item_data)
                if errors:
                    raise ValueError(f"Dados inválidos: {'; '.join(errors)}")
            
            # Remove existing items
            for item in budget.items:
                await db.delete(item)
            await db.flush()
            
            # Calculate totals using business rules calculator
            soma_pesos_pedido = sum(item.get('peso_compra', 0) for item in transformed_items)
            outras_despesas_totais = sum(item.get('outras_despesas_item', 0) for item in transformed_items)
            
            budget_result = BusinessRulesCalculator.calculate_complete_budget(
                transformed_items, outras_despesas_totais, soma_pesos_pedido
            )
            
            # Create new items with calculations from business rules
            for i, item_data in enumerate(transformed_items):
                calculated_item = budget_result['items'][i]
                
                budget_item = BudgetItem(
                    budget_id=budget.id,
                    description=calculated_item['description'],
                    weight=calculated_item['peso_compra'],
                    purchase_value_with_icms=calculated_item['valor_com_icms_compra'],
                    purchase_icms_percentage=calculated_item['percentual_icms_compra'],
                    purchase_other_expenses=calculated_item['outras_despesas_distribuidas'],
                    purchase_value_without_taxes=calculated_item['valor_sem_impostos_compra'],
                    purchase_value_with_weight_diff=calculated_item['valor_corrigido_peso'],
                    sale_weight=calculated_item['peso_venda'],
                    sale_value_with_icms=calculated_item['valor_com_icms_venda'],
                    sale_icms_percentage=calculated_item['percentual_icms_venda'],
                    sale_value_without_taxes=calculated_item['valor_sem_impostos_venda'],
                    weight_difference=calculated_item['diferenca_peso'],
                    profitability=calculated_item['rentabilidade_item'] * 100,  # Convert to percentage
                    total_purchase=calculated_item['total_compra_item'],
                    total_sale=calculated_item['total_venda_item'],
                    unit_value=calculated_item['valor_unitario_venda'],
                    total_value=calculated_item['total_venda_item'],
                    commission_value=calculated_item['valor_comissao'],
                    commission_percentage=calculated_item.get('percentual_comissao', 0.0),
                    commission_percentage_actual=calculated_item.get('commission_percentage_actual', 0.0),
                    dunamis_cost=item_data.get('dunamis_cost')
                )
                db.add(budget_item)
            
            # Update budget totals from business rules result
            setattr(budget, 'total_purchase_value', budget_result['totals']['soma_total_compra'])
            setattr(budget, 'total_sale_value', budget_result['totals']['soma_total_venda'])
            setattr(budget, 'total_commission', cast(float, sum(item['valor_comissao'] for item in budget_result['items'])))
            setattr(budget, 'profitability_percentage', budget_result['totals']['markup_pedido'])
            # Update markup_percentage if it wasn't explicitly set
            if 'markup_percentage' not in budget_dict:
                setattr(budget, 'markup_percentage', budget_result['totals']['markup_pedido'])
        
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
        
        # Get items data in BusinessRulesCalculator format
        items_data = []
        for item in budget.items:
            items_data.append({
                'description': item.description,
                'peso_compra': item.weight,
                'valor_com_icms_compra': item.purchase_value_with_icms,
                'percentual_icms_compra': item.purchase_icms_percentage,
                'outras_despesas_item': item.purchase_other_expenses,
                'peso_venda': item.sale_weight or item.weight,
                'valor_com_icms_venda': item.sale_value_with_icms,
                'percentual_icms_venda': item.sale_icms_percentage
            })
        
        # Recalculate using business rules
        soma_pesos_pedido = sum(item.get('peso_compra', 0) for item in items_data)
        outras_despesas_totais = sum(item.get('outras_despesas_item', 0) for item in items_data)
        
        budget_result = BusinessRulesCalculator.calculate_complete_budget(
            items_data, outras_despesas_totais, soma_pesos_pedido
        )
        
        # Update budget totals
        setattr(budget, 'total_purchase_value', budget_result['totals']['soma_total_compra'])
        setattr(budget, 'total_sale_value', budget_result['totals']['soma_total_venda'])
        setattr(budget, 'total_commission', cast(float, sum(item['valor_comissao'] for item in budget_result['items'])))
        setattr(budget, 'profitability_percentage', budget_result['totals']['markup_pedido'])
        setattr(budget, 'markup_percentage', budget_result['totals']['markup_pedido'])
        
        # Recalculate each item
        for i, item in enumerate(budget.items):
            calculated_item = budget_result['items'][i]
            
            item.purchase_value_without_taxes = calculated_item['valor_sem_impostos_compra']
            item.purchase_value_with_weight_diff = calculated_item['valor_corrigido_peso']
            item.sale_value_without_taxes = calculated_item['valor_sem_impostos_venda']
            item.weight_difference = calculated_item['diferenca_peso']
            item.profitability = calculated_item['rentabilidade_item'] * 100  # Convert to percentage
            item.total_purchase = calculated_item['total_compra_item']
            item.total_sale = calculated_item['total_venda_item']
            item.unit_value = calculated_item['valor_unitario_venda']
            item.total_value = calculated_item['total_venda_item']
            item.commission_value = calculated_item['valor_comissao']
            item.commission_percentage = calculated_item.get('percentual_comissao', 0.0)
            item.commission_percentage_actual = calculated_item.get('commission_percentage_actual', 0.0)
        
        await db.commit()
        await db.refresh(budget)
        return budget
    
    @staticmethod
    async def apply_markup_to_budget(db: AsyncSession, budget_id: int, markup_percentage: float) -> Optional[Budget]:
        """Apply markup percentage to budget and adjust prices"""
        budget = await BudgetService.get_budget_by_id(db, budget_id)
        if not budget:
            return None
        
        # Get items data in BusinessRulesCalculator format
        items_data = []
        for item in budget.items:
            items_data.append({
                'description': item.description,
                'peso_compra': item.weight,
                'valor_com_icms_compra': item.purchase_value_with_icms,
                'percentual_icms_compra': item.purchase_icms_percentage,
                'outras_despesas_item': item.purchase_other_expenses,
                'peso_venda': item.sale_weight or item.weight,
                'valor_com_icms_venda': item.sale_value_with_icms,
                'percentual_icms_venda': item.sale_icms_percentage
            })
        
        # Recalculate with existing values first
        soma_pesos_pedido = sum(item.get('peso_compra', 0) for item in items_data)
        outras_despesas_totais = sum(item.get('outras_despesas_item', 0) for item in items_data)
        
        result = BusinessRulesCalculator.calculate_complete_budget(
            items_data, outras_despesas_totais, soma_pesos_pedido
        )
        
        # Update budget with new markup
        setattr(budget, 'markup_percentage', cast(float, markup_percentage))
        setattr(budget, 'total_purchase_value', result['totals']['soma_total_compra'])
        setattr(budget, 'total_sale_value', result['totals']['soma_total_venda'])
        setattr(budget, 'total_commission', cast(float, sum(item['valor_comissao'] for item in result['items'])))
        setattr(budget, 'profitability_percentage', cast(float, markup_percentage))  # Set to desired markup
        
        # Update items with calculated values
        for i, item in enumerate(budget.items):
            calculated_item = result['items'][i]
            
            item.sale_value_with_icms = calculated_item['valor_com_icms_venda']
            item.sale_value_without_taxes = calculated_item['valor_sem_impostos_venda']
            item.total_sale = calculated_item['total_venda_item']
            item.unit_value = calculated_item['valor_unitario_venda']
            item.total_value = calculated_item['total_venda_item']
            item.profitability = calculated_item['rentabilidade_item'] * 100  # Convert to percentage
            item.commission_value = calculated_item['valor_comissao']
            item.commission_percentage = calculated_item.get('percentual_comissao', 0.0)
            item.commission_percentage_actual = calculated_item.get('commission_percentage_actual', 0.0)
        
        await db.commit()
        await db.refresh(budget)
        return budget
