#!/usr/bin/env python3
"""
Script para testar a correção do campo weight_difference_display
"""

import requests
import json

# Configuração
BASE_URL = "http://localhost:8002/api/v1"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTc2MTI2ODM1Mn0.1u-95X6IwyzGuJvXQqsXzKZzqmFZtsuy3OTptoR0a8M"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def test_weight_difference_display():
    print("🚀 Iniciando testes de correção do weight_difference_display")
    
    # Teste 1: Item com diferença de peso
    print("\n🧪 Testando correção do campo weight_difference_display...")
    
    budget_data = {
        "order_number": "TEST-WEIGHT-DIFF-001",
        "client_name": "Cliente Teste",
        "items": [
            {
                "description": "Item com diferença de peso",
                "peso_compra": 10.0,
                "peso_venda": 12.0,
                "valor_com_icms_compra": 100.0,
                "percentual_icms_compra": 0.17,
                "outras_despesas_item": 0.0,
                "valor_com_icms_venda": 150.0,
                "percentual_icms_venda": 0.17,
                "percentual_ipi": 0.0,
                "delivery_time": "5"
            }
        ]
    }
    
    print("📝 Criando orçamento com diferença de peso...")
    response = requests.post(f"{BASE_URL}/budgets/simplified", json=budget_data, headers=headers)
    
    if response.status_code == 201:
        budget = response.json()
        budget_id = budget["id"]
        print(f"✅ Orçamento criado com ID: {budget_id}")
        
        # Debug: Imprimir dados do orçamento criado
        print(f"🔍 DEBUG - Dados do orçamento criado:")
        print(f"   - Items count: {len(budget.get('items', []))}")
        if budget.get('items'):
            item = budget['items'][0]
            print(f"   - Item weight_difference_display: {item.get('weight_difference_display')}")
            print(f"   - Item weight_difference: {item.get('weight_difference')}")
            print(f"   - Item peso_compra: {item.get('weight')}")
            print(f"   - Item peso_venda: {item.get('sale_weight')}")
        
        print("🔍 Buscando orçamento para verificar weight_difference_display...")
        get_response = requests.get(f"{BASE_URL}/budgets/{budget_id}", headers=headers)
        
        if get_response.status_code == 200:
            budget_details = get_response.json()
            item = budget_details["items"][0]
            
            print("📊 Dados do item:")
            print(f"   - Peso compra: {item.get('weight')} kg")
            print(f"   - Peso venda: {item.get('sale_weight')} kg")
            print(f"   - Diferença peso: {item.get('weight_difference')} kg")
            print(f"   - Weight difference display: {item.get('weight_difference_display')}")
            
            # Debug adicional
            print(f"🔍 DEBUG - Todos os campos do item:")
            for key, value in item.items():
                if 'weight' in key.lower() or 'difference' in key.lower():
                    print(f"   - {key}: {value}")
            
            weight_diff_display = item.get('weight_difference_display')
            if weight_diff_display and weight_diff_display.get('has_difference'):
                print("✅ Campo weight_difference_display encontrado e correto!")
                test1_passed = True
            else:
                print("❌ Campo weight_difference_display não encontrado ou é None")
                test1_passed = False
        else:
            print(f"❌ Erro ao buscar orçamento: {get_response.status_code}")
            test1_passed = False
            
        # Limpar teste
        requests.delete(f"{BASE_URL}/budgets/{budget_id}", headers=headers)
    else:
        print(f"❌ Erro ao criar orçamento: {response.status_code}")
        print(f"Response: {response.text}")
        test1_passed = False
    
    # Teste 2: Item sem diferença de peso
    print("\n🧪 Testando item sem diferença de peso...")
    
    budget_data_no_diff = {
        "order_number": "TEST-NO-DIFF-001",
        "client_name": "Cliente Teste",
        "items": [
            {
                "description": "Item sem diferença de peso",
                "peso_compra": 10.0,
                "peso_venda": 10.0,
                "valor_com_icms_compra": 100.0,
                "percentual_icms_compra": 0.17,
                "outras_despesas_item": 0.0,
                "valor_com_icms_venda": 150.0,
                "percentual_icms_venda": 0.17,
                "percentual_ipi": 0.0,
                "delivery_time": "5"
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/budgets/simplified", json=budget_data_no_diff, headers=headers)
    
    if response.status_code == 201:
        budget = response.json()
        budget_id = budget["id"]
        
        get_response = requests.get(f"{BASE_URL}/budgets/{budget_id}", headers=headers)
        
        if get_response.status_code == 200:
            budget_details = get_response.json()
            item = budget_details["items"][0]
            
            print("📊 Item sem diferença:")
            print(f"   - Weight difference display: {item.get('weight_difference_display')}")
            
            weight_diff_display = item.get('weight_difference_display')
            if weight_diff_display is None or (weight_diff_display and not weight_diff_display.get('has_difference')):
                print("✅ Item sem diferença de peso está correto!")
                test2_passed = True
            else:
                print("❌ Item sem diferença de peso deveria ter weight_difference_display None ou has_difference=False")
                test2_passed = False
        else:
            print(f"❌ Erro ao buscar orçamento: {get_response.status_code}")
            test2_passed = False
            
        # Limpar teste
        requests.delete(f"{BASE_URL}/budgets/{budget_id}", headers=headers)
    else:
        print(f"❌ Erro ao criar orçamento: {response.status_code}")
        test2_passed = False
    
    # Resumo
    print("\n📋 Resumo dos testes:")
    print(f"   - Teste com diferença de peso: {'✅ PASSOU' if test1_passed else '❌ FALHOU'}")
    print(f"   - Teste sem diferença de peso: {'✅ PASSOU' if test2_passed else '❌ FALHOU'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 Todos os testes passaram! A correção está funcionando.")
    else:
        print("\n⚠️  Alguns testes falharam. Verifique os logs acima.")

if __name__ == "__main__":
    test_weight_difference_display()