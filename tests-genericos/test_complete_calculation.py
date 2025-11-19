#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'budget_service'))

from app.services.business_rules_calculator import BusinessRulesCalculator

def test_complete_calculation():
    print("=== TESTE COMPLETO COM BUSINESSRULESCALCULATOR ===")
    
    # Dados exatos da requisição do usuário
    item_data = {
        "description": "item",
        "delivery_time": "0",
        "peso_compra": 1000,
        "peso_venda": 1010,
        "valor_com_icms_compra": 2.11,
        "percentual_icms_compra": 0.18,
        "outras_despesas_item": 0,
        "valor_com_icms_venda": 4.32,
        "percentual_icms_venda": 0.18,
        "percentual_ipi": 0
    }
    
    outras_despesas_totais = 0.0
    soma_pesos_pedido = 1000  # Apenas um item
    freight_value_total = 500
    
    print(f"Dados de entrada:")
    print(f"- Frete total: R$ {freight_value_total}")
    print(f"- Peso compra: {item_data['peso_compra']} kg")
    print(f"- Peso venda: {item_data['peso_venda']} kg")
    print(f"- Valor com ICMS compra: R$ {item_data['valor_com_icms_compra']}")
    print(f"- Valor com ICMS venda: R$ {item_data['valor_com_icms_venda']}")
    print()
    
    # Calcular usando o método completo
    result = BusinessRulesCalculator.calculate_complete_item(
        item_data, outras_despesas_totais, soma_pesos_pedido, freight_value_total
    )
    
    print("=== RESULTADOS DO CÁLCULO COMPLETO ===")
    print(f"Total compra: R$ {result['total_purchase']:.2f}")
    print(f"Total venda: R$ {result['total_sale']:.2f}")
    print(f"Rentabilidade: {result['profitability']:.2f}%")
    print(f"Valor da comissão: R$ {result['commission_value']:.2f}")
    print(f"Percentual da comissão: {result['commission_percentage_actual']:.4f}")
    print()
    
    # Verificar cálculos intermediários
    print("=== CÁLCULOS INTERMEDIÁRIOS ===")
    frete_por_kg = BusinessRulesCalculator.calculate_freight_value_per_kg(freight_value_total, soma_pesos_pedido)
    print(f"Frete por kg: R$ {frete_por_kg:.4f}")
    
    valor_com_frete = item_data['valor_com_icms_compra'] + frete_por_kg
    print(f"Valor unitário COM frete: R$ {valor_com_frete:.4f}")
    
    total_compra_com_frete = item_data['peso_compra'] * valor_com_frete
    total_venda = item_data['peso_venda'] * item_data['valor_com_icms_venda']
    
    print(f"Total compra COM frete: R$ {total_compra_com_frete:.2f}")
    print(f"Total venda: R$ {total_venda:.2f}")
    
    rentabilidade_manual = ((total_venda - total_compra_com_frete) / total_compra_com_frete) * 100
    print(f"Rentabilidade manual: {rentabilidade_manual:.2f}%")
    
    print("\n=== COMPARAÇÃO COM VALORES ESPERADOS ===")
    print(f"Sistema calculou:")
    print(f"- Total compra: R$ {result['total_purchase']:.2f}")
    print(f"- Rentabilidade: {result['profitability']:.2f}%")
    print(f"- Comissão: R$ {result['commission_value']:.2f}")
    print(f"- Percentual comissão: {result['commission_percentage_actual']*100:.2f}%")
    
    print(f"\nValores esperados:")
    print(f"- Total compra: R$ 2070.16 (da resposta)")
    print(f"- Rentabilidade: 56.84%")
    print(f"- Comissão: R$ 130.90")
    print(f"- Percentual comissão: 3%")
    
    print(f"\nDiferenças:")
    print(f"- Total compra: R$ {result['total_purchase'] - 2070.16:.2f}")
    print(f"- Rentabilidade: {result['profitability'] - 56.84:.2f}%")
    print(f"- Comissão: R$ {result['commission_value'] - 130.90:.2f}")
    print(f"- Percentual comissão: {(result['commission_percentage_actual']*100) - 3:.2f}%")

if __name__ == "__main__":
    test_complete_calculation()