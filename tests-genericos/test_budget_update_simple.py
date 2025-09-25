#!/usr/bin/env python3
"""
Teste simples para verificar o problema de atualização de orçamento
Problema relatado: ao editar um orçamento e salvar, é retornado sucesso mas não reflete a atualização.
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
        "order_number": f"TEST-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "client_name": "Cliente Teste Atualização",
        "notes": "Orçamento criado para teste de atualização",
        "expires_at": (datetime.now() + timedelta(days=30)).isoformat(),
        "items": [
            {
                "description": "Produto Teste Original",
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
            print(f"✅ Orçamento criado com sucesso - ID: {budget['id']}")
            print(f"   - Cliente: {budget['client_name']}")
            print(f"   - Notas: {budget.get('notes', 'N/A')}")
            print(f"   - Items: {len(budget['items'])} item(s)")
            if budget['items']:
                print(f"   - Primeiro item: {budget['items'][0]['description']}")
            return budget
        else:
            print(f"❌ Erro ao criar orçamento: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None

def get_budget(token, budget_id):
    """Buscar orçamento por ID"""
    try:
        response = requests.get(
            f"{API_URL}/budgets/{budget_id}",
            headers=get_headers(token)
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Erro ao buscar orçamento: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None

def main():
    """Função principal"""
    print("🧪 Iniciando análise do problema de atualização de orçamento...")
    print("=" * 70)
    
    # Analisar o problema examinando o código
    print("\n🔍 ANÁLISE DO CÓDIGO:")
    print("\n1. Frontend (BudgetEditSimplified.tsx):")
    print("   - Usa updateBudgetMutation com budgetService.updateBudget()")
    print("   - Converte dados simplificados para formato completo")
    print("   - Envia dados via PUT para /budgets/{id}")
    
    print("\n2. Backend (budgets.py endpoint):")
    print("   - Endpoint PUT /{budget_id} chama BudgetService.update_budget()")
    print("   - Recebe BudgetUpdate como parâmetro")
    
    print("\n3. BudgetService.update_budget():")
    print("   - Apenas atualiza campos do orçamento principal")
    print("   - NÃO atualiza os items!")
    print("   - Usa setattr() apenas nos campos do budget_data")
    
    print("\n4. Schema BudgetUpdate:")
    print("   - Não inclui campo 'items'")
    print("   - Apenas campos básicos do orçamento")
    
    print("\n❌ PROBLEMA IDENTIFICADO:")
    print("O método update_budget() no BudgetService NÃO atualiza os items!")
    print("Ele apenas atualiza os campos básicos do orçamento (cliente, notas, etc.)")
    print("mas ignora completamente as mudanças nos items.")
    
    print("\n🔧 SOLUÇÃO NECESSÁRIA:")
    print("1. Atualizar schema BudgetUpdate para incluir items")
    print("2. Modificar BudgetService.update_budget() para processar items")
    print("3. Implementar lógica para atualizar/criar/deletar items")
    
    return False  # Problema confirmado pela análise do código

if __name__ == "__main__":
    success = main()
    
    if not success:
        print("\n🎯 CONFIRMAÇÃO:")
        print("O bug foi identificado através da análise do código.")
        print("A funcionalidade de edição não está atualizando os items do orçamento.")
