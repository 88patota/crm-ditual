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
    DEFAULT_PIS_COFINS_PERCENTAGE = 9.25  # PIS/COFINS fixo conforme regras (9,25%)
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
        Considera ICMS e PIS/COFINS conforme regra 1 e 3
        
        Args:
            purchase_value_with_icms: Valor de compra com ICMS
            purchase_icms_percentage: Percentual de ICMS na compra
            sale_value_with_icms: Valor de venda com ICMS  
            sale_icms_percentage: Percentual de ICMS na venda
            other_expenses: Outras despesas adicionais
            
        Returns:
            float: Markup percentual calculado
        """
        # Cálculo dos valores sem impostos conforme planilha (regras 1 e 3)
        # Regra 1: [Valor c/ICMS (Compra) * (1 - % ICMS (Compra))] * (1 - Taxa PIS/COFINS)
        purchase_value_without_taxes = (purchase_value_with_icms * (1 - purchase_icms_percentage / 100)) * (1 - BudgetCalculatorService.DEFAULT_PIS_COFINS_PERCENTAGE / 100)
        
        # Regra 3: [Valor c/ICMS (Venda) * (1 - % ICMS (Venda))] * (1 - Taxa PIS/COFINS)
        sale_value_without_taxes = (sale_value_with_icms * (1 - sale_icms_percentage / 100)) * (1 - BudgetCalculatorService.DEFAULT_PIS_COFINS_PERCENTAGE / 100)
        
        # Incluir outras despesas no custo base
        total_purchase_cost = purchase_value_without_taxes + other_expenses
        
        # Fórmula do markup da planilha (regra 5)
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
        # Calcular valor de compra sem impostos (regra 1)
        purchase_value_without_taxes = (purchase_value_with_icms * (1 - purchase_icms_percentage / 100)) * (1 - BudgetCalculatorService.DEFAULT_PIS_COFINS_PERCENTAGE / 100)
        total_purchase_cost = purchase_value_without_taxes + other_expenses
        
        # Calcular valor de venda sem impostos necessário
        sale_value_without_taxes = total_purchase_cost * (1 + desired_markup_percentage / 100)
        
        # Converter para valor com ICMS (processo inverso da regra 3)
        # sale_value_without_taxes = sale_value_with_icms * (1 - sale_icms_percentage / 100) * (1 - PIS_COFINS / 100)
        # Então: sale_value_with_icms = sale_value_without_taxes / [(1 - sale_icms_percentage / 100) * (1 - PIS_COFINS / 100)]
        sale_value_with_icms = sale_value_without_taxes / ((1 - sale_icms_percentage / 100) * (1 - BudgetCalculatorService.DEFAULT_PIS_COFINS_PERCENTAGE / 100))
        
        return round(sale_value_with_icms, 2)
        
        return round(sale_value_with_icms, 2)

    @staticmethod
    def calculate_simplified_item(item_input: BudgetItemSimplified) -> dict:
        """
        Calcula todos os valores de um item baseado apenas nos campos obrigatórios
        Usa os nomes corretos dos campos em português
        """
        
        # Usar campos do schema simplificado correto
        purchase_value_with_icms = item_input.valor_com_icms_compra
        purchase_icms_percentage = item_input.percentual_icms_compra * 100  # Converter decimal para percentual
        sale_value_with_icms = item_input.valor_com_icms_venda
        sale_icms_percentage = item_input.percentual_icms_venda * 100  # Converter decimal para percentual
        
        # REGRA 1: Valor s/Impostos (Compra) = [Valor c/ICMS (Compra) * (1 - % ICMS (Compra))] * (1 - Taxa PIS/COFINS) - Outras Despesas
        purchase_value_without_taxes = (purchase_value_with_icms * (1 - purchase_icms_percentage / 100)) * (1 - BudgetCalculatorService.DEFAULT_PIS_COFINS_PERCENTAGE / 100)
        if item_input.outras_despesas_item:
            purchase_value_without_taxes -= (item_input.outras_despesas_item / (item_input.peso_compra or 1))  # Proporcionalmente ao peso
        
        # REGRA 2: Valor c/Difer. Peso (Compra) = Valor s/Impostos (Compra) * (Peso (Compra) / Peso (Venda))
        peso_compra = item_input.peso_compra or 1.0
        peso_venda = item_input.peso_venda or peso_compra
        purchase_value_with_weight_diff = purchase_value_without_taxes * (peso_compra / peso_venda)
        
        # REGRA 3: Valor s/Impostos (Venda) = [Valor c/ICMS (Venda) * (1 - % ICMS (Venda))] * (1 - Taxa PIS/COFINS)
        sale_value_without_taxes = (sale_value_with_icms * (1 - sale_icms_percentage / 100)) * (1 - BudgetCalculatorService.DEFAULT_PIS_COFINS_PERCENTAGE / 100)
        
        # REGRA 4: Diferença de Peso = (Peso (Venda) - Peso (Compra)) / Peso (Compra)
        weight_difference = 0.0
        if peso_compra and peso_venda:
            weight_difference = (peso_venda - peso_compra) / peso_compra
        
        # REGRA 5: Rentabilidade = [Valor s/Impostos (Venda) / Valor c/Difer. Peso (Compra)] - 1
        if purchase_value_with_weight_diff > 0:
            profitability = (sale_value_without_taxes / purchase_value_with_weight_diff) - 1
        else:
            profitability = 0.0
        
        # REGRA 6: Total Compra = Peso (Compra) * Valor s/Impostos (Compra)
        total_purchase = peso_compra * purchase_value_without_taxes
        
        # REGRA 7: Total Venda = Peso (Venda) * Valor s/Impostos (Venda)
        total_sale = peso_venda * sale_value_without_taxes
        
        # REGRA 8: Valor Total = Peso (Venda) * Valor Unitário (Venda com ICMS)
        unit_value = sale_value_with_icms  # COM ICMS para o usuário ver
        total_value_with_icms = peso_venda * sale_value_with_icms  # COM ICMS para exibição
        
        # REGRA 9: Valor Comissão = Valor Total * % Comissão
        commission_percentage = BudgetCalculatorService.DEFAULT_COMMISSION_PERCENTAGE
        commission_value = total_value_with_icms * (commission_percentage / 100)
        
        # REGRA 10: Custo a ser lançado no Dunamis = Valor c/ICMS (Compra) / (1 - %ICMS (Venda)) / (1 - Taxa PIS/COFINS)
        dunamis_cost = BudgetCalculatorService.calculate_dunamis_cost(
            purchase_value_with_icms=purchase_value_with_icms,
            sale_icms_percentage=sale_icms_percentage
        )
        dunamis_cost = dunamis_cost * peso_compra  # Multiplicar pelo peso para totalizar
        
        return {
            # Dados de entrada preservados
            'description': item_input.description,
            'weight': peso_compra,
            'purchase_value_with_icms': purchase_value_with_icms,
            'purchase_icms_percentage': purchase_icms_percentage,
            'purchase_other_expenses': item_input.outras_despesas_item or 0,
            
            # Valores calculados
            'purchase_value_without_taxes': round(purchase_value_without_taxes, 6),  # Regra 1
            'purchase_value_with_weight_diff': round(purchase_value_with_weight_diff, 6),  # Regra 2
            'sale_weight': peso_venda,
            'sale_value_with_icms': sale_value_with_icms,
            'sale_icms_percentage': sale_icms_percentage,
            'sale_value_without_taxes': round(sale_value_without_taxes, 6),  # Regra 3
            'weight_difference': round(weight_difference, 6),  # Regra 4
            
            # Campos calculados finais
            'profitability': round(profitability * 100, 2),  # Regra 5 em percentual
            'total_purchase': round(total_purchase, 2),  # Regra 6
            'total_sale': round(total_sale, 2),  # Regra 7
            'unit_value': round(unit_value, 2),  # Regra 8
            'total_value': round(total_value_with_icms, 2),  # Regra 8
            
            # Comissão
            'commission_percentage': commission_percentage,
            'commission_value': round(commission_value, 2),  # Regra 9
            'dunamis_cost': round(dunamis_cost, 2)  # Regra 10
        }
    
    @staticmethod
    def calculate_simplified_budget(items_input: List[BudgetItemSimplified]) -> Dict[str, Any]:
        """
        Calcula orçamento completo baseado apenas nos campos obrigatórios
        Aplica as regras de negócio definidas no regras.md
        """
        calculated_items = []
        total_purchase_value = 0.0
        total_sale_value = 0.0
        total_commission = 0.0
        
        for item_input in items_input:
            # Calcular valores do item usando as regras definidas
            calculated_item = BudgetCalculatorService.calculate_simplified_item(item_input)
            calculated_items.append(calculated_item)
            
            # Somar totais baseados no peso (sem quantidade)
            total_purchase_value += calculated_item['total_purchase']
            total_sale_value += calculated_item['total_sale']
            total_commission += calculated_item['commission_value']
        
        # Calcular markup/rentabilidade resultante
        if total_purchase_value > 0:
            markup_percentage = ((total_sale_value - total_purchase_value) / total_purchase_value) * 100
            profitability_percentage = markup_percentage  # Mesmo valor conforme regras
        else:
            markup_percentage = 0.0
            profitability_percentage = 0.0
        
        return {
            'items': calculated_items,
            'totals': {
                'total_purchase_value': round(total_purchase_value, 2),
                'total_sale_value': round(total_sale_value, 2),
                'total_commission': round(total_commission, 2),
                'profitability_percentage': round(profitability_percentage, 2),
                'markup_percentage': round(markup_percentage, 2)
            }
        }
    
    @staticmethod
    def calculate_dunamis_cost(purchase_value_with_icms: float, sale_icms_percentage: float = None) -> float:
        """
        REGRA 10: Calcula o custo a ser lançado no Dunamis
        Fórmula: Valor c/ICMS (Compra) / (1 - %ICMS (Venda)) / (1 - Taxa PIS/COFINS)
        
        Args:
            purchase_value_with_icms: Valor de compra com ICMS
            sale_icms_percentage: Percentual de ICMS na venda (usa padrão se não fornecido)
            
        Returns:
            float: Custo ajustado para lançamento no Dunamis
        """
        if sale_icms_percentage is None:
            sale_icms_percentage = BudgetCalculatorService.DEFAULT_SALE_ICMS_PERCENTAGE
            
        # Aplicar fórmula da regra 10: divisão sequencial "por dentro"
        dunamis_cost = purchase_value_with_icms / (1 - sale_icms_percentage / 100) / (1 - BudgetCalculatorService.DEFAULT_PIS_COFINS_PERCENTAGE / 100)
        
        return round(dunamis_cost, 6)

    @staticmethod
    def validate_simplified_budget_data(budget_data: dict) -> List[str]:
        """
        Valida dados do orçamento simplificado
        Usa os nomes corretos dos campos em português
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
            
            # Usar os nomes corretos dos campos em português
            if not item.get('valor_com_icms_compra') or item['valor_com_icms_compra'] <= 0:
                errors.append(f"{item_prefix}Valor de compra deve ser maior que zero")
                
            if not item.get('valor_com_icms_venda') or item['valor_com_icms_venda'] <= 0:
                errors.append(f"{item_prefix}Valor de venda deve ser maior que zero")
            
            # Validar porcentagens usando nomes corretos
            for field, name in [('percentual_icms_compra', 'ICMS compra'), ('percentual_icms_venda', 'ICMS venda')]:
                if field in item:
                    # As porcentagens vêm em formato decimal (0.18 = 18%)
                    if item[field] < 0 or item[field] > 1:
                        errors.append(f"{item_prefix}{name} deve estar entre 0 e 1 (formato decimal)")
        
        return errors

    @staticmethod
    def calculate_item_totals(item_data: dict) -> dict:
        """
        Calculate all financial values for a budget item following business rules
        """
        # REGRA 1: Cálculo do valor sem impostos de compra
        purchase_value_without_taxes = (item_data['purchase_value_with_icms'] * (1 - item_data['purchase_icms_percentage'] / 100)) * (1 - BudgetCalculatorService.DEFAULT_PIS_COFINS_PERCENTAGE / 100)
        
        # REGRA 3: Cálculo do valor sem impostos de venda  
        sale_value_without_taxes = (item_data['sale_value_with_icms'] * (1 - item_data['sale_icms_percentage'] / 100)) * (1 - BudgetCalculatorService.DEFAULT_PIS_COFINS_PERCENTAGE / 100)
        
        # REGRA 6: Total purchase (including other expenses) - usar weight ao invés de quantity
        weight = item_data.get('weight', 1.0)
        total_purchase = (purchase_value_without_taxes + item_data.get('purchase_other_expenses', 0)) * weight
        
        # REGRA 7: Total sale - usar weight ao invés de quantity
        total_sale = sale_value_without_taxes * weight
        
        # Unit value (sale price per unit with ICMS for user display)
        unit_value = item_data['sale_value_with_icms']
        
        # Total value (with ICMS for user display) - REGRA 8 - usar weight ao invés de quantity
        total_value = item_data['sale_value_with_icms'] * weight
        
        # REGRA 5: Profitability calculation
        if total_purchase > 0:
            profitability = ((total_sale - total_purchase) / total_purchase) * 100
        else:
            profitability = 0.0
        
        # REGRA 9: Commission calculation (on total value with ICMS)
        commission_value = total_value * (item_data.get('commission_percentage', BudgetCalculatorService.DEFAULT_COMMISSION_PERCENTAGE) / 100)
        
        # REGRA 4: Weight difference calculation
        weight_difference = 0.0
        if item_data.get('weight') and item_data.get('sale_weight'):
            weight_difference = (item_data['sale_weight'] - item_data['weight']) / item_data['weight']
        
        return {
            'purchase_value_without_taxes': round(purchase_value_without_taxes, 6),
            'sale_value_without_taxes': round(sale_value_without_taxes, 6),
            'total_purchase': round(total_purchase, 2),
            'total_sale': round(total_sale, 2),
            'unit_value': round(unit_value, 2),
            'total_value': round(total_value, 2),
            'profitability': round(profitability, 2),
            'commission_value': round(commission_value, 2),
            'weight_difference': round(weight_difference, 6)
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
            
            # Validação removida: quantity não existe mais na tabela
            
            if not item.get('purchase_value_with_icms') or item['purchase_value_with_icms'] < 0:
                errors.append(f"{item_prefix}Valor de compra deve ser informado")
            
            if not item.get('sale_value_with_icms') or item['sale_value_with_icms'] < 0:
                errors.append(f"{item_prefix}Valor de venda deve ser informado")
            
            # Check if sale value is higher than purchase value
            if (item.get('sale_value_with_icms', 0) < item.get('purchase_value_with_icms', 0)):
                errors.append(f"{item_prefix}Valor de venda deve ser maior que o valor de compra")
        
        return errors
