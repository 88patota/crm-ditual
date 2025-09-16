#!/usr/bin/env python3
"""
Teste para reproduzir exatamente o cenário reportado pelo usuário
"""

import sys
import os
import json
import requests

# Adicionar o caminho do serviço de orçamentos
sys.path.append('/Users/erikpatekoski/dev/crm-ditual/services/budget_service')

def test_exact_user_scenario():
    """
    Teste com cenário exato reportado pelo usuário.
    
    Possível causa: O usuário pode estar usando um endpoint diferente,
    ou os dados podem estar chegando de uma forma diferente.
    """
    
    print("=== TESTE CENÁRIO EXATO DO USUÁRIO ===")
    print()
    
    # Vamos testar diferentes endpoints e formatos de dados
    endpoints_to_test = [
        "/api/v1/budgets/calculate-simplified",
        "/api/v1/budgets/calculate",  # Se existir
        "/api/v1/budgets/simplified",  # Create endpoint
    ]
    
    # Dados exatos do usuário com diferentes formatos
    test_scenarios = [
        {
            "name": "Formato Decimal (0.18)",
            "data": {
                "client_name": "Cliente Teste ICMS",
                "items": [{
                    "description": "Item teste usuário",
                    "peso_compra": 1000,
                    "peso_venda": 1050,  
                    "valor_com_icms_compra": 6.0,
                    "percentual_icms_compra": 0.06,  # 6% em decimal
                    "outras_despesas_item": 0.0,
                    "valor_com_icms_venda": 7.0,
                    "percentual_icms_venda": 0.07    # 7% em decimal
                }]
            }
        },
        {
            "name": "Formato Percentual (6.0, 7.0)",  
            "data": {
                "client_name": "Cliente Teste ICMS",
                "items": [{
                    "description": "Item teste usuário",
                    "peso_compra": 1000,
                    "peso_venda": 1050,  
                    "valor_com_icms_compra": 6.0,
                    "percentual_icms_compra": 6.0,  # 6% como percentual
                    "outras_despesas_item": 0.0,
                    "valor_com_icms_venda": 7.0,
                    "percentual_icms_venda": 7.0     # 7% como percentual
                }]
            }
        },
        {
            "name": "Formato Inglês (schema antigo)",
            "data": {
                "client_name": "Cliente Teste ICMS",
                "items": [{
                    "description": "Item teste usuário",
                    "weight": 1000,
                    "sale_weight": 1050,  
                    "purchase_value_with_icms": 6.0,
                    "purchase_icms_percentage": 6.0,  # 6%
                    "purchase_other_expenses": 0.0,
                    "sale_value_with_icms": 7.0,
                    "sale_icms_percentage": 7.0       # 7%
                }]
            }
        }
    ]
    
    base_url = "http://localhost:8002"
    headers = {"Content-Type": "application/json"}
    
    for scenario in test_scenarios:
        print(f"--- TESTANDO {scenario['name']} ---")
        
        for endpoint in endpoints_to_test:
            url = f"{base_url}{endpoint}"
            
            try:
                print(f"Endpoint: {endpoint}")
                response = requests.post(url, json=scenario['data'], headers=headers, timeout=10)
                
                print(f"Status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Analisar resultado para ver se ICMS está correto
                    if 'items_calculations' in result and result['items_calculations']:
                        item = result['items_calculations'][0]
                        
                        print(f"✅ Sucesso - Total venda: R$ {item.get('total_sale', 0):.2f}")
                        
                        # Calcular manualmente o esperado com ICMS 6% e 7%
                        if scenario['name'] == "Formato Decimal (0.18)":
                            # 6% e 7% em decimal
                            expected_compra = 6.0 * (1 - 0.06) * (1 - 0.0925) * 1000
                            expected_venda = 7.0 * (1 - 0.07) * (1 - 0.0925) * 1050
                        elif scenario['name'] == "Formato Percentual (6.0, 7.0)":
                            # 6% e 7% como percentual (pode estar sendo tratado errado)
                            # Se o sistema interpretar como decimal, ficaria 600% e 700%
                            expected_compra = 6.0 * (1 - 0.06) * (1 - 0.0925) * 1000
                            expected_venda = 7.0 * (1 - 0.07) * (1 - 0.0925) * 1050
                        else:
                            expected_compra = 6.0 * (1 - 0.06) * (1 - 0.0925) * 1000
                            expected_venda = 7.0 * (1 - 0.07) * (1 - 0.0925) * 1050
                        
                        actual_compra = item.get('total_purchase', 0)
                        actual_venda = item.get('total_sale', 0)
                        
                        print(f"   Compra: esperado R$ {expected_compra:.2f}, atual R$ {actual_compra:.2f}")
                        print(f"   Venda: esperado R$ {expected_venda:.2f}, atual R$ {actual_venda:.2f}")
                        
                        # Verificar se está usando 18% no lugar
                        expected_18_compra = 6.0 * (1 - 0.18) * (1 - 0.0925) * 1000
                        expected_18_venda = 7.0 * (1 - 0.18) * (1 - 0.0925) * 1050
                        
                        if (abs(actual_compra - expected_18_compra) < 0.01 and 
                            abs(actual_venda - expected_18_venda) < 0.01):
                            print("   🚨 PROBLEMA: Sistema está usando 18% ao invés dos valores corretos!")
                        elif (abs(actual_compra - expected_compra) < 0.01 and 
                              abs(actual_venda - expected_venda) < 0.01):
                            print("   ✅ Correto: ICMS sendo usado corretamente")
                        else:
                            print("   ❓ Valores inesperados")
                        
                elif response.status_code == 404:
                    print("   (Endpoint não existe)")
                elif response.status_code == 422:
                    print("   ❌ Erro de validação (dados inválidos)")
                    try:
                        error_detail = response.json()
                        print(f"   Detalhes: {error_detail.get('detail', 'N/A')}")
                    except:
                        pass
                else:
                    print(f"   ❌ Erro {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                print("   ❌ Serviço não está rodando")
                break
            except requests.exceptions.Timeout:
                print("   ❌ Timeout")
            except Exception as e:
                print(f"   ❌ Erro: {e}")
                
            print()
        print()

def test_frontend_backend_integration():
    """
    Teste para verificar se o problema pode estar na integração frontend->backend
    """
    print("=== TESTE INTEGRAÇÃO FRONTEND->BACKEND ===")
    
    # Simular dados como se viessem do frontend
    # O frontend pode estar enviando em formato diferente
    frontend_data = {
        "client_name": "Cliente Frontend",
        "items": [{
            "description": "Item do frontend",
            "peso_compra": 1000,
            "peso_venda": 1050,  
            "valor_com_icms_compra": 6.0,
            "percentual_icms_compra": 0.06,  # Frontend envia em decimal
            "outras_despesas_item": 0.0,
            "valor_com_icms_venda": 7.0,
            "percentual_icms_venda": 0.07    # Frontend envia em decimal
        }],
        "notes": "Teste integração"
    }
    
    print(f"Dados simulando frontend:")
    print(json.dumps(frontend_data, indent=2))
    
    # Importar diretamente os módulos para teste local
    try:
        from app.schemas.budget import BudgetSimplifiedCreate
        from app.services.business_rules_calculator import BusinessRulesCalculator
        
        print("\n1. Testando validação do schema...")
        budget_simplified = BudgetSimplifiedCreate(**frontend_data)
        print("✅ Schema válido")
        
        print("\n2. Convertendo para dict...")
        items_data = [item.dict() for item in budget_simplified.items]
        print(f"Item data: {items_data[0]}")
        
        print("\n3. Calculando com BusinessRulesCalculator...")
        outras_despesas_totais = 0.0
        soma_pesos_pedido = 1000
        
        resultado = BusinessRulesCalculator.calculate_complete_item(
            items_data[0], outras_despesas_totais, soma_pesos_pedido
        )
        
        print(f"✅ Cálculo concluído")
        print(f"ICMS compra usado: {resultado['percentual_icms_compra']*100:.0f}%")
        print(f"ICMS venda usado: {resultado['percentual_icms_venda']*100:.0f}%")
        print(f"Total compra: R$ {resultado['total_compra_item']:.2f}")
        print(f"Total venda: R$ {resultado['total_venda_item']:.2f}")
        
        # Verificar se está usando os valores corretos
        if (resultado['percentual_icms_compra'] == 0.06 and 
            resultado['percentual_icms_venda'] == 0.07):
            print("✅ ICMS correto sendo usado no cálculo")
        else:
            print(f"❌ PROBLEMA: ICMS incorreto - esperado 6%/7%, atual {resultado['percentual_icms_compra']*100:.0f}%/{resultado['percentual_icms_venda']*100:.0f}%")
        
    except Exception as e:
        print(f"❌ Erro no teste local: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_exact_user_scenario()
    test_frontend_backend_integration()