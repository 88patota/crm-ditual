#!/usr/bin/env python3
"""
Debug detalhado do problema de comissão
"""

import sys
import os

# Adicionar o caminho do serviço de orçamentos
sys.path.append('/Users/erikpatekoski/dev/crm-ditual/services/budget_service')

from app.services.business_rules_calculator import BusinessRulesCalculator
from app.services.commission_service import CommissionService

def debug_commission_step_by_step():
    """Debug passo a passo da comissão"""
    
    print("=== DEBUG DETALHADO DA COMISSÃO ===")
    print()
    
    # Dados do teste
    peso_compra = 1000
    peso_venda = 1050
    valor_com_icms_compra = 6.0
    valor_com_icms_venda = 7.0
    percentual_icms_compra = 0.18
    percentual_icms_venda = 0.18
    
    # Calcular valores sem impostos
    valor_sem_impostos_compra = valor_com_icms_compra * (1 - percentual_icms_compra) * (1 - 0.0925)
    valor_sem_impostos_venda = valor_com_icms_venda * (1 - percentual_icms_venda) * (1 - 0.0925)
    
    # Totais
    total_compra_item = peso_compra * valor_sem_impostos_compra
    total_venda_item = peso_venda * valor_sem_impostos_venda
    total_venda_item_com_icms = peso_venda * valor_com_icms_venda
    
    print("VALORES CALCULADOS:")
    print(f"Peso compra: {peso_compra}")
    print(f"Peso venda: {peso_venda}")
    print(f"Valor sem impostos compra: {valor_sem_impostos_compra:.6f}")
    print(f"Valor sem impostos venda: {valor_sem_impostos_venda:.6f}")
    print(f"Total compra item: {total_compra_item:.2f}")
    print(f"Total venda item: {total_venda_item:.2f}")
    print(f"Total venda item com ICMS: {total_venda_item_com_icms:.2f}")
    print()
    
    # Testar a nova função de comissão diretamente
    print("=== TESTE FUNÇÃO calculate_commission_value_with_quantity_adjustment ===")
    
    # Simular cenário onde peso_venda != peso_compra (que é o nosso caso)
    print(f"peso_venda ({peso_venda}) == peso_compra ({peso_compra})? {peso_venda == peso_compra}")
    print()
    
    if peso_venda != peso_compra:
        print(">>> Entrando no branch: peso_venda != peso_compra")
        
        # Calcular rentabilidade total usando a função interna
        rentabilidade_total = CommissionService._calculate_total_profitability(total_venda_item_com_icms, total_compra_item)
        print(f"Rentabilidade total calculada: {rentabilidade_total:.6f} ({rentabilidade_total*100:.2f}%)")
        
        # Aplicar comissão
        percentual_comissao = CommissionService.calculate_commission_percentage(rentabilidade_total)
        print(f"Percentual de comissão: {percentual_comissao:.6f} ({percentual_comissao*100:.2f}%)")
        
        valor_comissao = total_venda_item_com_icms * percentual_comissao
        print(f"Valor comissão: {valor_comissao:.2f}")
        print()
        
        # Comparar com o que deveria ser
        print("=== COMPARAÇÃO COM CÁLCULO CORRETO ===")
        total_compra_com_icms = peso_compra * valor_com_icms_compra
        rentabilidade_correta = (total_venda_item_com_icms / total_compra_com_icms) - 1
        print(f"Total compra com ICMS: {total_compra_com_icms:.2f}")
        print(f"Rentabilidade correta: {rentabilidade_correta:.6f} ({rentabilidade_correta*100:.2f}%)")
        
        percentual_correto = CommissionService.calculate_commission_percentage(rentabilidade_correta)
        comissao_correta = total_venda_item_com_icms * percentual_correto
        print(f"Percentual correto: {percentual_correto:.6f} ({percentual_correto*100:.2f}%)")
        print(f"Comissão correta: {comissao_correta:.2f}")
        print()
        
        # PROBLEMA IDENTIFICADO!
        print("=== PROBLEMA IDENTIFICADO ===")
        print(f"O sistema está usando total_compra_item (SEM ICMS): {total_compra_item:.2f}")
        print(f"Mas deveria usar total_compra_com_icms: {total_compra_com_icms:.2f}")
        print()
        print(f"Rentabilidade errada: {rentabilidade_total*100:.2f}% (usando total sem ICMS)")
        print(f"Rentabilidade correta: {rentabilidade_correta*100:.2f}% (usando total com ICMS)")
        print()
        print(f"Isso resulta em comissão de {percentual_comissao*100:.2f}% ao invés de {percentual_correto*100:.2f}%")
    
    # Testar método original para comparação
    print("=== TESTE MÉTODO ORIGINAL ===")
    rentabilidade_original = (valor_com_icms_venda / valor_com_icms_compra) - 1
    comissao_original = CommissionService.calculate_commission_value(total_venda_item_com_icms, rentabilidade_original)
    print(f"Rentabilidade original (unitária): {rentabilidade_original*100:.2f}%")
    print(f"Comissão método original: {comissao_original:.2f}")

if __name__ == "__main__":
    debug_commission_step_by_step()