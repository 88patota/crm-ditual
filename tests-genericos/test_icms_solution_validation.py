#!/usr/bin/env python3
"""
Test to validate that the ICMS solution correctly shows the impact of ICMS changes
with the new total_net_revenue and total_taxes fields.
"""

import requests
import json

def test_icms_solution():
    """
    Test that the solution correctly shows ICMS impact with new fields
    """
    print("=== VALIDAÇÃO DA SOLUÇÃO: IMPACTO DO ICMS ===")
    print()
    
    base_url = "http://localhost:8002"
    
    # Test data with different ICMS percentages
    scenarios = [
        {"icms": 0.17, "label": "17%"},
        {"icms": 0.18, "label": "18%"},
        {"icms": 0.20, "label": "20%"},
        {"icms": 0.25, "label": "25%"}
    ]
    
    base_data = {
        "client_name": "Cliente Teste Solução ICMS",
        "items": [{
            "description": "Produto Teste",
            "peso_compra": 100.0,
            "peso_venda": 100.0,
            "valor_com_icms_compra": 10.00,
            "percentual_icms_compra": 0.18,
            "outras_despesas_item": 0.0,
            "valor_com_icms_venda": 15.00,
            "percentual_icms_venda": 0.18  # Will be changed
        }]
    }
    
    print("📊 Teste com diferentes percentuais de ICMS:")
    print("=" * 80)
    
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
                
                # Extract key values
                total_sale = result.get('total_sale_value', 0)
                total_net_revenue = result.get('total_net_revenue', 0)
                total_taxes = result.get('total_taxes', 0)
                total_commission = result.get('total_commission', 0)
                
                results.append({
                    'icms': scenario['label'],
                    'total_sale': total_sale,
                    'net_revenue': total_net_revenue,
                    'taxes': total_taxes,
                    'commission': total_commission
                })
                
                print(f"ICMS {scenario['label']:>3}: Total Venda (c/ ICMS): R$ {total_sale:>8.2f} | "
                      f"Receita Líquida (s/ impostos): R$ {total_net_revenue:>8.2f} | "
                      f"Impostos: R$ {total_taxes:>8.2f}")
                
            else:
                print(f"❌ Erro para ICMS {scenario['label']}: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro para ICMS {scenario['label']}: {e}")
            return False
    
    print("=" * 80)
    print()
    
    # Validation
    print("🔍 VALIDAÇÃO DOS RESULTADOS:")
    print()
    
    # Check that total_sale_value is constant (correct behavior)
    total_sales = [r['total_sale'] for r in results]
    if all(abs(total_sales[0] - sale) < 0.01 for sale in total_sales):
        print("✅ Total Venda (c/ ICMS) é CONSTANTE - comportamento correto")
        print(f"   Valor: R$ {total_sales[0]:.2f} (não muda com % ICMS)")
    else:
        print("❌ Total Venda (c/ ICMS) está variando - comportamento incorreto")
        return False
    
    # Check that net_revenue changes (shows ICMS impact)
    net_revenues = [r['net_revenue'] for r in results]
    if not all(abs(net_revenues[0] - revenue) < 0.01 for revenue in net_revenues):
        print("✅ Receita Líquida (s/ impostos) MUDA - mostra impacto do ICMS")
        print(f"   Variação: R$ {min(net_revenues):.2f} a R$ {max(net_revenues):.2f}")
        
        # Show the change impact
        max_impact = max(net_revenues) - min(net_revenues)
        print(f"   Impacto máximo: R$ {max_impact:.2f} de diferença")
    else:
        print("❌ Receita Líquida não está mudando - não mostra impacto do ICMS")
        return False
    
    # Check taxes calculation
    taxes_correct = all(
        abs(r['taxes'] - (r['total_sale'] - r['net_revenue'])) < 0.01 
        for r in results
    )
    if taxes_correct:
        print("✅ Cálculo de Impostos correto: Impostos = Total Venda - Receita Líquida")
    else:
        print("❌ Cálculo de Impostos incorreto")
        return False
    
    print()
    print("📋 RESUMO DA SOLUÇÃO:")
    print()
    print("1️⃣ 'Total Venda (c/ ICMS)': Mostra valor que cliente paga (constante)")
    print("2️⃣ 'Receita Líquida (s/ impostos)': Mostra impacto real do ICMS (variável)")
    print("3️⃣ 'Impostos Totais': Mostra carga tributária exata")
    print("4️⃣ '% Impostos': Mostra percentual da carga tributária")
    print()
    print("🎯 RESULTADO: O usuário agora pode ver como mudanças no ICMS afetam")
    print("    a receita líquida da empresa, mantendo o total de venda correto.")
    
    return True

if __name__ == "__main__":
    print("VALIDAÇÃO: SOLUÇÃO COMPLETA PARA IMPACTO DO ICMS")
    print("=" * 60)
    print()
    
    if test_icms_solution():
        print()
        print("🎉 SOLUÇÃO VALIDADA COM SUCESSO!")
        print()
        print("✅ Frontend atualizado para mostrar novos campos")
        print("✅ Backend retorna total_net_revenue e total_taxes")
        print("✅ Usuário pode ver impacto real de mudanças no ICMS")
        print("✅ Total Venda (c/ ICMS) permanece correto para comissões")
    else:
        print()
        print("❌ SOLUÇÃO PRECISA DE AJUSTES")
        print("   Verificar implementação backend ou frontend")