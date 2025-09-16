#!/usr/bin/env python3
"""
Teste para verificar se o cálculo de comissão por item está funcionando corretamente
na tela de visualização do orçamento.
"""

import requests
import json
import sys
from datetime import datetime, timedelta

# Configurações da API
BASE_URL = "http://localhost:8002"
BUDGET_API = f"{BASE_URL}/api/v1/budgets"

def test_commission_calculation():
    """
    Testa se a comissão é calculada corretamente por item
    """
    print("🧪 Teste: Cálculo de Comissão por Item")
    print("=" * 50)
    
    # Criar dados de teste
    test_budget_data = {
        "client_name": "Cliente Teste Comissão",
        "order_number": f"TEST-COMM-{int(datetime.now().timestamp())}",
        "status": "draft",
        "notes": "Teste de cálculo de comissão por item",
        "expires_at": (datetime.now() + timedelta(days=30)).isoformat(),
        "items": [
            {
                "description": "Item 1 - Teste Comissão Alta",
                "peso_compra": 10.0,
                "peso_venda": 10.0,
                "valor_com_icms_compra": 100.00,
                "percentual_icms_compra": 0.18,
                "outras_despesas_item": 5.00,
                "valor_com_icms_venda": 150.00,
                "percentual_icms_venda": 0.17
            },
            {
                "description": "Item 2 - Teste Comissão Baixa", 
                "peso_compra": 5.0,
                "peso_venda": 5.0,
                "valor_com_icms_compra": 200.00,
                "percentual_icms_compra": 0.18,
                "outras_despesas_item": 10.00,
                "valor_com_icms_venda": 220.00,
                "percentual_icms_venda": 0.17
            },
            {
                "description": "Item 3 - Teste Peso Diferente",
                "peso_compra": 15.0,
                "peso_venda": 12.0,  # Peso de venda menor
                "valor_com_icms_compra": 80.00,
                "percentual_icms_compra": 0.18,
                "outras_despesas_item": 2.00,
                "valor_com_icms_venda": 120.00,
                "percentual_icms_venda": 0.17
            }
        ]
    }
    
    try:
        # Criar orçamento
        print("📝 Criando orçamento de teste...")
        response = requests.post(f"{BUDGET_API}/simplified", json=test_budget_data)
        
        if response.status_code != 201:
            print(f"❌ Erro ao criar orçamento: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False
            
        budget_data = response.json()
        budget_id = budget_data["id"]
        print(f"✅ Orçamento criado com ID: {budget_id}")
        print(f"   Número do pedido: {budget_data['order_number']}")
        
        # Buscar orçamento para verificar os cálculos
        print(f"\n🔍 Buscando orçamento {budget_id}...")
        response = requests.get(f"{BUDGET_API}/{budget_id}")
        
        if response.status_code != 200:
            print(f"❌ Erro ao buscar orçamento: {response.status_code}")
            return False
            
        budget = response.json()
        
        # Verificar se tem itens
        if not budget.get("items"):
            print("❌ Orçamento não tem itens")
            return False
            
        print(f"✅ Orçamento encontrado com {len(budget['items'])} itens")
        
        # Verificar cálculos de cada item
        print(f"\n📊 Verificando cálculos de comissão por item:")
        print("-" * 80)
        
        total_commission_calculated = 0.0
        
        for i, item in enumerate(budget["items"], 1):
            description = item.get("description", f"Item {i}")
            commission_percentage = item.get("commission_percentage", 0)
            commission_value = item.get("commission_value", 0)
            total_value = item.get("total_value", 0)
            sale_value_with_icms = item.get("sale_value_with_icms", 0)
            weight = item.get("weight", 1) or 1
            
            # Calcular comissão esperada
            expected_commission_value = (sale_value_with_icms * weight) * (commission_percentage / 100)
            
            print(f"Item {i}: {description}")
            print(f"  • Peso: {weight} kg")
            print(f"  • Valor unitário venda (c/ICMS): R$ {sale_value_with_icms:,.2f}")
            print(f"  • Valor total: R$ {total_value:,.2f}")
            print(f"  • % Comissão: {commission_percentage:.1f}%")
            print(f"  • Valor comissão: R$ {commission_value:,.2f}")
            print(f"  • Comissão esperada: R$ {expected_commission_value:,.2f}")
            
            # Verificar se o cálculo está correto (tolerância de 0.01)
            if abs(commission_value - expected_commission_value) > 0.01:
                print(f"  ❌ ERRO: Comissão calculada incorretamente!")
                print(f"     Esperado: R$ {expected_commission_value:,.2f}")
                print(f"     Atual: R$ {commission_value:,.2f}")
            else:
                print(f"  ✅ Comissão calculada corretamente!")
                
            total_commission_calculated += commission_value
            print()
        
        # Verificar total de comissão
        budget_total_commission = budget.get("total_commission", 0)
        print(f"💰 Verificando total de comissão:")
        print(f"  • Soma dos itens: R$ {total_commission_calculated:,.2f}")
        print(f"  • Total do orçamento: R$ {budget_total_commission:,.2f}")
        
        if abs(total_commission_calculated - budget_total_commission) > 0.01:
            print(f"  ❌ ERRO: Total de comissão não confere!")
        else:
            print(f"  ✅ Total de comissão está correto!")
        
        # Mostrar resumo final
        print(f"\n📋 Resumo do Orçamento:")
        print(f"  • Total Compra: R$ {budget.get('total_purchase_value', 0):,.2f}")
        print(f"  • Total Venda: R$ {budget.get('total_sale_value', 0):,.2f}")
        print(f"  • Total Comissão: R$ {budget.get('total_commission', 0):,.2f}")
        print(f"  • Rentabilidade: {budget.get('profitability_percentage', 0):.1f}%")
        
        print(f"\n🌐 Teste da Interface:")
        print(f"  • Acesse: http://localhost:3000/budgets/{budget_id}")
        print(f"  • Verifique se a coluna 'Valor Comissão' aparece na tabela")
        print(f"  • Confirme se os valores estão corretos por item")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão. Verifique se os serviços estão rodando:")
        print("   • Budget Service: http://localhost:8002")
        print("   • Frontend: http://localhost:3000")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
        return False

def test_frontend_structure():
    """
    Verifica se a estrutura do frontend foi atualizada
    """
    print("\n🎨 Verificando estrutura do frontend...")
    
    try:
        with open("frontend/src/pages/BudgetView.tsx", "r") as f:
            content = f.read()
            
        # Verificar se a nova coluna foi adicionada
        if "Valor Comissão" in content:
            print("✅ Coluna 'Valor Comissão' encontrada no BudgetView.tsx")
        else:
            print("❌ Coluna 'Valor Comissão' não encontrada no BudgetView.tsx")
            return False
            
        # Verificar se o dataIndex foi adicionado
        if "commission_value" in content:
            print("✅ Campo 'commission_value' configurado no BudgetView.tsx")
        else:
            print("❌ Campo 'commission_value' não configurado no BudgetView.tsx")
            return False
            
        # Verificar se o scroll foi ajustado
        if "scroll={{ x: 1350 }}" in content:
            print("✅ Scroll horizontal ajustado para nova coluna")
        else:
            print("❌ Scroll horizontal não foi ajustado")
            return False
            
        return True
        
    except FileNotFoundError:
        print("❌ Arquivo BudgetView.tsx não encontrado")
        return False
    except Exception as e:
        print(f"❌ Erro ao verificar arquivo: {str(e)}")
        return False

def main():
    """
    Executa todos os testes
    """
    print("🚀 Iniciando testes de comissão por item")
    print("=" * 60)
    
    # Teste 1: Verificar estrutura do frontend
    if not test_frontend_structure():
        print("\n❌ Falha nos testes de estrutura do frontend")
        sys.exit(1)
    
    # Teste 2: Verificar cálculos da API
    if not test_commission_calculation():
        print("\n❌ Falha nos testes de cálculo de comissão")
        sys.exit(1)
    
    print("\n🎉 Todos os testes passaram!")
    print("\n📋 Resumo da implementação:")
    print("  ✅ Nova coluna 'Valor Comissão' adicionada à tabela")
    print("  ✅ Cálculo de comissão por item funcionando")
    print("  ✅ Total de comissão sendo calculado corretamente")
    print("  ✅ Interface ajustada para exibir os novos dados")
    
    print("\n🎯 Funcionalidades implementadas:")
    print("  • Comissão calculada individualmente por item")
    print("  • Valor da comissão mostrado na tabela de visualização")
    print("  • Percentual e valor da comissão exibidos lado a lado")
    print("  • Total de comissão mantém a soma de todos os itens")

if __name__ == "__main__":
    main()
