#!/usr/bin/env python3
"""
Script para testar a correção do cálculo do valor com ICMS (Venda)
"""

import sys
import os

# Adicionar o caminho do serviço de budget ao sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'services', 'budget_service'))

from app.services.budget_calculator import BudgetCalculatorService
from app.schemas.budget import BudgetItemSimplified

def test_value_calculation():
    """Teste para verificar se o valor com ICMS está sendo usado nos totais"""
    
    # Item de teste
    item = BudgetItemSimplified(
        description="Item de Teste",
        quantity=2.0,
        weight=1.0,
        purchase_value_with_icms=100.0,  # R$ 100,00 com ICMS
        purchase_icms_percentage=17.0,   # 17% ICMS compra
        purchase_other_expenses=5.0,     # R$ 5,00 outras despesas
        sale_value_with_icms=150.0,      # R$ 150,00 com ICMS
        sale_icms_percentage=17.0        # 17% ICMS venda
    )
    
    # Calcular o item
    result = BudgetCalculatorService.calculate_simplified_item(item)
    
    print("=== TESTE DE CORREÇÃO - VALOR COM ICMS (VENDA) ===")
    print(f"Quantidade: {item.quantity}")
    print(f"Valor de compra c/ICMS (unitário): R$ {item.purchase_value_with_icms:.2f}")
    print(f"Valor de venda c/ICMS (unitário): R$ {item.sale_value_with_icms:.2f}")
    print()
    
    # Valores calculados
    print("VALORES CALCULADOS:")
    print(f"Total de compra: R$ {result['total_purchase']:.2f}")
    print(f"Total de venda: R$ {result['total_sale']:.2f}")
    print(f"Comissão (1,5%): R$ {result['commission_value']:.2f}")
    print()
    
    # Verificações
    expected_total_sale = item.sale_value_with_icms * item.quantity  # 150 * 2 = 300
    expected_commission = expected_total_sale * (1.5 / 100)  # 300 * 1.5% = 4.5
    
    print("VERIFICAÇÕES:")
    print(f"Total de venda esperado (c/ICMS): R$ {expected_total_sale:.2f}")
    print(f"Total de venda calculado: R$ {result['total_sale']:.2f}")
    print(f"✅ Correto!" if abs(result['total_sale'] - expected_total_sale) < 0.01 else f"❌ Incorreto!")
    print()
    
    print(f"Comissão esperada: R$ {expected_commission:.2f}")
    print(f"Comissão calculada: R$ {result['commission_value']:.2f}")
    print(f"✅ Correto!" if abs(result['commission_value'] - expected_commission) < 0.01 else f"❌ Incorreto!")
    print()
    
    # Teste de orçamento completo
    print("=== TESTE ORÇAMENTO COMPLETO ===")
    budget_result = BudgetCalculatorService.calculate_simplified_budget([item])
    
    print(f"Total geral de venda: R$ {budget_result['totals']['total_sale_value']:.2f}")
    print(f"Total de comissão: R$ {budget_result['totals']['total_commission']:.2f}")
    print(f"Rentabilidade: {budget_result['totals']['profitability_percentage']:.1f}%")
    
    print("\n=== CONCLUSÃO ===")
    if (abs(result['total_sale'] - expected_total_sale) < 0.01 and 
        abs(result['commission_value'] - expected_commission) < 0.01):
        print("✅ CORREÇÃO APLICADA COM SUCESSO!")
        print("O valor com ICMS (venda) agora está sendo contabilizado corretamente.")
    else:
        print("❌ CORREÇÃO NÃO APLICADA!")
        print("Ainda há problemas no cálculo.")

if __name__ == "__main__":
    test_value_calculation()
