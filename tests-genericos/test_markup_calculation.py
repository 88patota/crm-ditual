#!/usr/bin/env python3
"""
Script para testar diferentes abordagens de cálculo de markup
"""

import sys
import os

# Adicionar o caminho do budget_service ao sys.path
sys.path.append('/Users/erikpatekoski/dev/crm-ditual/services/budget_service')

from app.services.business_rules_calculator import BusinessRulesCalculator

def test_markup_approaches():
    """Testa diferentes abordagens para calcular markup"""
    
    # Dados de teste
    item_data = {
        'description': 'Item Teste',
        'peso_compra': 1.0,
        'peso_venda': 2.0,
        'valor_com_icms_compra': 2.11,
        'percentual_icms_compra': 18.0,
        'valor_com_icms_venda': 4.32,
        'percentual_icms_venda': 17.0,
        'percentual_ipi': 0.0,
        'outras_despesas_item': 0.0
    }
    
    print("=== TESTE DE DIFERENTES ABORDAGENS DE MARKUP ===")
    print(f"Dados de entrada:")
    print(f"  valor_com_icms_compra: {item_data['valor_com_icms_compra']}")
    print(f"  valor_com_icms_venda: {item_data['valor_com_icms_venda']}")
    print(f"  peso_compra: {item_data['peso_compra']}")
    print(f"  peso_venda: {item_data['peso_venda']}")
    print()
    
    # Abordagem 1: Markup unitário (valores unitários)
    markup_unitario = BusinessRulesCalculator.calculate_budget_markup(
        item_data['valor_com_icms_venda'], 
        item_data['valor_com_icms_compra']
    )
    
    print(f"1. Markup unitário: {markup_unitario:.4f} ({markup_unitario*100:.2f}%)")
    print(f"   Cálculo: ({item_data['valor_com_icms_venda']} / {item_data['valor_com_icms_compra']}) - 1")
    print()
    
    # Abordagem 2: Markup com correção de peso (atual)
    total_venda_com_icms = item_data['valor_com_icms_venda'] * item_data['peso_venda']
    total_compra_com_icms_corrigido = item_data['valor_com_icms_compra'] * item_data['peso_venda']
    
    markup_com_peso = BusinessRulesCalculator.calculate_budget_markup(
        total_venda_com_icms, 
        total_compra_com_icms_corrigido
    )
    
    print(f"2. Markup com correção de peso: {markup_com_peso:.4f} ({markup_com_peso*100:.2f}%)")
    print(f"   Total venda: {total_venda_com_icms}")
    print(f"   Total compra corrigido: {total_compra_com_icms_corrigido}")
    print()
    
    # Abordagem 3: Markup com peso real
    total_compra_com_icms_real = item_data['valor_com_icms_compra'] * item_data['peso_compra']
    
    markup_peso_real = BusinessRulesCalculator.calculate_budget_markup(
        total_venda_com_icms, 
        total_compra_com_icms_real
    )
    
    print(f"3. Markup com peso real: {markup_peso_real:.4f} ({markup_peso_real*100:.2f}%)")
    print(f"   Total venda: {total_venda_com_icms}")
    print(f"   Total compra real: {total_compra_com_icms_real}")
    print()
    
    print("=== ANÁLISE ===")
    print("Para exibição, o markup deveria ser baseado nos valores unitários (abordagem 1),")
    print("pois representa a rentabilidade real do produto.")
    print("A correção de peso é importante para cálculos de comissão e totais,")
    print("mas não para a rentabilidade unitária exibida ao usuário.")

if __name__ == "__main__":
    test_markup_approaches()