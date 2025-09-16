#!/usr/bin/env python3
"""
Debug detalhado para identificar onde o IPI está sendo perdido
"""
import sys
import os

# Add the budget service to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'budget_service'))

from app.services.business_rules_calculator import BusinessRulesCalculator

def debug_ipi_step_by_step():
    """Debug passo a passo do cálculo de IPI"""
    print("=== DEBUG DETALHADO - CÁLCULO IPI ===")

    # Dados de teste
    test_item = {
        'description': 'Item Teste IPI',
        'peso_compra': 100.0,
        'peso_venda': 100.0,
        'valor_com_icms_compra': 10.00,
        'percentual_icms_compra': 0.18,
        'outras_despesas_item': 0.0,
        'valor_com_icms_venda': 15.00,
        'percentual_icms_venda': 0.17,
        'percentual_ipi': 0.0325  # 3.25%
    }

    print(f"Dados de entrada: {test_item}")
    print()

    # Teste 1: Validação
    print("=== PASSO 1: VALIDAÇÃO ===")
    errors = BusinessRulesCalculator.validate_item_data(test_item)
    if errors:
        print(f"❌ Erros de validação: {errors}")
        return False
    else:
        print("✅ Validação passou")
    print()

    # Teste 2: Cálculo individual do item
    print("=== PASSO 2: CÁLCULO DO ITEM ===")
    try:
        calculated_item = BusinessRulesCalculator.calculate_complete_item(
            test_item, 0.0, 100.0  # outras_despesas_totais, soma_pesos_pedido
        )
        
        print("✅ Cálculo do item executado com sucesso")
        print(f"Campos calculados disponíveis: {list(calculated_item.keys())}")
        print()
        
        # Verificar campos de IPI especificamente
        print("=== CAMPOS IPI NO ITEM CALCULADO ===")
        ipi_fields = {k: v for k, v in calculated_item.items() if 'ipi' in k.lower()}
        for field, value in ipi_fields.items():
            print(f"{field}: {value} (tipo: {type(value).__name__})")
        
        if not ipi_fields:
            print("❌ PROBLEMA: Nenhum campo IPI encontrado no item calculado!")
        print()
        
    except Exception as e:
        print(f"❌ Erro no cálculo do item: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Teste 3: Cálculo do orçamento completo
    print("=== PASSO 3: CÁLCULO ORÇAMENTO COMPLETO ===")
    try:
        budget_result = BusinessRulesCalculator.calculate_complete_budget(
            [test_item], 0.0, 100.0
        )
        
        print("✅ Cálculo do orçamento executado com sucesso")
        print(f"Totals disponíveis: {list(budget_result['totals'].keys())}")
        print(f"Items count: {len(budget_result['items'])}")
        print()
        
        # Verificar totals de IPI
        print("=== TOTALS IPI ===")
        ipi_totals = {k: v for k, v in budget_result['totals'].items() if 'ipi' in k.lower()}
        for field, value in ipi_totals.items():
            print(f"totals['{field}']: {value} (tipo: {type(value).__name__})")
        
        if not ipi_totals:
            print("❌ PROBLEMA: Nenhum total IPI encontrado!")
        print()
        
        # Verificar item no resultado do orçamento
        if budget_result['items']:
            item_result = budget_result['items'][0]
            print("=== CAMPOS IPI NO ITEM DO ORÇAMENTO ===")
            item_ipi_fields = {k: v for k, v in item_result.items() if 'ipi' in k.lower()}
            for field, value in item_ipi_fields.items():
                print(f"items[0]['{field}']: {value} (tipo: {type(value).__name__})")
            
            if not item_ipi_fields:
                print("❌ PROBLEMA: Nenhum campo IPI encontrado no item do orçamento!")
            print()
        
    except Exception as e:
        print(f"❌ Erro no cálculo do orçamento: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Teste 4: Cálculo manual de IPI para comparação
    print("=== PASSO 4: CÁLCULO MANUAL IPI ===")
    try:
        manual_ipi_value = BusinessRulesCalculator.calculate_ipi_value(
            test_item['valor_com_icms_venda'], test_item['percentual_ipi']
        )
        manual_total_ipi = BusinessRulesCalculator.calculate_total_ipi_item(
            test_item['peso_venda'], test_item['valor_com_icms_venda'], test_item['percentual_ipi']
        )
        manual_total_with_ipi = BusinessRulesCalculator.calculate_total_value_with_ipi(
            test_item['valor_com_icms_venda'], test_item['percentual_ipi']
        )
        
        print(f"Manual IPI unitário: R$ {manual_ipi_value:.2f}")
        print(f"Manual IPI total: R$ {manual_total_ipi:.2f}")
        print(f"Manual total com IPI: R$ {manual_total_with_ipi:.2f}")
        print()
        
        # Valores esperados
        expected_ipi_unitario = 15.00 * 0.0325  # R$ 0.4875
        expected_ipi_total = 100.0 * 15.00 * 0.0325  # R$ 48.75
        expected_total_with_ipi = 15.00 + expected_ipi_unitario  # R$ 15.4875
        
        print(f"Esperado IPI unitário: R$ {expected_ipi_unitario:.4f}")
        print(f"Esperado IPI total: R$ {expected_ipi_total:.2f}")
        print(f"Esperado total com IPI: R$ {expected_total_with_ipi:.4f}")
        print()
        
        # Comparação
        if abs(manual_ipi_value - expected_ipi_unitario) < 0.01:
            print("✅ Cálculo manual IPI unitário correto")
        else:
            print("❌ Cálculo manual IPI unitário incorreto")
            
        if abs(manual_total_ipi - expected_ipi_total) < 0.01:
            print("✅ Cálculo manual IPI total correto")
        else:
            print("❌ Cálculo manual IPI total incorreto")
            
        if abs(manual_total_with_ipi - expected_total_with_ipi) < 0.01:
            print("✅ Cálculo manual total com IPI correto")
        else:
            print("❌ Cálculo manual total com IPI incorreto")
        
    except Exception as e:
        print(f"❌ Erro no cálculo manual: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":
    print("Debug detalhado do cálculo de IPI")
    print("Este teste verifica cada etapa do processo de cálculo")
    print()

    success = debug_ipi_step_by_step()
    if success:
        print("\n✅ Debug concluído - verifique os resultados acima")
    else:
        print("\n❌ Debug falhou - há problemas no cálculo de IPI")
