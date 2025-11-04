#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'budget_service'))

from app.services.business_rules_calculator import BusinessRulesCalculator
import json

def test_result_keys():
    print("=== VERIFICANDO CHAVES DO RESULTADO ===")
    
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
    
    # Calcular usando o método completo
    result = BusinessRulesCalculator.calculate_complete_item(
        item_data, outras_despesas_totais, soma_pesos_pedido, freight_value_total
    )
    
    print("Chaves disponíveis no resultado:")
    for key in sorted(result.keys()):
        print(f"- {key}: {result[key]}")
    
    print("\n=== RESULTADO FORMATADO ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_result_keys()