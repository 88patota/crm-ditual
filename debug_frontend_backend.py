#!/usr/bin/env python3
"""
Debug da discrepância entre frontend e backend com 1 item
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'budget_service'))

from app.services.business_rules_calculator import BusinessRulesCalculator

def debug_frontend_backend():
    """Debug exato do problema reportado pelo usuário"""
    
    print("=== DEBUG FRONTEND vs BACKEND ===")
    
    # Dados EXATOS enviados pelo frontend
    budget_data = {
        "order_number": "PED-0016",
        "client_name": "Cliente Teste",
        "status": "draft",
        "payment_condition": "À vista",
        "freight_type": "FOB",
        "freight_value_total": 500,
        "total_purchase_value": 2070.16,
        "total_sale_value": 3246.88,
        "profitability_percentage": 104.74,
        "markup_percentage": 104.74,
        "total_ipi_value": 0,
        "total_taxes": 1116.32,
        "total_final_value": 4363.2,
        "items": [
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
                "weight_difference_display": {
                    "has_difference": True,
                    "absolute_difference": 10,
                    "percentage_difference": 1,
                    "formatted_display": "1.0%"
                }
            }
        ]
    }
    
    # Resposta EXATA do backend
    backend_response = {
        "total_purchase_value": 2070.16,
        "total_sale_value": 3246.88,
        "total_net_revenue": 3246.88,
        "total_taxes": 1116.32,
        "total_commission": 218.16,
        "commission_percentage_actual": 6.72,
        "profitability_percentage": 104.74,
        "markup_percentage": 104.74,
        "items_calculations": [{
            "description": "item",
            "peso_compra": 1000.0,
            "peso_venda": 1010.0,
            "total_purchase": 2070.157,
            "total_sale": 3246.87528,
            "profitability": 104.739336492891,
            "commission_value": 218.16,
            "commission_percentage_actual": 0.05,
            "ipi_percentage": 0.0,
            "ipi_value": 0.0,
            "total_value_with_ipi": 4363.200000000001,
            "weight_difference_display": {
                "has_difference": True,
                "absolute_difference": 10.0,
                "percentage_difference": 1.0,
                "formatted_display": "1.0%"
            }
        }],
        "total_ipi_value": 0.0,
        "total_final_value": 4363.2,
        "total_weight_difference_percentage": 1.0
    }
    
    print("=== VALORES DO FRONTEND ===")
    print(f"Total compra (frontend): R$ {budget_data['total_purchase_value']:.2f}")
    print(f"Total venda (frontend): R$ {budget_data['total_sale_value']:.2f}")
    print(f"Rentabilidade (frontend): {budget_data['profitability_percentage']:.2f}%")
    print(f"Frete total: R$ {budget_data['freight_value_total']:.2f}")
    
    print("\n=== VALORES DO BACKEND ===")
    print(f"Total compra (backend): R$ {backend_response['total_purchase_value']:.2f}")
    print(f"Total venda (backend): R$ {backend_response['total_sale_value']:.2f}")
    print(f"Rentabilidade (backend): {backend_response['profitability_percentage']:.2f}%")
    
    print("\n=== CÁLCULO MANUAL DO ITEM ===")
    item = budget_data['items'][0]
    
    # Cálculo básico sem frete
    compra_basica = item['peso_compra'] * item['valor_com_icms_compra']
    venda_basica = item['peso_venda'] * item['valor_com_icms_venda']
    
    print(f"Compra básica (sem frete): {item['peso_compra']} × {item['valor_com_icms_compra']} = R$ {compra_basica:.2f}")
    print(f"Venda básica: {item['peso_venda']} × {item['valor_com_icms_venda']} = R$ {venda_basica:.2f}")
    
    # Calcular com BusinessRulesCalculator
    print("\n=== TESTE COM BUSINESSRULESCALCULATOR ===")
    
    items_data = budget_data['items']
    # Usar peso_compra para distribuição e somar outras despesas como R$/kg * peso_compra
    soma_pesos_pedido = sum(item.get('peso_compra', 0) for item in items_data)
    outras_despesas_totais = sum(
        (item.get('outras_despesas_item', 0) or 0.0) * (item.get('peso_compra', 0) or 0.0)
        for item in items_data
    )
    
    print(f"Soma pesos pedido (peso_venda): {soma_pesos_pedido} kg")
    print(f"Frete por kg: R$ {budget_data['freight_value_total'] / soma_pesos_pedido:.6f}")
    
    calculator = BusinessRulesCalculator()
    result = calculator.calculate_complete_budget(
        items_data=items_data,
        outras_despesas_totais=outras_despesas_totais,
        soma_pesos_pedido=soma_pesos_pedido,
        freight_value_total=budget_data['freight_value_total']
    )
    
    print(f"\nResultado BusinessRulesCalculator:")
    print(f"Total compra: R$ {result['totals']['soma_total_compra']:.2f}")
    print(f"Total venda: R$ {result['totals']['soma_total_venda']:.2f}")
    
    if result['totals']['soma_total_compra'] > 0:
        rentabilidade_calc = ((result['totals']['soma_total_venda'] - result['totals']['soma_total_compra']) / result['totals']['soma_total_compra']) * 100
        print(f"Rentabilidade calculada: {rentabilidade_calc:.2f}%")
    
    print("\n=== ANÁLISE DAS DIFERENÇAS ===")
    diff_compra_frontend = abs(result['totals']['soma_total_compra'] - budget_data['total_purchase_value'])
    diff_venda_frontend = abs(result['totals']['soma_total_venda'] - budget_data['total_sale_value'])
    
    print(f"Diferença compra (Calculator vs Frontend): R$ {diff_compra_frontend:.2f}")
    print(f"Diferença venda (Calculator vs Frontend): R$ {diff_venda_frontend:.2f}")
    
    diff_compra_backend = abs(result['totals']['soma_total_compra'] - backend_response['total_purchase_value'])
    diff_venda_backend = abs(result['totals']['soma_total_venda'] - backend_response['total_sale_value'])
    
    print(f"Diferença compra (Calculator vs Backend): R$ {diff_compra_backend:.2f}")
    print(f"Diferença venda (Calculator vs Backend): R$ {diff_venda_backend:.2f}")
    
    print("\n=== DETALHES DO ITEM CALCULADO ===")
    if result['items']:
        item_calc = result['items'][0]
        print(f"Total compra item: R$ {item_calc['total_compra_item']:.2f}")
        print(f"Total venda item: R$ {item_calc['total_venda_item']:.2f}")
        print(f"Valor sem impostos compra: R$ {item_calc['valor_sem_impostos_compra']:.6f}")
        print(f"Valor sem impostos venda: R$ {item_calc['valor_sem_impostos_venda']:.6f}")
        print(f"Frete distribuído por kg: R$ {item_calc['frete_distribuido_por_kg']:.6f}")
        
        # Verificar se o frete está sendo incluído corretamente
        valor_compra_sem_frete = BusinessRulesCalculator.calculate_purchase_value_without_taxes(
            item['valor_com_icms_compra'], item['percentual_icms_compra'], 0.0
        )
        print(f"Valor compra SEM frete: R$ {valor_compra_sem_frete:.6f}")
        print(f"Valor compra COM frete: R$ {item_calc['valor_sem_impostos_compra']:.6f}")
        print(f"Diferença (deve ser o frete): R$ {item_calc['valor_sem_impostos_compra'] - valor_compra_sem_frete:.6f}")

if __name__ == "__main__":
    debug_frontend_backend()