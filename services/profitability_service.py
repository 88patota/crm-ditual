"""
Service unificado para cálculo de rentabilidade com base nas regras válidas de comissão.

Regras válidas:
1. Rentabilidade por item: valor venda sem ICMS / valor compra sem ICMS - 1 + frete diluído
2. Rentabilidade do orçamento: total venda sem ICMS / total compra sem ICMS - 1
"""

from decimal import Decimal, ROUND_HALF_UP


class ProfitabilityService:
    """
    Service unificado para cálculos de rentabilidade.
    Fonte única de verdade para regras de comissão.
    """
    
    @staticmethod
    def _to_decimal(value):
        """Converte valor para Decimal com precisão."""
        if value is None:
            return Decimal('0')
        return Decimal(str(value))
    
    @staticmethod
    def _remove_taxes(value, icms_rate=0.18, pis_cofins_rate=0.095):
        """Remove ICMS e PIS/COFINS de um valor."""
        if not value:
            return Decimal('0')
        
        decimal_value = ProfitabilityService._to_decimal(value)
        total_tax_rate = icms_rate + pis_cofins_rate
        return decimal_value / (1 + total_tax_rate)
    
    @staticmethod
    def calculate_item_profitability_without_taxes(
        valor_venda_item_sem_icms, 
        valor_compra_item_sem_icms, 
        valor_frete_total=None,
        peso_compra_item=None,
        peso_total_compra=None,
        # Aliases usados em testes/regressão
        freight_value=None,
        purchase_weight=None,
        total_purchase_weight=None
    ):
        """
        Calcula rentabilidade por item SEM ICMS (regra válida para comissão).
        
        Args:
            valor_venda_item_sem_icms: Valor de venda do item sem ICMS
            valor_compra_item_sem_icms: Valor de compra do item sem ICMS  
            valor_frete_total: Valor total do frete (opcional)
            peso_compra_item: Peso do item na compra (opcional)
            peso_total_compra: Peso total da compra (opcional)
            
        Returns:
            Decimal: Rentabilidade do item (sem ICMS, com frete diluído se fornecido)
        """
        # Mapear aliases se fornecidos
        if valor_frete_total is None and freight_value is not None:
            valor_frete_total = freight_value
        if peso_compra_item is None and purchase_weight is not None:
            peso_compra_item = purchase_weight
        if peso_total_compra is None and total_purchase_weight is not None:
            peso_total_compra = total_purchase_weight

        venda = ProfitabilityService._to_decimal(valor_venda_item_sem_icms)
        compra = ProfitabilityService._to_decimal(valor_compra_item_sem_icms)
        
        # Adiciona frete diluído pelo peso se fornecido
        if (valor_frete_total and peso_compra_item and peso_total_compra and 
            peso_total_compra > 0):
            
            frete_diluido = (ProfitabilityService._to_decimal(valor_frete_total) * 
                           ProfitabilityService._to_decimal(peso_compra_item) / 
                           ProfitabilityService._to_decimal(peso_total_compra))
            compra += frete_diluido
        
        if compra <= 0:
            return Decimal('0')
            
        rentabilidade = (venda / compra - 1).quantize(Decimal('0.0001'), ROUND_HALF_UP)
        return rentabilidade
    
    @staticmethod
    def calculate_budget_profitability(
        valor_total_venda_sem_icms,
        valor_total_compra_sem_icms
    ):
        """
        Calcula rentabilidade do orçamento total SEM ICMS (regra válida).
        
        Args:
            valor_total_venda_sem_icms: Valor total de venda sem ICMS
            valor_total_compra_sem_icms: Valor total de compra sem ICMS
            
        Returns:
            Decimal: Rentabilidade total do orçamento
        """
        venda_total = ProfitabilityService._to_decimal(valor_total_venda_sem_icms)
        compra_total = ProfitabilityService._to_decimal(valor_total_compra_sem_icms)
        
        if compra_total <= 0:
            return Decimal('0')
            
        rentabilidade = (venda_total / compra_total - 1).quantize(Decimal('0.0001'), ROUND_HALF_UP)
        return rentabilidade
    
    @staticmethod
    def calculate_commission_profitability(
        valor_venda_item_sem_icms,
        valor_compra_item_sem_icms,
        valor_frete_total=None,
        peso_compra_item=None,
        peso_total_compra=None
    ):
        """
        Calcula rentabilidade específica para comissão (usa mesma lógica do item sem ICMS).
        
        Returns:
            Decimal: Rentabilidade para cálculo de comissão
        """
        return ProfitabilityService.calculate_item_profitability_without_taxes(
            valor_venda_item_sem_icms,
            valor_compra_item_sem_icms,
            valor_frete_total,
            peso_compra_item,
            peso_total_compra
        )
    
    @staticmethod
    def calculate_display_profitability(
        valor_venda_item_com_icms=None,
        valor_compra_item_com_icms=None,
        valor_venda_item_sem_icms=None,
        valor_compra_item_sem_icms=None,
        usar_valores_com_icms=True
    ):
        """
        Calcula rentabilidade para exibição (pode usar valores com ICMS).
        
        Args:
            usar_valores_com_icms: Se True, usa valores com ICMS, senão usa sem ICMS
            
        Returns:
            Decimal: Rentabilidade para display do usuário
        """
        if usar_valores_com_icms and valor_venda_item_com_icms and valor_compra_item_com_icms:
            venda = ProfitabilityService._to_decimal(valor_venda_item_com_icms)
            compra = ProfitabilityService._to_decimal(valor_compra_item_com_icms)
        elif valor_venda_item_sem_icms and valor_compra_item_sem_icms:
            venda = ProfitabilityService._to_decimal(valor_venda_item_sem_icms)
            compra = ProfitabilityService._to_decimal(valor_compra_item_sem_icms)
        else:
            return Decimal('0')
            
        if compra <= 0:
            return Decimal('0')
            
        rentabilidade = (venda / compra - 1).quantize(Decimal('0.0001'), ROUND_HALF_UP)
        return rentabilidade
    
    @staticmethod
    def convert_to_percentage(decimal_value, precision=2):
        """
        Converte valor decimal para percentual.
        
        Args:
            decimal_value: Valor em decimal (ex: 0.25 para 25%)
            precision: Número de casas decimais
            
        Returns:
            Decimal: Valor percentual
        """
        return (ProfitabilityService._to_decimal(decimal_value) * 100).quantize(
            Decimal(f'0.{"0" * precision}'), ROUND_HALF_UP
        )