#!/usr/bin/env python3
"""
Teste de Validação para a Nova Funcionalidade de IPI
Garante que os cálculos de IPI estão corretos conforme especificação da PM
"""

import sys
import os

# Adicionar o caminho dos serviços ao sys.path
sys.path.append('/Users/erikpatekoski/dev/crm-ditual/services/budget_service')

from app.services.business_rules_calculator import BusinessRulesCalculator
from app.services.budget_calculator import BudgetCalculatorService
from app.schemas.budget import BudgetItemSimplified

def test_ipi_calculation_basic():
    """
    Teste básico de cálculo do IPI
    """
    print("=== TESTE BÁSICO DE CÁLCULO DO IPI ===\n")
    
    # Teste com valor de R$ 1000,00 e IPI de 3,25%
    valor_com_icms = 1000.0
    percentual_ipi = 0.0325  # 3.25% em decimal
    
    # Calcular IPI
    valor_ipi = BusinessRulesCalculator.calculate_ipi_value(valor_com_icms, percentual_ipi)
    valor_final = BusinessRulesCalculator.calculate_total_value_with_ipi(valor_com_icms, percentual_ipi)
    
    # Valores esperados
    valor_ipi_esperado = 32.50  # 1000 * 0.0325
    valor_final_esperado = 1032.50  # 1000 + 32.50
    
    print(f"Valor COM ICMS: R$ {valor_com_icms:.2f}")
    print(f"Percentual IPI: {percentual_ipi * 100:.2f}%")
    print(f"Valor IPI Calculado: R$ {valor_ipi:.2f}")
    print(f"Valor IPI Esperado: R$ {valor_ipi_esperado:.2f}")
    print(f"Valor Final Calculado: R$ {valor_final:.2f}")
    print(f"Valor Final Esperado: R$ {valor_final_esperado:.2f}")
    
    # Validar resultados
    assert abs(valor_ipi - valor_ipi_esperado) < 0.01, f"IPI incorreto: {valor_ipi} != {valor_ipi_esperado}"
    assert abs(valor_final - valor_final_esperado) < 0.01, f"Valor final incorreto: {valor_final} != {valor_final_esperado}"
    
    print("✅ Teste básico de IPI: PASSOU\n")
    return True

def test_ipi_percentages_validation():
    """
    Teste de validação dos percentuais permitidos de IPI
    """
    print("=== TESTE DE VALIDAÇÃO DOS PERCENTUAIS DE IPI ===\n")
    
    # Percentuais válidos: 0%, 3.25%, 5%
    percentuais_validos = [0.0, 0.0325, 0.05]
    valor_base = 100.0
    
    for percentual in percentuais_validos:
        try:
            valor_ipi = BusinessRulesCalculator.calculate_ipi_value(valor_base, percentual)
            print(f"✅ Percentual {percentual * 100:.2f}% - Válido: R$ {valor_ipi:.2f}")
        except ValueError as e:
            print(f"❌ Erro inesperado para percentual válido {percentual}: {e}")
            return False
    
    # Percentuais inválidos
    percentuais_invalidos = [0.01, 0.02, 0.04, 0.06, 0.10]
    
    for percentual in percentuais_invalidos:
        try:
            valor_ipi = BusinessRulesCalculator.calculate_ipi_value(valor_base, percentual)
            print(f"❌ Percentual {percentual * 100:.2f}% deveria ser inválido mas foi aceito")
            return False
        except ValueError:
            print(f"✅ Percentual {percentual * 100:.2f}% - Corretamente rejeitado")
    
    print("✅ Teste de validação de percentuais: PASSOU\n")
    return True

