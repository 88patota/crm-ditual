#!/usr/bin/env python3
"""
Teste para verificar se a correção dos endpoints /calculate e /calculate-simplified funcionou
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'budget_service'))

from app.services.business_rules_calculator import BusinessRulesCalculator

def teste_correcao_endpoints():
    """Teste com os dados EXATOS do usuário"""
    
    print("=== TESTE CORREÇÃO ENDPOINTS ===")
    
    # Dados EXATOS enviados pelo frontend
    items_data = [
        {
            "description": "item",
            "delivery_time": "0",
            "peso_compra": 1000,
            "peso_venda": 1010,
            "valor_com_icms_compra": 2.11,
            "percentual_icms_compra": 0.18,
            "outras_despesas_item": 0,
            "valor_com_icms_venda": 4.32,
            "percentual_icms_venda": 0.18,
            "percentual_ipi": 0,
        }
    ]
    
    freight_value_total = 500
    
    # Valores esperados pelo frontend
    expected_total_purchase = 2070.16
    expected_total_sale = 3246.88
    expected_profitability = 104.74
    
    print("=== VALORES ESPERADOS (FRONTEND) ===")
    print(f"Total compra: R$ {expected_total_purchase:.2f}")
    print(f"Total venda: R$ {expected_total_sale:.2f}")
    print(f"Rentabilidade: {expected_profitability:.2f}%")
    print(f"Frete total: R$ {freight_value_total:.2f}")
    
    # Simular o cálculo correto do endpoint (usando peso_venda)
    total_peso_pedido = sum(item.get('peso_venda', item.get('peso_compra', 1.0)) for item in items_data)
    outras_despesas_totais = sum(item.get('outras_despesas_item', 0) for item in items_data)
    
    print(f"\n=== CÁLCULO CORRETO (PESO_VENDA) ===")
    print(f"Soma pesos pedido (peso_venda): {total_peso_pedido} kg")
    print(f"Frete por kg: R$ {freight_value_total / total_peso_pedido:.6f}")
    
    calculator = BusinessRulesCalculator()
    result = calculator.calculate_complete_budget(
        items_data=items_data,
        outras_despesas_totais=outras_despesas_totais,
        soma_pesos_pedido=total_peso_pedido,
        freight_value_total=freight_value_total
    )
    
    print(f"\nResultado BusinessRulesCalculator:")
    print(f"Total compra: R$ {result['totals']['soma_total_compra']:.2f}")
    print(f"Total venda: R$ {result['totals']['soma_total_venda']:.2f}")
    
    if result['totals']['soma_total_compra'] > 0:
        rentabilidade_calc = ((result['totals']['soma_total_venda'] - result['totals']['soma_total_compra']) / result['totals']['soma_total_compra']) * 100
        print(f"Rentabilidade calculada: {rentabilidade_calc:.2f}%")
    
    print("\n=== COMPARAÇÃO COM VALORES ESPERADOS ===")
    diff_compra = abs(result['totals']['soma_total_compra'] - expected_total_purchase)
    diff_venda = abs(result['totals']['soma_total_venda'] - expected_total_sale)
    diff_rentabilidade = abs(rentabilidade_calc - expected_profitability)
    
    print(f"Diferença compra: R$ {diff_compra:.2f}")
    print(f"Diferença venda: R$ {diff_venda:.2f}")
    print(f"Diferença rentabilidade: {diff_rentabilidade:.2f} pontos percentuais")
    
    # Tolerância de 1 real para diferenças de arredondamento
    tolerance = 1.0
    tolerance_percent = 1.0
    
    print("\n=== RESULTADO ===")
    if (diff_compra <= tolerance and 
        diff_venda <= tolerance and 
        diff_rentabilidade <= tolerance_percent):
        print("✅ CORREÇÃO FUNCIONOU! Os valores estão dentro da tolerância esperada.")
    else:
        print("❌ AINDA HÁ DISCREPÂNCIAS significativas.")
        
        # Investigar mais profundamente
        print("\n=== INVESTIGAÇÃO ADICIONAL ===")
        item_calc = result['items'][0]
        print(f"Frete distribuído por kg: R$ {item_calc['frete_distribuido_por_kg']:.6f}")
        print(f"Valor sem impostos compra: R$ {item_calc['valor_sem_impostos_compra']:.6f}")
        print(f"Valor sem impostos venda: R$ {item_calc['valor_sem_impostos_venda']:.6f}")
        print(f"Total compra item: R$ {item_calc['total_compra_item']:.2f}")
        print(f"Total venda item: R$ {item_calc['total_venda_item']:.2f}")
        
        # Calcular manualmente para comparar
        print("\n=== CÁLCULO MANUAL PARA COMPARAÇÃO ===")
        
        # Valor sem ICMS compra
        valor_sem_icms_compra = 2.11 / (1 + 0.18)
        print(f"Valor sem ICMS compra: R$ {valor_sem_icms_compra:.6f}")
        
        # Frete por kg
        frete_por_kg = 500 / 1010
        print(f"Frete por kg: R$ {frete_por_kg:.6f}")
        
        # Valor compra com frete
        valor_compra_com_frete = valor_sem_icms_compra + frete_por_kg
        print(f"Valor compra com frete: R$ {valor_compra_com_frete:.6f}")
        
        # Total compra
        total_compra_manual = valor_compra_com_frete * 1000
        print(f"Total compra manual: R$ {total_compra_manual:.2f}")
        
        # Valor sem ICMS venda
        valor_sem_icms_venda = 4.32 / (1 + 0.18)
        print(f"Valor sem ICMS venda: R$ {valor_sem_icms_venda:.6f}")
        
        # Total venda
        total_venda_manual = valor_sem_icms_venda * 1010
        print(f"Total venda manual: R$ {total_venda_manual:.2f}")
        
        # Rentabilidade manual
        rentabilidade_manual = ((total_venda_manual - total_compra_manual) / total_compra_manual) * 100
        print(f"Rentabilidade manual: {rentabilidade_manual:.2f}%")

if __name__ == "__main__":
    teste_correcao_endpoints()