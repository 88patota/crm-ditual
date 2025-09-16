#!/usr/bin/env python3
"""
Test para verificar se o markup_percentage está sendo calculado e salvo corretamente no backend
"""

import requests
import json

def test_markup_calculation():
    """
    Teste direto da API para verificar se markup está sendo calculado
    """
    print("=== TESTE: VERIFICAÇÃO DO MARKUP_PERCENTAGE ===")
    print()
    
    base_url = "http://localhost:8002"
    
    # Dados de teste simples
    budget_data = {
        "client_name": "Cliente Teste Markup",
        "items": [{
            "description": "Item Teste Markup",
            "peso_compra": 100.0,
            "peso_venda": 100.0,
            "valor_com_icms_compra": 10.00,  # R$ 10,00/kg
            "percentual_icms_compra": 0.18,  # 18%
            "outras_despesas_item": 0.0,
            "valor_com_icms_venda": 15.00,   # R$ 15,00/kg
            "percentual_icms_venda": 0.17   # 17%
        }]
    }
    
    try:
        print("1. Testando cálculo simplificado...")
        response = requests.post(
            f"{base_url}/api/v1/budgets/calculate-simplified",
            json=budget_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            calculation = response.json()
            print(f"✅ Cálculo realizado com sucesso")
            print(f"   Markup calculado: {calculation.get('markup_percentage', 'NÃO ENCONTRADO')}%")
            print(f"   Total Compra: R$ {calculation.get('total_purchase_value', 0):.2f}")
            print(f"   Total Venda: R$ {calculation.get('total_sale_value', 0):.2f}")
            print()
            
            # Cálculo manual esperado para validação
            # Valor compra sem impostos: 10.00 * (1-0.18) * (1-0.0925) = 7.437
            # Valor venda sem impostos: 15.00 * (1-0.17) * (1-0.0925) = 11.303
            # Markup esperado: ((11.303 - 7.437) / 7.437) * 100 = 52.0%
            
            expected_markup = 52.0  # Aproximado
            actual_markup = calculation.get('markup_percentage', 0)
            
            if abs(actual_markup - expected_markup) < 5:  # 5% tolerance
                print(f"✅ Markup calculado corretamente: {actual_markup:.1f}% (esperado ~{expected_markup:.1f}%)")
            else:
                print(f"⚠️ Markup pode estar incorreto: {actual_markup:.1f}% (esperado ~{expected_markup:.1f}%)")
        else:
            print(f"❌ Erro no cálculo: {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        print()
        print("2. Testando criação de orçamento...")
        response = requests.post(
            f"{base_url}/api/v1/budgets/simplified",
            json=budget_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            created_budget = response.json()
            budget_id = created_budget['id']
            
            print(f"✅ Orçamento criado - ID: {budget_id}")
            print(f"   Markup salvo no BD: {created_budget.get('markup_percentage', 'NÃO ENCONTRADO')}%")
            print()
            
            # Buscar o orçamento para verificar se o markup foi salvo
            print("3. Verificando orçamento salvo...")
            response = requests.get(f"{base_url}/api/v1/budgets/{budget_id}")
            
            if response.status_code == 200:
                saved_budget = response.json()
                markup_saved = saved_budget.get('markup_percentage')
                
                print(f"✅ Orçamento recuperado")
                print(f"   Markup no BD: {markup_saved}%")
                
                if markup_saved is not None and markup_saved > 0:
                    print(f"✅ Markup está sendo salvo corretamente: {markup_saved:.1f}%")
                    return True
                else:
                    print(f"❌ Markup não está sendo salvo ou é zero: {markup_saved}")
                    return False
            else:
                print(f"❌ Erro ao buscar orçamento: {response.status_code}")
                return False
        else:
            print(f"❌ Erro ao criar orçamento: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

if __name__ == "__main__":
    print("DIAGNÓSTICO: VERIFICAÇÃO DO MARKUP_PERCENTAGE")
    print("=" * 50)
    print()
    
    if test_markup_calculation():
        print()
        print("🎉 MARKUP FUNCIONANDO CORRETAMENTE!")
        print()
        print("✅ Markup é calculado pelo backend")
        print("✅ Markup é salvo no banco de dados")
        print("✅ Markup é retornado nas consultas")
        print()
        print("🔍 SE O FRONTEND NÃO EXIBE:")
        print("   • Verificar se budget.markup_percentage não é null/undefined")
        print("   • Verificar console do browser para erros")
        print("   • Verificar se o campo está sendo renderizado")
    else:
        print()
        print("❌ PROBLEMA ENCONTRADO NO BACKEND")
        print()
        print("🔧 VERIFICAR:")
        print("   • BusinessRulesCalculator está calculando markup?")
        print("   • Markup está sendo salvo no banco?")
        print("   • API está retornando o campo markup_percentage?")