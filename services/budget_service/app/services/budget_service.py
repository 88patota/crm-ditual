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
                    'delivery_time': item_data.get('delivery_time', '0'),  # 🔧 CORREÇÃO: Preservar delivery_time
                    'peso_compra': item_data.get('weight', 1.0),
                    'peso_venda': item_data.get('sale_weight') or item_data.get('weight', 1.0),
                    'valor_com_icms_compra': item_data.get('purchase_value_with_icms', 0),
                    'percentual_icms_compra': item_data.get('purchase_icms_percentage', 0.18),
                    'outras_despesas_item': item_data.get('purchase_other_expenses', 0),
                    'valor_com_icms_venda': item_data.get('sale_value_with_icms', 0),
                    'percentual_icms_venda': item_data.get('sale_icms_percentage', 0.18),
                    'percentual_ipi': item_data.get('ipi_percentage', 0.0),  # IPI percentage
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
            markup_percentage=budget_result['totals']['markup_pedido'],  # Use calculated markup
            notes=budget_data.notes,
            expires_at=budget_data.expires_at,
            created_by=created_by,
            total_purchase_value=totals['total_purchase_value'],
            total_sale_value=totals['total_sale_value'],
            total_sale_with_icms=budget_result['totals']['soma_total_venda_com_icms'],
            total_commission=totals['total_commission'],
            profitability_percentage=totals['profitability_percentage'],
            # Add freight_type field
            freight_type=budget_data.freight_type,
            # IPI totals - Fix the key names to match what's returned from BusinessRulesCalculator
            total_ipi_value=budget_result['totals'].get('total_ipi_orcamento', 0.0),
            total_final_value=budget_result['totals'].get('total_final_com_ipi', 0.0)
        )
        
        db.add(budget)
        await db.flush()  # Get the budget ID
        
        # Create items with calculations from business rules
        for i, item_data in enumerate(transformed_items):
            calculated_item = budget_result['items'][i]
            
            # Ensure IPI values are properly calculated and set
            ipi_percentage = calculated_item.get('percentual_ipi', 0.0)
            sale_value_with_icms = calculated_item.get('valor_com_icms_venda', 0.0)
            sale_weight = calculated_item.get('peso_venda', 1.0)
            
            # Calculate IPI value explicitly to ensure it's correct
            ipi_value = BusinessRulesCalculator.calculate_total_ipi_item(
                sale_weight, sale_value_with_icms, ipi_percentage
            )
            
            # Use correct IPI field names from BusinessRulesCalculator
            total_value_with_ipi = calculated_item.get('total_final_com_ipi', 0.0)
            
            budget_item = BudgetItem(
                budget_id=budget.id,
                description=calculated_item['description'],
                delivery_time=item_data.get('delivery_time', '0'),  # CORREÇÃO: Usar delivery_time do item_data original
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
                # IPI fields - use values calculated by BusinessRulesCalculator
                ipi_percentage=ipi_percentage,
                ipi_value=calculated_item.get('valor_ipi_total', ipi_value),  # Use valor_ipi_total from calculator
                total_value_with_ipi=total_value_with_ipi,
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
        budget = result.scalar_one_or_none()
        
        # Campo delivery_time corrigido - valores preservados corretamente
        
        return budget
    
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
        created_by: Optional[str] = None,
        days: Optional[int] = None,
        custom_start: Optional[str] = None,
        custom_end: Optional[str] = None
    ) -> List[Budget]:
        """Get budgets with filtering"""
        from datetime import datetime, timedelta
        
        query = select(Budget).options(selectinload(Budget.items))
        
        # Apply filters
        conditions = []
        if status:
            conditions.append(Budget.status == status)
        if client_name:
            conditions.append(Budget.client_name.ilike(f"%{client_name}%"))
        if created_by:
            conditions.append(Budget.created_by == created_by)
        
        # Date filtering
        if custom_start and custom_end:
            # Custom date range
            start_date = datetime.strptime(custom_start, "%Y-%m-%d")
            end_date = datetime.strptime(custom_end, "%Y-%m-%d")
            # Adjust end_date to include the full day
            end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
            conditions.append(Budget.created_at >= start_date)
            conditions.append(Budget.created_at <= end_date)
        elif days:
            # Days-based filtering
            end_date = datetime.now()
            if days == 1:
                # For "today", start from 00:00:00
                start_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
            else:
                start_date = end_date - timedelta(days=days)
            conditions.append(Budget.created_at >= start_date)
            conditions.append(Budget.created_at <= end_date)
        
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
        
        # Armazenar o freight_type original antes de qualquer processamento
        original_freight_type = budget.freight_type
        print(f"🔍 DEBUG - Original freight_type: {original_freight_type}")
        
        budget_dict = budget_data.dict(exclude_unset=True)
        print(f"DEBUG: budget_dict = {budget_dict}")
        
        # Handle items update separately if provided
        items_data = budget_dict.pop('items', None)
        
        # Store freight_type value before processing items (if it exists in update data)
        freight_type_value = budget_dict.get('freight_type', None)
        print(f"🔍 DEBUG - Freight type in update data: {freight_type_value}")
        
        # Update budget fields (excluding items)
        for field, value in budget_dict.items():
            # Skip freight_type for now, we'll handle it after item processing
            if field != 'freight_type':
                print(f"DEBUG: Setting {field} = {value}")
                setattr(budget, field, value)
        
        # Explicitly handle freight_type if it's in the update data
        if 'freight_type' in budget_dict:
            budget.freight_type = budget_dict['freight_type']
            print(f"DEBUG: Explicitly set freight_type to {budget.freight_type}")
            # Garantir que o valor seja salvo no banco de dados
            await db.flush()
        
        # Update items if provided
        if items_data is not None:
            # Convert items to list of dicts if needed
            items_list = [item.dict() if hasattr(item, 'dict') else item for item in items_data]
            
            # Transform from English schema format to Portuguese BusinessRulesCalculator format
            transformed_items = []
            for item_data in items_list:
                transformed_item = {
                    'description': item_data.get('description', ''),
                    'delivery_time': item_data.get('delivery_time', '0'),  # CORREÇÃO: Incluir delivery_time
                    'peso_compra': item_data.get('weight', 1.0),
                    'peso_venda': item_data.get('sale_weight') or item_data.get('weight', 1.0),
                    'valor_com_icms_compra': item_data.get('purchase_value_with_icms', 0),
                    'percentual_icms_compra': item_data.get('purchase_icms_percentage', 0.18),
                    'outras_despesas_item': item_data.get('purchase_other_expenses', 0),
                    'valor_com_icms_venda': item_data.get('sale_value_with_icms', 0),
                    'percentual_icms_venda': item_data.get('sale_icms_percentage', 0.18),
                    'percentual_ipi': item_data.get('ipi_percentage', 0.0),  # IPI percentage
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
                
                # DEBUG: Log delivery_time values
                print(f"🔍 DEBUG - Item {i}: delivery_time from item_data = {item_data.get('delivery_time')}")
                print(f"🔍 DEBUG - Item {i}: delivery_time from calculated_item = {calculated_item.get('delivery_time')}")
                
                # Ensure IPI values are properly calculated and set
                ipi_percentage = calculated_item.get('percentual_ipi', 0.0)
                sale_value_with_icms = calculated_item.get('valor_com_icms_venda', 0.0)
                sale_weight = calculated_item.get('peso_venda', 1.0)
                
                # Calculate IPI value explicitly to ensure it's correct
                ipi_value = BusinessRulesCalculator.calculate_total_ipi_item(
                    sale_weight, sale_value_with_icms, ipi_percentage
                )
                
                # Use correct IPI field names from BusinessRulesCalculator
                total_value_with_ipi = calculated_item.get('total_final_com_ipi', 0.0)
                
                budget_item = BudgetItem(
                    budget_id=budget.id,
                    description=calculated_item['description'],
                    delivery_time=item_data.get('delivery_time', '0'),  # CORREÇÃO: Usar delivery_time do item_data original
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
                    # IPI fields - use values calculated by BusinessRulesCalculator
                    ipi_percentage=ipi_percentage,
                    ipi_value=calculated_item.get('valor_ipi_total', ipi_value),  # Use valor_ipi_total from calculator
                    total_value_with_ipi=total_value_with_ipi,
                    dunamis_cost=item_data.get('dunamis_cost')
                )
                db.add(budget_item)
            
            # Update budget totals from business rules result
            setattr(budget, 'total_purchase_value', budget_result['totals']['soma_total_compra'])
            setattr(budget, 'total_sale_value', budget_result['totals']['soma_total_venda'])
            setattr(budget, 'total_sale_with_icms', budget_result['totals']['soma_total_venda_com_icms'])
            setattr(budget, 'total_commission', cast(float, sum(item['valor_comissao'] for item in budget_result['items'])))
            setattr(budget, 'profitability_percentage', budget_result['totals']['markup_pedido'])
            # Always set markup_percentage to the calculated value from business rules
            setattr(budget, 'markup_percentage', budget_result['totals']['markup_pedido'])
            # IPI totals - Fix the key names to match what's returned from BusinessRulesCalculator
            setattr(budget, 'total_ipi_value', budget_result['totals'].get('total_ipi_orcamento', 0.0))
            setattr(budget, 'total_final_value', budget_result['totals'].get('total_final_com_ipi', 0.0))
        
        # CORREÇÃO: Garantir que o freight_type seja sempre definido corretamente
        # Se freight_type estiver nos dados de atualização, use-o
        # Caso contrário, mantenha o valor original
        if freight_type_value is not None:
            budget.freight_type = freight_type_value
            print(f"DEBUG: Final freight_type set to {budget.freight_type}")
        else:
            # Garantir que o valor original seja mantido
            budget.freight_type = original_freight_type
            print(f"DEBUG: Preserving original freight_type: {original_freight_type}")
        
        # Forçar a persistência imediata do freight_type
        await db.flush()
        
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
                'percentual_icms_venda': item.sale_icms_percentage,
                'percentual_ipi': item.ipi_percentage or 0.0  # IPI percentage
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
        setattr(budget, 'total_sale_with_icms', budget_result['totals']['soma_total_venda_com_icms'])
        setattr(budget, 'total_commission', cast(float, sum(item['valor_comissao'] for item in budget_result['items'])))
        setattr(budget, 'profitability_percentage', budget_result['totals']['markup_pedido'])
        setattr(budget, 'markup_percentage', budget_result['totals']['markup_pedido'])
        # IPI totals - Fix the key names to match what's returned from BusinessRulesCalculator
        setattr(budget, 'total_ipi_value', budget_result['totals'].get('total_ipi_orcamento', 0.0))
        setattr(budget, 'total_final_value', budget_result['totals'].get('total_final_com_ipi', 0.0))
        
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
            # IPI fields - explicitly calculate to ensure correctness
            ipi_percentage = calculated_item.get('percentual_ipi', 0.0)
            sale_value_with_icms = calculated_item.get('valor_com_icms_venda', 0.0)
            sale_weight = calculated_item.get('peso_venda', item.sale_weight or item.weight or 1.0)
            
            # Calculate IPI value explicitly to ensure it's correct
            ipi_value = BusinessRulesCalculator.calculate_total_ipi_item(
                sale_weight, sale_value_with_icms, ipi_percentage
            )
            
            item.ipi_percentage = ipi_percentage
            item.ipi_value = ipi_value
            item.total_value_with_ipi = calculated_item.get('total_final_com_ipi', 0.0)
        
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
                'percentual_icms_venda': item.sale_icms_percentage,
                'percentual_ipi': item.ipi_percentage or 0.0  # IPI percentage
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
        setattr(budget, 'total_sale_with_icms', result['totals']['soma_total_venda_com_icms'])
        setattr(budget, 'total_commission', cast(float, sum(item['valor_comissao'] for item in result['items'])))
        setattr(budget, 'profitability_percentage', cast(float, markup_percentage))  # Set to desired markup
        # IPI totals - Fix the key names to match what's returned from BusinessRulesCalculator
        setattr(budget, 'total_ipi_value', result['totals'].get('total_ipi_orcamento', 0.0))
        setattr(budget, 'total_final_value', result['totals'].get('total_final_com_ipi', 0.0))
        
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
            # IPI fields - explicitly calculate to ensure correctness
            ipi_percentage = calculated_item.get('percentual_ipi', 0.0)
            sale_value_with_icms = calculated_item.get('valor_com_icms_venda', 0.0)
            sale_weight = calculated_item.get('peso_venda', item.sale_weight or item.weight or 1.0)
            
            # Calculate IPI value explicitly to ensure it's correct
            ipi_value = BusinessRulesCalculator.calculate_total_ipi_item(
                sale_weight, sale_value_with_icms, ipi_percentage
            )
            
            item.ipi_percentage = ipi_percentage
            item.ipi_value = ipi_value
            item.total_value_with_ipi = calculated_item.get('total_final_com_ipi', 0.0)
        
        await db.commit()
        await db.refresh(budget)
        return budget
