#!/usr/bin/env python3
"""
Test to validate that Total Sale calculation is now correctly using sale value WITH ICMS
instead of WITHOUT taxes.

This test verifies the fix for the issue where total_sale was incorrectly calculated
using sale_value_without_taxes instead of sale_value_with_icms.
"""

import sys
sys.path.append('services/budget_service')

from app.services.business_rules_calculator import BusinessRulesCalculator
from app.services.budget_calculator import BudgetCalculatorService
from app.schemas.budget import BudgetItemSimplified

def test_total_sale_calculation_with_icms():
    """
    Test that validates Total Sale is calculated using sale value WITH ICMS
    """
    print("=== TESTE DE VALIDAÇÃO: TOTAL VENDA COM ICMS ===")
    print()
    
    # Test data
    peso_venda = 100.0  # kg
    valor_com_icms_venda = 15.00  # R$ per kg WITH ICMS
    percentual_icms_venda = 0.18  # 18%
    
    # Expected calculation: Total Sale = peso_venda * valor_com_icms_venda
    expected_total_sale = peso_venda * valor_com_icms_venda  # 100 * 15.00 = 1500.00
    
    print(f"Dados de entrada:")
    print(f"  Peso venda: {peso_venda} kg")
    print(f"  Valor c/ ICMS venda: R$ {valor_com_icms_venda}/kg")
    print(f"  ICMS venda: {percentual_icms_venda * 100}%")
    print()
    
    # Calculate using the new method
    calculated_total_sale = BusinessRulesCalculator.calculate_total_sale_item_with_icms(
        peso_venda, valor_com_icms_venda
    )
    
    print(f"Resultado esperado: R$ {expected_total_sale:.2f}")
    print(f"Resultado calculado: R$ {calculated_total_sale:.2f}")
    print()
    
    # Validation
    if abs(calculated_total_sale - expected_total_sale) < 0.01:
        print("✅ TESTE PASSOU: Total de venda calculado corretamente COM ICMS")
    else:
        print("❌ TESTE FALHOU: Total de venda não está usando valor COM ICMS")
        return False
    
    # Also test that it's different from the WITHOUT taxes calculation
    valor_sem_icms_venda = valor_com_icms_venda * (1 - percentual_icms_venda) * (1 - 0.0925)
    total_sale_without_taxes = peso_venda * valor_sem_icms_venda
    
    print(f"Comparação:")
    print(f"  Valor sem impostos: R$ {valor_sem_icms_venda:.6f}/kg")
    print(f"  Total SEM impostos: R$ {total_sale_without_taxes:.2f}")
    print(f"  Total COM ICMS: R$ {calculated_total_sale:.2f}")
    print(f"  Diferença: R$ {calculated_total_sale - total_sale_without_taxes:.2f}")
    print()
    
    if calculated_total_sale > total_sale_without_taxes:
        print("✅ VALIDAÇÃO: Total COM ICMS é maior que SEM impostos (correto)")
    else:
        print("❌ ERRO: Total COM ICMS deveria ser maior que SEM impostos")
        return False
    
    return True

def test_budget_calculator_consistency():
    """
    Test that the budget calculator also uses the correct total sale calculation
    """
    print("=== TESTE DE CONSISTÊNCIA: BUDGET CALCULATOR ===")
    print()
    
    # Create test item
    item = BudgetItemSimplified(
        description="Item Teste",
        peso_compra=50.0,
        peso_venda=50.0,
        valor_com_icms_compra=10.00,
        percentual_icms_compra=0.17,
        valor_com_icms_venda=15.00,
        percentual_icms_venda=0.18,
        outras_despesas_item=0.0
    )
    
    # Calculate using simplified method
    result = BudgetCalculatorService.calculate_simplified_item(item)
    
    # Expected total sale WITH ICMS
    expected_total_sale = item.peso_venda * item.valor_com_icms_venda  # 50 * 15 = 750
    
    print(f"Dados do item:")
    print(f"  Peso venda: {item.peso_venda} kg")
    print(f"  Valor venda c/ ICMS: R$ {item.valor_com_icms_venda}/kg")
    print()
    
    print(f"Resultado esperado: R$ {expected_total_sale:.2f}")
    print(f"Total sale calculado: R$ {result['total_sale']:.2f}")
    print(f"Total value (c/ ICMS): R$ {result['total_value']:.2f}")
    print()
    
    # The total_sale should now equal total_value (both with ICMS)
    if abs(result['total_sale'] - expected_total_sale) < 0.01:
        print("✅ TESTE PASSOU: Budget Calculator usa valor COM ICMS")
    else:
        print("❌ TESTE FALHOU: Budget Calculator não está usando valor COM ICMS")
        return False
    
    if abs(result['total_sale'] - result['total_value']) < 0.01:
        print("✅ CONSISTÊNCIA: total_sale = total_value (ambos COM ICMS)")
    else:
        print("❌ INCONSISTÊNCIA: total_sale ≠ total_value")
        return False
    
    return True

def test_complete_item_calculation():
    """
    Test the complete item calculation using business rules calculator
    """
    print("=== TESTE: CÁLCULO COMPLETO DE ITEM ===")
    print()
    
    item_data = {
        'description': 'Teste Item Completo',
        'peso_compra': 75.0,
        'peso_venda': 75.0,
        'valor_com_icms_compra': 12.00,
        'percentual_icms_compra': 0.17,
        'valor_com_icms_venda': 18.00,
        'percentual_icms_venda': 0.18
    }
    
    result = BusinessRulesCalculator.calculate_complete_item(
        item_data, outras_despesas_totais=0.0, soma_pesos_pedido=75.0
    )
    
    # Expected total sale WITH ICMS
    expected_total_sale = item_data['peso_venda'] * item_data['valor_com_icms_venda']  # 75 * 18 = 1350
    
    print(f"Item: {item_data['description']}")
    print(f"Peso venda: {item_data['peso_venda']} kg")
    print(f"Valor venda c/ ICMS: R$ {item_data['valor_com_icms_venda']}/kg")
    print()
    
    print(f"Resultado esperado: R$ {expected_total_sale:.2f}")
    print(f"Total venda calculado: R$ {result['total_venda_item']:.2f}")
    print()
    
    if abs(result['total_venda_item'] - expected_total_sale) < 0.01:
        print("✅ TESTE PASSOU: Cálculo completo usa valor COM ICMS")
        return True
    else:
        print("❌ TESTE FALHOU: Cálculo completo não está usando valor COM ICMS")
        return False

if __name__ == "__main__":
    print("VALIDAÇÃO DA CORREÇÃO: TOTAL VENDA COM ICMS")
    print("=" * 50)
    print()
    
    tests_passed = 0
    total_tests = 3
    
    # Run tests
    if test_total_sale_calculation_with_icms():
        tests_passed += 1
    print()
    
    if test_budget_calculator_consistency():
        tests_passed += 1
    print()
    
    if test_complete_item_calculation():
        tests_passed += 1
    print()
    
    # Summary
    print("=" * 50)
    print(f"RESUMO DOS TESTES: {tests_passed}/{total_tests} passaram")
    
    if tests_passed == total_tests:
        print("🎉 TODOS OS TESTES PASSARAM - CORREÇÃO VALIDADA!")
        print()
        print("✅ Total de venda agora usa valor COM ICMS corretamente")
        print("✅ Cálculos de comissão serão baseados no valor real pago pelo cliente")
        print("✅ Relatórios mostrarão valores de faturamento corretos")
    else:
        print("⚠️  ALGUNS TESTES FALHARAM - VERIFICAR IMPLEMENTAÇÃO")
        sys.exit(1)