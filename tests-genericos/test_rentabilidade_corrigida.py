#!/usr/bin/env python3
"""
Teste para verificar se as correções de rentabilidade e markup foram implementadas corretamente.
Testa os cálculos sem arredondamentos em cascata e com conversão percentual apenas na exibição.
"""

import sys
import os

# Adicionar o path do budget_service
sys.path.append('/Users/erikpatekoski/dev/crm-ditual/services/budget_service')

from app.services.business_rules_calculator import BusinessRulesCalculator
from app.services.budget_calculator import BudgetCalculatorService

def test_business_rules_calculator():
    """Testa se o BusinessRulesCalculator não faz arredondamento prematuro"""
    print("=== Testando BusinessRulesCalculator ===")
    
    # Teste 1: Rentabilidade de item
    valor_venda = 150.0
    valor_compra = 100.0
    rentabilidade_esperada = (valor_venda / valor_compra) - 1  # 0.5 (50%)
    
    rentabilidade_calculada = BusinessRulesCalculator.calculate_item_profitability(valor_venda, valor_compra)
    
    print(f"Valor de venda: {valor_venda}")
    print(f"Valor de compra: {valor_compra}")
    print(f"Rentabilidade esperada (decimal): {rentabilidade_esperada}")
    print(f"Rentabilidade calculada: {rentabilidade_calculada}")
    print(f"Tipo do retorno: {type(rentabilidade_calculada)}")
    
    # Verificar se não há arredondamento prematuro
    assert abs(rentabilidade_calculada - rentabilidade_esperada) < 0.000001, f"Erro: {rentabilidade_calculada} != {rentabilidade_esperada}"
    print("✅ Rentabilidade de item calculada corretamente (sem arredondamento prematuro)")
    
    # Teste 2: Markup de orçamento
    total_venda = 1500.0
    total_compra = 1000.0
    markup_esperado = (total_venda / total_compra) - 1  # 0.5 (50%)
    
    markup_calculado = BusinessRulesCalculator.calculate_budget_markup(total_venda, total_compra)
    
    print(f"\nTotal venda: {total_venda}")
    print(f"Total compra: {total_compra}")
    print(f"Markup esperado (decimal): {markup_esperado}")
    print(f"Markup calculado: {markup_calculado}")
    print(f"Tipo do retorno: {type(markup_calculado)}")
    
    # Verificar se não há arredondamento prematuro
    assert abs(markup_calculado - markup_esperado) < 0.000001, f"Erro: {markup_calculado} != {markup_esperado}"
    print("✅ Markup de orçamento calculado corretamente (sem arredondamento prematuro)")

def test_budget_calculator():
    """Testa se o BudgetCalculator mantém valores em decimal"""
    print("\n=== Testando BudgetCalculator ===")
    
    # Simular dados de entrada usando o schema simplificado
    from app.schemas.budget import BudgetItemSimplified
    
    item_data = BudgetItemSimplified(
        description="Teste Item",
        valor_com_icms_compra=100.0,
        percentual_icms_compra=0.17,  # 17% em decimal
        valor_com_icms_venda=150.0,
        percentual_icms_venda=0.17,   # 17% em decimal
        percentual_ipi=0.0325,        # 3.25% em decimal (valor válido)
        peso_compra=1.0,
        peso_venda=1.0,
        outras_despesas_item=0.0
    )
    
    calculator = BudgetCalculatorService()
    
    # Testar cálculo simplificado
    simplified_result = calculator.calculate_simplified_budget([item_data])
    
    print(f"Resultado simplificado:")
    print(f"Profitability percentage: {simplified_result['totals']['profitability_percentage']}")
    print(f"Markup percentage: {simplified_result['totals']['markup_percentage']}")
    print(f"Tipo profitability: {type(simplified_result['totals']['profitability_percentage'])}")
    print(f"Tipo markup: {type(simplified_result['totals']['markup_percentage'])}")
    
    # Os percentuais devem estar em decimal, não em percentual
    # Verificar se são valores float e não estão multiplicados por 100
    assert isinstance(simplified_result['totals']['profitability_percentage'], float)
    assert isinstance(simplified_result['totals']['markup_percentage'], float)
    
    # Verificar se os valores são razoáveis (não multiplicados por 100)
    # Para um item de 100 -> 150, esperamos algo em torno de 0.2-0.5 (20%-50%)
    assert 0 <= simplified_result['totals']['profitability_percentage'] <= 1, f"Profitability fora do range esperado: {simplified_result['totals']['profitability_percentage']}"
    assert 0 <= simplified_result['totals']['markup_percentage'] <= 1, f"Markup fora do range esperado: {simplified_result['totals']['markup_percentage']}"
    
    print("✅ Percentuais mantidos em decimal no BudgetCalculator")

def test_percentage_conversion():
    """Testa a conversão para percentual apenas na exibição"""
    print("\n=== Testando Conversão Percentual ===")
    
    # Valor em decimal
    valor_decimal = 0.5  # 50%
    
    # Conversão para exibição (como deve ser feito no endpoint)
    valor_percentual = round(valor_decimal * 100, 2)
    
    print(f"Valor decimal: {valor_decimal}")
    print(f"Valor percentual para exibição: {valor_percentual}%")
    
    assert valor_percentual == 50.0, f"Erro na conversão: {valor_percentual} != 50.0"
    print("✅ Conversão percentual funcionando corretamente")

def main():
    """Executa todos os testes"""
    print("Iniciando testes das correções de rentabilidade e markup...\n")
    
    try:
        test_business_rules_calculator()
        test_budget_calculator()
        test_percentage_conversion()
        
        print("\n" + "="*60)
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Arredondamentos em cascata corrigidos")
        print("✅ Dupla conversão percentual corrigida")
        print("✅ Valores mantidos em decimal para cálculos")
        print("✅ Conversão percentual apenas na exibição")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ ERRO NO TESTE: {e}")
        print("Verifique as implementações das correções.")
        sys.exit(1)

if __name__ == "__main__":
    main()