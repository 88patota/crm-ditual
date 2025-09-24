#!/usr/bin/env python3

import requests
import json

# Test data demonstrating the issue
test_data = {
    "order_number": "PED-0001",
    "client_name": "Cliente Teste",
    "status": "draft",
    "expires_at": "2025-08-19T03:00:00.000Z",
    "prazo_medio": 1,
    "outras_despesas_totais": 0,
    "items": [{
        "description": "item",
                "peso_compra": 5.500,  # This should be preserved as 5.500
        "peso_venda": 5.5,
        "valor_com_icms_compra": 3.45,
        "percentual_icms_compra": 0.12,
        "outras_despesas_item": 0,
        "valor_com_icms_venda": 46,
        "percentual_icms_venda": 0.12
    }]
}

def test_peso_decimal():
    """Test to reproduce the peso_compra decimal issue"""
    
    print("=== TESTE DO PROBLEMA COM DECIMAIS ===")
    print(f"Valor enviado pelo frontend: peso_compra = {test_data['items'][0]['peso_compra']}")
    
    # Simulate what happens in the frontend/backend communication
    print("\n1. Dados JSON sendo enviados:")
    json_str = json.dumps(test_data, indent=2)
    print(json_str)
    
    # Parse back to simulate backend reception
    print("\n2. Dados após parse no backend:")
    parsed_data = json.loads(json_str)
    received_peso_compra = parsed_data['items'][0]['peso_compra']
    print(f"peso_compra recebido: {received_peso_compra}")
    print(f"Tipo: {type(received_peso_compra)}")
    
    # Test potential precision issues
    print(f"\n3. Verificação de precisão:")
    print(f"Original: {test_data['items'][0]['peso_compra']}")
    print(f"Após JSON: {received_peso_compra}")
    print(f"São iguais? {test_data['items'][0]['peso_compra'] == received_peso_compra}")
    
    # Test different scenarios
    test_values = [5.0, 5.5, 5.50, 5.500, 5.555]
    
    print(f"\n4. Testando diferentes valores:")
    for val in test_values:
        json_test = json.dumps({"peso": val})
        parsed = json.loads(json_test)
        print(f"{val} -> {parsed['peso']} (tipo: {type(parsed['peso'])})")

if __name__ == "__main__":
    test_peso_decimal()
