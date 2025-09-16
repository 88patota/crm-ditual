#!/usr/bin/env python3
"""
Teste para verificar se a correção da comissão funcionou
"""

import sys
import os

# Adicionar o caminho do serviço de orçamentos
sys.path.append('/Users/erikpatekoski/dev/crm-ditual/services/budget_service')

from app.services.business_rules_calculator import BusinessRulesCalculator
from app.services.commission_service import CommissionService

def test_fixed_commission():
    """Teste da comissão corrigida"""
    
    print("=== TESTE DA CORREÇÃO DA COMISSÃO ===")
    print()
    
    # Dados do orçamento ID 79
    item_data = {
        'description': 'Item Orçamento ID 79 - CORRIGIDO',
        'peso_compra': 1000,
        'peso_venda': 1050,  
        'valor_com_icms_compra': 6.0,  # R$ 6,00 por kg
        'percentual_icms_compra': 0.18,  # 18%
        'valor_com_icms_venda': 7.0,    # R$ 7,00 por kg
        'percentual_icms_venda': 0.18    # 18%
    }
    
    print("DADOS DE ENTRADA:")
    for key, value in item_data.items():
        if 'percentual' in key:
            print(f"{key}: {value*100:.0f}%")
        else:
            print(f"{key}: {value}")
    print()
    
    # Calcular usando o sistema corrigido
    outras_despesas_totais = 0.0
    soma_pesos_pedido = item_data['peso_compra']
    
    try:
        resultado = BusinessRulesCalculator.calculate_complete_item(
            item_data, outras_despesas_totais, soma_pesos_pedido
        )
        
        print("=== RESULTADOS CORRIGIDOS ===")
        print(f"Total compra (sem ICMS): R$ {resultado['total_compra_item']:.2f}")
        print(f"Total venda (sem ICMS): R$ {resultado['total_venda_item']:.2f}")
        print(f"Total compra (com ICMS): R$ {resultado['total_compra_item_com_icms']:.2f}")
        print(f"Total venda (com ICMS): R$ {resultado['total_venda_item_com_icms']:.2f}")
        print(f"Rentabilidade do item: {resultado['rentabilidade_item']*100:.2f}%")
        print(f"Valor da comissão: R$ {resultado['valor_comissao']:.2f}")
        print()
        
        # Verificar se está correto
        expected_commission = 73.50
        if abs(resultado['valor_comissao'] - expected_commission) < 0.01:
            print("✅ SUCCESS: Comissão corrigida com sucesso!")
        else:
            print(f"❌ ERROR: Comissão ainda está errada. Esperado: R$ {expected_commission:.2f}")
        
        # Teste manual da nova função
        print()
        print("=== TESTE DIRETO DA FUNÇÃO CORRIGIDA ===")
        comissao_direta = CommissionService.calculate_commission_value_with_quantity_adjustment(
            resultado['total_venda_item_com_icms'],
            resultado['total_compra_item_com_icms'],
            item_data['peso_venda'],
            item_data['peso_compra'],
            item_data['valor_com_icms_venda'],
            item_data['valor_com_icms_compra']
        )
        print(f"Comissão direta: R$ {comissao_direta:.2f}")
        
        # Verificar rentabilidade correta
        rentabilidade_correta = (resultado['total_venda_item_com_icms'] / resultado['total_compra_item_com_icms']) - 1
        print(f"Rentabilidade correta: {rentabilidade_correta*100:.2f}%")
        
        percentual_comissao = CommissionService.calculate_commission_percentage(rentabilidade_correta)
        print(f"Percentual de comissão: {percentual_comissao*100:.2f}%")
        
    except Exception as e:
        print(f"ERRO no cálculo: {e}")
        import traceback
        traceback.print_exc()

def test_edge_cases():
    """Teste casos extremos"""
    print()
    print("=== TESTES DE CASOS EXTREMOS ===")
    
    # Caso 1: Mesma quantidade (deve usar rentabilidade unitária)
    print()
    print("Caso 1: Mesma quantidade")
    comissao_mesma_qtd = CommissionService.calculate_commission_value_with_quantity_adjustment(
        7000.0,  # total venda com ICMS
        6000.0,  # total compra com ICMS  
        1000,    # peso venda
        1000,    # peso compra (igual)
        7.0,     # valor unitário venda
        6.0      # valor unitário compra
    )
    print(f"Comissão mesma quantidade: R$ {comissao_mesma_qtd:.2f}")
    
    # Caso 2: Quantidade menor na venda
    print()
    print("Caso 2: Venda menor que compra")
    comissao_menor = CommissionService.calculate_commission_value_with_quantity_adjustment(
        6300.0,  # 900kg * 7.0 = total venda com ICMS
        6000.0,  # 1000kg * 6.0 = total compra com ICMS
        900,     # peso venda (menor)
        1000,    # peso compra
        7.0,     # valor unitário venda
        6.0      # valor unitário compra
    )
    print(f"Comissão venda menor: R$ {comissao_menor:.2f}")

if __name__ == "__main__":
    test_fixed_commission()
    test_edge_cases()