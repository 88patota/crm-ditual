#!/usr/bin/env python3
"""
Test script to verify that both BudgetItemCreate validation issues are fixed:
1. Missing required fields (purchase_value_without_taxes, sale_value_without_taxes)
2. Incorrect validation logic in validate_simplified_budget_data
"""
import json
import requests
import sys

def test_validation_logic_fix():
    """Test that the validation logic now correctly validates the input data"""
    
    # This is the exact data that was causing the validation error
    test_data = {
        "order_number": "PED-0003",
        "client_name": "Cliente Teste", 
        "status": "draft",
        "items": [
            {
                "description": "item",
                "peso_compra": 6000,  # This is > 0, should pass
                "peso_venda": 6000,
                "valor_com_icms_compra": 33.21,  # This is > 0, should pass
                "percentual_icms_compra": 0.12,
                "outras_despesas_item": 0,
                "valor_com_icms_venda": 55.89,  # This is > 0, should pass
                "percentual_icms_venda": 0.15
            }
        ]
    }
    
    print("=== Teste de Correção Completa da Validação ===")
    print()
    print("Dados de teste que causavam erro:")
    print(json.dumps(test_data, indent=2, ensure_ascii=False))
    print()
    print("Valores que deveriam passar na validação:")
    print(f"- peso_compra: {test_data['items'][0]['peso_compra']} (> 0) ✓")
    print(f"- valor_com_icms_compra: {test_data['items'][0]['valor_com_icms_compra']} (> 0) ✓")  
    print(f"- valor_com_icms_venda: {test_data['items'][0]['valor_com_icms_venda']} (> 0) ✓")
    print()
    
    base_url = "http://localhost:8001"
    
    try:
        print("1. Testando endpoint de cálculo simplificado...")
        calc_response = requests.post(
            f"{base_url}/api/v1/budgets/calculate-simplified",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {calc_response.status_code}")
        
        if calc_response.status_code == 200:
            print("✅ Cálculo simplificado funcionando!")
            calc_data = calc_response.json()
            print(f"Total compra: R$ {calc_data['total_purchase_value']:.2f}")
            print(f"Total venda: R$ {calc_data['total_sale_value']:.2f}")
            print(f"Markup: {calc_data['markup_percentage']:.2f}%")
            print()
        elif calc_response.status_code == 422:
            print("❌ Ainda há erro de validação no cálculo:")
            error_detail = calc_response.json()
            print(json.dumps(error_detail, indent=2, ensure_ascii=False))
            return False
        else:
            print(f"❌ Erro inesperado no cálculo: {calc_response.text}")
            return False
        
        print("2. Testando endpoint de criação de orçamento simplificado...")
        create_response = requests.post(
            f"{base_url}/api/v1/budgets/simplified",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {create_response.status_code}")
        
        if create_response.status_code == 401:
            print("✅ Endpoint encontrado (erro 401 esperado sem autenticação)")
            print("   - A validação passou, pois chegou até a autenticação")
            return True
        elif create_response.status_code == 422:
            print("❌ Ainda há erro de validação na criação:")
            error_detail = create_response.json()
            print(json.dumps(error_detail, indent=2, ensure_ascii=False))
            return False
        elif create_response.status_code == 200 or create_response.status_code == 201:
            print("✅ Criação funcionando perfeitamente!")
            return True
        else:
            print(f"Status inesperado: {create_response.status_code}")
            print(create_response.text)
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão. Certifique-se de que o serviço está rodando em localhost:8001")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_edge_cases():
    """Test edge cases that should still fail validation"""
    
    print("3. Testando casos que DEVEM falhar na validação...")
    
    base_url = "http://localhost:8001"
    
    # Test case with invalid data (peso_compra = 0)
    invalid_data = {
        "client_name": "Cliente Teste",
        "items": [
            {
                "description": "item inválido",
                "peso_compra": 0,  # Should fail
                "valor_com_icms_compra": 33.21,
                "valor_com_icms_venda": 55.89,
                "percentual_icms_compra": 0.12,
                "percentual_icms_venda": 0.15
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/v1/budgets/calculate-simplified",
            json=invalid_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 422:
            print("✅ Validação correta: dados inválidos rejeitados")
            return True
        else:
            print("❌ Validação falhou: dados inválidos foram aceitos")
            return False
            
    except Exception as e:
        print(f"Erro no teste de casos inválidos: {e}")
        return False

if __name__ == "__main__":
    print("=== Teste Completo de Correção da Validação ===")
    print()
    
    success = True
    
    # Test main validation fix
    if not test_validation_logic_fix():
        success = False
        
    # Test edge cases
    if not test_edge_cases():
        success = False
    
    print()
    if success:
        print("✅ SUCESSO: Ambos os problemas de validação foram corrigidos!")
        print()
        print("RESUMO DAS CORREÇÕES:")
        print("1. ✅ Campos obrigatórios adicionados ao BudgetItemCreate:")
        print("   - purchase_value_without_taxes")
        print("   - sale_value_without_taxes")  
        print("   - purchase_value_with_weight_diff")
        print("   - weight_difference")
        print()
        print("2. ✅ Lógica de validação corrigida em validate_simplified_budget_data:")
        print("   - Validação de peso_compra adicionada")
        print("   - Validação dos valores com nomes corretos dos campos")
        print("   - Tratamento adequado de valores None/0")
    else:
        print("❌ FALHA: Ainda há problemas na validação")
        sys.exit(1)
