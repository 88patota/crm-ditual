#!/usr/bin/env python3
import requests
import json

# Configuração da API
BASE_URL = "http://localhost:8002"

def test_freight_commission():
    print("=== Teste Rápido: Comissão com Frete ===\n")
    
    # Dados de teste
    test_data = {
        "client_name": "Cliente Teste",
        "items": [
            {
                "description": "Item Teste",
                "peso_compra": 1.0,
                "peso_venda": 1.0,
                "preco_compra": 50.0,
                "preco_venda": 100.0,
                "quantidade_compra": 1,
                "quantidade_venda": 1,
                "percentual_ipi": 0.0
            }
        ],
        "freight_value_total": 25.0  # Frete de R$ 25
    }
    
    try:
        # Fazer requisição
        response = requests.post(f"{BASE_URL}/budgets/calculate-simplified", json=test_data)
        
        if response.status_code != 200:
            print(f"❌ Erro na requisição: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
            
        result = response.json()
        
        # Verificar se tem itens calculados
        if "items_calculations" not in result or not result["items_calculations"]:
            print("❌ Erro: Não há itens calculados na resposta")
            return False
            
        item = result["items_calculations"][0]
        
        print(f"Total purchase: R$ {item['total_purchase']:.2f}")
        print(f"Rentabilidade: {item['profitability']:.2f}%")
        print(f"Comissão: R$ {item['commission_value']:.2f}")
        print(f"Total final: R$ {result['total_final_value']:.2f}")
        
        # Verificar se o frete foi incluído no custo
        expected_purchase_with_freight = 50.0 + 25.0  # preço base + frete
        actual_purchase = item['total_purchase']
        
        print(f"\nVerificação:")
        print(f"Custo esperado com frete: R$ {expected_purchase_with_freight:.2f}")
        print(f"Custo atual: R$ {actual_purchase:.2f}")
        
        if abs(actual_purchase - expected_purchase_with_freight) < 0.01:
            print("✅ Frete incluído corretamente no custo")
            return True
        else:
            print("❌ Frete NÃO foi incluído no custo")
            return False
            
    except Exception as e:
        print(f"❌ Erro na execução: {e}")
        return False

if __name__ == "__main__":
    success = test_freight_commission()
    if success:
        print("\n🎉 Teste passou!")
    else:
        print("\n❌ Teste falhou!")