"""
BusinessRulesCalculator REFATORADO - Usando regras de comissão válidas
"""
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Any, Optional
from app.services.commission_service import CommissionService
from services.profitability_service import ProfitabilityService


class BusinessRulesCalculatorRefactored:
    """
    Calculadora de regras de negócio refatorada
    Agora usa as regras de comissão válidas como fonte de verdade
    """
    
    # Constantes existentes
    PIS_COFINS_PERCENTAGE = Decimal('9.25')
    ICMS_DEFAULT_PERCENTAGE = Decimal('18.00')
    IPI_VALID_PERCENTAGES = [0.0, 3.25, 5.0]
    
    @staticmethod
    def _to_decimal(value: float) -> Decimal:
        """Converter para Decimal com precisão"""
        return Decimal(str(value))
    
    @staticmethod
    def calculate_item_profitability_refactored(
        valor_venda_sem_icms: float, 
        valor_compra_sem_icms_com_frete: float
    ) -> float:
        """
        REGRA ATUALIZADA: Rentabilidade por item SEM ICMS
        
        Args:
            valor_venda_sem_icms: Valor de venda sem ICMS e sem PIS/COFINS
            valor_compra_sem_icms_com_frete: Valor de compra sem ICMS e com frete diluído
        
        Returns:
            float: Rentabilidade em decimal
        """
        venda = BusinessRulesCalculatorRefactored._to_decimal(valor_venda_sem_icms)
        compra = BusinessRulesCalculatorRefactored._to_decimal(valor_compra_sem_icms_com_frete)
        
        if compra <= 0:
            return 0.0
        
        profitability = (venda / compra) - Decimal('1')
        
        return float(profitability.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP))
    
    @staticmethod
    def calculate_budget_markup_refactored(
        soma_total_venda_pedido: float, 
        soma_total_compra_pedido: float
    ) -> float:
        """
        REGRA MANTIDA: Rentabilidade do orçamento COM ICMS
        """
        return BusinessRulesCalculatorRefactored.calculate_budget_markup(
            soma_total_venda_pedido, soma_total_compra_pedido
        )
    
    @staticmethod
    def calculate_complete_item_refactored(
        item_data: Dict[str, Any], 
        outras_despesas_totais: float, 
        soma_pesos_pedido: float, 
        freight_value_total: float = 0.0
    ) -> Dict[str, Any]:
        """
        Método completo refatorado usando regras de comissão válidas
        """
        # ... [manter todos os cálculos anteriores até a rentabilidade] ...
        
        # REGRA ATUALIZADA: Calcular rentabilidade SEM ICMS para comissão
        rentabilidade_item_sem_icms = ProfitabilityService.calculate_item_profitability_without_taxes(
            purchase_value_with_icms=valor_com_icms_compra,
            purchase_icms_percentage=percentual_icms_compra,
            sale_value_with_icms=valor_com_icms_venda,
            sale_icms_percentage=percentual_icms_venda,
            freight_value_per_kg=frete_distribuido_por_kg,
            weight_kg=peso_compra
        )
        
        # REGRA MANTIDA: Rentabilidade para exibição pode usar valores com ICMS
        rentabilidade_display = BusinessRulesCalculatorRefactored.calculate_item_profitability(
            valor_com_icms_venda, valor_com_icms_compra_unitario_com_frete
        )
        
        # REGRA ATUALIZADA: Comissão usa rentabilidade SEM ICMS
        rentabilidade_para_comissao = float(rentabilidade_item_sem_icms)
        percentual_comissao = CommissionService.calculate_commission_percentage(
            rentabilidade_para_comissao
        )
        
        # Calcular valor da comissão baseado na rentabilidade correta
        valor_comissao = total_venda_item_com_icms * (percentual_comissao / 100)
        
        return {
            # ... [todos os campos anteriores] ...
            'rentabilidade_item_sem_icms': float(rentabilidade_item_sem_icms),  # Para comissão
            'rentabilidade_item_display': rentabilidade_display,  # Para exibição
            'percentual_comissao': percentual_comissao,
            'valor_comissao': valor_comissao,
            # ... [restante dos campos] ...
        }