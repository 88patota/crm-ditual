#!/usr/bin/env python3
"""
Teste para reproduzir o problema do frete que está causando rentabilidade negativa incorreta
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'budget_service'))

from app.services.business_rules_calculator import BusinessRulesCalculator

def test_freight_problem():
    """Teste baseado nos dados fornecidos pelo usuário"""
    
    # Dados do item conforme fornecido pelo usuário
    item_data = {
        "description": "item",
        "delivery_time": "0",
        "peso_compra": 1000,
        "peso_venda": 1010,
        "valor_com_icms_compra": 2.11,
        "percentual_icms_compra": 0.18,
        "outras_despesas_item": 0,
        "valor_com_icms_venda": 4.32,
        "percentual_icms_venda": 0.18,
        "percentual_ipi": 0
    }
    
    items_data = [item_data]
    outras_despesas_totais = 0.0
    soma_pesos_pedido = 1000.0  # peso_compra do item
    
    print("=== TESTE SEM FRETE ===")
    freight_value_total = 0.0
    
    result_sem_frete = BusinessRulesCalculator.calculate_complete_budget(
        items_data, outras_despesas_totais, soma_pesos_pedido, freight_value_total
    )
    
    item_sem_frete = result_sem_frete['items'][0]
    totals_sem_frete = result_sem_frete['totals']
    
    print(f"Total compra: {totals_sem_frete['soma_total_compra']:.2f}")
    print(f"Total venda: {totals_sem_frete['soma_total_venda']:.2f}")
    print(f"Total venda COM ICMS: {totals_sem_frete['soma_total_venda_com_icms']:.2f}")
    print(f"Total comissão: {totals_sem_frete['total_comissao']:.2f}")
    print(f"Markup pedido: {totals_sem_frete['markup_pedido'] * 100:.2f}%")
    print(f"Rentabilidade item: {item_sem_frete['rentabilidade_item'] * 100:.2f}%")
    print(f"Valor compra COM ICMS (item): {item_sem_frete['valor_com_icms_compra']:.2f}")
    print(f"Total compra COM ICMS (item): {item_sem_frete['total_compra_item_com_icms']:.2f}")
    
    print("\n=== TESTE COM FRETE R$ 200 ===")
    freight_value_total = 200.0
    
    result_com_frete = BusinessRulesCalculator.calculate_complete_budget(
        items_data, outras_despesas_totais, soma_pesos_pedido, freight_value_total
    )
    
    item_com_frete = result_com_frete['items'][0]
    totals_com_frete = result_com_frete['totals']
    
    print(f"Total compra: {totals_com_frete['soma_total_compra']:.2f}")
    print(f"Total venda: {totals_com_frete['soma_total_venda']:.2f}")
    print(f"Total venda COM ICMS: {totals_com_frete['soma_total_venda_com_icms']:.2f}")
    print(f"Total comissão: {totals_com_frete['total_comissao']:.2f}")
    print(f"Markup pedido: {totals_com_frete['markup_pedido'] * 100:.2f}%")
    print(f"Rentabilidade item: {item_com_frete['rentabilidade_item'] * 100:.2f}%")
    print(f"Frete distribuído por kg: {item_com_frete['frete_distribuido_por_kg']:.2f}")
    print(f"Valor compra COM ICMS (item): {item_com_frete['valor_com_icms_compra']:.2f}")
    print(f"Total compra COM ICMS (item): {item_com_frete['total_compra_item_com_icms']:.2f}")
    
    print("\n=== ANÁLISE DO PROBLEMA ===")
    print(f"Diferença na comissão: {totals_com_frete['total_comissao'] - totals_sem_frete['total_comissao']:.2f}")
    print(f"Diferença no markup: {(totals_com_frete['markup_pedido'] - totals_sem_frete['markup_pedido']) * 100:.2f}%")
    print(f"Diferença na rentabilidade: {(item_com_frete['rentabilidade_item'] - item_sem_frete['rentabilidade_item']) * 100:.2f}%")
    
    # Verificar se o frete está sendo incluído corretamente
    expected_valor_com_icms_compra_com_frete = item_sem_frete['valor_com_icms_compra'] + (200.0 / 1000.0)  # R$ 0.20 por kg
    print(f"Valor COM ICMS esperado com frete: {expected_valor_com_icms_compra_com_frete:.2f}")
    print(f"Valor COM ICMS calculado com frete: {item_com_frete['valor_com_icms_compra'] + item_com_frete['frete_distribuido_por_kg']:.2f}")

if __name__ == "__main__":
    test_freight_problem()