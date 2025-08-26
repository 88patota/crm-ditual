#!/usr/bin/env python3
"""
Test script to understand the commission calculation issue with weight differences
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'budget_service'))

from app.services.business_rules_calculator import BusinessRulesCalculator
from app.services.commission_service import CommissionService

def test_commission_with_weight_differences():
    """Test commission calculation with different peso_venda vs peso_compra"""
    
    print("=" * 80)
    print("TESTE: Comissão com Diferenças de Peso")
    print("=" * 80)
    
    # Test case: Same item with different sale vs purchase weights
    base_item = {
        'description': 'Produto Teste',
        'peso_compra': 100.0,  # Comprar 100kg
        'valor_com_icms_compra': 10.0,  # R$ 10 por kg com ICMS
        'percentual_icms_compra': 0.18,
        'valor_com_icms_venda': 20.0,   # R$ 20 por kg com ICMS
        'percentual_icms_venda': 0.18,
    }
    
    outras_despesas_totais = 0.0
    soma_pesos_pedido = 100.0
    
    print("\nCenário Base:")
    print(f"Peso Compra: {base_item['peso_compra']} kg")
    print(f"Valor Compra: R$ {base_item['valor_com_icms_compra']}/kg")
    print(f"Valor Venda: R$ {base_item['valor_com_icms_venda']}/kg")
    
    # Test 1: Same weight for purchase and sale
    print("\n" + "-" * 50)
    print("TESTE 1: Peso Venda = Peso Compra (100kg)")
    print("-" * 50)
    
    item1 = base_item.copy()
    item1['peso_venda'] = 100.0  # Vender a mesma quantidade
    
    result1 = BusinessRulesCalculator.calculate_complete_item(
        item1, outras_despesas_totais, soma_pesos_pedido
    )
    
    print(f"Peso Venda: {result1['peso_venda']} kg")
    print(f"Total Compra: R$ {result1['total_compra_item']:.2f}")
    print(f"Total Venda: R$ {result1['total_venda_item']:.2f}")
    print(f"Rentabilidade: {result1['rentabilidade_item']*100:.2f}%")
    print(f"Comissão: R$ {result1['valor_comissao']:.2f}")
    
    # Test 2: Higher weight for sale (selling more than purchased)
    print("\n" + "-" * 50)
    print("TESTE 2: Peso Venda > Peso Compra (120kg vs 100kg)")
    print("-" * 50)
    
    item2 = base_item.copy()
    item2['peso_venda'] = 120.0  # Vender mais que comprou
    
    result2 = BusinessRulesCalculator.calculate_complete_item(
        item2, outras_despesas_totais, soma_pesos_pedido
    )
    
    print(f"Peso Venda: {result2['peso_venda']} kg")
    print(f"Total Compra: R$ {result2['total_compra_item']:.2f}")
    print(f"Total Venda: R$ {result2['total_venda_item']:.2f}")
    print(f"Rentabilidade: {result2['rentabilidade_item']*100:.2f}%")
    print(f"Comissão: R$ {result2['valor_comissao']:.2f}")
    
    # Test 3: Lower weight for sale (selling less than purchased)
    print("\n" + "-" * 50)
    print("TESTE 3: Peso Venda < Peso Compra (80kg vs 100kg)")
    print("-" * 50)
    
    item3 = base_item.copy()
    item3['peso_venda'] = 80.0  # Vender menos que comprou
    
    result3 = BusinessRulesCalculator.calculate_complete_item(
        item3, outras_despesas_totais, soma_pesos_pedido
    )
    
    print(f"Peso Venda: {result3['peso_venda']} kg")
    print(f"Total Compra: R$ {result3['total_compra_item']:.2f}")
    print(f"Total Venda: R$ {result3['total_venda_item']:.2f}")
    print(f"Rentabilidade: {result3['rentabilidade_item']*100:.2f}%")
    print(f"Comissão: R$ {result3['valor_comissao']:.2f}")
    
    # Analysis
    print("\n" + "=" * 80)
    print("ANÁLISE DOS RESULTADOS")
    print("=" * 80)
    
    print(f"\nVariação Total Venda:")
    print(f"Teste 1: R$ {result1['total_venda_item']:.2f}")
    print(f"Teste 2: R$ {result2['total_venda_item']:.2f} (+{((result2['total_venda_item']/result1['total_venda_item'])-1)*100:.1f}%)")
    print(f"Teste 3: R$ {result3['total_venda_item']:.2f} ({((result3['total_venda_item']/result1['total_venda_item'])-1)*100:.1f}%)")
    
    print(f"\nVariação Comissão:")
    print(f"Teste 1: R$ {result1['valor_comissao']:.2f}")
    print(f"Teste 2: R$ {result2['valor_comissao']:.2f} (+{((result2['valor_comissao']/result1['valor_comissao'])-1)*100:.1f}%)" if result1['valor_comissao'] > 0 else "N/A")
    print(f"Teste 3: R$ {result3['valor_comissao']:.2f} ({((result3['valor_comissao']/result1['valor_comissao'])-1)*100:.1f}%)" if result1['valor_comissao'] > 0 else "N/A")
    
    # Check if commission scales proportionally with total_venda_item
    if result1['valor_comissao'] > 0:
        ratio_venda_2_1 = result2['total_venda_item'] / result1['total_venda_item']
        ratio_comissao_2_1 = result2['valor_comissao'] / result1['valor_comissao']
        
        ratio_venda_3_1 = result3['total_venda_item'] / result1['total_venda_item']
        ratio_comissao_3_1 = result3['valor_comissao'] / result1['valor_comissao']
        
        print(f"\nVerificação Proporcionalidade:")
        print(f"Teste 2 vs 1 - Ratio Venda: {ratio_venda_2_1:.3f}, Ratio Comissão: {ratio_comissao_2_1:.3f}")
        print(f"Teste 3 vs 1 - Ratio Venda: {ratio_venda_3_1:.3f}, Ratio Comissão: {ratio_comissao_3_1:.3f}")
        
        if abs(ratio_venda_2_1 - ratio_comissao_2_1) < 0.001:
            print("✓ Comissão escala proporcionalmente com total_venda_item")
        else:
            print("✗ Comissão NÃO escala proporcionalmente com total_venda_item")

if __name__ == "__main__":
    test_commission_with_weight_differences()