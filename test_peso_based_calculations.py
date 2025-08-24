#!/usr/bin/env python3
"""
Test peso-based calculations after removing quantity dependency
Verifies that calculations work correctly with weight-only logic
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services/budget_service'))

from app.services.business_rules_calculator import BusinessRulesCalculator

def test_peso_based_calculations():
    """Test that all calculations work with peso-only logic"""
    print("🧪 Testando cálculos baseados em peso (sem quantidade)")
    print("=" * 60)
    
    # Dados de teste - item baseado em peso
    item_data = {
        'description': 'Produto teste (peso-based)',
        'peso_compra': 2.5,  # 2.5 kg
        'peso_venda': 2.3,   # 2.3 kg (diferença de peso)
        'valor_com_icms_compra': 100.0,  # R$ 100/kg
        'percentual_icms_compra': 0.18,  # 18%
        'valor_com_icms_venda': 150.0,   # R$ 150/kg
        'percentual_icms_venda': 0.18,   # 18%
    }
    
    outras_despesas_totais = 50.0
    soma_pesos_pedido = 10.0  # Total de pesos do pedido
    
    print(f"📊 Dados de entrada:")
    print(f"   • Descrição: {item_data['description']}")
    print(f"   • Peso Compra: {item_data['peso_compra']} kg")
    print(f"   • Peso Venda: {item_data['peso_venda']} kg")
    print(f"   • Valor Compra: R$ {item_data['valor_com_icms_compra']:.2f}/kg")
    print(f"   • Valor Venda: R$ {item_data['valor_com_icms_venda']:.2f}/kg")
    print(f"   • ICMS: {item_data['percentual_icms_compra']*100:.1f}%")
    print()
    
    # Calcular item completo
    resultado = BusinessRulesCalculator.calculate_complete_item(
        item_data, outras_despesas_totais, soma_pesos_pedido
    )
    
    print("🎯 Resultados dos cálculos peso-based:")
    print(f"   • Total Compra Item: R$ {resultado['total_compra_item']:.2f}")
    print(f"     (= {item_data['peso_compra']} kg × valor_sem_impostos_compra)")
    print()
    print(f"   • Total Venda Item: R$ {resultado['total_venda_item']:.2f}")
    print(f"     (= {item_data['peso_venda']} kg × valor_sem_impostos_venda)")
    print()
    print(f"   • Rentabilidade: {resultado['rentabilidade_item']:.1f}%")
    print(f"   • Comissão: R$ {resultado['valor_comissao']:.2f}")
    print()
    
    # Verificar se não há referências a quantity
    assert 'quantity' not in resultado, "❌ Ainda há referência a 'quantity' no resultado!"
    
    # Verificar cálculos básicos
    expected_total_compra = item_data['peso_compra'] * resultado['valor_sem_impostos_compra']
    expected_total_venda = item_data['peso_venda'] * resultado['valor_sem_impostos_venda']
    
    assert abs(resultado['total_compra_item'] - expected_total_compra) < 0.01, "❌ Total compra incorreto"
    assert abs(resultado['total_venda_item'] - expected_total_venda) < 0.01, "❌ Total venda incorreto"
    
    print("✅ Todos os cálculos peso-based estão funcionando corretamente!")
    print()
    
    # Teste com múltiplos itens
    print("📋 Testando orçamento completo com múltiplos itens:")
    items_data = [
        {
            'description': 'Item 1',
            'peso_compra': 1.0, 'peso_venda': 0.9,
            'valor_com_icms_compra': 50.0, 'valor_com_icms_venda': 80.0,
            'percentual_icms_compra': 0.18, 'percentual_icms_venda': 0.18,
        },
        {
            'description': 'Item 2',
            'peso_compra': 3.5, 'peso_venda': 3.2,
            'valor_com_icms_compra': 120.0, 'valor_com_icms_venda': 180.0,
            'percentual_icms_compra': 0.18, 'percentual_icms_venda': 0.18,
        },
    ]
    
    outras_despesas_totais = 50.0
    soma_pesos_pedido = 10.0
    budget_result = BusinessRulesCalculator.calculate_complete_budget(items_data, outras_despesas_totais, soma_pesos_pedido)
    
    print(f"   • Total de itens: {budget_result['totals']['items_count']}")
    print(f"   • Soma total pesos: {budget_result['totals']['soma_pesos_pedido']} kg")
    print(f"   • Total Compra: R$ {budget_result['totals']['soma_total_compra']:.2f}")
    print(f"   • Total Venda: R$ {budget_result['totals']['soma_total_venda']:.2f}")
    print(f"   • Markup: {budget_result['totals']['markup_pedido']:.1f}%")
    print()
    
    # Verificar se todos os itens foram calculados corretamente
    for i, item in enumerate(budget_result['items']):
        assert 'quantity' not in item, f"❌ Item {i+1} ainda contém 'quantity'!"
        assert item['peso_compra'] > 0, f"❌ Item {i+1} peso_compra deve ser > 0!"
        assert item['peso_venda'] > 0, f"❌ Item {i+1} peso_venda deve ser > 0!"
    
    print("✅ Orçamento completo peso-based calculado com sucesso!")
    print()
    print("🎉 TESTE CONCLUÍDO: Sistema agora funciona 100% baseado em peso!")
    print("   • Quantidade removida de todos os cálculos")
    print("   • Fórmulas seguem a lógica da planilha: Total = peso × valor_unitário")
    print("   • Validações funcionando corretamente")

if __name__ == "__main__":
    test_peso_based_calculations()
