#!/usr/bin/env python3
"""
Script para testar o endpoint de salvamento de orçamento e reproduzir erros
"""
import requests
import json
from datetime import datetime, timedelta
import sys

# Configurações
BASE_URL = "http://localhost:8002"  # URL do serviço de orçamentos
USER_SERVICE_URL = "http://localhost:8001"  # URL do serviço de usuários

def get_auth_token():
    """Obter token de autenticação"""
    try:
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        print("🔐 Fazendo login para obter token...")
        response = requests.post(f"{USER_SERVICE_URL}/api/v1/users/login", json=login_data)
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get("access_token")
            print(f"✅ Token obtido com sucesso")
            return token
        else:
            print(f"❌ Erro ao fazer login: {response.status_code}")
            print(f"Resposta: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erro na requisição de login: {e}")
        return None

def test_create_complete_budget(token):
    """Testar criação de orçamento completo"""
    print("\n📋 Testando criação de orçamento completo...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Dados do orçamento completo
    budget_data = {
        "order_number": f"TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "client_name": "Cliente Teste",
        "markup_percentage": 25.0,
        "notes": "Orçamento de teste para reprodução de erro",
        "expires_at": (datetime.now() + timedelta(days=30)).isoformat(),
        "items": [
            {
                "description": "Item Teste 1",
                "weight": 10.5,
                "purchase_icms_percentage": 0.17,
                "purchase_other_expenses": 0.0,
                "purchase_value_without_taxes": 100.0,
                "purchase_value_with_weight_diff": 105.0,
                "sale_weight": 10.8,
                "sale_icms_percentage": 0.17,
                "sale_value_without_taxes": 130.0,
                "weight_difference": 0.3,
                "commission_percentage": 0.015,
                "dunamis_cost": 120.0,
                "profitability": 25.0,
                "total_purchase": 105.0,
                "total_sale": 140.4,
                "unit_value": 13.0,
                "total_value": 140.4,
                "commission_value": 2.1
            },
            {
                "description": "Item Teste 2",
                "weight": 5.2,
                "purchase_icms_percentage": 0.17,
                "purchase_other_expenses": 2.5,
                "purchase_value_without_taxes": 50.0,
                "purchase_value_with_weight_diff": 52.6,
                "sale_weight": 5.3,
                "sale_icms_percentage": 0.17,
                "sale_value_without_taxes": 65.0,
                "weight_difference": 0.1,
                "commission_percentage": 0.015,
                "dunamis_cost": 62.8,
                "profitability": 20.0,
                "total_purchase": 55.1,
                "total_sale": 70.89,
                "unit_value": 13.38,
                "total_value": 70.89,
                "commission_value": 1.06
            }
        ]
    }
    
    try:
        print(f"Enviando requisição para: {BASE_URL}/api/v1/budgets/")
        print(f"Dados: {json.dumps(budget_data, indent=2, default=str)}")
        
        response = requests.post(
            f"{BASE_URL}/api/v1/budgets/",
            headers=headers,
            json=budget_data
        )
        
        print(f"\n📊 Status da resposta: {response.status_code}")
        print(f"📄 Headers da resposta: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            print(f"📄 Conteúdo da resposta (JSON):")
            print(json.dumps(response_json, indent=2, default=str))
        except:
            print(f"📄 Conteúdo da resposta (texto):")
            print(f"'{response.text}'")
        
        if response.status_code == 201:
            print("✅ Orçamento criado com sucesso!")
            return response.json()
        else:
            print("❌ Erro ao criar orçamento")
            return None
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None

def test_create_simplified_budget(token):
    """Testar criação de orçamento simplificado"""
    print("\n📋 Testando criação de orçamento simplificado...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Dados do orçamento simplificado
    budget_data = {
        "client_name": "Cliente Teste Simplificado",
        "notes": "Teste de orçamento simplificado",
        "expires_at": (datetime.now() + timedelta(days=30)).isoformat(),
        "items": [
            {
                "description": "Item Simples 1",
                "peso_compra": 10.5,
                "valor_com_icms_compra": 150.0,
                "percentual_icms_compra": 0.17,
                "outras_despesas_item": 0.0,
                "peso_venda": 10.8,
                "valor_com_icms_venda": 200.0,
                "percentual_icms_venda": 0.17
            },
            {
                "description": "Item Simples 2", 
                "peso_compra": 5.2,
                "valor_com_icms_compra": 80.0,
                "percentual_icms_compra": 0.17,
                "outras_despesas_item": 2.5,
                "peso_venda": 5.3,
                "valor_com_icms_venda": 110.0,
                "percentual_icms_venda": 0.17
            }
        ]
    }
    
    try:
        print(f"Enviando requisição para: {BASE_URL}/api/v1/budgets/simplified")
        print(f"Dados: {json.dumps(budget_data, indent=2, default=str)}")
        
        response = requests.post(
            f"{BASE_URL}/api/v1/budgets/simplified",
            headers=headers,
            json=budget_data
        )
        
        print(f"\n📊 Status da resposta: {response.status_code}")
        print(f"📄 Headers da resposta: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            print(f"📄 Conteúdo da resposta (JSON):")
            print(json.dumps(response_json, indent=2, default=str))
        except:
            print(f"📄 Conteúdo da resposta (texto):")
            print(f"'{response.text}'")
        
        if response.status_code == 201:
            print("✅ Orçamento simplificado criado com sucesso!")
            return response.json()
        else:
            print("❌ Erro ao criar orçamento simplificado")
            return None
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None

def test_calculate_preview(token):
    """Testar cálculo de preview do orçamento"""
    print("\n📋 Testando cálculo de preview...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Dados para cálculo
    budget_data = {
        "order_number": "PREVIEW-TEST",
        "client_name": "Cliente Preview",
        "markup_percentage": 30.0,
        "items": [
            {
                "description": "Preview Item",
                "weight": 8.0,
                "purchase_icms_percentage": 0.17,
                "purchase_other_expenses": 1.0,
                "purchase_value_without_taxes": 80.0,
                "sale_icms_percentage": 0.17,
                "sale_value_without_taxes": 110.0,
                "commission_percentage": 0.015
            }
        ]
    }
    
    try:
        print(f"Enviando requisição para: {BASE_URL}/api/v1/budgets/calculate")
        print(f"Dados: {json.dumps(budget_data, indent=2, default=str)}")
        
        response = requests.post(
            f"{BASE_URL}/api/v1/budgets/calculate",
            headers=headers,
            json=budget_data
        )
        
        print(f"\n📊 Status da resposta: {response.status_code}")
        print(f"📄 Headers da resposta: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            print(f"📄 Conteúdo da resposta (JSON):")
            print(json.dumps(response_json, indent=2, default=str))
        except:
            print(f"📄 Conteúdo da resposta (texto):")
            print(f"'{response.text}'")
        
        if response.status_code == 200:
            print("✅ Cálculo realizado com sucesso!")
            return response.json()
        else:
            print("❌ Erro no cálculo")
            return None
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None

def test_health_check():
    """Verificar se os serviços estão funcionando"""
    print("🏥 Verificando saúde dos serviços...")
    
    services = [
        ("Budget Service", f"{BASE_URL}/api/v1/budgets/markup-settings"),
        ("User Service", f"{USER_SERVICE_URL}/api/v1/auth/health" if "health" in USER_SERVICE_URL else f"{USER_SERVICE_URL}/docs")
    ]
    
    for service_name, url in services:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code in [200, 404]:  # 404 pode ser esperado para algumas rotas
                print(f"✅ {service_name}: OK (Status: {response.status_code})")
            else:
                print(f"⚠️ {service_name}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {service_name}: Erro - {e}")

def main():
    """Função principal"""
    print("🧪 TESTE DO ENDPOINT DE ORÇAMENTOS")
    print("=" * 50)
    
    # Verificar saúde dos serviços
    test_health_check()
    
    # Obter token de autenticação
    token = get_auth_token()
    if not token:
        print("❌ Não foi possível obter token. Verifique se o serviço de usuários está rodando.")
        return
    
    # Executar testes
    print("\n🚀 Iniciando testes dos endpoints...")
    
    # Teste 1: Cálculo de preview
    preview_result = test_calculate_preview(token)
    
    # Teste 2: Orçamento simplificado
    simplified_result = test_create_simplified_budget(token)
    
    # Teste 3: Orçamento completo
    complete_result = test_create_complete_budget(token)
    
    # Resumo dos resultados
    print("\n" + "=" * 50)
    print("📋 RESUMO DOS TESTES:")
    print(f"Preview de cálculo: {'✅ OK' if preview_result else '❌ FALHOU'}")
    print(f"Orçamento simplificado: {'✅ OK' if simplified_result else '❌ FALHOU'}")
    print(f"Orçamento completo: {'✅ OK' if complete_result else '❌ FALHOU'}")
    
    if not any([preview_result, simplified_result, complete_result]):
        print("\n❌ TODOS OS TESTES FALHARAM - Verifique os logs acima para detalhes do erro")
        sys.exit(1)
    else:
        print("\n✅ Pelo menos um teste passou!")

if __name__ == "__main__":
    main()
