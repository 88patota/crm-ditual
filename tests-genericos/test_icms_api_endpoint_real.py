#!/usr/bin/env python3
"""
Teste para reproduzir o problema real de ICMS no endpoint
"""

import sys
import os
import json
import requests

# Adicionar o caminho do serviço de orçamentos
sys.path.append('/Users/erikpatekoski/dev/crm-ditual/services/budget_service')

def test_icms_api_endpoint():
    """Teste direto no endpoint da API para reproduzir o problema do ICMS"""
    
    print("=== TESTE ENDPOINT API - PROBLEMA ICMS ===")
    print()
    
    # URL do endpoint
    url = "http://localhost:8002/api/v1/budgets/calculate-simplified"
    
    # Teste 1: ICMS 12% e 7% (diferente de 18%)
    test_data_case1 = {
        "client_name": "Teste ICMS Diferente",
        "items": [{
            "description": "Produto com ICMS 12% e 7%",
            "peso_compra": 1000,
            "peso_venda": 1000,  
            "valor_com_icms_compra": 10.0,
            "percentual_icms_compra": 0.12,  # 12% em formato decimal
            "outras_despesas_item": 0.0,
            "valor_com_icms_venda": 15.0,
            "percentual_icms_venda": 0.07    # 7% em formato decimal
        }],
        "notes": "Teste com ICMS diferente de 18%"
    }
    
    print("CASO 1: ICMS Compra 12%, ICMS Venda 7%")
    print(f"Dados enviados: {json.dumps(test_data_case1, indent=2)}")
    print()
    
    # Headers
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # Fazer requisição
        print("Enviando requisição para o endpoint...")
        response = requests.post(url, json=test_data_case1, headers=headers)
        
        print(f"Status da resposta: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Resposta recebida com sucesso!")
            print()
            
            # Analisar os resultados
            print("RESULTADO DA API:")
            print(f"Total venda: R$ {result.get('total_sale_value', 0):.2f}")
            print(f"Total compra: R$ {result.get('total_purchase_value', 0):.2f}")
            print(f"Markup: {result.get('markup_percentage', 0):.2f}%")
            print()
            
            # Verificar os cálculos dos itens
            if 'items_calculations' in result and result['items_calculations']:
                item_calc = result['items_calculations'][0]
                print("ITEM CALCULADO:")
                print(f"Total venda: R$ {item_calc.get('total_sale', 0):.2f}")
                print(f"Total compra: R$ {item_calc.get('total_purchase', 0):.2f}")
                print(f"Rentabilidade: {item_calc.get('profitability', 0):.2f}%")
                print()
                
                # Calcular manualmente o que deveria ser
                # Com ICMS 12% compra e 7% venda
                valor_sem_icms_compra_esperado = 10.0 * (1 - 0.12) * (1 - 0.0925)
                valor_sem_icms_venda_esperado = 15.0 * (1 - 0.07) * (1 - 0.0925)
                total_compra_esperado = 1000 * valor_sem_icms_compra_esperado
                total_venda_esperado = 1000 * valor_sem_icms_venda_esperado
                
                print("VALORES ESPERADOS (CÁLCULO MANUAL):")
                print(f"Valor sem ICMS compra: R$ {valor_sem_icms_compra_esperado:.6f}")
                print(f"Valor sem ICMS venda: R$ {valor_sem_icms_venda_esperado:.6f}")
                print(f"Total compra esperado: R$ {total_compra_esperado:.2f}")
                print(f"Total venda esperado: R$ {total_venda_esperado:.2f}")
                print()
                
                # Comparar
                diff_compra = abs(item_calc.get('total_purchase', 0) - total_compra_esperado)
                diff_venda = abs(item_calc.get('total_sale', 0) - total_venda_esperado)
                
                if diff_compra < 0.01 and diff_venda < 0.01:
                    print("✅ SUCESSO: Cálculos estão corretos com ICMS diferente!")
                else:
                    print("❌ PROBLEMA: Cálculos não batem!")
                    print(f"  Diferença total compra: R$ {diff_compra:.2f}")
                    print(f"  Diferença total venda: R$ {diff_venda:.2f}")
                    
                    # Suspeita: sistema pode estar usando 18% ao invés dos valores enviados
                    valor_18_compra = 10.0 * (1 - 0.18) * (1 - 0.0925) * 1000
                    valor_18_venda = 15.0 * (1 - 0.18) * (1 - 0.0925) * 1000
                    
                    if (abs(item_calc.get('total_purchase', 0) - valor_18_compra) < 0.01 and
                        abs(item_calc.get('total_sale', 0) - valor_18_venda) < 0.01):
                        print("🚨 CONFIRMADO: Sistema está usando 18% ao invés dos valores enviados!")
        else:
            print(f"❌ Erro na API: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"Detalhes do erro: {error_detail}")
            except:
                print(f"Texto do erro: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão: Verifique se o serviço está rodando na porta 8002")
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        
def test_icms_zero_api():
    """Teste com ICMS zero"""
    print()
    print("=== TESTE CASO 2: ICMS ZERO ===")
    
    url = "http://localhost:8002/api/v1/budgets/calculate-simplified"
    
    test_data_zero = {
        "client_name": "Teste ICMS Zero",
        "items": [{
            "description": "Produto com ICMS 0%",
            "peso_compra": 100,
            "peso_venda": 100,  
            "valor_com_icms_compra": 10.0,
            "percentual_icms_compra": 0.0,  # 0%
            "outras_despesas_item": 0.0,
            "valor_com_icms_venda": 15.0,
            "percentual_icms_venda": 0.0    # 0%
        }]
    }
    
    print(f"Dados: ICMS compra e venda = 0%")
    
    try:
        response = requests.post(url, json=test_data_zero)
        
        if response.status_code == 200:
            result = response.json()
            
            if 'items_calculations' in result and result['items_calculations']:
                item_calc = result['items_calculations'][0]
                
                # Com ICMS 0%, só deveria descontar PIS/COFINS (9.25%)
                valor_esperado_compra = 10.0 * (1 - 0.0925) * 100  # 907.50
                valor_esperado_venda = 15.0 * (1 - 0.0925) * 100   # 1361.25
                
                print(f"Total compra API: R$ {item_calc.get('total_purchase', 0):.2f}")
                print(f"Total compra esperado: R$ {valor_esperado_compra:.2f}")
                print(f"Total venda API: R$ {item_calc.get('total_sale', 0):.2f}")
                print(f"Total venda esperado: R$ {valor_esperado_venda:.2f}")
                
                if (abs(item_calc.get('total_purchase', 0) - valor_esperado_compra) < 0.01 and
                    abs(item_calc.get('total_sale', 0) - valor_esperado_venda) < 0.01):
                    print("✅ ICMS 0% funcionando corretamente!")
                else:
                    print("❌ Problema com ICMS 0%")
        else:
            print(f"❌ Erro: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_icms_api_endpoint()
    test_icms_zero_api()