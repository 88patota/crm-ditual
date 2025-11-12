#!/usr/bin/env python3
"""
Script para debugar o cálculo de rentabilidade
"""

import sys
import os

# Adicionar o caminho do budget_service ao sys.path
sys.path.append('/Users/erikpatekoski/dev/crm-ditual/services/budget_service')

from app.services.business_rules_calculator import BusinessRulesCalculator

def debug_profitability_calculation():
    """Debug do cálculo de rentabilidade"""
    
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
    
    print("=== DEBUG DO CÁLCULO DE RENTABILIDADE ===")
    print(f"Dados de entrada:")
    print(f"  valor_com_icms_compra: {item_data['valor_com_icms_compra']}")
    print(f"  valor_com_icms_venda: {item_data['valor_com_icms_venda']}")
    print(f"  peso_compra: {item_data['peso_compra']}")
    print(f"  peso_venda: {item_data['peso_venda']}")
    print()
    
    # Calcular valor de compra COM ICMS corrigido pelo peso
    valor_compra_com_icms_corrigido = item_data['valor_com_icms_compra'] * (item_data['peso_venda'] / item_data['peso_compra']) if item_data['peso_compra'] > 0 else item_data['valor_com_icms_compra']
    
    print(f"Valor compra COM ICMS corrigido pelo peso: {valor_compra_com_icms_corrigido}")
    print(f"  Cálculo: {item_data['valor_com_icms_compra']} * ({item_data['peso_venda']} / {item_data['peso_compra']}) = {valor_compra_com_icms_corrigido}")
    print()
    
    # Calcular rentabilidade usando o método do BusinessRulesCalculator
    rentabilidade_calculada = BusinessRulesCalculator.calculate_item_profitability(
        item_data['valor_com_icms_venda'], valor_compra_com_icms_corrigido
    )
    
    print(f"Rentabilidade calculada: {rentabilidade_calculada:.4f} ({rentabilidade_calculada*100:.2f}%)")
    print(f"  Cálculo: ({item_data['valor_com_icms_venda']} / {valor_compra_com_icms_corrigido}) - 1 = {rentabilidade_calculada}")
    print()
    
    # Calcular rentabilidade esperada (unitária)
    rentabilidade_esperada = (item_data['valor_com_icms_venda'] / item_data['valor_com_icms_compra']) - 1
    
    print(f"Rentabilidade esperada (unitária): {rentabilidade_esperada:.4f} ({rentabilidade_esperada*100:.2f}%)")
    print(f"  Cálculo: ({item_data['valor_com_icms_venda']} / {item_data['valor_com_icms_compra']}) - 1 = {rentabilidade_esperada}")
    print()
    
    print("=== ANÁLISE ===")
    print("O problema é que estamos corrigindo o valor de compra pelo peso,")
    print("mas para rentabilidade unitária, devemos usar os valores unitários diretamente.")
    print("A correção de peso deve ser aplicada apenas no cálculo da comissão total,")
    print("não na rentabilidade unitária.")

if __name__ == "__main__":
    debug_profitability_calculation()