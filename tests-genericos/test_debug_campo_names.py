#!/usr/bin/env python3
"""
Teste para debugging dos nomes de campos no erro de validação
"""
import requests
import json

# Dados de teste com os nomes de campos conforme schema simplificado
test_budget_data = {
    "client_name": "Cliente Teste",
    "notes": "Teste de campos",
    "items": [
        {
            "description": "Item de teste",
            "peso_compra": 1.0,
            "peso_venda": 1.0,
            "valor_com_icms_compra": 100.0,
            "percentual_icms_compra": 0.18,
            "outras_despesas_item": 0.0,
            "valor_com_icms_venda": 120.0,
            "percentual_icms_venda": 0.18
        }
    ]
}

def test_simplified_budget_creation():
    """Testa criação de orçamento simplificado"""
    url = "http://localhost:8001/api/v1/budgets/simplified"
    
    print("=== TESTE CRIAÇÃO ORÇAMENTO SIMPLIFICADO ===")
    print(f"URL: {url}")
    print(f"Dados enviados:")
    print(json.dumps(test_budget_data, indent=2, ensure_ascii=False))
    print("\n" + "="*50 + "\n")
    
    try:
        response = requests.post(url, json=test_budget_data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body:")
        
        try:
            response_json = response.json()
            print(json.dumps(response_json, indent=2, ensure_ascii=False))
        except:
            print(response.text)
            
        print("\n" + "="*50 + "\n")
        
        if response.status_code != 201:
            print("❌ ERRO ENCONTRADO!")
            if "detail" in response.json():
                print(f"Detalhe do erro: {response.json()['detail']}")
        else:
            print("✅ Orçamento criado com sucesso!")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

def test_calculate_simplified():
    """Testa endpoint de cálculo simplificado"""
    url = "http://localhost:8001/api/v1/budgets/calculate-simplified"
    
    print("=== TESTE CÁLCULO SIMPLIFICADO ===")
    print(f"URL: {url}")
    print(f"Dados enviados:")
    print(json.dumps(test_budget_data, indent=2, ensure_ascii=False))
    print("\n" + "="*50 + "\n")
    
    try:
        response = requests.post(url, json=test_budget_data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Body:")
        
        try:
            response_json = response.json()
            print(json.dumps(response_json, indent=2, ensure_ascii=False))
        except:
            print(response.text)
            
        print("\n" + "="*50 + "\n")
        
        if response.status_code != 200:
            print("❌ ERRO ENCONTRADO!")
            if "detail" in response.json():
                print(f"Detalhe do erro: {response.json()['detail']}")
        else:
            print("✅ Cálculo realizado com sucesso!")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

if __name__ == "__main__":
    print("Iniciando testes de debugging dos campos...\n")
    
    # Testar cálculo primeiro
    test_calculate_simplified()
    
    # Testar criação
    test_simplified_budget_creation()
