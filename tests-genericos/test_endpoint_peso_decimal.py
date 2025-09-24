#!/usr/bin/env python3

import requests
import json
import sys

# Test data with specific decimal values
test_data = {
    "order_number": "PED-TEST-DECIMAL",
    "client_name": "Cliente Teste Decimal",
    "status": "draft",
    "expires_at": "2025-08-19T03:00:00.000Z",
    "prazo_medio": 1,
    "outras_despesas_totais": 0,
    "items": [{
        "description": "item teste decimal",
                "peso_compra": 5.500,  # This should be preserved as 5.500
        "peso_venda": 5.5,
        "valor_com_icms_compra": 3.45,
        "percentual_icms_compra": 0.12,
        "outras_despesas_item": 0,
        "valor_com_icms_venda": 46,
        "percentual_icms_venda": 0.12
    }]
}

def test_calculate_endpoint():
    """Test the calculate-simplified endpoint with decimal values"""
    
    BASE_URL = "http://localhost:8002/api/v1/budgets"
    
    print("=== TESTE ENDPOINT CALCULATE-SIMPLIFIED ===")
    print(f"Valor enviado: peso_compra = {test_data['items'][0]['peso_compra']}")
    print(f"Esperado no backend: peso_compra = 5.500")
    
    try:
        # Test the calculate endpoint
        print(f"\n1. Enviando dados para {BASE_URL}/calculate-simplified...")
        
        response = requests.post(
            f"{BASE_URL}/calculate-simplified",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n2. Resposta do cálculo:")
            print(json.dumps(result, indent=2))
            
            # Check if peso_compra was preserved
            if 'items_calculations' in result and result['items_calculations']:
                item = result['items_calculations'][0]
                if 'peso_compra' in item:
                    received_peso = item['peso_compra']
                    print(f"\n3. Verificação:")
                    print(f"peso_compra original: {test_data['items'][0]['peso_compra']}")
                    print(f"peso_compra retornado: {received_peso}")
                    print(f"Preservou decimal? {received_peso == test_data['items'][0]['peso_compra']}")
                else:
                    print("\n3. Campo peso_compra não encontrado na resposta")
            else:
                print("\n3. items_calculations não encontrado na resposta")
                
        elif response.status_code == 422:
            # Validation error - let's see the details
            error_detail = response.json()
            print(f"\n2. Erro de validação:")
            print(json.dumps(error_detail, indent=2))
            
        else:
            print(f"\n2. Erro: {response.status_code}")
            print(response.text)
            
    except requests.ConnectionError:
        print("Erro: Não foi possível conectar ao servidor. Certifique-se de que o backend está rodando em localhost:8001")
        sys.exit(1)
    except Exception as e:
        print(f"Erro inesperado: {e}")
        sys.exit(1)

def test_different_decimal_values():
    """Test with various decimal values to see how they're handled"""
    
    BASE_URL = "http://localhost:8002/api/v1/budgets"
    
    test_values = [5.0, 5.5, 5.50, 5.500, 5.555, 5.123456789]
    
    print(f"\n=== TESTE COM DIFERENTES VALORES DECIMAIS ===")
    
    for test_value in test_values:
        print(f"\n--- Testando valor: {test_value} ---")
        
        # Create test data with this specific value
        current_test_data = test_data.copy()
        current_test_data['order_number'] = f"PED-TEST-{str(test_value).replace('.', '-')}"
        current_test_data['items'][0]['peso_compra'] = test_value
        
        try:
            response = requests.post(
                f"{BASE_URL}/calculate-simplified",
                json=current_test_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'items_calculations' in result and result['items_calculations']:
                    item = result['items_calculations'][0]
                    if 'peso_compra' in item:
                        received_peso = item['peso_compra']
                        print(f"Enviado: {test_value} -> Recebido: {received_peso}")
                        print(f"Preservou? {received_peso == test_value}")
                    else:
                        print(f"Campo peso_compra não encontrado na resposta")
                else:
                    print(f"items_calculations não encontrado")
            else:
                print(f"Erro {response.status_code}: {response.text[:200]}")
                
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    test_calculate_endpoint()
    test_different_decimal_values()
