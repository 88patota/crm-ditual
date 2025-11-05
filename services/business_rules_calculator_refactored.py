"""
BusinessRulesCalculator refatorado para usar regras válidas de comissão.

MUDANÇAS PRINCIPAIS:
1. Comissão agora usa valores SEM ICMS (regra válida)
2. Rentabilidade display mantém com ICMS (para usuário)
3. Rentabilidade do orçamento usa valores COM ICMS (manter compatibilidade)
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Any
import os

from services.profitability_service import ProfitabilityService
from app.services.business_rules_calculator import BusinessRulesCalculator
from app.services.commission_service import CommissionService


class BusinessRulesCalculatorRefactored:
    """
    Versão refatorada do BusinessRulesCalculator que usa regras válidas de comissão.
    """
    
    @staticmethod
    def _to_decimal(value):
        """Converte valor para Decimal com precisão."""
        if value is None:
            return Decimal('0')
        return Decimal(str(value))
    
    @staticmethod
    def calculate_item_profitability_refactored(
        valor_venda_sem_icms, 
        valor_compra_sem_icms,
        freight_value=None,
        purchase_weight=None,
        total_purchase_weight=None
    ):
        """
        NOVA VERSÃO: Usa regra válida SEM ICMS para comissão.
        
        Args:
            valor_venda_sem_icms: Valor de venda do item sem ICMS
            valor_compra_item_sem_icms: Valor de compra do item sem ICMS
            freight_value: Valor do frete (opcional)
            purchase_weight: Peso do item (opcional)
            total_purchase_weight: Peso total (opcional)
            
        Returns:
            Decimal: Rentabilidade do item para comissão (SEM ICMS)
        """
        return ProfitabilityService.calculate_item_profitability_without_taxes(
            valor_venda_sem_icms,
            valor_compra_sem_icms,
            freight_value,
            purchase_weight,
            total_purchase_weight
        )
    
    @staticmethod
    def calculate_budget_markup_refactored(
        soma_total_venda_com_icms, 
        soma_total_compra_com_icms
    ):
        """
        Mantém regra COM ICMS para markup do orçamento (compatibilidade).
        
        Args:
            soma_total_venda_com_icms: Total de venda com ICMS
            soma_total_compra_com_icms: Total de compra com ICMS
            
        Returns:
            Decimal: Markup do pedido
        """
        venda_total = BusinessRulesCalculatorRefactored._to_decimal(soma_total_venda_com_icms)
        compra_total = BusinessRulesCalculatorRefactored._to_decimal(soma_total_compra_com_icms)
        
        if compra_total <= 0:
            return Decimal('0')
            
        markup = (venda_total / compra_total - 1).quantize(Decimal('0.0001'), ROUND_HALF_UP)
        return markup
    
    @staticmethod
    def calculate_complete_item_refactored(
        item_data: Dict,
        outras_despesas_totais: float,
        soma_pesos_pedido: float,
        freight_value_total: float = 0.0
    ) -> Dict[str, Any]:
        """
        VERSÃO REFATORADA: Mantém duas rentabilidades:
        1. Para comissão: SEM ICMS (regra válida)
        2. Para display: COM ICMS (para usuário)
        
        Args:
            item_data: Dados do item
            outras_despesas_totais: Total de outras despesas
            soma_pesos_pedido: Soma total dos pesos
            freight_value_total: Valor total do frete
            
        Returns:
            Dict: Item calculado com rentabilidades separadas
        """
        # Importar métodos do BusinessRulesCalculator original (já importado no topo)
        
        # Calcular valores básicos (usar lógica existente)
        peso_compra = item_data.get('peso_compra', 0)
        peso_venda = item_data.get('peso_venda', peso_compra)
        valor_com_icms_compra = item_data.get('valor_com_icms_compra', 0)
        valor_com_icms_venda = item_data.get('valor_com_icms_venda', 0)
        percentual_icms_compra = item_data.get('percentual_icms_compra', 0.18)
        percentual_icms_venda = item_data.get('percentual_icms_venda', 0.18)
        percentual_ipi = item_data.get('percentual_ipi', 0)
        outras_despesas_item = item_data.get('outras_despesas_item', 0)
        
        # Calcular valores sem impostos
        valor_sem_impostos_compra = BusinessRulesCalculator.calculate_purchase_value_without_taxes(
            valor_com_icms_compra, percentual_icms_compra
        )
        valor_sem_impostos_venda = BusinessRulesCalculator.calculate_sale_value_without_taxes(
            valor_com_icms_venda, percentual_icms_venda
        )
        
        # Calcular frete distribuído
        frete_distribuido_por_kg = 0.0
        if freight_value_total and freight_value_total > 0 and soma_pesos_pedido > 0:
            frete_distribuido_por_kg = freight_value_total / soma_pesos_pedido
        
        # Calcular valores totais
        total_compra_item = peso_compra * valor_sem_impostos_compra
        total_venda_item = peso_venda * valor_sem_impostos_venda
        total_compra_item_com_icms = peso_compra * (valor_com_icms_compra + frete_distribuido_por_kg)
        total_venda_item_com_icms = peso_venda * valor_com_icms_venda
        
        # 🎯 **REGRA VÁLIDA**: Rentabilidade para comissão SEM ICMS
        rentabilidade_comissao = ProfitabilityService.calculate_item_profitability_without_taxes(
            valor_sem_impostos_venda,  # venda sem ICMS
            valor_sem_impostos_compra,  # compra sem ICMS
            freight_value_total,
            peso_compra,
            soma_pesos_pedido
        )
        
        # 📊 DISPLAY: Exibir rentabilidade SEM ICMS (alinhado às regras)
        rentabilidade_display = BusinessRulesCalculator.calculate_item_profitability(
            valor_sem_impostos_venda, valor_sem_impostos_compra
        )
        
        # Comissão: percentual via rentabilidade SEM ICMS; valor sobre TOTAL COM ICMS
        if peso_venda == peso_compra:
            rentabilidade_comissao = CommissionService._calculate_unit_profitability(
                valor_sem_impostos_venda, valor_sem_impostos_compra + frete_distribuido_por_kg
            )
        else:
            rentabilidade_comissao = CommissionService._calculate_total_profitability(
                total_venda_item, total_compra_item
            )
        percentual_comissao = CommissionService.calculate_commission_percentage(rentabilidade_comissao)
        valor_comissao = CommissionService.calculate_commission_value(
            total_venda_item_com_icms, rentabilidade_comissao
        )
        
        # Calcular percentual de comissão baseado na rentabilidade SEM ICMS
        percentual_comissao = CommissionService.calculate_commission_percentage(
            rentabilidade_comissao  # Usa rentabilidade SEM ICMS para percentual
        )
        
        # Calcular IPI com sanitização de percentual (evitar erro por valores não previstos)
        try:
            valor_ipi_unitario = BusinessRulesCalculator.calculate_ipi_value(
                valor_com_icms_venda, percentual_ipi
            )
            valor_ipi_total = BusinessRulesCalculator.calculate_total_ipi_item(
                peso_venda, valor_com_icms_venda, percentual_ipi
            )
            valor_final_com_ipi = BusinessRulesCalculator.calculate_total_value_with_ipi(
                valor_com_icms_venda, percentual_ipi
            )
        except ValueError:
            # Se percentual inválido, usar o mais próximo permitido para manter fluxo
            allowed = [float(p) for p in BusinessRulesCalculator.IPI_VALID_PERCENTAGES]
            # Escolher o valor permitido mais próximo do informado
            percentual_sanitizado = min(allowed, key=lambda p: abs(p - float(percentual_ipi))) if allowed else 0.0
            valor_ipi_unitario = BusinessRulesCalculator.calculate_ipi_value(
                valor_com_icms_venda, percentual_sanitizado
            )
            valor_ipi_total = BusinessRulesCalculator.calculate_total_ipi_item(
                peso_venda, valor_com_icms_venda, percentual_sanitizado
            )
            valor_final_com_ipi = BusinessRulesCalculator.calculate_total_value_with_ipi(
                valor_com_icms_venda, percentual_sanitizado
            )
        total_final_com_ipi = peso_venda * valor_final_com_ipi
        
        # Calcular diferença de peso
        weight_difference_display = BusinessRulesCalculator.calculate_weight_difference_display(
            peso_venda, peso_compra
        )
        
        return {
            'description': item_data.get('description', ''),
            'peso_compra': peso_compra,
            'peso_venda': peso_venda,
            'valor_com_icms_compra': valor_com_icms_compra,
            'percentual_icms_compra': percentual_icms_compra,
            'valor_com_icms_venda': valor_com_icms_venda,
            'percentual_icms_venda': percentual_icms_venda,
            'percentual_ipi': percentual_ipi,
            'outras_despesas_item': outras_despesas_item,
            'valor_sem_impostos_compra': valor_sem_impostos_compra,
            'valor_sem_impostos_venda': valor_sem_impostos_venda,
            'valor_unitario_venda': valor_sem_impostos_venda,
            # 🎯 **DUAS RENTABILIDADES SEPARADAS**
            'rentabilidade_item': rentabilidade_display,  # Para display (SEM ICMS)
            'rentabilidade_comissao': rentabilidade_comissao,  # Para comissão (SEM ICMS)
            'total_compra_item': total_compra_item,
            'total_venda_item': total_venda_item,
            'total_compra_item_com_icms': total_compra_item_com_icms,
            'total_venda_com_icms_item': total_venda_item_com_icms,
            'valor_comissao': valor_comissao,
            'percentual_comissao': percentual_comissao,
            'commission_percentage_actual': percentual_comissao,
            'valor_ipi_unitario': valor_ipi_unitario,
            'valor_ipi_total': valor_ipi_total,
            'valor_final_com_ipi': valor_final_com_ipi,
            'total_final_com_ipi': total_final_com_ipi,
            'frete_distribuido_por_kg': frete_distribuido_por_kg,
            'weight_difference_display': weight_difference_display
        }
    
    @staticmethod
    def calculate_complete_budget_refactored(
        items_data: List[Dict],
        outras_despesas_totais: float,
        soma_pesos_pedido: float,
        freight_value_total: float = 0.0
    ) -> Dict[str, Any]:
        """
        VERSÃO REFATORADA: Mantém markup COM ICMS para compatibilidade.
        
        Args:
            items_data: Lista de dados dos itens
            outras_despesas_totais: Total de outras despesas
            soma_pesos_pedido: Soma total dos pesos
            freight_value_total: Valor total do frete
            
        Returns:
            Dict: Orçamento calculado
        """
        # Importar método original
        from business_rules_calculator import BusinessRulesCalculator
        
        # Usar método original mas com items refatorados
        calculated_items = []
        
        # Totais
        soma_total_compra = 0.0
        soma_total_venda = 0.0
        soma_total_compra_com_icms = 0.0
        soma_total_venda_com_icms = 0.0
        total_comissao = 0.0
        total_ipi_orcamento = 0.0
        total_final_com_ipi = 0.0
        total_peso_compra = 0.0
        total_peso_venda = 0.0
        
        # Calcular cada item com nova lógica
        for item_data in items_data:
            calculated_item = BusinessRulesCalculatorRefactored.calculate_complete_item_refactored(
                item_data, outras_despesas_totais, soma_pesos_pedido, freight_value_total
            )
            calculated_items.append(calculated_item)
            
            # Somar totais
            soma_total_compra += calculated_item['total_compra_item']
            soma_total_venda += calculated_item['total_venda_item']
            soma_total_compra_com_icms += calculated_item['total_compra_item_com_icms']
            soma_total_venda_com_icms += calculated_item['total_venda_com_icms_item']
            total_comissao += calculated_item['valor_comissao']
            total_ipi_orcamento += calculated_item['valor_ipi_total']
            total_final_com_ipi += calculated_item['total_final_com_ipi']
            total_peso_compra += calculated_item['peso_compra']
            total_peso_venda += calculated_item['peso_venda']
        
        # Markup do pedido COM ICMS (manter compatibilidade)
        markup_pedido = BusinessRulesCalculatorRefactored.calculate_budget_markup_refactored(
            soma_total_venda_com_icms, soma_total_compra_com_icms
        )
        
        # Calcular diferença total de peso
        total_weight_difference_percentage = BusinessRulesCalculator.calculate_total_weight_difference_percentage(
            total_peso_venda, total_peso_compra
        )
        
        # Calcular frete por kg
        valor_frete_compra = 0.0
        if freight_value_total and freight_value_total > 0 and soma_pesos_pedido > 0:
            valor_frete_compra = freight_value_total / soma_pesos_pedido
        
        return {
            'items': calculated_items,
            'totals': {
                'soma_total_compra': soma_total_compra,
                'soma_total_venda': soma_total_venda,
                'soma_total_venda_com_icms': soma_total_venda_com_icms,
                'total_comissao': total_comissao,
                'markup_pedido': markup_pedido,
                'total_ipi_orcamento': total_ipi_orcamento,
                'total_final_com_ipi': total_final_com_ipi,
                'total_peso_compra': total_peso_compra,
                'total_peso_venda': total_peso_venda,
                'total_weight_difference_percentage': total_weight_difference_percentage,
                'valor_frete_compra': valor_frete_compra
            }
        }