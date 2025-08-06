from typing import List, Dict, Any
from app.schemas.budget import BudgetItemCreate, BudgetItemResponse


class BudgetCalculatorService:
    """
    Service for calculating budget profitability, commissions, and markups
    Based on the spreadsheet logic provided
    """
    
    @staticmethod
    def calculate_item_totals(item_data: dict) -> dict:
        """
        Calculate all financial values for a budget item
        """
        # Basic calculations
        purchase_value_without_taxes = item_data['purchase_value_with_icms'] * (1 - item_data['purchase_icms_percentage'] / 100)
        sale_value_without_taxes = item_data['sale_value_with_icms'] * (1 - item_data['sale_icms_percentage'] / 100)
        
        # Total purchase (including other expenses)
        total_purchase = (purchase_value_without_taxes + item_data.get('purchase_other_expenses', 0)) * item_data['quantity']
        
        # Total sale
        total_sale = sale_value_without_taxes * item_data['quantity']
        
        # Unit value (sale price per unit)
        unit_value = sale_value_without_taxes
        
        # Total value (same as total sale)
        total_value = total_sale
        
        # Profitability calculation
        if total_purchase > 0:
            profitability = ((total_sale - total_purchase) / total_purchase) * 100
        else:
            profitability = 0.0
        
        # Commission calculation
        commission_value = total_sale * (item_data.get('commission_percentage', 0) / 100)
        
        # Weight difference calculation
        weight_difference = 0.0
        if item_data.get('weight') and item_data.get('sale_weight'):
            weight_difference = item_data['sale_weight'] - item_data['weight']
        
        return {
            'purchase_value_without_taxes': purchase_value_without_taxes,
            'sale_value_without_taxes': sale_value_without_taxes,
            'total_purchase': total_purchase,
            'total_sale': total_sale,
            'unit_value': unit_value,
            'total_value': total_value,
            'profitability': profitability,
            'commission_value': commission_value,
            'weight_difference': weight_difference
        }
    
    @staticmethod
    def calculate_budget_totals(items: List[dict]) -> Dict[str, float]:
        """
        Calculate total values for the entire budget
        """
        total_purchase_value = 0.0
        total_sale_value = 0.0
        total_commission = 0.0
        
        for item in items:
            calculations = BudgetCalculatorService.calculate_item_totals(item)
            total_purchase_value += calculations['total_purchase']
            total_sale_value += calculations['total_sale']
            total_commission += calculations['commission_value']
        
        # Overall profitability
        if total_purchase_value > 0:
            profitability_percentage = ((total_sale_value - total_purchase_value) / total_purchase_value) * 100
        else:
            profitability_percentage = 0.0
        
        # Markup calculation
        if total_purchase_value > 0:
            markup_percentage = ((total_sale_value - total_purchase_value) / total_purchase_value) * 100
        else:
            markup_percentage = 0.0
        
        return {
            'total_purchase_value': total_purchase_value,
            'total_sale_value': total_sale_value,
            'total_commission': total_commission,
            'profitability_percentage': profitability_percentage,
            'markup_percentage': markup_percentage
        }
    
    @staticmethod
    def calculate_with_markup(items: List[dict], desired_markup_percentage: float) -> Dict[str, Any]:
        """
        Calculate budget values with a desired markup percentage
        Adjusts sale prices to achieve the target markup
        """
        adjusted_items = []
        total_purchase_value = 0.0
        
        # First pass: calculate total purchase value
        for item in items:
            calculations = BudgetCalculatorService.calculate_item_totals(item)
            total_purchase_value += calculations['total_purchase']
        
        # Calculate required total sale value for desired markup
        required_total_sale_value = total_purchase_value * (1 + desired_markup_percentage / 100)
        
        # Adjust item prices proportionally
        current_total_sale = sum(
            BudgetCalculatorService.calculate_item_totals(item)['total_sale'] 
            for item in items
        )
        
        if current_total_sale > 0:
            adjustment_factor = required_total_sale_value / current_total_sale
            
            for item in items:
                adjusted_item = item.copy()
                adjusted_item['sale_value_with_icms'] *= adjustment_factor
                
                # Recalculate with adjusted prices
                calculations = BudgetCalculatorService.calculate_item_totals(adjusted_item)
                adjusted_item.update(calculations)
                adjusted_items.append(adjusted_item)
        
        # Calculate final totals
        final_totals = BudgetCalculatorService.calculate_budget_totals(adjusted_items)
        
        return {
            'adjusted_items': adjusted_items,
            'totals': final_totals
        }
    
    @staticmethod
    def calculate_commission_summary(items: List[dict]) -> Dict[str, float]:
        """
        Calculate commission summary for the budget
        """
        total_commission = 0.0
        commission_by_percentage = {}
        
        for item in items:
            calculations = BudgetCalculatorService.calculate_item_totals(item)
            commission_value = calculations['commission_value']
            commission_percentage = item.get('commission_percentage', 0)
            
            total_commission += commission_value
            
            if commission_percentage not in commission_by_percentage:
                commission_by_percentage[commission_percentage] = 0.0
            commission_by_percentage[commission_percentage] += commission_value
        
        return {
            'total_commission': total_commission,
            'commission_by_percentage': commission_by_percentage
        }
    
    @staticmethod
    def validate_budget_data(budget_data: dict) -> List[str]:
        """
        Validate budget data and return list of validation errors
        """
        errors = []
        
        # Check if budget has items
        if not budget_data.get('items'):
            errors.append("Orçamento deve ter pelo menos um item")
        
        # Validate each item
        for i, item in enumerate(budget_data.get('items', [])):
            item_prefix = f"Item {i+1}: "
            
            if not item.get('description'):
                errors.append(f"{item_prefix}Descrição é obrigatória")
            
            if not item.get('quantity') or item['quantity'] <= 0:
                errors.append(f"{item_prefix}Quantidade deve ser maior que zero")
            
            if not item.get('purchase_value_with_icms') or item['purchase_value_with_icms'] < 0:
                errors.append(f"{item_prefix}Valor de compra deve ser informado")
            
            if not item.get('sale_value_with_icms') or item['sale_value_with_icms'] < 0:
                errors.append(f"{item_prefix}Valor de venda deve ser informado")
            
            # Check if sale value is higher than purchase value
            if (item.get('sale_value_with_icms', 0) < item.get('purchase_value_with_icms', 0)):
                errors.append(f"{item_prefix}Valor de venda deve ser maior que o valor de compra")
        
        return errors