def test_ipi_item_calculation():
    """
    Teste de cálculo de IPI para um item completo
    """
    print("=== TESTE DE CÁLCULO DE IPI PARA ITEM COMPLETO ===\n")
    
    # Criar item de teste
    peso_venda = 10.0  # 10 kg
    valor_com_icms_venda = 50.0  # R$ 50 por kg
    percentual_ipi = 0.05  # 5%
    
    # Calcular IPI total do item
    valor_ipi_total = BusinessRulesCalculator.calculate_total_ipi_item(
        peso_venda, valor_com_icms_venda, percentual_ipi
    )
    
    # Valor esperado: 10 kg * R$ 50/kg * 5% = R$ 500 * 5% = R$ 25
    valor_esperado = 25.0
    
    print(f"Peso de venda: {peso_venda} kg")
    print(f"Valor com ICMS por kg: R$ {valor_com_icms_venda:.2f}")
    print(f"Percentual IPI: {percentual_ipi * 100:.2f}%")
    print(f"Valor total com ICMS: R$ {peso_venda * valor_com_icms_venda:.2f}")
    print(f"IPI Total Calculado: R$ {valor_ipi_total:.2f}")
    print(f"IPI Total Esperado: R$ {valor_esperado:.2f}")
    
    assert abs(valor_ipi_total - valor_esperado) < 0.01, f"IPI total incorreto: {valor_ipi_total} != {valor_esperado}"
    
    print("✅ Teste de cálculo de IPI para item: PASSOU\n")
    return True

def test_ipi_integration_with_budget_calculator():
    """
    Teste de integração com o BudgetCalculatorService
    """
    print("=== TESTE DE INTEGRAÇÃO COM BUDGET CALCULATOR ===\n")
    
    # Criar item simplificado com IPI
    item_input = BudgetItemSimplified(
        description="Produto Teste com IPI",
        peso_compra=5.0,
        peso_venda=5.0,
        valor_com_icms_compra=40.0,
        percentual_icms_compra=0.18,  # 18%
        outras_despesas_item=0.0,
        valor_com_icms_venda=60.0,
        percentual_icms_venda=0.18,  # 18%
        percentual_ipi=0.0325  # 3.25%
    )
    
    # Calcular item com IPI
    resultado = BudgetCalculatorService.calculate_simplified_item(item_input)
    
    print("RESULTADOS DO CÁLCULO:")
    print(f"Descrição: {resultado['description']}")
    print(f"Valor com ICMS (Venda): R$ {resultado.get('sale_value_with_icms', 0):.2f}")
    print(f"Peso de venda: {resultado.get('sale_weight', 0)} kg")
    print(f"Percentual IPI: {resultado.get('ipi_percentage', 0) * 100:.2f}%")
    
    # Verificar se os campos de IPI estão presentes
    assert 'ipi_percentage' in resultado, "Campo percentual_ipi não encontrado no resultado"
    assert 'ipi_value_per_unit' in resultado, "Campo ipi_value_per_unit não encontrado no resultado"
    assert 'total_ipi_value' in resultado, "Campo total_ipi_value não encontrado no resultado"
    assert 'final_value_with_ipi' in resultado, "Campo final_value_with_ipi não encontrado no resultado"
    assert 'total_final_with_ipi' in resultado, "Campo total_final_with_ipi não encontrado no resultado"
    
    # Validar cálculos de IPI
    ipi_per_unit_esperado = 60.0 * 0.0325  # R$ 1.95
    total_ipi_esperado = ipi_per_unit_esperado * 5.0  # R$ 9.75
    final_value_esperado = 60.0 + ipi_per_unit_esperado  # R$ 61.95
    total_final_esperado = final_value_esperado * 5.0  # R$ 309.75
    
    print(f"IPI por unidade: R$ {resultado['ipi_value_per_unit']:.2f} (esperado: R$ {ipi_per_unit_esperado:.2f})")
    print(f"IPI total: R$ {resultado['total_ipi_value']:.2f} (esperado: R$ {total_ipi_esperado:.2f})")
    print(f"Valor final por unidade: R$ {resultado['final_value_with_ipi']:.2f} (esperado: R$ {final_value_esperado:.2f})")
    print(f"Valor final total: R$ {resultado['total_final_with_ipi']:.2f} (esperado: R$ {total_final_esperado:.2f})")
    
    # Validações
    assert abs(resultado['ipi_value_per_unit'] - ipi_per_unit_esperado) < 0.01
    assert abs(resultado['total_ipi_value'] - total_ipi_esperado) < 0.01
    assert abs(resultado['final_value_with_ipi'] - final_value_esperado) < 0.01
    assert abs(resultado['total_final_with_ipi'] - total_final_esperado) < 0.01
    
    print("✅ Teste de integração com BudgetCalculator: PASSOU\n")
    return True

