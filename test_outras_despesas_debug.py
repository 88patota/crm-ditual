#!/usr/bin/env python3
"""
Script para testar se o backend está processando corretamente as outras despesas.
"""

import requests
import json

# Configuração da API
BASE_URL = "http://localhost:8001"
CALCULATE_URL = f"{BASE_URL}/budgets/calculate-simplified"

def test_outras_despesas():
    """Testa se as outras despesas estão sendo processadas corretamente"""
    
    # Dados de teste com outras despesas
    test_data = {
        "order_number": "TEST-OUTRAS-001",
        "client_name": "Cliente Teste",
        "freight_type": "FOB",
        "payment_condition": "À vista",
        "items": [
            {
                "description": "Item Teste",
                "peso_compra": 10.0,
                "peso_venda": 10.0,
                "valor_com_icms_compra": 100.0,
                "percentual_icms_compra": 0.17,
                "outras_despesas_item": 15.0,  # VALOR DE TESTE
                "valor_com_icms_venda": 150.0,
                "percentual_icms_venda": 0.18,
                "percentual_ipi": 0.0
            }
        ]
    }
    
    print("🔍 Testando cálculo com outras despesas...")
    print(f"📊 Dados enviados:")
    print(json.dumps(test_data, indent=2, ensure_ascii=False))
    
    try:
        response = requests.post(CALCULATE_URL, json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Resposta recebida:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            # Verificar se as outras despesas estão sendo consideradas
            if 'items_calculations' in result and len(result['items_calculations']) > 0:
                item_calc = result['items_calculations'][0]
                print(f"\n🔍 Análise do item calculado:")
                print(f"   - Valor de compra total: {item_calc.get('total_purchase', 'N/A')}")
                print(f"   - Valor de venda total: {item_calc.get('total_sale', 'N/A')}")
                print(f"   - Rentabilidade: {item_calc.get('profitability', 'N/A')}")
                
                # Verificar se o valor de compra inclui as outras despesas
                expected_purchase = 100.0 + 15.0  # valor_com_icms_compra + outras_despesas_item
                actual_purchase = item_calc.get('total_purchase', 0)
                
                print(f"\n📈 Verificação das outras despesas:")
                print(f"   - Valor esperado (com outras despesas): {expected_purchase}")
                print(f"   - Valor calculado: {actual_purchase}")
                
                if abs(actual_purchase - expected_purchase) < 0.01:
                    print("   ✅ OUTRAS DESPESAS ESTÃO SENDO CONSIDERADAS!")
                else:
                    print("   ❌ OUTRAS DESPESAS NÃO ESTÃO SENDO CONSIDERADAS!")
                    
            else:
                print("❌ Não foi possível encontrar cálculos dos itens na resposta")
                
        else:
            print(f"❌ Erro na requisição: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro ao fazer requisição: {e}")

def test_sem_outras_despesas():
    """Testa o mesmo cálculo sem outras despesas para comparação"""
    
    test_data = {
        "order_number": "TEST-SEM-OUTRAS-001",
        "client_name": "Cliente Teste",
        "freight_type": "FOB",
        "payment_condition": "À vista",
        "items": [
            {
                "description": "Item Teste",
                "peso_compra": 10.0,
                "peso_venda": 10.0,
                "valor_com_icms_compra": 100.0,
                "percentual_icms_compra": 0.17,
                "outras_despesas_item": 0.0,  # SEM OUTRAS DESPESAS
                "valor_com_icms_venda": 150.0,
                "percentual_icms_venda": 0.18,
                "percentual_ipi": 0.0
            }
        ]
    }
    
    print("\n\n🔍 Testando cálculo SEM outras despesas (para comparação)...")
    
    try:
        response = requests.post(CALCULATE_URL, json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            
            if 'items_calculations' in result and len(result['items_calculations']) > 0:
                item_calc = result['items_calculations'][0]
                print(f"📊 Valor de compra SEM outras despesas: {item_calc.get('total_purchase', 'N/A')}")
                
        else:
            print(f"❌ Erro na requisição: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao fazer requisição: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando teste de outras despesas...")
    test_outras_despesas()
    test_sem_outras_despesas()
    print("\n✅ Teste concluído!")