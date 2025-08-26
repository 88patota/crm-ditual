"""
Sistema de Comissões por Faixas de Rentabilidade
Baseado no documento REGRAS_NEGOCIO_ORCAMENTOS_SISTEMA.md
"""
from typing import Dict, List


class CommissionService:
    """
    Service para cálculo de comissões baseadas em faixas de rentabilidade
    Conforme seção 6 do documento de regras de negócio
    """
    
    # Tabela de faixas de comissão conforme documento
    COMMISSION_BRACKETS = [
        {"min_profitability": 0.0, "max_profitability": 0.20, "commission_rate": 0.00},    # < 20% = 0%
        {"min_profitability": 0.20, "max_profitability": 0.30, "commission_rate": 0.01},   # 20-30% = 1%
        {"min_profitability": 0.30, "max_profitability": 0.40, "commission_rate": 0.015},  # 30-40% = 1.5%
        {"min_profitability": 0.40, "max_profitability": 0.50, "commission_rate": 0.025},  # 40-50% = 2.5%
        {"min_profitability": 0.50, "max_profitability": 0.60, "commission_rate": 0.03},   # 50-60% = 3%
        {"min_profitability": 0.60, "max_profitability": 0.80, "commission_rate": 0.04},   # 60-80% = 4%
        {"min_profitability": 0.80, "max_profitability": float('inf'), "commission_rate": 0.05}  # >=80% = 5%
    ]
    
    @staticmethod
    def calculate_commission_percentage(rentabilidade: float) -> float:
        """
        Calcula o percentual de comissão baseado na rentabilidade do item
        
        Formula conforme documento:
        IF(M7="","",IF(M7<20%,0,IF(M7<30%,1%,IF(M7<40%,1.5%,IF(M7<50%,2.5%,IF(M7<60%,3%,IF(M7<80%,4%,IF(M7<100%,5%,5%))))))))
        
        Args:
            rentabilidade: Rentabilidade do item em decimal (ex: 0.25 = 25%)
            
        Returns:
            float: Percentual de comissão em decimal (ex: 0.015 = 1.5%)
        """
        # Tratar valores nulos ou vazios
        if rentabilidade is None or rentabilidade == "":
            return 0.0
        
        # Implementação da fórmula usando as faixas definidas
        for bracket in CommissionService.COMMISSION_BRACKETS:
            if rentabilidade >= bracket["min_profitability"] and rentabilidade < bracket["max_profitability"]:
                return bracket["commission_rate"]
        
        # Para rentabilidades muito altas (>=80%), usar comissão máxima
        return 0.05
    
    @staticmethod
    def calculate_commission_value_with_quantity_adjustment(total_venda_item: float, total_compra_item: float, peso_venda: float, peso_compra: float, valor_sem_impostos_venda: float, valor_sem_impostos_compra: float) -> float:
        """
        Calcula o valor da comissão considerando diferenças de quantidade entre venda e compra
        
        Esta nova regra considera que quando se vende uma quantidade maior que a comprada,
        a comissão deve refletir o valor real da operação, não apenas a rentabilidade unitária.
        
        Args:
            total_venda_item: Valor total de venda do item
            total_compra_item: Valor total de compra do item  
            peso_venda: Quantidade/peso vendido
            peso_compra: Quantidade/peso comprado
            valor_sem_impostos_venda: Valor unitário de venda sem impostos
            valor_sem_impostos_compra: Valor unitário de compra sem impostos
            
        Returns:
            float: Valor da comissão considerando ajuste de quantidade
        """
        
        # Se não há diferença de peso, usar cálculo tradicional
        if peso_venda == peso_compra:
            rentabilidade_unitaria = CommissionService._calculate_unit_profitability(valor_sem_impostos_venda, valor_sem_impostos_compra)
            return CommissionService.calculate_commission_value(total_venda_item, rentabilidade_unitaria)
        
        # Para casos com diferença de peso, calcular rentabilidade baseada nos totais reais
        rentabilidade_total = CommissionService._calculate_total_profitability(total_venda_item, total_compra_item)
        
        # Aplicar comissão sobre o valor total de venda
        percentual_comissao = CommissionService.calculate_commission_percentage(rentabilidade_total)
        valor_comissao = total_venda_item * percentual_comissao
        
        return round(valor_comissao, 2)
    
    @staticmethod
    def _calculate_unit_profitability(valor_sem_impostos_venda: float, valor_sem_impostos_compra: float) -> float:
        """
        Calcula rentabilidade unitária (valor por kg/unidade)
        
        Args:
            valor_sem_impostos_venda: Valor unitário de venda sem impostos
            valor_sem_impostos_compra: Valor unitário de compra sem impostos
            
        Returns:
            float: Rentabilidade unitária em decimal
        """
        if valor_sem_impostos_compra == 0:
            return 0.0
        
        return (valor_sem_impostos_venda / valor_sem_impostos_compra) - 1
    
    @staticmethod
    def _calculate_total_profitability(total_venda_item: float, total_compra_item: float) -> float:
        """
        Calcula rentabilidade baseada nos valores totais da operação
        
        Esta abordagem considera o valor real da operação completa,
        incluindo diferenças de quantidade vendida vs comprada.
        
        Args:
            total_venda_item: Valor total de venda do item
            total_compra_item: Valor total de compra do item
            
        Returns:
            float: Rentabilidade total da operação em decimal
        """
        if total_compra_item == 0:
            return 0.0
        
        return (total_venda_item / total_compra_item) - 1
    
    @staticmethod
    def calculate_commission_value(total_venda_item: float, rentabilidade: float) -> float:
        """
        Calcula o valor da comissão para um item (método original)
        
        Formula conforme documento (Regra 6.2.3):
        R7*S7 = valor_total_venda_item * percentual_comissao
        
        Args:
            total_venda_item: Valor total de venda do item
            rentabilidade: Rentabilidade do item em decimal
            
        Returns:
            float: Valor da comissão em R$
        """
        percentual_comissao = CommissionService.calculate_commission_percentage(rentabilidade)
        valor_comissao = total_venda_item * percentual_comissao
        return round(valor_comissao, 2)
    
    @staticmethod
    def calculate_budget_total_commission(items_data: List[Dict]) -> Dict:
        """
        Calcula comissão total do pedido e resumo por faixas
        
        Formula conforme documento (Regra 6.2.4):
        SUM(T7:T26) = soma(valor_comissao_todos_itens_pedido)
        
        Args:
            items_data: Lista de dados dos itens do pedido
            
        Returns:
            dict: Resumo das comissões calculadas
        """
        total_commission = 0.0
        commission_by_bracket = {}
        items_summary = []
        
        for item in items_data:
            # Obter dados necessários
            total_venda_item = item.get('total_venda_item', 0.0)
            rentabilidade = item.get('rentabilidade_item', 0.0)
            
            # Calcular comissão do item
            percentual_comissao = CommissionService.calculate_commission_percentage(rentabilidade)
            valor_comissao = CommissionService.calculate_commission_value(total_venda_item, rentabilidade)
            
            # Somar ao total
            total_commission += valor_comissao
            
            # Agrupar por faixa para relatório
            bracket_key = f"{percentual_comissao*100:.1f}%"
            if bracket_key not in commission_by_bracket:
                commission_by_bracket[bracket_key] = 0.0
            commission_by_bracket[bracket_key] += valor_comissao
            
            # Resumo do item
            items_summary.append({
                'description': item.get('description', ''),
                'rentabilidade': rentabilidade * 100,  # Em percentual
                'percentual_comissao': percentual_comissao * 100,  # Em percentual
                'valor_comissao': valor_comissao,
                'total_venda_item': total_venda_item
            })
        
        return {
            'total_commission': round(total_commission, 2),
            'commission_by_bracket': commission_by_bracket,
            'items_summary': items_summary,
            'items_count': len(items_data)
        }
    
    @staticmethod
    def get_commission_brackets_info() -> List[Dict]:
        """
        Retorna informações sobre as faixas de comissão para documentação/interface
        
        Returns:
            List[Dict]: Lista das faixas com informações detalhadas
        """
        brackets_info = []
        
        for i, bracket in enumerate(CommissionService.COMMISSION_BRACKETS):
            min_perc = bracket["min_profitability"] * 100
            max_perc = bracket["max_profitability"] * 100 if bracket["max_profitability"] != float('inf') else None
            comm_perc = bracket["commission_rate"] * 100
            
            if max_perc is None:
                range_desc = f">= {min_perc:.0f}%"
            elif i == 0:
                range_desc = f"< {max_perc:.0f}%"
            else:
                range_desc = f"{min_perc:.0f}% a < {max_perc:.0f}%"
            
            brackets_info.append({
                "range_description": range_desc,
                "min_profitability": min_perc,
                "max_profitability": max_perc,
                "commission_percentage": comm_perc,
                "examples": CommissionService._generate_bracket_examples(bracket)
            })
        
        return brackets_info
    
    @staticmethod
    def _generate_bracket_examples(bracket: Dict) -> List[str]:
        """
        Gera exemplos para cada faixa de comissão
        
        Args:
            bracket: Dados da faixa de comissão
            
        Returns:
            List[str]: Lista de exemplos práticos
        """
        examples = []
        comm_rate = bracket["commission_rate"] * 100
        
        if comm_rate == 0:
            examples.append("Rentabilidade baixa - sem comissão")
        elif comm_rate == 1:
            examples.append("Rentabilidade padrão - comissão básica")
        elif comm_rate <= 2.5:
            examples.append("Boa rentabilidade - comissão intermediária")
        elif comm_rate <= 4:
            examples.append("Excelente rentabilidade - comissão alta")
        else:
            examples.append("Rentabilidade excepcional - comissão máxima")
        
        return examples
    
    @staticmethod
    def validate_commission_calculation(rentabilidade: float, valor_total_venda: float) -> Dict:
        """
        Valida e documenta o cálculo de comissão para auditoria
        
        Args:
            rentabilidade: Rentabilidade do item
            valor_total_venda: Valor total de venda do item
            
        Returns:
            dict: Detalhes da validação e cálculo
        """
        percentual_comissao = CommissionService.calculate_commission_percentage(rentabilidade)
        valor_comissao = CommissionService.calculate_commission_value(valor_total_venda, rentabilidade)
        
        # Identificar a faixa aplicada
        faixa_aplicada = None
        for bracket in CommissionService.COMMISSION_BRACKETS:
            if rentabilidade >= bracket["min_profitability"] and rentabilidade < bracket["max_profitability"]:
                faixa_aplicada = bracket
                break
        
        return {
            "validation_passed": True,
            "rentabilidade_input": rentabilidade * 100,  # Em %
            "faixa_aplicada": {
                "min": faixa_aplicada["min_profitability"] * 100 if faixa_aplicada else 0,
                "max": faixa_aplicada["max_profitability"] * 100 if faixa_aplicada and faixa_aplicada["max_profitability"] != float('inf') else "∞",
                "commission_rate": faixa_aplicada["commission_rate"] * 100 if faixa_aplicada else 0
            },
            "calculation_steps": {
                "step1": f"Rentabilidade: {rentabilidade*100:.2f}%",
                "step2": f"Faixa identificada: {percentual_comissao*100:.1f}%",
                "step3": f"Cálculo: R$ {valor_total_venda:.2f} × {percentual_comissao*100:.1f}%",
                "result": f"Comissão: R$ {valor_comissao:.2f}"
            }
        }
