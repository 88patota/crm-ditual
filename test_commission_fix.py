#!/usr/bin/env python3
"""
Script para testar a correção do cálculo de comissão
"""

import sys
import os

# Adicionar o caminho do budget_service ao sys.path
sys.path.append('/Users/erikpatekoski/dev/crm-ditual/services/budget_service')

from app.services.business_rules_calculator import BusinessRulesCalculator
from app.services.commission_service import CommissionService

def test_commission_calculation():
    """Testa o cálculo de comissão com os dados fornecidos"""
    
    # Dados de teste
    item_data = {
        'description': 'Item Teste',
        'peso_compra': 1.0,
        'peso_venda': 2.0,
        'valor_com_icms_compra': 2.11,
        'percentual_icms_compra': 18.0,
        'valor_com_icms_venda': 4.32,
        'percentual_icms_venda': 17.0,
        'percentual_ipi': 0.0,
        'outras_despesas_item': 0.0
    }
    
    print("=== TESTE DE CORREÇÃO DO CÁLCULO DE COMISSÃO ===")
    print(f"Dados de entrada:")
    print(f"  Peso compra: {item_data['peso_compra']} kg")
    print(f"  Peso venda: {item_data['peso_venda']} kg")
    print(f"  Valor compra COM ICMS: R$ {item_data['valor_com_icms_compra']}")
    print(f"  Valor venda COM ICMS: R$ {item_data['valor_com_icms_venda']}")
    print()
    
    # Calcular item completo
    calculated_item = BusinessRulesCalculator.calculate_complete_item(
        item_data, 0.0, 2.0, 0.0  # outras_despesas_totais, soma_pesos_pedido, freight_value_total
    )
    
    print("=== RESULTADOS CALCULADOS ===")
    print(f"Rentabilidade do item: {calculated_item['rentabilidade_item']:.4f} ({calculated_item['rentabilidade_item']*100:.2f}%)")
    print(f"Percentual de comissão: {calculated_item['percentual_comissao']:.4f} ({calculated_item['percentual_comissao']*100:.2f}%)")
    print(f"Valor da comissão: R$ {calculated_item['valor_comissao']:.2f}")
    print(f"Total venda COM ICMS: R$ {calculated_item['total_venda_com_icms_item']:.2f}")
    print()
    
    # Calcular orçamento completo
    budget_result = BusinessRulesCalculator.calculate_complete_budget(
        [item_data], 0.0, 2.0, 0.0
    )
    
    print("=== TOTAIS DO ORÇAMENTO ===")
    print(f"Total venda COM ICMS: R$ {budget_result['totals']['soma_total_venda_com_icms']:.2f}")
    print(f"Total comissão: R$ {budget_result['totals']['total_comissao']:.2f}")
    print(f"Markup do pedido: {budget_result['totals']['markup_pedido']:.4f} ({budget_result['totals']['markup_pedido']*100:.2f}%)")
    print()
    
    # Verificar se a correção funcionou
    expected_profitability = (4.32 / 2.11) - 1  # Rentabilidade COM ICMS unitária
    expected_commission_rate = 0.05  # 5% para rentabilidade >= 80%
    expected_commission_value = 8.64 * expected_commission_rate  # Total venda COM ICMS * taxa
    
    print("=== VERIFICAÇÃO ===")
    print(f"Rentabilidade esperada COM ICMS: {expected_profitability:.4f} ({expected_profitability*100:.2f}%)")
    print(f"Taxa de comissão esperada: {expected_commission_rate:.4f} ({expected_commission_rate*100:.2f}%)")
    print(f"Valor de comissão esperado: R$ {expected_commission_value:.2f}")
    print()
    
    # Verificar se os valores estão corretos
    rentabilidade_ok = abs(calculated_item['rentabilidade_item'] - expected_profitability) < 0.001
    comissao_ok = abs(calculated_item['valor_comissao'] - expected_commission_value) < 0.01
    markup_ok = abs(budget_result['totals']['markup_pedido'] - expected_profitability) < 0.001
    
    print("=== RESULTADO DO TESTE ===")
    print(f"✓ Rentabilidade correta: {'SIM' if rentabilidade_ok else 'NÃO'}")
    print(f"✓ Comissão correta: {'SIM' if comissao_ok else 'NÃO'}")
    print(f"✓ Markup correto: {'SIM' if markup_ok else 'NÃO'}")
    print(f"✓ Teste geral: {'PASSOU' if all([rentabilidade_ok, comissao_ok, markup_ok]) else 'FALHOU'}")

if __name__ == "__main__":
    test_commission_calculation()