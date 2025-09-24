#!/usr/bin/env python3
"""
Teste para debug dos valores sendo passados do frontend para backend
Identifica problemas na transmissão/conversão dos valores de compra e venda
"""

import requests
import json
from decimal import Decimal

# Configuração
BASE_URL = "http://localhost:8002/api/v1/budgets"

# Dados de teste que simulam o que o frontend está enviando
test_data = {
    "client_name": "Cliente Teste",
    "status": "draft",
    "items": [
        {
            "description": "Produto Teste",
            "peso_compra": 1.5,  # 1.5 kg
            "peso_venda": 1.5,   # 1.5 kg
            "valor_com_icms_compra": 100.0,  # R$ 100,00
            "percentual_icms_compra": 0.18,  # 18%
            "outras_despesas_item": 0.0,
            "valor_com_icms_venda": 150.0,   # R$ 150,00
            "percentual_icms_venda": 0.18    # 18%
        }
    ]
}

def test_calculate_endpoint():
    """Testa o endpoint de cálculo e mostra os valores recebidos"""
    print("=== TESTE DO ENDPOINT DE CÁLCULO ===")
    print(f"Dados enviados: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(f"{BASE_URL}/calculate-simplified", json=test_data)
        
        print(f"\nStatus da resposta: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Resposta recebida: {json.dumps(result, indent=2)}")
            
            # Analisar valores específicos
            print("\n=== ANÁLISE DOS VALORES ===")
            print(f"Total Compra: R$ {result.get('total_purchase_value', 0):.2f}")
            print(f"Total Venda: R$ {result.get('total_sale_value', 0):.2f}")
            print(f"Markup: {result.get('markup_percentage', 0):.2f}%")
            print(f"Rentabilidade: {result.get('profitability_percentage', 0):.2f}%")
            
            # Verificar se os valores fazem sentido
            expected_purchase = 100.0 * (1 - 0.18) * (1 - 0.0925) * 1.5  # ~111.735
            expected_sale = 150.0 * (1 - 0.18) * (1 - 0.0925) * 1.5       # ~167.6025
            
            print(f"\n=== VALORES ESPERADOS (manual) ===")
            print(f"Compra esperada: R$ {expected_purchase:.2f}")
            print(f"Venda esperada: R$ {expected_sale:.2f}")
            
        else:
            print(f"Erro na resposta: {response.text}")
            
    except Exception as e:
        print(f"Erro na requisição: {e}")

def test_different_number_formats():
    """Testa diferentes formatos de números para identificar problemas de conversão"""
    print("\n=== TESTE DE FORMATOS DIFERENTES ===")
    
    test_cases = [
        {"name": "Decimais com ponto", "peso_compra": 1.5, "valor_compra": 100.0},
        {"name": "Decimais como string", "peso_compra": "1.5", "valor_compra": "100.0"},
        {"name": "Decimais com vírgula", "peso_compra": "1,5", "valor_compra": "100,0"},
        {"name": "Inteiros", "peso_compra": 2, "valor_compra": 100},
    ]
    
    for case in test_cases:
        print(f"\nTeste: {case['name']}")
        
        test_data_case = {
            "client_name": "Cliente Teste",
            "items": [{
                "description": "Produto Teste",
                "peso_compra": case["peso_compra"],
                "peso_venda": case["peso_compra"],
                "valor_com_icms_compra": case["valor_compra"],
                "percentual_icms_compra": 0.18,
                "outras_despesas_item": 0.0,
                "valor_com_icms_venda": 150.0,
                "percentual_icms_venda": 0.18
            }]
        }
        
        try:
            response = requests.post(f"{BASE_URL}/calculate-simplified", json=test_data_case)
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✓ Sucesso - Total Compra: R$ {result.get('total_purchase_value', 0):.2f}")
            else:
                print(f"  ✗ Erro {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"  ✗ Exceção: {e}")

def analyze_frontend_component():
    """Análise do componente do frontend"""
    print("\n=== ANÁLISE DO COMPONENTE FRONTEND ===")
    
    print("Campos identificados no SimplifiedBudgetForm.tsx:")
    print("- peso_compra: InputNumber com precision=3, step=0.001")
    print("- peso_venda: InputNumber com precision=3, step=0.001")
    print("- valor_com_icms_compra: InputNumber com precision=2, step=0.01")
    print("- valor_com_icms_venda: InputNumber com precision=2, step=0.01")
    print("- percentual_icms_compra: Convertido de % para decimal (valor * 100 no display, /100 no onChange)")
    print("- percentual_icms_venda: Convertido de % para decimal (valor * 100 no display, /100 no onChange)")
    
    print("\nPossíveis problemas identificados:")
    print("1. Conversão de percentual pode estar incorreta")
    print("2. Precision dos InputNumber pode causar arredondamentos")
    print("3. Formato de número (vírgula vs ponto) pode não estar consistente")

def test_manual_calculation():
    """Testa cálculo manual para comparar com o backend"""
    print("\n=== CÁLCULO MANUAL PARA COMPARAÇÃO ===")
    
    # Dados do teste
    peso_compra = 1.5
    peso_venda = 1.5
    valor_com_icms_compra = 100.0
    percentual_icms_compra = 0.18
    valor_com_icms_venda = 150.0
    percentual_icms_venda = 0.18
    pis_cofins = 0.0925
    
    # Cálculos conforme as regras de negócio
    valor_sem_icms_compra = valor_com_icms_compra * (1 - percentual_icms_compra)
    valor_sem_impostos_compra = valor_sem_icms_compra * (1 - pis_cofins)
    total_compra_item = peso_compra * valor_sem_impostos_compra
    
    valor_sem_icms_venda = valor_com_icms_venda * (1 - percentual_icms_venda)
    valor_sem_impostos_venda = valor_sem_icms_venda * (1 - pis_cofins)
    total_venda_item = peso_venda * valor_sem_impostos_venda
    
    markup = (total_venda_item / total_compra_item - 1) * 100 if total_compra_item > 0 else 0
    
    print(f"Valor sem ICMS (Compra): R$ {valor_sem_icms_compra:.6f}")
    print(f"Valor sem impostos (Compra): R$ {valor_sem_impostos_compra:.6f}")
    print(f"Total Compra Item: R$ {total_compra_item:.2f}")
    
    print(f"Valor sem ICMS (Venda): R$ {valor_sem_icms_venda:.6f}")
    print(f"Valor sem impostos (Venda): R$ {valor_sem_impostos_venda:.6f}")
    print(f"Total Venda Item: R$ {total_venda_item:.2f}")
    
    print(f"Markup: {markup:.2f}%")

if __name__ == "__main__":
    analyze_frontend_component()
    test_manual_calculation()
    test_calculate_endpoint()
    test_different_number_formats()
