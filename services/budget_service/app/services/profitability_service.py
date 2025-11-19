"""
Service unificado para cálculo de rentabilidade - Fonte Única de Verdade
"""
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Optional


class ProfitabilityService:
    """
    Service central para todos os cálculos de rentabilidade
    
    REGRAS DE COMISSÃO VÁLIDAS:
    1. Rentabilidade por item: (valor venda sem icms / valor compra sem icms - 1)
       - Frete diluído pelo peso de compra sem icms
    2. Rentabilidade do orçamento: (valor total venda / valor total compra - 1)
    """
    
    # Constantes
    PIS_COFINS_PERCENTAGE = Decimal('9.25')
    ICMS_DEFAULT_PERCENTAGE = Decimal('18.00')
    
    @staticmethod
    def _to_decimal(value: float) -> Decimal:
        """Converter para Decimal com precisão"""
        return Decimal(str(value))
    
    @staticmethod
    def _remove_taxes(value_with_icms: float, icms_percentage: float) -> Decimal:
        """Remover ICMS e PIS/COFINS do valor"""
        value = ProfitabilityService._to_decimal(value_with_icms)
        icms = ProfitabilityService._to_decimal(icms_percentage)
        pis_cofins = ProfitabilityService.PIS_COFINS_PERCENTAGE
        
        # Remover ICMS primeiro
        value_without_icms = value * (Decimal('1') - icms / Decimal('100'))
        # Depois remover PIS/COFINS
        value_without_taxes = value_without_icms * (Decimal('1') - pis_cofins / Decimal('100'))
        
        return value_without_taxes
    
    @staticmethod
    def calculate_item_profitability_without_taxes(
        purchase_value_with_icms: float,
        purchase_icms_percentage: float,
        sale_value_with_icms: float,
        sale_icms_percentage: float,
        freight_value_per_kg: float = 0.0,
        weight_kg: float = 1.0
    ) -> Decimal:
        """
        REGRA 1: Rentabilidade por item SEM ICMS
        
        Args:
            purchase_value_with_icms: Valor de compra com ICMS
            purchase_icms_percentage: % ICMS na compra
            sale_value_with_icms: Valor de venda com ICMS
            sale_icms_percentage: % ICMS na venda
            freight_value_per_kg: Frete por kg (será diluído)
            weight_kg: Peso em kg para diluição do frete
        
        Returns:
            Decimal: Rentabilidade em decimal (ex: 0.20 para 20%)
        """
        # Converter valores sem impostos
        purchase_without_taxes = ProfitabilityService._remove_taxes(
            purchase_value_with_icms, purchase_icms_percentage
        )
        sale_without_taxes = ProfitabilityService._remove_taxes(
            sale_value_with_icms, sale_icms_percentage
        )
        
        # Adicionar frete diluído ao valor de compra
        freight_total = ProfitabilityService._to_decimal(freight_value_per_kg) * ProfitabilityService._to_decimal(weight_kg)
        purchase_with_freight = purchase_without_taxes + freight_total
        
        # Evitar divisão por zero
        if purchase_with_freight <= 0:
            return Decimal('0')
        
        # Calcular rentabilidade
        profitability = (sale_without_taxes / purchase_with_freight) - Decimal('1')
        
        return profitability.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_budget_profitability(
        total_purchase_value: float,
        total_sale_value: float
    ) -> Decimal:
        """
        REGRA 2: Rentabilidade do orçamento todo
        
        Args:
            total_purchase_value: Valor total de compra (pode ser com ou sem ICMS)
            total_sale_value: Valor total de venda (pode ser com ou sem ICMS)
        
        Returns:
            Decimal: Rentabilidade em decimal
        """
        purchase = ProfitabilityService._to_decimal(total_purchase_value)
        sale = ProfitabilityService._to_decimal(total_sale_value)
        
        # Evitar divisão por zero
        if purchase <= 0:
            return Decimal('0')
        
        profitability = (sale / purchase) - Decimal('1')
        
        return profitability.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_commission_profitability(
        purchase_value_with_icms: float,
        purchase_icms_percentage: float,
        sale_value_with_icms: float,
        sale_icms_percentage: float,
        freight_value_per_kg: float = 0.0,
        weight_kg: float = 1.0
    ) -> Decimal:
        """
        Rentabilidade específica para cálculo de comissão
        Usa a mesma lógica da rentabilidade por item sem impostos
        """
        return ProfitabilityService.calculate_item_profitability_without_taxes(
            purchase_value_with_icms=purchase_value_with_icms,
            purchase_icms_percentage=purchase_icms_percentage,
            sale_value_with_icms=sale_value_with_icms,
            sale_icms_percentage=sale_icms_percentage,
            freight_value_per_kg=freight_value_per_kg,
            weight_kg=weight_kg
        )
    
    @staticmethod
    def calculate_display_profitability(
        valor_venda: float,
        valor_compra: float
    ) -> Decimal:
        """
        Rentabilidade para exibição (quando não envolve comissão)
        Pode usar valores com ICMS para simplificação
        """
        venda = ProfitabilityService._to_decimal(valor_venda)
        compra = ProfitabilityService._to_decimal(valor_compra)
        
        if compra <= 0:
            return Decimal('0')
        
        profitability = (venda / compra) - Decimal('1')
        
        return profitability.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def convert_to_percentage(decimal_value: Decimal, decimals: int = 2) -> Decimal:
        """Converter valor decimal para percentual"""
        return (decimal_value * Decimal('100')).quantize(
            Decimal(f'0.{"0" * decimals}'), rounding=ROUND_HALF_UP
        )