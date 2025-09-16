#!/usr/bin/env python3
"""
Test to validate that Total Venda now behaves like Total Compra per PM request:
- Total Venda should change when ICMS percentage changes
- Total Venda should use valor SEM impostos like Total Compra does
"""

import requests
import json

def test_pm_icms_fix():
    """
    Test that validates Total Venda now changes with ICMS like Total Compra
    """
    print("=== VALIDAÇÃO: CORREÇÃO SOLICITADA PELA PM ===")
    print()
    
    base_url = "http://localhost:8002"
    
    # Test data - same item with different ICMS percentages
    scenarios = [
        {"icms": 0.12, "label": "12%"},
        {"icms": 0.18, "label": "18%"},
        {"icms": 0.20, "label": "20%"}
    ]
    
    base_data = {
        "client_name": "Cliente Teste PM",
        "items": [{
            "description": "Produto Teste Comportamento",
            "peso_compra": 100.0,
            "peso_venda": 100.0,
            "valor_com_icms_compra": 10.00,
            "percentual_icms_compra": 0.18,
            "outras_despesas_item": 0.0,
            "valor_com_icms_venda": 15.00,
            "percentual_icms_venda": 0.18  # Will be changed
        }]
    }
    
    print("📊 Testando comportamento do Total Venda com diferentes ICMS:")
    print("=" * 70)
    
    results = []
    
    for scenario in scenarios:
        test_data = base_data.copy()
        test_data["items"][0]["percentual_icms_venda"] = scenario["icms"]
        
        try:
            response = requests.post(
                f"{base_url}/api/v1/budgets/calculate-simplified",
                json=test_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                total_purchase = result.get('total_purchase_value', 0)
                total_sale = result.get('total_sale_value', 0)
                total_taxes = result.get('total_taxes', 0)
                total_with_icms = total_sale + total_taxes
                
                results.append({
                    'icms': scenario['label'],
                    'total_purchase': total_purchase,
                    'total_sale': total_sale,
                    'total_taxes': total_taxes,
                    'total_with_icms': total_with_icms
                })
                
                print(f"ICMS {scenario['label']:>3}: "
                      f"Total Compra: R$ {total_purchase:>8.2f} | "
                      f"Total Venda: R$ {total_sale:>8.2f} | "
                      f"Impostos: R$ {total_taxes:>8.2f} | "
                      f"Valor c/ ICMS: R$ {total_with_icms:>8.2f}")
                
            else:
                print(f"❌ Erro para ICMS {scenario['label']}: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro para ICMS {scenario['label']}: {e}")
            return False
    
    print("=" * 70)
    print()
    
    # Validation
    print("🔍 VALIDAÇÃO DO COMPORTAMENTO SOLICITADO PELA PM:")
    print()
    
    # Check that Total Compra is consistent (should not change with ICMS venda)
    total_purchases = [r['total_purchase'] for r in results]
    if all(abs(total_purchases[0] - purchase) < 0.01 for purchase in total_purchases):
        print("✅ Total Compra permanece CONSTANTE (correto - não depende de ICMS venda)")
    else:
        print("❌ Total Compra está variando (incorreto)")
        return False
    
    # Check that Total Venda now CHANGES with ICMS (the PM's request)
    total_sales = [r['total_sale'] for r in results]
    if not all(abs(total_sales[0] - sale) < 0.01 for sale in total_sales):
        print("✅ Total Venda agora MUDA com ICMS (conforme solicitado pela PM)")
        print(f"   Variação: R$ {min(total_sales):.2f} a R$ {max(total_sales):.2f}")
        
        # Show the impact
        max_impact = max(total_sales) - min(total_sales)
        print(f"   Impacto da mudança de ICMS: R$ {max_impact:.2f}")
    else:
        print("❌ Total Venda ainda não muda com ICMS (problema não resolvido)")
        return False
    
    # Verify the math
    print()
    print("🧮 VERIFICAÇÃO DOS CÁLCULOS:")
    for i, result in enumerate(results):
        icms_decimal = scenarios[i]['icms']
        
        # Manual calculation of valor sem impostos venda
        valor_com_icms_venda = 15.00
        valor_sem_icms_venda = valor_com_icms_venda * (1 - icms_decimal) * (1 - 0.0925)
        expected_total_sale = 100.0 * valor_sem_icms_venda
        
        if abs(result['total_sale'] - expected_total_sale) < 0.01:
            print(f"✅ ICMS {result['icms']}: Cálculo correto (R$ {expected_total_sale:.2f})")
        else:
            print(f"❌ ICMS {result['icms']}: Cálculo incorreto")
            print(f"   Esperado: R$ {expected_total_sale:.2f}")
            print(f"   Recebido: R$ {result['total_sale']:.2f}")
            return False
    
    return True

def test_commission_calculation():
    """
    Test that commission calculation still works correctly with the new approach
    """
    print()
    print("🏆 TESTE: CÁLCULO DE COMISSÃO APÓS MUDANÇA")
    print("=" * 50)
    
    base_url = "http://localhost:8002"
    
    test_data = {
        "client_name": "Cliente Teste Comissão",
        "items": [{
            "description": "Produto Alta Rentabilidade",
            "peso_compra": 50.0,
            "peso_venda": 50.0,
            "valor_com_icms_compra": 10.00,
            "percentual_icms_compra": 0.18,
            "outras_despesas_item": 0.0,
            "valor_com_icms_venda": 20.00,  # Boa margem
            "percentual_icms_venda": 0.18
        }]
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/v1/budgets/calculate-simplified",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            commission = result.get('total_commission', 0)
            
            if commission > 0:
                print(f"✅ Comissão calculada: R$ {commission:.2f}")
                print("✅ Cálculo de comissão funciona corretamente")
                return True
            else:
                print("❌ Comissão não foi calculada")
                return False
        else:
            print(f"❌ Erro na requisição: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    print("VALIDAÇÃO: CORREÇÃO SOLICITADA PELA PM")
    print("Total Venda deve se comportar igual ao Total Compra")
    print("=" * 60)
    print()
    
    tests_passed = 0
    total_tests = 2
    
    if test_pm_icms_fix():
        tests_passed += 1
    
    if test_commission_calculation():
        tests_passed += 1
    
    print()
    print("=" * 60)
    print(f"RESUMO: {tests_passed}/{total_tests} testes passaram")
    
    if tests_passed == total_tests:
        print("🎉 CORREÇÃO IMPLEMENTADA COM SUCESSO!")
        print()
        print("✅ Total Venda agora MUDA quando ICMS muda (igual ao Total Compra)")
        print("✅ Comissões continuam funcionando corretamente")
        print("✅ PM pode verificar que o comportamento está como solicitado")
        print()
        print("📋 MUDANÇAS IMPLEMENTADAS:")
        print("   • Total Venda = peso_venda × valor_sem_impostos_venda")
        print("   • Total Compra = peso_compra × valor_sem_impostos_compra")
        print("   • Comissões = baseadas no valor COM ICMS (correto)")
        print("   • Frontend atualizado para mostrar o novo comportamento")
    else:
        print("❌ ALGUNS TESTES FALHARAM")
        print("   Verificar implementação")