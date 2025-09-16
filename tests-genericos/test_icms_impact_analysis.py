#!/usr/bin/env python3
"""
Test to analyze what should change when ICMS percentage changes
and verify if the correct values are being displayed to the user.
"""

import sys
import requests
import json

def test_icms_impact_detailed():
    """
    Detailed analysis of what changes when ICMS percentage changes
    """
    print("=== ANÁLISE DETALHADA: IMPACTO DA MUDANÇA DE ICMS ===")
    print()
    
    base_url = "http://localhost:8002"
    
    # Base test data
    base_item = {
        "description": "Produto Teste",
        "peso_compra": 100.0,
        "peso_venda": 100.0,
        "valor_com_icms_compra": 10.00,  # R$ 10/kg WITH ICMS
        "percentual_icms_compra": 0.18,  # 18%
        "outras_despesas_item": 0.0,
        "valor_com_icms_venda": 15.00,   # R$ 15/kg WITH ICMS
        "percentual_icms_venda": 0.18    # 18% (will be changed)
    }
    
    scenarios = [
        {"icms": 0.17, "label": "17%"},
        {"icms": 0.18, "label": "18%"},
        {"icms": 0.20, "label": "20%"},
        {"icms": 0.25, "label": "25%"}
    ]
    
    print("Dados base:")
    print(f"  Peso venda: {base_item['peso_venda']} kg")
    print(f"  Valor COM ICMS venda: R$ {base_item['valor_com_icms_venda']}/kg")
    print()
    
    results = []
    
    for scenario in scenarios:
        print(f"--- Testando ICMS {scenario['label']} ---")
        
        # Create test data with modified ICMS
        test_data = {
            "client_name": "Cliente Teste",
            "items": [base_item.copy()]
        }
        test_data["items"][0]["percentual_icms_venda"] = scenario["icms"]
        
        try:
            response = requests.post(
                f"{base_url}/api/v1/budgets/calculate-simplified",
                json=test_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract calculated values
                item_calc = result['items_calculations'][0] if result['items_calculations'] else {}
                
                analysis = {
                    "icms_percentage": scenario['label'],
                    "icms_decimal": scenario['icms'],
                    
                    # API Response Fields
                    "total_sale_value": result.get('total_sale_value', 0),  # From API
                    "total_purchase_value": result.get('total_purchase_value', 0),
                    "total_commission": result.get('total_commission', 0),
                    "markup_percentage": result.get('markup_percentage', 0),
                    
                    # Item-level calculations
                    "item_total_sale": item_calc.get('total_sale', 0),
                    "item_total_purchase": item_calc.get('total_purchase', 0),
                    "item_profitability": item_calc.get('profitability', 0),
                    "item_commission": item_calc.get('commission_value', 0),
                }
                
                # Manual calculations for comparison
                valor_sem_icms_venda = base_item['valor_com_icms_venda'] * (1 - scenario['icms']) * (1 - 0.0925)
                total_sem_icms = base_item['peso_venda'] * valor_sem_icms_venda
                total_com_icms = base_item['peso_venda'] * base_item['valor_com_icms_venda']
                
                analysis.update({
                    "manual_valor_sem_icms_venda": valor_sem_icms_venda,
                    "manual_total_sem_icms": total_sem_icms,
                    "manual_total_com_icms": total_com_icms,
                })
                
                results.append(analysis)
                
                print(f"  API total_sale_value: R$ {result.get('total_sale_value', 0):.2f}")
                print(f"  Manual total SEM ICMS: R$ {total_sem_icms:.2f}")
                print(f"  Manual total COM ICMS: R$ {total_com_icms:.2f}")
                print(f"  Diferença sem/com ICMS: R$ {total_com_icms - total_sem_icms:.2f}")
                print()
                
            else:
                print(f"  ❌ Erro: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Erro: {e}")
    
    # Analysis Summary
    print("=" * 60)
    print("RESUMO DA ANÁLISE")
    print("=" * 60)
    
    print("\n1. VALORES QUE NÃO MUDAM COM ICMS:")
    for result in results:
        print(f"   ICMS {result['icms_percentage']}: Total Sale Value = R$ {result['total_sale_value']:.2f}")
    
    print("\n2. VALORES QUE MUDAM COM ICMS (Manual - SEM ICMS):")
    for result in results:
        print(f"   ICMS {result['icms_percentage']}: Total SEM ICMS = R$ {result['manual_total_sem_icms']:.2f}")
    
    print("\n3. COMISSÕES (baseadas no valor COM ICMS):")
    for result in results:
        print(f"   ICMS {result['icms_percentage']}: Comissão = R$ {result['total_commission']:.2f}")
    
    # Determine what the API is actually returning
    print("\n4. CONCLUSÃO SOBRE O QUE A API RETORNA:")
    api_values = [r['total_sale_value'] for r in results]
    com_icms_values = [r['manual_total_com_icms'] for r in results]
    sem_icms_values = [r['manual_total_sem_icms'] for r in results]
    
    if all(abs(api_values[0] - v) < 0.01 for v in api_values):
        print("   ✅ API retorna valor CONSTANTE (não muda com ICMS)")
        
        if abs(api_values[0] - com_icms_values[0]) < 0.01:
            print("   ✅ API usa valor COM ICMS (correto para comissões)")
        elif abs(api_values[0] - sem_icms_values[0]) < 0.01:
            print("   ⚠️  API usa valor SEM ICMS")
        else:
            print("   ❓ API usa algum outro cálculo")
    else:
        print("   ✅ API retorna valor VARIÁVEL (muda com ICMS)")
    
    return results

def analyze_user_expectation():
    """
    Analyze what the user might be expecting to see
    """
    print("\n5. ANÁLISE DA EXPECTATIVA DO USUÁRIO:")
    print("=" * 50)
    
    print("\nO usuário relatou: 'Total Venda não está refletindo a atualização do valor com a mudança do ICMS'")
    print("\nPossíveis interpretações:")
    print("1. EXPECTATIVA INCORRETA: Usuário espera que 'Total Venda' mude com ICMS")
    print("   → Problema: Total COM ICMS não deveria mudar quando % ICMS muda")
    print("   → Solução: Educação do usuário ou mudança de nomenclatura")
    print()
    print("2. EXPECTATIVA CORRETA: Usuário quer ver impacto do ICMS em algum lugar")
    print("   → Problema: Sistema não mostra valor SEM ICMS que muda")
    print("   → Solução: Adicionar campo 'Receita Líquida' (sem impostos)")
    print()
    print("3. BUG NO CÁLCULO: Sistema deveria mostrar valor SEM ICMS como 'Total Venda'")
    print("   → Problema: Confusão sobre qual valor mostrar")
    print("   → Solução: Clarificar se deve usar COM ou SEM ICMS")

def recommend_solution():
    """
    Recommend solution based on analysis
    """
    print("\n6. RECOMENDAÇÃO DE SOLUÇÃO:")
    print("=" * 40)
    
    print("\nBasado na análise e nas especificações do sistema:")
    print()
    print("✅ SITUAÇÃO ATUAL ESTÁ CORRETA:")
    print("   - Total Sale usa valor COM ICMS")
    print("   - Comissões calculadas sobre valor real pago pelo cliente")
    print("   - Consistente com regras de negócio implementadas")
    print()
    print("💡 MELHORIAS SUGERIDAS:")
    print("   1. Adicionar campo 'Receita Líquida' que mostra valor SEM impostos")
    print("   2. Clarificar nomenclatura: 'Total Faturado' vs 'Receita Líquida'")
    print("   3. Mostrar impacto fiscal: 'Impostos sobre Venda: R$ X,XX'")
    print("   4. Adicionar tooltip explicativo nos campos")
    print()
    print("🔧 IMPLEMENTAÇÃO:")
    print("   - Manter 'Total Venda' atual (COM ICMS)")
    print("   - Adicionar 'Receita Líquida' (SEM ICMS) que muda com ICMS")
    print("   - Adicionar 'Impostos' = Total Venda - Receita Líquida")

if __name__ == "__main__":
    print("ANÁLISE DETALHADA: IMPACTO DO ICMS NO TOTAL DE VENDA")
    print("=" * 60)
    
    try:
        results = test_icms_impact_detailed()
        analyze_user_expectation()
        recommend_solution()
    except Exception as e:
        print(f"❌ Erro na análise: {e}")
        sys.exit(1)