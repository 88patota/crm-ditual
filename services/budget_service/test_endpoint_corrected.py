#!/usr/bin/env python3
"""
Teste do endpoint /calculate-simplified para verificar se está retornando
os valores corretos com frete incluído.
"""

import requests
import json

def test_calculate_simplified_endpoint():
    """Testa o endpoint /calculate-simplified com os dados do usuário"""
    
    # URL do endpoint
    url = "http://localhost:8001/api/v1/budgets/calculate-simplified"
    
    # Dados do usuário
    payload = {
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
                "percentual_ipi": 0
            }
        ],
        "freight_value_total": 500
    }
    
    print("=== TESTE DO ENDPOINT /calculate-simplified ===\n")
    print("Dados enviados:")
    print(json.dumps(payload, indent=2))
    
    try:
        # Fazer requisição
        response = requests.post(url, json=payload)
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n=== RESULTADOS DO ENDPOINT ===")
            print(f"Total Purchase Value: R$ {result['total_purchase_value']:.2f}")
            print(f"Total Sale Value: R$ {result['total_sale_value']:.2f}")
            print(f"Total Commission: R$ {result['total_commission']:.2f}")
            print(f"Commission Percentage Actual: {result['commission_percentage_actual']:.2f}%")
            print(f"Profitability Percentage: {result['profitability_percentage']:.2f}%")
            print(f"Markup Percentage: {result['markup_percentage']:.2f}%")
            
            # Verificar item individual
            if result['items_calculations']:
                item = result['items_calculations'][0]
                print(f"\n=== ITEM INDIVIDUAL ===")
                print(f"Total Purchase: R$ {item['total_purchase']:.2f}")
                print(f"Total Sale: R$ {item['total_sale']:.2f}")
                print(f"Profitability: {item['profitability']:.2f}%")
                print(f"Commission Value: R$ {item['commission_value']:.2f}")
                print(f"Commission Percentage Actual: {item.get('commission_percentage_actual', 0):.2f}%")
            
            # Comparar com valores esperados
            print(f"\n=== COMPARAÇÃO COM VALORES ESPERADOS ===")
            print(f"Comissão esperada: R$ 130.90")
            print(f"Comissão calculada: R$ {result['total_commission']:.2f}")
            print(f"Diferença: R$ {abs(130.90 - result['total_commission']):.2f}")
            
            print(f"\nRentabilidade esperada: 56.84%")
            print(f"Rentabilidade calculada: {result['profitability_percentage']:.2f}%")
            print(f"Diferença: {abs(56.84 - result['profitability_percentage']):.2f}%")
            
            print(f"\nPercentual comissão esperado: 3%")
            print(f"Percentual comissão calculado: {result['commission_percentage_actual']:.2f}%")
            print(f"Diferença: {abs(3.0 - result['commission_percentage_actual']):.2f}%")
            
            # Verificar se está próximo dos valores esperados
            commission_ok = abs(130.90 - result['total_commission']) < 50  # Tolerância de R$ 50
            profitability_ok = abs(56.84 - result['profitability_percentage']) < 10  # Tolerância de 10%
            
            print(f"\n=== ANÁLISE ===")
            print(f"Comissão próxima do esperado: {'✓' if commission_ok else '✗'}")
            print(f"Rentabilidade próxima do esperado: {'✓' if profitability_ok else '✗'}")
            
            if commission_ok and profitability_ok:
                print("\n✅ SUCESSO: Valores estão próximos dos esperados!")
            else:
                print("\n❌ PROBLEMA: Valores ainda divergem significativamente dos esperados")
                
        else:
            print(f"Erro na requisição: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERRO: Não foi possível conectar ao servidor")
        print("Certifique-se de que o servidor está rodando em http://localhost:8001")
    except Exception as e:
        print(f"❌ ERRO: {str(e)}")

if __name__ == "__main__":
    test_calculate_simplified_endpoint()