def test_ipi_budget_totals():
    """
    Teste de totais de IPI no orçamento completo
    """
    print("=== TESTE DE TOTAIS DE IPI NO ORÇAMENTO ===\n")
    
    # Criar múltiplos itens com diferentes percentuais de IPI
    items_input = [
        BudgetItemSimplified(
            description="Item 1 - Isento",
            peso_compra=2.0,
            peso_venda=2.0,
            valor_com_icms_compra=100.0,
            percentual_icms_compra=0.18,
            outras_despesas_item=0.0,
            valor_com_icms_venda=150.0,
            percentual_icms_venda=0.18,
            percentual_ipi=0.0  # Isento
        ),
        BudgetItemSimplified(
            description="Item 2 - 3.25%",
            peso_compra=3.0,
            peso_venda=3.0,
            valor_com_icms_compra=200.0,
            percentual_icms_compra=0.18,
            outras_despesas_item=0.0,
            valor_com_icms_venda=300.0,
            percentual_icms_venda=0.18,
            percentual_ipi=0.0325  # 3.25%
        ),
        BudgetItemSimplified(
            description="Item 3 - 5%",
            peso_compra=1.0,
            peso_venda=1.0,
            valor_com_icms_compra=50.0,
            percentual_icms_compra=0.18,
            outras_despesas_item=0.0,
            valor_com_icms_venda=80.0,
            percentual_icms_venda=0.18,
            percentual_ipi=0.05  # 5%
        )
    ]
    
    # Calcular orçamento completo
    resultado = BudgetCalculatorService.calculate_simplified_budget(items_input)
    
    # Cálculos esperados:
    # Item 1: 2kg * R$ 150 * 0% = R$ 0 de IPI
    # Item 2: 3kg * R$ 300 * 3.25% = R$ 900 * 3.25% = R$ 29.25 de IPI
    # Item 3: 1kg * R$ 80 * 5% = R$ 80 * 5% = R$ 4.00 de IPI
    # Total IPI esperado: R$ 0 + R$ 29.25 + R$ 4.00 = R$ 33.25
    
    total_ipi_esperado = 0.0 + 29.25 + 4.00
    
    print("ITENS CALCULADOS:")
    for i, item in enumerate(resultado['items']):
        print(f"Item {i+1}: {item['description']}")
        print(f"  IPI Total: R$ {item.get('total_ipi_value', 0):.2f}")
        print(f"  Valor Final com IPI: R$ {item.get('total_final_with_ipi', 0):.2f}")
    
    print(f"\nTOTAIS DO ORÇAMENTO:")
    print(f"Total IPI Calculado: R$ {resultado['totals'].get('total_ipi_value', 0):.2f}")
    print(f"Total IPI Esperado: R$ {total_ipi_esperado:.2f}")
    print(f"Valor Final Total: R$ {resultado['totals'].get('total_final_value', 0):.2f}")
    
    # Validar se o total de IPI está correto
    total_ipi_calculado = resultado['totals'].get('total_ipi_value', 0)
    assert abs(total_ipi_calculado - total_ipi_esperado) < 0.01, f"Total IPI incorreto: {total_ipi_calculado} != {total_ipi_esperado}"
    
    print("✅ Teste de totais de IPI no orçamento: PASSOU\n")
    return True

