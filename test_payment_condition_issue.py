#!/usr/bin/env python3
"""
Teste para reproduzir o problema da condição de pagamento não sendo exibida corretamente.
"""

import requests
import json

def test_payment_condition_issue():
    """
    Testa a criação de um orçamento com payment_condition e verifica se é retornado corretamente
    """
    print("=== TESTE: PROBLEMA DA CONDIÇÃO DE PAGAMENTO ===")
    print()
    
    base_url = "http://localhost:8002"
    
    # Dados do orçamento conforme fornecido pelo usuário
    budget_data = {
        "order_number": "PED-0066",
        "client_name": "Cliente Teste",
        "status": "draft",
        "payment_condition": "28/35/42",
        "freight_type": "FOB",
        "items": [
            {
                "description": "item",
                "delivery_time": "0",
                "peso_compra": 100,
                "peso_venda": 100,
                "valor_com_icms_compra": 1.12,
                "percentual_icms_compra": 0.18,
                "outras_despesas_item": 0,
                "valor_com_icms_venda": 3.12,
                "percentual_icms_venda": 0.18,
                "percentual_ipi": 0
            }
        ]
    }
    
    try:
        # 1. Criar orçamento
        print("1. Criando orçamento com payment_condition='28/35/42'...")
        print(f"   Dados enviados: {json.dumps(budget_data, indent=2)}")
        
        response = requests.post(
            f"{base_url}/api/v1/budgets/simplified",
            json=budget_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   Status da resposta: {response.status_code}")
        
        if response.status_code == 201:
            created_budget = response.json()
            budget_id = created_budget.get('id')
            print(f"✅ Orçamento criado com ID: {budget_id}")
            print(f"   Payment condition retornado: {repr(created_budget.get('payment_condition'))}")
            
            # 2. Buscar orçamento por ID (simula o que BudgetView faz)
            print()
            print("2. Buscando orçamento por ID (simulando BudgetView)...")
            
            response = requests.get(f"{base_url}/api/v1/budgets/{budget_id}")
            
            if response.status_code == 200:
                retrieved_budget = response.json()
                print(f"✅ Orçamento recuperado")
                print(f"   Payment condition: {repr(retrieved_budget.get('payment_condition'))}")
                print(f"   Freight type: {repr(retrieved_budget.get('freight_type'))}")
                print(f"   Client name: {repr(retrieved_budget.get('client_name'))}")
                
                # Verificar se payment_condition está presente e correto
                if retrieved_budget.get('payment_condition') == '28/35/42':
                    print("✅ Payment condition está correto!")
                elif retrieved_budget.get('payment_condition') is None:
                    print("❌ Payment condition está NULL/None")
                else:
                    print(f"❌ Payment condition incorreto: {repr(retrieved_budget.get('payment_condition'))}")
                    
            else:
                print(f"❌ Erro ao buscar orçamento: {response.status_code}")
                print(f"   Resposta: {response.text}")
                
        else:
            print(f"❌ Erro ao criar orçamento: {response.status_code}")
            print(f"   Resposta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão. Verifique se o servidor está rodando em http://localhost:8002")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    test_payment_condition_issue()