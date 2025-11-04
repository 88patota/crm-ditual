#!/usr/bin/env python3
"""
Teste para verificar se o sistema deveria aplicar a lógica correta
baseada nos valores SEM ICMS + correção de peso
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'budget_service'))

from app.services.business_rules_calculator import BusinessRulesCalculator

def teste_logica_correta():
    """Testa se o sistema deveria aplicar a lógica de valores SEM ICMS + correção de peso"""
    
    print("=== TESTE DA LÓGICA CORRETA ===")
    
    # Dados dos itens (conforme payload do usuário)
    item1 = {
        'peso_compra': 1000,
        'peso_venda': 1010,
        'valor_com_icms_compra': 2.11,
        'valor_com_icms_venda': 4.32,
        'percentual_icms_compra': 0.18,
        'percentual_icms_venda': 0.18,
        'percentual_ipi': 0.0,
        'outras_despesas_item': 0.0
    }
    
    item2 = item1.copy()  # Item idêntico
    
    # Calcular usando BusinessRulesCalculator
    resultado1 = BusinessRulesCalculator.calculate_complete_item(item1, 0.0, 2020.0)
    resultado2 = BusinessRulesCalculator.calculate_complete_item(item2, 0.0, 2020.0)
    
    print("=== RESULTADOS DO SISTEMA ATUAL ===")
    print(f"Item 1 - Total compra: R$ {resultado1['total_compra_item']:.2f}")
    print(f"Item 1 - Total venda: R$ {resultado1['total_venda_item']:.2f}")
    print(f"Item 1 - Rentabilidade: {resultado1['rentabilidade_item']:.4f} = {resultado1['rentabilidade_item']*100:.2f}%")
    
    total_compra_sistema = resultado1['total_compra_item'] + resultado2['total_compra_item']
    total_venda_sistema = resultado1['total_venda_item'] + resultado2['total_venda_item']
    rentabilidade_sistema = (total_venda_sistema - total_compra_sistema) / total_compra_sistema
    
    print(f"\nTotais do sistema:")
    print(f"Total compra: R$ {total_compra_sistema:.2f}")
    print(f"Total venda: R$ {total_venda_sistema:.2f}")
    print(f"Rentabilidade: {rentabilidade_sistema:.4f} = {rentabilidade_sistema*100:.2f}%")
    
    # Valores esperados pelo usuário
    total_compra_esperado = 3640.314
    total_venda_esperado = 6493.75056
    rentabilidade_esperada = 0.7838435255859797
    
    print(f"\n=== VALORES ESPERADOS PELO USUÁRIO ===")
    print(f"Total compra: R$ {total_compra_esperado:.2f}")
    print(f"Total venda: R$ {total_venda_esperado:.2f}")
    print(f"Rentabilidade: {rentabilidade_esperada:.4f} = {rentabilidade_esperada*100:.2f}%")
    
    print(f"\n=== DIFERENÇAS ===")
    diff_compra = total_compra_sistema - total_compra_esperado
    diff_venda = total_venda_sistema - total_venda_esperado
    diff_rentabilidade = rentabilidade_sistema - rentabilidade_esperada
    
    print(f"Diferença compra: R$ {diff_compra:.2f}")
    print(f"Diferença venda: R$ {diff_venda:.2f}")
    print(f"Diferença rentabilidade: {diff_rentabilidade:.4f} = {diff_rentabilidade*100:.2f} pontos percentuais")
    
    print(f"\n=== ANÁLISE DETALHADA ===")
    print("Valores do sistema (SEM impostos):")
    print(f"  Valor sem impostos compra: R$ {resultado1['valor_sem_impostos_compra']:.6f}")
    print(f"  Valor sem impostos venda: R$ {resultado1['valor_sem_impostos_venda']:.6f}")
    # print(f"  Valor compra corrigido: R$ {resultado1['valor_compra_corrigido']:.6f}")  # Chave não existe
    
    # Calcular manualmente o que deveria ser
    print(f"\nCálculo manual esperado:")
    
    # 1. Valores SEM ICMS e SEM PIS/COFINS
    icms = 0.18
    pis_cofins = 0.0925
    
    valor_sem_impostos_compra = (item1['valor_com_icms_compra'] / (1 + icms)) * (1 - pis_cofins)
    valor_sem_impostos_venda = (item1['valor_com_icms_venda'] / (1 + icms)) * (1 - pis_cofins)
    
    print(f"  Valor sem impostos compra: R$ {valor_sem_impostos_compra:.6f}")
    print(f"  Valor sem impostos venda: R$ {valor_sem_impostos_venda:.6f}")
    
    # 2. Correção de peso na compra
    valor_compra_corrigido = valor_sem_impostos_compra * (item1['peso_compra'] / item1['peso_venda'])
    print(f"  Valor compra corrigido: R$ {valor_compra_corrigido:.6f}")
    
    # 3. Totais
    total_compra_manual = 2 * item1['peso_venda'] * valor_compra_corrigido  # Usar peso_venda
    total_venda_manual = 2 * item1['peso_venda'] * valor_sem_impostos_venda
    
    print(f"  Total compra manual: R$ {total_compra_manual:.2f}")
    print(f"  Total venda manual: R$ {total_venda_manual:.2f}")
    
    rentabilidade_manual = (total_venda_manual - total_compra_manual) / total_compra_manual
    print(f"  Rentabilidade manual: {rentabilidade_manual:.4f} = {rentabilidade_manual*100:.2f}%")
    
    print(f"\n=== COMPARAÇÃO COM ESPERADO ===")
    print(f"Diferença compra manual vs esperado: R$ {abs(total_compra_manual - total_compra_esperado):.2f}")
    print(f"Diferença venda manual vs esperado: R$ {abs(total_venda_manual - total_venda_esperado):.2f}")
    print(f"Diferença rentabilidade manual vs esperada: {abs(rentabilidade_manual - rentabilidade_esperada):.6f}")
    
    if abs(total_compra_manual - total_compra_esperado) < 10.0:
        print("✅ LÓGICA CORRETA IDENTIFICADA!")
        print("O sistema deveria usar valores SEM impostos + correção de peso")
    else:
        print("❌ Ainda há discrepância na lógica")

if __name__ == "__main__":
    teste_logica_correta()