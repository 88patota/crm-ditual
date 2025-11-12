#!/usr/bin/env python3
"""
Script para testar a correção do cálculo de frete
"""

import sys
import os
sys.path.append('/Users/erikpatekoski/dev/crm-ditual/services/budget_service')

from app.services.business_rules_calculator import BusinessRulesCalculator

def test_freight_calculation():
    """Testa o cálculo de frete com os dados fornecidos pelo usuário"""
    
    # Dados do item sem frete
    item_data = {
        'description': 'item',
        'delivery_time': '0',
        'peso_compra': 1000.0,
        'peso_venda': 1010.0,
        'valor_com_icms_compra': 2.11,
        'percentual_icms_compra': 0.18,
        'outras_despesas_item': 0.0,
        'valor_com_icms_venda': 4.32,
        'percentual_icms_venda': 0.18,
        'percentual_ipi': 0.0
    }
    
    items_data = [item_data]
    outras_despesas_totais = 0.0
    
    print("=== TESTE SEM FRETE ===")
    # Teste sem frete
    soma_pesos_pedido_sem_frete = 1000.0  # peso_compra
    result_sem_frete = BusinessRulesCalculator.calculate_complete_budget(
        items_data, outras_despesas_totais, soma_pesos_pedido_sem_frete
    )
    
    print(f"Total Purchase Value (sem frete): R$ {result_sem_frete['totals']['soma_total_compra']:.2f}")
    print(f"Total Sale Value (sem frete): R$ {result_sem_frete['totals']['soma_total_venda']:.2f}")
    
    # Calcular rentabilidade manualmente
    rentabilidade_sem_frete = ((result_sem_frete['totals']['soma_total_venda'] / result_sem_frete['totals']['soma_total_compra']) - 1) * 100 if result_sem_frete['totals']['soma_total_compra'] > 0 else 0
    print(f"Profitability (sem frete): {rentabilidade_sem_frete:.2f}%")
    
    print("\n=== TESTE COM FRETE ===")
    # Teste com frete
    freight_value_total = 500.0
    soma_pesos_pedido_com_frete = 1000.0  # peso_compra
    result_com_frete = BusinessRulesCalculator.calculate_complete_budget(
        items_data, outras_despesas_totais, soma_pesos_pedido_com_frete, freight_value_total
    )
    
    print(f"Total Purchase Value (com frete): R$ {result_com_frete['totals']['soma_total_compra']:.2f}")
    print(f"Total Sale Value (com frete): R$ {result_com_frete['totals']['soma_total_venda']:.2f}")
    
    # Calcular rentabilidade manualmente
    rentabilidade_com_frete = ((result_com_frete['totals']['soma_total_venda'] / result_com_frete['totals']['soma_total_compra']) - 1) * 100 if result_com_frete['totals']['soma_total_compra'] > 0 else 0
    print(f"Profitability (com frete): {rentabilidade_com_frete:.2f}%")
    
    print("\n=== ANÁLISE DA DIFERENÇA ===")
    diferenca_compra = result_com_frete['totals']['soma_total_compra'] - result_sem_frete['totals']['soma_total_compra']
    print(f"Diferença no valor de compra: R$ {diferenca_compra:.2f}")
    print(f"Valor do frete esperado: R$ {freight_value_total:.2f}")
    
    if abs(diferenca_compra - freight_value_total) < 0.01:
        print("✅ CORREÇÃO FUNCIONOU! O frete está sendo incluído corretamente.")
    else:
        print(f"❌ PROBLEMA AINDA EXISTE! Diferença esperada: R$ {freight_value_total:.2f}, Diferença real: R$ {diferenca_compra:.2f}")
    
    return result_sem_frete, result_com_frete

if __name__ == "__main__":
    try:
        test_freight_calculation()
    except Exception as e:
        print(f"Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()