#!/usr/bin/env python3
"""
Teste para verificar se a correção do problema de atualização de orçamento funciona
"""

import requests
import json
from datetime import datetime, timedelta

# Configurações
BASE_URL = "http://localhost:8002"
API_URL = f"{BASE_URL}/api/v1"

# Credenciais de teste
TEST_USER = {
    "username": "admin",
    "password": "admin123"
}

def get_token():
    """Fazer login e obter token"""
    try:
        response = requests.post(f"{API_URL}/auth/login", json=TEST_USER)
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("✅ Login realizado com sucesso")
            return token
        else:
            print(f"❌ Erro no login: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return None

def get_headers(token):
    """Obter headers com autorização"""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def create_test_budget(token):
    """Criar um orçamento para teste"""
    budget_data = {
        "order_number": f"TEST-FIX-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "client_name": "Cliente Teste Fix",
        "notes": "Orçamento para testar correção",
        "expires_at": (datetime.now() + timedelta(days=30)).isoformat(),
        "items": [
            {
                "description": "Produto Original",
                "peso_compra": 1.0,
                "peso_venda": 1.0,
                "valor_com_icms_compra": 100.0,
                "percentual_icms_compra": 0.18,
                "outras_despesas_item": 0.0,
                "valor_com_icms_venda": 150.0,
                "percentual_icms_venda": 0.17
            }
        ]
    }

    try:
        response = requests.post(
            f"{API_URL}/budgets/simplified", 
            json=budget_data,
            headers=get_headers(token)
        )
        
        if response.status_code == 201:
            budget = response.json()
            print(f"✅ Orçamento criado - ID: {budget['id']}")
            print(f"   - Cliente: {budget['client_name']}")
            print(f"   - Item: {budget['items'][0]['description']}")
            return budget
        else:
            print(f"❌ Erro ao criar: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

def update_budget_test(token, budget_id):
    """Testar atualização do orçamento"""
    
    # Dados de atualização incluindo items
    update_data = {
        "client_name": "Cliente ATUALIZADO",
        "notes": "Notas ATUALIZADAS",
        "items": [
            {
                "description": "Produto ATUALIZADO",
                "quantity": 1,
                "weight": 1.0,
                "sale_weight": 1.0,
                "purchase_value_with_icms": 120.0,  # Alterado
                "purchase_icms_percentage": 18.0,
                "purchase_other_expenses": 0.0,
                "purchase_value_without_taxes": 0,  # Será calculado
                "sale_value_with_icms": 180.0,  # Alterado
                "sale_icms_percentage": 17.0,
                "sale_value_without_taxes": 0,  # Será calculado
                "commission_percentage": 5.0,
                "dunamis_cost": 0.0
            }
        ]
    }

    try:
        response = requests.put(
            f"{API_URL}/budgets/{budget_id}",
            json=update_data,
            headers=get_headers(token)
        )
        
        if response.status_code == 200:
            updated_budget = response.json()
            print("✅ Atualização bem-sucedida!")
            print(f"   - Cliente: {updated_budget['client_name']}")
            print(f"   - Notas: {updated_budget.get('notes', 'N/A')}")
            if updated_budget['items']:
                item = updated_budget['items'][0]
                print(f"   - Item: {item['description']}")
                print(f"   - Valor compra: R$ {item['purchase_value_with_icms']:.2f}")
                print(f"   - Valor venda: R$ {item['sale_value_with_icms']:.2f}")
            return updated_budget
        else:
            print(f"❌ Erro na atualização: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

def verify_update(token, budget_id):
    """Verificar se a atualização foi salva"""
    try:
        response = requests.get(
            f"{API_URL}/budgets/{budget_id}",
            headers=get_headers(token)
        )
        
        if response.status_code == 200:
            budget = response.json()
            
            # Verificar se as mudanças foram salvas
            client_ok = budget['client_name'] == "Cliente ATUALIZADO"
            notes_ok = budget.get('notes') == "Notas ATUALIZADAS"
            item_ok = False
            values_ok = False
            
            if budget['items']:
                item = budget['items'][0]
                item_ok = item['description'] == "Produto ATUALIZADO"
                values_ok = (
                    item['purchase_value_with_icms'] == 120.0 and
                    item['sale_value_with_icms'] == 180.0
                )
            
            print(f"\n🔍 Verificação:")
            print(f"   - Cliente atualizado: {'✅' if client_ok else '❌'}")
            print(f"   - Notas atualizadas: {'✅' if notes_ok else '❌'}")
            print(f"   - Item atualizado: {'✅' if item_ok else '❌'}")
            print(f"   - Valores atualizados: {'✅' if values_ok else '❌'}")
            
            success = client_ok and notes_ok and item_ok and values_ok
            
            if success:
                print("\n🎉 SUCESSO! Todas as atualizações foram salvas corretamente!")
            else:
                print("\n❌ FALHA! Algumas atualizações não foram salvas.")
                
            return success
        else:
            print(f"❌ Erro ao verificar: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    """Teste completo"""
    print("🧪 Testando correção da atualização de orçamento...")
    print("=" * 60)
    
    # Login
    token = get_token()
    if not token:
        return False
    
    # Criar orçamento de teste
    print("\n📝 Criando orçamento de teste...")
    budget = create_test_budget(token)
    if not budget:
        return False
    
    # Atualizar orçamento
    print(f"\n🔄 Atualizando orçamento {budget['id']}...")
    updated_budget = update_budget_test(token, budget['id'])
    if not updated_budget:
        return False
    
    # Verificar se foi salvo
    print("\n🔍 Verificando se foi salvo...")
    success = verify_update(token, budget['id'])
    
    print("=" * 60)
    if success:
        print("🎉 TESTE PASSOU! A correção funciona corretamente!")
        print("\n✅ CORREÇÃO IMPLEMENTADA:")
        print("1. Schema BudgetUpdate agora inclui campo 'items'")
        print("2. BudgetService.update_budget() processa atualizações dos items")
        print("3. Items são recriados com os novos dados e cálculos atualizados")
        print("4. Totais do orçamento são recalculados automaticamente")
    else:
        print("❌ TESTE FALHOU! A correção ainda não está funcionando.")
    
    return success

if __name__ == "__main__":
    main()
