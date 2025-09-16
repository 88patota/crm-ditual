#!/usr/bin/env python3
"""
Teste das regras de negócio implementadas no BudgetCalculatorService
Baseado nos valores de exemplo do arquivo regras.md
"""

import sys
import os

# Adicionar o caminho dos serviços ao sys.path
sys.path.append('/Users/erikpatekoski/dev/crm-ditual/services/budget_service')

from app.services.budget_calculator import BudgetCalculatorService
from app.schemas.budget import BudgetItemSimplified

def test_regras_planilha():
    """
    Teste usando os valores de exemplo das regras:
    - Valor c/ICMS (Compra) = 6.5
    - %ICMS (Compra) = 18% (0.18)
    - Valor c/ICMS (Venda) = 8.5
    - %ICMS (Venda) = 17% (0.17)
    - Taxa PIS/COFINS = 9.25% (0.0925)
    - Peso = 100 kg
    - Quantidade = 1
    """
    
    print("=== TESTE DAS REGRAS DE NEGÓCIO ===\n")
    
    # Dados de entrada baseados no exemplo das regras
    item_input = BudgetItemSimplified(
        description="Produto Teste",
        quantity=1,
        weight=100,  # 100 kg
        purchase_value_with_icms=6.5,
        purchase_icms_percentage=18.0,
        purchase_other_expenses=0.0,
        sale_value_with_icms=8.5,
        sale_icms_percentage=17.0
    )
    
    print("DADOS DE ENTRADA:")
    print(f"- Valor c/ICMS (Compra): R$ {item_input.purchase_value_with_icms}")
    print(f"- %ICMS (Compra): {item_input.purchase_icms_percentage}%")
    print(f"- Valor c/ICMS (Venda): R$ {item_input.sale_value_with_icms}")
    print(f"- %ICMS (Venda): {item_input.sale_icms_percentage}%")
    print(f"- Taxa PIS/COFINS: {BudgetCalculatorService.DEFAULT_PIS_COFINS_PERCENTAGE}%")
    print(f"- Peso: {item_input.weight} kg")
    print(f"- Quantidade: {item_input.quantity}")
    print(f"- Outras Despesas: R$ {item_input.purchase_other_expenses or 0}")
    print()
    
    # Executar cálculos
    resultado = BudgetCalculatorService.calculate_simplified_item(item_input)
    
    print("RESULTADOS CALCULADOS:")
    print(f"1. Valor s/Impostos (Compra): R$ {resultado['purchase_value_without_taxes']}")
    print(f"   Esperado: ~R$ 4.836975")
    print()
    
    print(f"2. Valor c/Difer. Peso (Compra): R$ {resultado['purchase_value_with_weight_diff']}")
    print(f"   Esperado: ~R$ 4.836975 (mesmo valor pois peso igual)")
    print()
    
    print(f"3. Valor s/Impostos (Venda): R$ {resultado['sale_value_without_taxes']}")
    print(f"   Esperado: ~R$ 6.325275")
    print()
    
    print(f"4. Diferença de Peso: {resultado['weight_difference']}")
    print(f"   Esperado: 0 (pesos iguais)")
    print()
    
    print(f"5. Rentabilidade: {resultado['profitability']}%")
    print(f"   Esperado: ~30.77% (0.3076923077)")
    print()
    
    print(f"6. Total Compra: R$ {resultado['total_purchase']}")
    print(f"   Esperado: ~R$ 483.6975 (para 100kg)")
    print()
    
    print(f"7. Total Venda: R$ {resultado['total_sale']}")
    print(f"   Esperado: ~R$ 632.5275 (para 100kg)")
    print()
    
    print(f"8. Valor Total: R$ {resultado['total_value']}")
    print(f"   Esperado: ~R$ 850 (8.5 * 100kg)")
    print()
    
    print(f"9. Valor Comissão: R$ {resultado['commission_value']}")
    print(f"   Esperado: ~R$ 12.75 (1.5% de 850)")
    print()
    
    print(f"10. Custo Dunamis: R$ {resultado['dunamis_cost']}")
    print(f"    Esperado: valor calculado com fórmula da regra 10")
    print()
    
    # Testar cálculo específico do Dunamis
    dunamis_unitario = BudgetCalculatorService.calculate_dunamis_cost(
        purchase_value_with_icms=6.5,
        sale_icms_percentage=17.0
    )
    print(f"Dunamis Unitário: R$ {dunamis_unitario}")
    print(f"Fórmula: 6.5 / (1 - 0.17) / (1 - 0.0925)")
    print(f"= 6.5 / 0.83 / 0.9075")
    print(f"≈ {6.5 / 0.83 / 0.9075:.6f}")
    print()

def test_markup_automatico():
    """Teste do cálculo automático de markup"""
    print("=== TESTE MARKUP AUTOMÁTICO ===\n")
    
    markup = BudgetCalculatorService.calculate_automatic_markup_from_planilha(
        purchase_value_with_icms=6.5,
        purchase_icms_percentage=18.0,
        sale_value_with_icms=8.5,
        sale_icms_percentage=17.0,
        other_expenses=0.0
    )
    
    print(f"Markup calculado: {markup}%")
    print(f"Esperado: ~30.77%")
    print()

def test_preco_venda_sugerido():
    """Teste do cálculo de preço de venda para markup desejado"""
    print("=== TESTE PREÇO DE VENDA SUGERIDO ===\n")
    
    preco_sugerido = BudgetCalculatorService.calculate_sale_price_from_markup(
        purchase_value_with_icms=6.5,
        purchase_icms_percentage=18.0,
        sale_icms_percentage=17.0,
        desired_markup_percentage=30.0,
        other_expenses=0.0
    )
    
    print(f"Preço de venda sugerido para markup de 30%: R$ {preco_sugerido}")
    print()

if __name__ == "__main__":
    try:
        test_regras_planilha()
        test_markup_automatico()
        test_preco_venda_sugerido()
        print("✅ Testes executados com sucesso!")
    except Exception as e:
        print(f"❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()