def test_ipi_non_impact_on_commission():
    """
    Teste para garantir que IPI não afeta cálculos de comissão
    """
    print("=== TESTE: IPI NÃO AFETA COMISSÃO ===\n")
    
    # Criar dois itens idênticos, um com IPI e outro sem
    item_sem_ipi = BudgetItemSimplified(
        description="Produto SEM IPI",
        peso_compra=1.0,
        peso_venda=1.0,
        valor_com_icms_compra=100.0,
        percentual_icms_compra=0.18,
        outras_despesas_item=0.0,
        valor_com_icms_venda=150.0,
        percentual_icms_venda=0.18,
        percentual_ipi=0.0  # Sem IPI
    )
    
    item_com_ipi = BudgetItemSimplified(
        description="Produto COM IPI",
        peso_compra=1.0,
        peso_venda=1.0,
        valor_com_icms_compra=100.0,
        percentual_icms_compra=0.18,
        outras_despesas_item=0.0,
        valor_com_icms_venda=150.0,
        percentual_icms_venda=0.18,
        percentual_ipi=0.05  # 5% de IPI
    )
    
    # Calcular ambos os itens
    resultado_sem_ipi = BudgetCalculatorService.calculate_simplified_item(item_sem_ipi)
    resultado_com_ipi = BudgetCalculatorService.calculate_simplified_item(item_com_ipi)
    
    print("COMPARAÇÃO DE COMISSÕES:")
    print(f"Item SEM IPI - Comissão: R$ {resultado_sem_ipi.get('commission_value', 0):.2f}")
    print(f"Item COM IPI - Comissão: R$ {resultado_com_ipi.get('commission_value', 0):.2f}")
    print(f"Item SEM IPI - Rentabilidade: {resultado_sem_ipi.get('profitability', 0):.2f}%")
    print(f"Item COM IPI - Rentabilidade: {resultado_com_ipi.get('profitability', 0):.2f}%")
    
    # A comissão deve ser IGUAL (IPI não afeta comissão conforme especificação)
    comissao_sem_ipi = resultado_sem_ipi.get('commission_value', 0)
    comissao_com_ipi = resultado_com_ipi.get('commission_value', 0)
    rentabilidade_sem_ipi = resultado_sem_ipi.get('profitability', 0)
    rentabilidade_com_ipi = resultado_com_ipi.get('profitability', 0)
    
    assert abs(comissao_sem_ipi - comissao_com_ipi) < 0.01, f"Comissões diferentes: {comissao_sem_ipi} != {comissao_com_ipi}"
    assert abs(rentabilidade_sem_ipi - rentabilidade_com_ipi) < 0.01, f"Rentabilidades diferentes: {rentabilidade_sem_ipi} != {rentabilidade_com_ipi}"
    
    print("✅ Teste: IPI não afeta comissão: PASSOU\n")
    return True

def main():
    """
    Executar todos os testes de validação do IPI
    """
    print("🚀 INICIANDO TESTES DE VALIDAÇÃO DO IPI\n")
    
    testes = [
        test_ipi_calculation_basic,
        test_ipi_percentages_validation,
        test_ipi_item_calculation,
        test_ipi_integration_with_budget_calculator,
        test_ipi_budget_totals,
        test_ipi_non_impact_on_commission
    ]
    
    sucessos = 0
    falhas = 0
    
    for teste in testes:
        try:
            if teste():
                sucessos += 1
        except Exception as e:
            print(f"❌ {teste.__name__} FALHOU: {e}\n")
            falhas += 1
    
    print("=" * 50)
    print("📊 RESULTADO DOS TESTES DE IPI")
    print("=" * 50)
    print(f"✅ Testes bem-sucedidos: {sucessos}")
    print(f"❌ Testes falharam: {falhas}")
    print(f"📈 Taxa de sucesso: {(sucessos / len(testes)) * 100:.1f}%")
    
    if falhas == 0:
        print("\n🎉 TODOS OS TESTES DE IPI PASSARAM!")
        print("✅ A funcionalidade de IPI está implementada corretamente!")
    else:
        print(f"\n⚠️  {falhas} teste(s) falharam. Revisar implementação.")
    
    return falhas == 0

if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)