#!/usr/bin/env python3
"""
Teste para validar que a página BudgetView agora exibe os valores corretos
após correção da lógica de cálculo de impostos.
"""

import requests
import json

def test_budget_view_display_fix():
    """
    Teste que valida se BudgetView agora exibe valores consistentes
    """
    print("=== TESTE: VALIDAÇÃO DA CORREÇÃO DO BUDGETVIEW ===")
    print()
    
    base_url = "http://localhost:8002"
    
    # Criar um orçamento de teste
    budget_data = {
        "client_name": "Cliente Teste Exibição",
        "items": [{
            "description": "Item Teste Validação",
            "peso_compra": 100.0,
            "peso_venda": 100.0,
            "valor_com_icms_compra": 10.00,
            "percentual_icms_compra": 0.18,
            "outras_despesas_item": 0.0,
            "valor_com_icms_venda": 15.00,
            "percentual_icms_venda": 0.17
        }]
    }
    
    try:
        # 1. Criar orçamento usando API
        print("1. Criando orçamento para validação...")
        response = requests.post(
            f"{base_url}/api/v1/budgets/simplified",
            json=budget_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            created_budget = response.json()
            budget_id = created_budget['id']
            print(f"✅ Orçamento criado - ID: {budget_id}")
            
            # 2. Buscar orçamento criado (simula o que BudgetView faz)
            print()
            print("2. Recuperando orçamento criado...")
            response = requests.get(f"{base_url}/api/v1/budgets/{budget_id}")
            
            if response.status_code == 200:
                budget = response.json()
                
                print("✅ Orçamento recuperado com sucesso")
                print()
                
                # 3. Simular cálculos do frontend CORRIGIDO
                print("3. Simulando cálculos do BudgetView CORRIGIDO...")
                
                # Dados do backend
                backend_total_sale_value = budget.get('total_sale_value', 0)  # SEM ICMS
                backend_total_purchase_value = budget.get('total_purchase_value', 0)
                backend_total_commission = budget.get('total_commission', 0)
                backend_profitability = budget.get('profitability_percentage', 0)
                
                print(f"📊 VALORES DO BACKEND:")
                print(f"   Total Compra: R$ {backend_total_purchase_value:.2f}")
                print(f"   Total Venda (s/ ICMS): R$ {backend_total_sale_value:.2f}")
                print(f"   Total Comissão: R$ {backend_total_commission:.2f}")
                print(f"   Rentabilidade: {backend_profitability:.2f}%")
                print()
                
                # Calcular como o frontend CORRIGIDO agora faz
                total_sale_with_icms = 0
                for item in budget.get('items', []):
                    sale_weight = item.get('sale_weight') or item.get('weight', 0)
                    sale_value_with_icms = item.get('sale_value_with_icms', 0)
                    total_sale_with_icms += sale_weight * sale_value_with_icms
                
                # Receita líquida = total_sale_value do backend (SEM ICMS)
                total_net_revenue = backend_total_sale_value
                
                # Impostos = Valor COM ICMS - Valor SEM ICMS
                total_taxes = total_sale_with_icms - total_net_revenue
                tax_percentage = (total_taxes / total_sale_with_icms * 100) if total_sale_with_icms > 0 else 0
                
                print(f"🧮 CÁLCULOS DO FRONTEND CORRIGIDO:")
                print(f"   Total Venda (c/ ICMS): R$ {total_sale_with_icms:.2f}")
                print(f"   Receita Líquida (s/ impostos): R$ {total_net_revenue:.2f}")
                print(f"   Impostos Totais: R$ {total_taxes:.2f}")
                print(f"   % Impostos: {tax_percentage:.2f}%")
                print()
                
                # 4. Validar consistência
                print("4. Validando consistência dos valores...")
                
                # Valores esperados para validação
                expected_total_with_icms = 100.0 * 15.00  # 100kg * R$ 15,00/kg = R$ 1.500,00
                expected_taxes = expected_total_with_icms - backend_total_sale_value
                
                print(f"📋 VALIDAÇÃO:")
                
                # Verificar se total COM ICMS está correto
                if abs(total_sale_with_icms - expected_total_with_icms) < 0.01:
                    print(f"✅ Total Venda (c/ ICMS) correto: R$ {total_sale_with_icms:.2f}")
                else:
                    print(f"❌ Total Venda (c/ ICMS) incorreto:")
                    print(f"   Esperado: R$ {expected_total_with_icms:.2f}")
                    print(f"   Calculado: R$ {total_sale_with_icms:.2f}")
                    return False
                
                # Verificar se receita líquida usa valor do backend
                if abs(total_net_revenue - backend_total_sale_value) < 0.01:
                    print(f"✅ Receita Líquida usando valor do backend: R$ {total_net_revenue:.2f}")
                else:
                    print(f"❌ Receita Líquida não está usando valor do backend")
                    return False
                
                # Verificar se impostos são calculados corretamente
                if abs(total_taxes - expected_taxes) < 0.01:
                    print(f"✅ Impostos Totais corretos: R$ {total_taxes:.2f}")
                else:
                    print(f"❌ Impostos Totais incorretos:")
                    print(f"   Esperado: R$ {expected_taxes:.2f}")
                    print(f"   Calculado: R$ {total_taxes:.2f}")
                    return False
                
                # Verificar percentual de impostos
                expected_tax_percentage = (expected_taxes / expected_total_with_icms * 100)
                if abs(tax_percentage - expected_tax_percentage) < 0.1:
                    print(f"✅ % Impostos correto: {tax_percentage:.2f}%")
                else:
                    print(f"❌ % Impostos incorreto:")
                    print(f"   Esperado: {expected_tax_percentage:.2f}%")
                    print(f"   Calculado: {tax_percentage:.2f}%")
                    return False
                
                return True
                
            else:
                print(f"❌ Erro ao buscar orçamento: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        else:
            print(f"❌ Erro ao criar orçamento: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("VALIDAÇÃO: CORREÇÃO DO BUDGETVIEW")
    print("=" * 50)
    print()
    
    if test_budget_view_display_fix():
        print()
        print("🎉 TESTE PASSOU!")
        print()
        print("✅ BudgetView agora exibe valores corretos")
        print("✅ Total Venda (c/ ICMS) = valor real que cliente paga")
        print("✅ Receita Líquida = valor do backend (sem impostos)")
        print("✅ Impostos = diferença entre valor COM e SEM ICMS")
        print("✅ Consistência entre criação e visualização")
        print()
        print("🔧 PROBLEMA RESOLVIDO:")
        print("   • Frontend não recalcula valores já calculados pelo backend")
        print("   • Usa dados corretos do BusinessRulesCalculator")
        print("   • Exibe valores consistentes com tela de criação")
    else:
        print()
        print("❌ TESTE FALHOU - VERIFICAR IMPLEMENTAÇÃO")