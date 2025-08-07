from typing import List, Dict, Any
from app.schemas.budget import BudgetItemCreate, BudgetItemResponse, BudgetItemSimplified


class BudgetCalculatorService:
    """
    Service for calculating budget profitability, commissions, and markups
    Baseado na planilha fornecida e requisitos do PM
    """
    
    # Configurações padrão do sistema
    DEFAULT_COMMISSION_PERCENTAGE = 1.5  # 1,5% conforme planilha
    DEFAULT_SALE_ICMS_PERCENTAGE = 17.0  # ICMS padrão para vendas
    DEFAULT_OTHER_EXPENSES = 0.0  # Outras despesas padrão
    DEFAULT_MINIMUM_MARKUP = 20.0  # 20% mínimo
    DEFAULT_MAXIMUM_MARKUP = 200.0  # 200% máximo
    DEFAULT_TARGET_MARGIN = 30.0   # 30% margem alvo
    
    # NOTA: Funções de markup automático temporariamente desabilitadas
    # Elas serão reativadas quando BudgetItemInput for implementado
    
    @staticmethod
    def calculate_automatic_markup_from_planilha(purchase_value_with_icms: float, purchase_icms_percentage: float, 
                                                sale_value_with_icms: float, sale_icms_percentage: float,
                                                other_expenses: float = 0.0) -> float:
        """
        Calcula markup automaticamente seguindo exatamente a fórmula da planilha
        
        Fórmula: ((Valor Venda s/Impostos - Valor Compra s/Impostos) / Valor Compra s/Impostos) * 100
        
        Args:
            purchase_value_with_icms: Valor de compra com ICMS
            purchase_icms_percentage: Percentual de ICMS na compra
            sale_value_with_icms: Valor de venda com ICMS  
            sale_icms_percentage: Percentual de ICMS na venda
            other_expenses: Outras despesas adicionais
            
        Returns:
            float: Markup percentual calculado
        """
        # Cálculo dos valores sem impostos conforme planilha
        purchase_value_without_taxes = purchase_value_with_icms * (1 - purchase_icms_percentage / 100)
        sale_value_without_taxes = sale_value_with_icms * (1 - sale_icms_percentage / 100)
        
        # Incluir outras despesas no custo base
        total_purchase_cost = purchase_value_without_taxes + other_expenses
        
        # Fórmula do markup da planilha
        if total_purchase_cost > 0:
            markup_percentage = ((sale_value_without_taxes - total_purchase_cost) / total_purchase_cost) * 100
        else:
            markup_percentage = 0.0
            
        return round(markup_percentage, 2)

    @staticmethod
    def calculate_sale_price_from_markup(purchase_value_with_icms: float, purchase_icms_percentage: float,
                                       sale_icms_percentage: float, desired_markup_percentage: float,
                                       other_expenses: float = 0.0) -> float:
        """
        Calcula o preço de venda necessário para atingir um markup desejado
        
        Args:
            purchase_value_with_icms: Valor de compra com ICMS
            purchase_icms_percentage: Percentual de ICMS na compra
            sale_icms_percentage: Percentual de ICMS na venda
            desired_markup_percentage: Markup desejado em percentual
            other_expenses: Outras despesas adicionais
            
        Returns:
            float: Preço de venda com ICMS necessário
        """
        # Calcular valor de compra sem impostos
        purchase_value_without_taxes = purchase_value_with_icms * (1 - purchase_icms_percentage / 100)
        total_purchase_cost = purchase_value_without_taxes + other_expenses
        
        # Calcular valor de venda sem impostos necessário
        sale_value_without_taxes = total_purchase_cost * (1 + desired_markup_percentage / 100)
        
        # Converter para valor com ICMS
        sale_value_with_icms = sale_value_without_taxes / (1 - sale_icms_percentage / 100)
        
        return round(sale_value_with_icms, 2)

    @staticmethod
    def calculate_simplified_item(item_input: BudgetItemSimplified) -> dict:
        """
        Calcula todos os valores de um item baseado apenas nos campos obrigatórios
        Segue as fórmulas da planilha fornecida
        """
        
        # Cálculos básicos conforme a planilha
        purchase_value_without_taxes = item_input.purchase_value_with_icms * (1 - item_input.purchase_icms_percentage / 100)
        sale_value_without_taxes = item_input.sale_value_with_icms * (1 - item_input.sale_icms_percentage / 100)
        
        # Valor com diferença de peso (mesmo valor sem impostos por enquanto)
        purchase_value_with_weight_diff = purchase_value_without_taxes
        
        # Totais
        total_purchase = (purchase_value_without_taxes + (item_input.purchase_other_expenses or 0)) * item_input.quantity
        total_sale = sale_value_without_taxes * item_input.quantity
        
        # Valores unitários
        unit_value = sale_value_without_taxes
        total_value = total_sale
        
        # Rentabilidade (markup) usando a nova fórmula da planilha
        markup_percentage = BudgetCalculatorService.calculate_automatic_markup_from_planilha(
            purchase_value_with_icms=item_input.purchase_value_with_icms,
            purchase_icms_percentage=item_input.purchase_icms_percentage,
            sale_value_with_icms=item_input.sale_value_with_icms,
            sale_icms_percentage=item_input.sale_icms_percentage,
            other_expenses=(item_input.purchase_other_expenses or 0.0)
        )
        
        profitability = markup_percentage
        
        # Comissão (usando valor padrão)
        commission_percentage = BudgetCalculatorService.DEFAULT_COMMISSION_PERCENTAGE
        commission_value = total_sale * (commission_percentage / 100)
        
        # Diferença de peso
        weight_difference = 0.0
        sale_weight = item_input.weight
        
        # Custo Dunamis (baseado na planilha)
        dunamis_cost = purchase_value_without_taxes * item_input.quantity
        
        return {
            # Dados de entrada preservados
            'description': item_input.description,
            'quantity': item_input.quantity,
            'weight': item_input.weight,
            'purchase_value_with_icms': item_input.purchase_value_with_icms,
            'purchase_icms_percentage': item_input.purchase_icms_percentage,
            'purchase_other_expenses': item_input.purchase_other_expenses or 0,
            
            # Valores calculados
            'purchase_value_without_taxes': purchase_value_without_taxes,
            'purchase_value_with_weight_diff': purchase_value_with_weight_diff,
            'sale_weight': sale_weight,
            'sale_value_with_icms': item_input.sale_value_with_icms,
            'sale_icms_percentage': item_input.sale_icms_percentage,
            'sale_value_without_taxes': sale_value_without_taxes,
            'weight_difference': weight_difference,
            
            # Campos calculados finais
            'profitability': profitability,
            'total_purchase': total_purchase,
            'total_sale': total_sale,
            'unit_value': unit_value,
            'total_value': total_value,
            
            # Comissão
            'commission_percentage': commission_percentage,
            'commission_value': commission_value,
            'dunamis_cost': dunamis_cost
        }
    
    @staticmethod
    def calculate_simplified_budget(items_input: List[BudgetItemSimplified]) -> Dict[str, Any]:
        """
        Calcula orçamento completo baseado apenas nos campos obrigatórios
        """
        calculated_items = []
        total_purchase_value = 0.0
        total_sale_value = 0.0
        total_commission = 0.0
        
        for item_input in items_input:
            # Calcular valores do item
            calculated_item = BudgetCalculatorService.calculate_simplified_item(item_input)
            calculated_items.append(calculated_item)
            
            total_purchase_value += calculated_item['total_purchase']
            total_sale_value += calculated_item['total_sale']
            total_commission += calculated_item['commission_value']
        
        # Calcular markup resultante
        if total_purchase_value > 0:
            markup_percentage = ((total_sale_value - total_purchase_value) / total_purchase_value) * 100
        else:
            markup_percentage = 0.0
        
        # Calcular rentabilidade geral
        if total_purchase_value > 0:
            profitability_percentage = ((total_sale_value - total_purchase_value) / total_purchase_value) * 100
        else:
            profitability_percentage = 0.0
        
        return {
            'items': calculated_items,
            'totals': {
                'total_purchase_value': total_purchase_value,
                'total_sale_value': total_sale_value,
                'total_commission': total_commission,
                'profitability_percentage': profitability_percentage,
                'markup_percentage': markup_percentage
            }
        }
    
    @staticmethod
    def validate_simplified_budget_data(budget_data: dict) -> List[str]:
        """
        Valida dados do orçamento simplificado
        """
        errors = []
        
        # Verificar se tem itens
        if not budget_data.get('items'):
            errors.append("Orçamento deve ter pelo menos um item")
        
        # Validar cada item
        for i, item in enumerate(budget_data.get('items', [])):
            item_prefix = f"Item {i+1}: "
            
            if not item.get('description'):
                errors.append(f"{item_prefix}Descrição é obrigatória")
            
            if not item.get('quantity') or item['quantity'] <= 0:
                errors.append(f"{item_prefix}Quantidade deve ser maior que zero")
            
            if not item.get('purchase_value_with_icms') or item['purchase_value_with_icms'] <= 0:
                errors.append(f"{item_prefix}Valor de compra deve ser maior que zero")
                
            if not item.get('sale_value_with_icms') or item['sale_value_with_icms'] <= 0:
                errors.append(f"{item_prefix}Valor de venda deve ser maior que zero")
            
            # Validar porcentagens
            for field, name in [('purchase_icms_percentage', 'ICMS compra'), ('sale_icms_percentage', 'ICMS venda')]:
                if field in item:
                    if item[field] < 0 or item[field] > 100:
                        errors.append(f"{item_prefix}{name} deve estar entre 0 e 100%")
        
        return errors

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