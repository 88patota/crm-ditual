#!/usr/bin/env python3
"""
Test script to verify complete IPI persistence flow with authentication
"""
import requests
import json
import sys

# Configuration
USER_SERVICE_URL = "http://localhost:8001"
BUDGET_SERVICE_URL = "http://localhost:8002"
API_PREFIX = "/api/v1"

def get_auth_token():
    """Get authentication token"""
    print("=== GETTING AUTHENTICATION TOKEN ===")
    
    # Try to login with demo user
    login_data = {
        "username": "admin@admin.com",
        "password": "admin123"
    }
    
    url = f"{USER_SERVICE_URL}{API_PREFIX}/users/login"
    print(f"Attempting login at: {url}")
    
    try:
        response = requests.post(url, json=login_data)
        print(f"Login response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            token = result.get('access_token')
            if token:
                print("✅ Authentication successful!")
                return token
            else:
                print("❌ No access token in response")
                return None
        else:
            print(f"❌ Login failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return None

def test_ipi_calculation_only():
    """Test IPI calculation endpoint"""
    print("\n=== TESTING IPI CALCULATION ENDPOINT ===")
    
    test_data = {
        "order_number": "TEST-IPI-CALC-001",
        "client_name": "Cliente Teste IPI",
        "items": [
            {
                "description": "Item com IPI 3.25%",
                "weight": 100.0,
                "purchase_value_with_icms": 10.00,
                "purchase_icms_percentage": 0.18,
                "purchase_other_expenses": 0.0,
                "purchase_value_without_taxes": 8.00,
                "sale_weight": 100.0,
                "sale_value_with_icms": 15.00,
                "sale_icms_percentage": 0.17,
                "sale_value_without_taxes": 12.45,
                "ipi_percentage": 0.0325,
                "commission_percentage": 0.0
            }
        ]
    }

    url = f"{BUDGET_SERVICE_URL}{API_PREFIX}/budgets/calculate"
    
    try:
        response = requests.post(url, json=test_data)
        print(f"Calculation response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Calculation successful!")
            
            total_ipi = result.get('total_ipi_value', 0)
            print(f"Total IPI calculated: R$ {total_ipi:.2f}")
            
            # Expected: 100kg * R$15.00 * 3.25% = R$48.75
            expected_ipi = 100.0 * 15.00 * 0.0325
            print(f"Expected IPI: R$ {expected_ipi:.2f}")
            
            if abs(total_ipi - expected_ipi) < 0.01:
                print("✅ IPI calculation is correct!")
                return True, result
            else:
                print("❌ IPI calculation is incorrect!")
                return False, result
        else:
            print(f"❌ Calculation failed: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ Calculation error: {e}")
        return False, None

def test_ipi_persistence_with_auth(token):
    """Test IPI persistence with authentication"""
    print("\n=== TESTING IPI PERSISTENCE WITH AUTHENTICATION ===")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Create budget with IPI
    budget_data = {
        "order_number": f"TEST-IPI-PERSIST-001",
        "client_name": "Cliente Teste Persistencia IPI",
        "items": [
            {
                "description": "Item com IPI 3.25%",
                "weight": 100.0,
                "purchase_value_with_icms": 10.00,
                "purchase_icms_percentage": 0.18,
                "purchase_other_expenses": 0.0,
                "purchase_value_without_taxes": 8.00,
                "sale_weight": 100.0,
                "sale_value_with_icms": 15.00,
                "sale_icms_percentage": 0.17,
                "sale_value_without_taxes": 12.45,
                "ipi_percentage": 0.0325,
                "commission_percentage": 0.0
            }
        ]
    }
    
    # Test simplified creation endpoint
    url = f"{BUDGET_SERVICE_URL}{API_PREFIX}/budgets/simplified"
    print(f"Creating budget at: {url}")
    
    try:
        response = requests.post(url, json=budget_data, headers=headers)
        print(f"Creation response status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            budget_id = result.get('id')
            print(f"✅ Budget created with ID: {budget_id}")
            
            # Verify IPI values in created budget
            items = result.get('items', [])
            if items:
                item = items[0]
                saved_ipi_percentage = item.get('ipi_percentage', 0)
                saved_ipi_value = item.get('ipi_value', 0)
                
                print(f"Saved IPI percentage: {saved_ipi_percentage * 100:.2f}%")
                print(f"Saved IPI value: R$ {saved_ipi_value:.2f}")
                
                # Check if values were saved correctly
                if abs(saved_ipi_percentage - 0.0325) < 0.0001:
                    print("✅ IPI percentage saved correctly!")
                else:
                    print("❌ IPI percentage NOT saved correctly!")
                    print(f"Expected: 3.25%, Got: {saved_ipi_percentage * 100:.2f}%")
                    return False
                
                expected_ipi_value = 100.0 * 15.00 * 0.0325  # 48.75
                if abs(saved_ipi_value - expected_ipi_value) < 0.01:
                    print("✅ IPI value saved correctly!")
                    return True
                else:
                    print("❌ IPI value NOT saved correctly!")
                    print(f"Expected: R$ {expected_ipi_value:.2f}, Got: R$ {saved_ipi_value:.2f}")
                    return False
            else:
                print("❌ No items found in created budget")
                return False
                
        else:
            print(f"❌ Budget creation failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Persistence test error: {e}")
        return False

def main():
    print("=== TESTE COMPLETO DE PERSISTÊNCIA DO IPI ===")
    print("Este teste verifica se o IPI está sendo salvo corretamente no banco de dados")
    print()
    
    # Step 1: Test calculation without auth
    print("PASSO 1: Testando cálculo do IPI...")
    calc_success, calc_result = test_ipi_calculation_only()
    
    if not calc_success:
        print("❌ Falha no cálculo do IPI - interrompendo teste")
        sys.exit(1)
    
    # Step 2: Get authentication token
    print("\nPASSO 2: Obtendo token de autenticação...")
    token = get_auth_token()
    
    if not token:
        print("❌ Falha na autenticação - não é possível testar persistência")
        print("Certifique-se que o serviço de usuários está rodando e o usuário admin@admin.com existe")
        sys.exit(1)
    
    # Step 3: Test persistence
    print("\nPASSO 3: Testando persistência do IPI...")
    persist_success = test_ipi_persistence_with_auth(token)
    
    if persist_success:
        print("\n🎉 TESTE COMPLETO PASSOU!")
        print("✅ IPI está sendo calculado E persistido corretamente!")
    else:
        print("\n❌ TESTE FALHOU!")
        print("❌ IPI não está sendo persistido corretamente no banco de dados!")
        print("\nISSO CONFIRMA O BUG REPORTADO PELO USUÁRIO!")

if __name__ == "__main__":
    main()
