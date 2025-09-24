"""
Calculadora de Regras de Negócio para Orçamentos
Implementação completa baseada no documento REGRAS_NEGOCIO_ORCAMENTOS_SISTEMA.md
"""
from typing import List, Dict, Any
from decimal import Decimal, ROUND_HALF_UP
from app.services.commission_service import CommissionService

class BusinessRulesCalculator:
    @staticmethod
    def calculate_purchase_value_with_weight_correction(valor_sem_impostos_compra: float, peso_compra: float, peso_venda: float) -> float:
        """
        REGRA 3.2.3: Valor Corrigido por Peso (Compra)
        Formula Sistema: valor_sem_impostos_compra * (peso_compra / peso_venda)
        
        Args:
            valor_sem_impostos_compra (float): Valor de compra sem impostos
            peso_compra (float): Peso de compra
            peso_venda (float): Peso de venda
            
        Returns:
            float: Valor corrigido por peso
        """
        valor_compra_dec = BusinessRulesCalculator._to_decimal(valor_sem_impostos_compra)
        peso_compra_dec = BusinessRulesCalculator._to_decimal(peso_compra)
        peso_venda_dec = BusinessRulesCalculator._to_decimal(peso_venda)
        
        if peso_venda_dec == 0:
            return 0.0
            
        valor_corrigido = valor_compra_dec * (peso_compra_dec / peso_venda_dec)
        return float(valor_corrigido.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP))
    """
    Implementa todas as fórmulas e regras de negócio para cálculo de orçamentos
    Seguindo exatamente as especificações do documento de regras
    """
    
    # Constantes do sistema conforme documento
    PIS_COFINS_PERCENTAGE = Decimal('0.0925')  # 9.25% fixo
    ICMS_DEFAULT_PERCENTAGE = Decimal('0.18')  # 18% padrão
    
    # Constantes IPI (Imposto sobre Produtos Industrializados)
    IPI_VALID_PERCENTAGES = [Decimal('0.0'), Decimal('0.0325'), Decimal('0.05')]  # 0%, 3.25%, 5%
    
    @staticmethod
    def _to_decimal(value: Any) -> Decimal:
        """Converte valor para Decimal para cálculos precisos"""
        if value is None or value == "":
            return Decimal('0')
        return Decimal(str(value))
    
    @staticmethod
    def calculate_distributed_other_expenses(peso_item: float, soma_pesos_pedido: float, outras_despesas_totais: float) -> float:
        """
        REGRA 3.2.1: Distribuição Proporcional de Outras Despesas
        Formula Excel: IF(B7="",0,F27/SUM(B7:B26))
        Formula Sistema: IF peso_item = 0 THEN 0 ELSE outras_despesas_totais / soma_pesos_todos_itens_pedido
        """
        peso_item_dec = BusinessRulesCalculator._to_decimal(peso_item)
        soma_pesos_dec = BusinessRulesCalculator._to_decimal(soma_pesos_pedido)
        outras_despesas_dec = BusinessRulesCalculator._to_decimal(outras_despesas_totais)
        
        if peso_item_dec == 0 or soma_pesos_dec == 0:
            return 0.0
        
        distribuicao = outras_despesas_dec * (peso_item_dec / soma_pesos_dec)
        return float(distribuicao.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
    
    @staticmethod
    def calculate_purchase_value_without_taxes(valor_com_icms: float, percentual_icms: float, outras_despesas_distribuidas: float = 0.0) -> float:
        """
        REGRA 3.2.2: Cálculo do Valor sem Impostos (Compra)
        Formula Excel: C7*(1-D7)*(1-9.25%)+E7
        Formula Sistema: valor_com_icms * (1 - percentual_icms) * (1 - 0.0925) + outras_despesas_distribuidas
        """
        valor_com_icms_dec = BusinessRulesCalculator._to_decimal(valor_com_icms)
        # Convert decimal format (0.18) to actual percentage calculation
        percentual_icms_dec = BusinessRulesCalculator._to_decimal(percentual_icms)
        outras_despesas_dec = BusinessRulesCalculator._to_decimal(outras_despesas_distribuidas)
        
        # Aplicar descontos sequenciais: primeiro ICMS, depois PIS/COFINS
        # Note: percentual_icms is already in decimal format (0.18 for 18%)
        valor_sem_icms = valor_com_icms_dec * (Decimal('1') - percentual_icms_dec)
        valor_sem_impostos = valor_sem_icms * (Decimal('1') - BusinessRulesCalculator.PIS_COFINS_PERCENTAGE)
        
        # Somar outras despesas distribuídas
        resultado = valor_sem_impostos + outras_despesas_dec
        
        return float(resultado.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP))
    
    @staticmethod
    def calculate_sale_value_without_taxes(valor_com_icms: float, percentual_icms: float) -> float:
        """
        REGRA 4.2.1: Cálculo do Valor sem Impostos (Venda)
        Formula Excel: I7*(1-J7)*(1-9.25%)
        Formula Sistema: valor_com_icms * (1 - percentual_icms) * (1 - 0.0925)
        """
        valor_com_icms_dec = BusinessRulesCalculator._to_decimal(valor_com_icms)
        # Convert decimal format (0.18) to actual percentage calculation
        percentual_icms_dec = BusinessRulesCalculator._to_decimal(percentual_icms)
        
        # Aplicar descontos sequenciais
        # Note: percentual_icms is already in decimal format (0.18 for 18%)
        valor_sem_icms = valor_com_icms_dec * (Decimal('1') - percentual_icms_dec)
        valor_sem_impostos = valor_sem_icms * (Decimal('1') - BusinessRulesCalculator.PIS_COFINS_PERCENTAGE)
        
        return float(valor_sem_impostos.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP))
    
    @staticmethod
    def calculate_weight_difference(peso_venda: float, peso_compra: float) -> float:
        """
        Calculate the weight difference between sale and purchase.

        Args:
            peso_venda (float): The weight for sale.
            peso_compra (float): The weight for purchase.

        Returns:
            float: The weight difference.
        """
        return peso_venda - peso_compra

    @staticmethod
    def calculate_unit_sale_value(valor_sem_impostos_venda: float, peso_venda: float) -> float:
        """
        REGRA 4.2.3: Valor Unitário de Venda
        Formula Sistema: IF peso_venda = 0 THEN 0 ELSE valor_sem_impostos_venda / peso_venda
        """
        valor_sem_impostos_dec = BusinessRulesCalculator._to_decimal(valor_sem_impostos_venda)
        peso_venda_dec = BusinessRulesCalculator._to_decimal(peso_venda)
        
        if peso_venda_dec == 0:
            return 0.0
        
        valor_unitario = valor_sem_impostos_dec / peso_venda_dec
        return float(valor_unitario.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP))
    
    @staticmethod
    def calculate_item_profitability(valor_venda: float, valor_compra: float) -> float:
        """
        REGRA 5.2.1: Rentabilidade por Item
        Formula Excel: IFERROR(K7/G7-1,0)
        Formula Sistema: IF valor_compra = 0 THEN 0 ELSE (valor_venda / valor_compra) - 1
        
        NOTA: Para cálculo correto de markup/rentabilidade, usar valores COM ICMS
        tanto para compra quanto para venda para comparação consistente.
        """
        valor_venda_dec = BusinessRulesCalculator._to_decimal(valor_venda)
        valor_compra_dec = BusinessRulesCalculator._to_decimal(valor_compra)
        
        if valor_compra_dec == 0:
            return 0.0
        
        rentabilidade = (valor_venda_dec / valor_compra_dec) - Decimal('1')
        return float(rentabilidade.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP))
    
    @staticmethod
    def calculate_budget_markup(soma_total_venda_pedido: float, soma_total_compra_pedido: float) -> float:
        """
        REGRA 5.2.4: Markup do Pedido
        Formula Excel: IFERROR(O7/N7-1,0)
        Formula Sistema: IF soma_total_compra_pedido = 0 THEN 0 ELSE (soma_total_venda_pedido / soma_total_compra_pedido) - 1
        """
        soma_venda_dec = BusinessRulesCalculator._to_decimal(soma_total_venda_pedido)
        soma_compra_dec = BusinessRulesCalculator._to_decimal(soma_total_compra_pedido)
        
        if soma_compra_dec == 0:
            return 0.0
        
        markup = (soma_venda_dec / soma_compra_dec) - Decimal('1')
        return float(markup.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP))
    
    @staticmethod
    def calculate_dunamis_cost_v1(valor_sem_impostos_compra: float, percentual_icms_venda: float) -> float:
        """
        REGRA 7.2.1: Custo com Ajuste de Impostos (Versão 1)
        Formula Excel: G7/(1-J7)/(1-9.25%)
        Formula Sistema: valor_sem_impostos_compra / (1 - percentual_icms) / (1 - 0.0925)
        """
        valor_compra_dec = BusinessRulesCalculator._to_decimal(valor_sem_impostos_compra)
        percentual_icms_dec = BusinessRulesCalculator._to_decimal(percentual_icms_venda)
        
        # Aplicar ajustes sequenciais (divisões "por dentro")
        custo_ajustado = valor_compra_dec / (Decimal('1') - percentual_icms_dec)
        custo_final = custo_ajustado / (Decimal('1') - BusinessRulesCalculator.PIS_COFINS_PERCENTAGE)
        
        return float(custo_final.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP))
    
    @staticmethod
    def calculate_dunamis_cost_v2(valor_sem_impostos_compra: float, percentual_icms_venda: float) -> float:
        """
        REGRA 7.2.2: Custo com Ajuste de Impostos (Versão 2)
        Formula Excel: G7/(1-J7)
        Formula Sistema: valor_sem_impostos_compra / (1 - percentual_icms)
        """
        valor_compra_dec = BusinessRulesCalculator._to_decimal(valor_sem_impostos_compra)
        percentual_icms_dec = BusinessRulesCalculator._to_decimal(percentual_icms_venda)
        
        custo_ajustado = valor_compra_dec / (Decimal('1') - percentual_icms_dec)
        return float(custo_ajustado.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP))
    
    @staticmethod
    def calculate_total_purchase_item(peso_compra: float, valor_sem_impostos_compra: float) -> float:
        """
        REGRA 5.2.2: Total Compra do Item
        Formula Sistema: peso_compra * valor_sem_impostos_compra
        """
        peso_compra_dec = BusinessRulesCalculator._to_decimal(peso_compra)
        valor_compra_dec = BusinessRulesCalculator._to_decimal(valor_sem_impostos_compra)
        total_compra = peso_compra_dec * valor_compra_dec
        return float(total_compra.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP))
    
    @staticmethod
    def calculate_total_sale_item_with_icms(peso_venda: float, valor_com_icms_venda: float) -> float:
        """
        REGRA 5.2.3: Total Venda do Item (COM ICMS)
        Formula Sistema: peso_venda * valor_com_icms_venda
        
        IMPORTANTE: Usa valor COM ICMS porque:
        - Representa o valor real pago pelo cliente
        - Base para cálculo de comissões
        - Reflete o faturamento real da empresa
        """
        peso_venda_dec = BusinessRulesCalculator._to_decimal(peso_venda)
        valor_venda_dec = BusinessRulesCalculator._to_decimal(valor_com_icms_venda)
        total_venda = peso_venda_dec * valor_venda_dec
        return float(total_venda.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP))
    
    @staticmethod
    def calculate_ipi_value(valor_com_icms: float, percentual_ipi: float) -> float:
        """
        REGRA IPI.1: Cálculo do Valor do IPI
        Fórmula Sistema: valor_com_icms * percentual_ipi
        
        O IPI é calculado sobre o valor COM ICMS e somado ao valor final.
        Não afeta cálculos de rentabilidade ou comissão.
        
        Args:
            valor_com_icms (float): Valor base com ICMS
            percentual_ipi (float): Percentual de IPI em formato decimal (0.0, 0.0325, 0.05)
            
        Returns:
            float: Valor do IPI calculado
        """
        valor_base_dec = BusinessRulesCalculator._to_decimal(valor_com_icms)
        percentual_ipi_dec = BusinessRulesCalculator._to_decimal(percentual_ipi)
        
        # Validar se o percentual é um dos valores válidos
        if percentual_ipi_dec not in BusinessRulesCalculator.IPI_VALID_PERCENTAGES:
            raise ValueError(f"Percentual de IPI inválido: {percentual_ipi}. Valores aceitos: 0%, 3.25%, 5%")
        
        valor_ipi = valor_base_dec * percentual_ipi_dec
        return float(valor_ipi.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
    
    @staticmethod
    def calculate_total_value_with_ipi(valor_com_icms: float, percentual_ipi: float) -> float:
        """
        REGRA IPI.2: Cálculo do Valor Final com IPI
        Fórmula Sistema: valor_com_icms + (valor_com_icms * percentual_ipi)
        
        Este é o valor final que o cliente pagará.
        
        Args:
            valor_com_icms (float): Valor base com ICMS
            percentual_ipi (float): Percentual de IPI em formato decimal
            
        Returns:
            float: Valor final incluindo IPI
        """
        valor_base_dec = BusinessRulesCalculator._to_decimal(valor_com_icms)
        valor_ipi = BusinessRulesCalculator.calculate_ipi_value(valor_com_icms, percentual_ipi)
        valor_ipi_dec = BusinessRulesCalculator._to_decimal(valor_ipi)
        
        valor_final = valor_base_dec + valor_ipi_dec
        return float(valor_final.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
    
    @staticmethod
    def calculate_total_ipi_item(peso_venda: float, valor_com_icms_venda: float, percentual_ipi: float) -> float:
        """
        REGRA IPI.3: Cálculo do IPI Total do Item
        Fórmula Sistema: peso_venda * valor_com_icms_venda * percentual_ipi
        
        Calcula o valor total de IPI para um item considerando seu peso/quantidade.
        
        Args:
            peso_venda (float): Peso/quantidade de venda
            valor_com_icms_venda (float): Valor unitário com ICMS
            percentual_ipi (float): Percentual de IPI em formato decimal
            
        Returns:
            float: Valor total do IPI para o item
        """
        peso_venda_dec = BusinessRulesCalculator._to_decimal(peso_venda)
        valor_base_total = peso_venda_dec * BusinessRulesCalculator._to_decimal(valor_com_icms_venda)
        
        # Calcular IPI sobre o valor total com ICMS
        valor_ipi_total = BusinessRulesCalculator.calculate_ipi_value(float(valor_base_total), percentual_ipi)
        return valor_ipi_total
    
    @staticmethod
    def calculate_complete_item(item_data: Dict, outras_despesas_totais: float, soma_pesos_pedido: float) -> Dict[str, Any]:
        """
        Calcula todos os valores de um item aplicando todas as regras de negócio sequencialmente
        """
        peso_compra = item_data.get('peso_compra', 0)
        peso_venda = item_data.get('peso_venda', peso_compra)

        if peso_compra <= 0:
            raise ValueError("peso_compra deve ser maior que zero.")
        if peso_venda <= 0:
            raise ValueError("peso_venda deve ser maior que zero.")

        valor_com_icms_compra = item_data.get('valor_com_icms_compra', 0)
        percentual_icms_compra = item_data.get('percentual_icms_compra', 0.18)
        valor_com_icms_venda = item_data.get('valor_com_icms_venda', 0)
        percentual_icms_venda = item_data.get('percentual_icms_venda', 0.18)
        percentual_ipi = item_data.get('percentual_ipi', 0.0)  # IPI padrão 0%

        outras_despesas_distribuidas = BusinessRulesCalculator.calculate_distributed_other_expenses(
            peso_compra, soma_pesos_pedido, outras_despesas_totais
        )

        valor_sem_impostos_compra = BusinessRulesCalculator.calculate_purchase_value_without_taxes(
            valor_com_icms_compra, percentual_icms_compra, outras_despesas_distribuidas
        )

        valor_corrigido_peso = BusinessRulesCalculator.calculate_purchase_value_with_weight_correction(
            valor_sem_impostos_compra, peso_compra, peso_venda
        )

        valor_sem_impostos_venda = BusinessRulesCalculator.calculate_sale_value_without_taxes(
            valor_com_icms_venda, percentual_icms_venda
        )

        diferenca_peso = BusinessRulesCalculator.calculate_weight_difference(peso_venda, peso_compra)

        valor_unitario_venda = BusinessRulesCalculator.calculate_unit_sale_value(valor_sem_impostos_venda, peso_venda)

        # CORREÇÃO: Para comissão, usar rentabilidade baseada em valores SEM impostos
        # Isso reflete a verdadeira rentabilidade operacional da empresa
        # Valores COM ICMS são apenas para markup/comparação de faturamento
        rentabilidade_item = BusinessRulesCalculator.calculate_item_profitability(valor_sem_impostos_venda, valor_sem_impostos_compra)

        total_compra_item = BusinessRulesCalculator.calculate_total_purchase_item(peso_compra, valor_sem_impostos_compra)

        # IMPORTANTE: Total de venda deve usar valor SEM ICMS para que mude quando percentual ICMS muda
        # Conforme regras de negócio originais: total venda = peso * valor_sem_impostos_venda
        total_venda_item = BusinessRulesCalculator.calculate_total_purchase_item(peso_venda, valor_sem_impostos_venda)
        
        # Para cálculo de markup/rentabilidade: usar valores COM ICMS tanto para compra quanto venda
        total_compra_item_com_icms = BusinessRulesCalculator.calculate_total_sale_item_with_icms(peso_compra, valor_com_icms_compra)
        total_venda_item_com_icms = BusinessRulesCalculator.calculate_total_sale_item_with_icms(peso_venda, valor_com_icms_venda)

        # Cálculos de IPI (não afetam rentabilidade ou comissão)
        valor_ipi_unitario = BusinessRulesCalculator.calculate_ipi_value(valor_com_icms_venda, percentual_ipi)
        valor_ipi_total = BusinessRulesCalculator.calculate_total_ipi_item(peso_venda, valor_com_icms_venda, percentual_ipi)
        valor_final_com_ipi = BusinessRulesCalculator.calculate_total_value_with_ipi(valor_com_icms_venda, percentual_ipi)
        
        # CORREÇÃO BUG CENTAVOS: Calcular total final sem arredondamento intermediário
        peso_venda_dec = BusinessRulesCalculator._to_decimal(peso_venda)
        valor_com_icms_venda_dec = BusinessRulesCalculator._to_decimal(valor_com_icms_venda)
        percentual_ipi_dec = BusinessRulesCalculator._to_decimal(percentual_ipi)
        
        # Calcular IPI total sem arredondamento intermediário
        total_base = peso_venda_dec * valor_com_icms_venda_dec
        total_ipi = total_base * percentual_ipi_dec
        total_final_com_ipi_dec = total_base + total_ipi
        total_final_com_ipi = float(total_final_com_ipi_dec.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

        try:
            # IMPORTANTE: Para cálculo correto de comissão quando há diferença de peso:
            # - Se peso_venda = peso_compra: usa rentabilidade unitária
            # - Se peso_venda ≠ peso_compra: usa rentabilidade total (reflete operação completa)
            # Porém, sempre calculamos a rentabilidade com valores SEM impostos primeiro
            
            # Calcular totais SEM impostos para rentabilidade total correta
            total_compra_sem_impostos = peso_compra * valor_sem_impostos_compra
            total_venda_sem_impostos = peso_venda * valor_sem_impostos_venda
            
            if peso_venda == peso_compra:
                # Mesma quantidade: usar rentabilidade unitária (SEM impostos)
                percentual_comissao = CommissionService.calculate_commission_percentage(rentabilidade_item)
            else:
                # Quantidade diferente: usar rentabilidade total (SEM impostos) 
                if total_compra_sem_impostos == 0:
                    rentabilidade_total = 0.0
                else:
                    rentabilidade_total = (total_venda_sem_impostos / total_compra_sem_impostos) - 1
                percentual_comissao = CommissionService.calculate_commission_percentage(rentabilidade_total)
            
            # Aplicar comissão sobre valor COM ICMS (faturamento real)
            valor_comissao = total_venda_item_com_icms * percentual_comissao
            valor_comissao = round(valor_comissao, 2)
        except Exception as e:
            valor_comissao = 0.0
            percentual_comissao = 0.0  # Definir percentual de comissão como 0 em caso de erro
            print(f"Erro ao calcular comissão: {e}")

        return {
            'description': item_data.get('description', ''),
            'peso_compra': peso_compra,
            'peso_venda': peso_venda,
            'valor_com_icms_compra': valor_com_icms_compra,
            'percentual_icms_compra': percentual_icms_compra,
            'valor_com_icms_venda': valor_com_icms_venda,
            'percentual_icms_venda': percentual_icms_venda,
            'percentual_ipi': percentual_ipi,  # Incluir percentual de IPI
            'delivery_time': item_data.get('delivery_time', '0'),  # Prazo de entrega em dias
            'outras_despesas_distribuidas': outras_despesas_distribuidas,
            'valor_sem_impostos_compra': valor_sem_impostos_compra,
            'valor_corrigido_peso': valor_corrigido_peso,
            'valor_sem_impostos_venda': valor_sem_impostos_venda,
            'diferenca_peso': diferenca_peso,
            'valor_unitario_venda': valor_unitario_venda,
            'rentabilidade_item': rentabilidade_item,
            'total_compra_item': total_compra_item,
            'total_venda_item': total_venda_item,
            'total_compra_item_com_icms': total_compra_item_com_icms,
            'total_venda_item_com_icms': total_venda_item_com_icms,
            'valor_comissao': valor_comissao,
            'commission_percentage_actual': percentual_comissao,  # Actual percentage used
            # Campos de IPI
            'valor_ipi_unitario': valor_ipi_unitario,  # IPI por unidade
            'valor_ipi_total': valor_ipi_total,  # IPI total do item
            'valor_final_com_ipi': valor_final_com_ipi,  # Valor unitário final com IPI
            'total_final_com_ipi': total_final_com_ipi,  # Valor total final com IPI
        }
    
    @staticmethod
    def calculate_complete_budget(items_data: List[Dict], outras_despesas_totais: float, soma_pesos_pedido: float) -> Dict[str, Any]:
        """
        Calcula o orçamento completo com base em múltiplos itens.
        """
        total_compra = 0.0
        total_venda = 0.0
        total_comissao = 0.0
        # Para cálculo de markup correto: usar valores COM ICMS
        total_compra_com_icms = 0.0
        total_venda_com_icms = 0.0
        # Totais de IPI - CORREÇÃO BUG CENTAVOS: Usar Decimal para acumulação precisa dos totais
        total_ipi_orcamento_dec = Decimal('0')
        total_final_com_ipi_dec = Decimal('0')
        resultados_itens = []
        
        for item_data in items_data:
            resultado_item = BusinessRulesCalculator.calculate_complete_item(
                item_data, outras_despesas_totais, soma_pesos_pedido
            )
            total_compra += resultado_item['total_compra_item']
            total_venda += resultado_item['total_venda_item']
            total_comissao += resultado_item['valor_comissao']
            # Acumular valores COM ICMS para cálculo correto de markup
            total_compra_com_icms += resultado_item['total_compra_item_com_icms']
            total_venda_com_icms += resultado_item['total_venda_item_com_icms']
            # Acumular IPI com precisão decimal
            item_ipi = resultado_item.get('valor_ipi_total', 0.0)
            item_total_final = resultado_item.get('total_final_com_ipi', resultado_item['total_venda_item_com_icms'])
            total_ipi_orcamento_dec += BusinessRulesCalculator._to_decimal(item_ipi)
            total_final_com_ipi_dec += BusinessRulesCalculator._to_decimal(item_total_final)
            resultados_itens.append(resultado_item)
        
        # Converter de volta para float com precisão correta
        total_ipi_orcamento = float(total_ipi_orcamento_dec.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
        total_final_com_ipi = float(total_final_com_ipi_dec.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

        items_count = len(resultados_itens)
        # CORREÇÃO PM: Usar valores SEM ICMS para markup correto quando ICMS compra ≠ ICMS venda
        # Markup deve refletir a rentabilidade real da operação, não valores brutos com impostos
        markup_pedido = ((total_venda / total_compra) - 1) * 100 if total_compra > 0 else 0.0

        return {
            'totals': {
                'items_count': items_count,
                'soma_pesos_pedido': soma_pesos_pedido,
                'soma_total_compra': total_compra,
                'soma_total_venda': total_venda,
                'soma_total_compra_com_icms': total_compra_com_icms,
                'soma_total_venda_com_icms': total_venda_com_icms,
                'markup_pedido': markup_pedido,
                # Totais de IPI
                'total_ipi_orcamento': total_ipi_orcamento,
                'total_final_com_ipi': total_final_com_ipi,
                'total_comissao': total_comissao,
            },
            'items': resultados_itens,
        }

    @staticmethod
    def validate_item_data(item_data: Dict) -> List[str]:
        """
        Valida dados de um item conforme regras de negócio
        """
        errors = []
        
        # Validações obrigatórias (8.1.1)
        if not item_data.get('description'):
            errors.append("Descrição não pode estar vazia")
        
        # Validar valores de compra e venda (usar nomes corretos dos campos)
        valor_com_icms_compra = item_data.get('valor_com_icms_compra', 0)
        if valor_com_icms_compra <= 0:
            errors.append("Valor de compra deve ser maior que zero")
        
        valor_com_icms_venda = item_data.get('valor_com_icms_venda', 0)
        if valor_com_icms_venda <= 0:
            errors.append("Valor de venda deve ser maior que zero")
        
        # Validar peso de compra
        peso_compra = item_data.get('peso_compra', 0)
        if peso_compra <= 0:
            errors.append("Peso de compra deve ser maior que zero")
        
        # Validar percentuais de ICMS (8.1.2)
        for field_name, field_label in [('percentual_icms_compra', 'ICMS compra'), ('percentual_icms_venda', 'ICMS venda')]:
            percentual = item_data.get(field_name, 0)
            if percentual < 0 or percentual > 1:
                errors.append(f"Percentual de {field_label} deve estar entre 0 e 1")
        
        return errors
