#!/usr/bin/env python3
"""
Teste com o payload fornecido pelo usuário
Rentabilidade esperada: 78.38%
Taxa de comissão esperada: 4%
"""

import sys
import os
sys.path.append('/Users/erikpatekoski/dev/crm-ditual/services/budget_service')

from app.services.business_rules_calculator import BusinessRulesCalculator

def test_payload_usuario():
    """Testa com o payload exato fornecido pelo usuário"""
    
    # Payload fornecido pelo usuário
    payload = {
        "order_number": "PED-0015",
        "client_name": "Cliente Teste", 
        "status": "draft",
        "payment_condition": "À vista",
        "freight_type": "FOB",
        "freight_value_total": 500,
        "notes": None,
        "total_purchase_value": 3640.314,
        "total_sale_value": 6493.75056,
        "profitability_percentage": 0.7838435255859797,
        "markup_percentage": 0.7838435255859797,
        "total_ipi_value": 0,
        "valor_frete_compra": 0,
        "total_final_value": 8726.400000000001,
        "items": [
            {
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
            },
            {
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
        ]
    }
    
    print("=== ANÁLISE DO PAYLOAD DO USUÁRIO ===")
    print(f"Rentabilidade esperada pelo usuário: {payload['profitability_percentage']:.4f} = {payload['profitability_percentage']*100:.2f}%")
    print(f"Total compra informado: R$ {payload['total_purchase_value']:.2f}")
    print(f"Total venda informado: R$ {payload['total_sale_value']:.2f}")
    
    # Calcular manualmente a rentabilidade baseada nos totais informados
    rentabilidade_manual = ((payload['total_sale_value'] - payload['total_purchase_value']) / payload['total_purchase_value']) * 100
    print(f"Rentabilidade calculada manualmente: {rentabilidade_manual:.2f}%")
    
    print("\n=== ANÁLISE DOS ITENS ===")
    for i, item in enumerate(payload['items'], 1):
        print(f"\nItem {i}:")
        print(f"  Peso compra: {item['peso_compra']} kg")
        print(f"  Peso venda: {item['peso_venda']} kg") 
        print(f"  Valor unitário compra (com ICMS): R$ {item['valor_com_icms_compra']}")
        print(f"  Valor unitário venda (com ICMS): R$ {item['valor_com_icms_venda']}")
        
        # Calcular totais do item
        total_compra_item = item['peso_compra'] * item['valor_com_icms_compra']
        total_venda_item = item['peso_venda'] * item['valor_com_icms_venda']
        
        print(f"  Total compra item: {item['peso_compra']} x {item['valor_com_icms_compra']} = R$ {total_compra_item:.2f}")
        print(f"  Total venda item: {item['peso_venda']} x {item['valor_com_icms_venda']} = R$ {total_venda_item:.2f}")
        
        # Rentabilidade do item
        rentabilidade_item = ((total_venda_item - total_compra_item) / total_compra_item) * 100
        print(f"  Rentabilidade item: {rentabilidade_item:.2f}%")
    
    print("\n=== TESTE COM BUSINESS RULES CALCULATOR ===")
    
    # Calcular soma dos pesos e outras despesas
    soma_pesos_pedido = sum(item['peso_compra'] for item in payload['items'])
    outras_despesas_totais = sum(item['outras_despesas_item'] for item in payload['items'])
    
    print(f"Soma pesos pedido: {soma_pesos_pedido}")
    print(f"Outras despesas totais: {outras_despesas_totais}")
    
    # Testar primeiro item
    item1 = payload['items'][0]
    resultado_item1 = BusinessRulesCalculator.calculate_complete_item(
        item1, outras_despesas_totais, soma_pesos_pedido
    )
    
    print(f"Resultado BusinessRulesCalculator - Item 1:")
    print(f"  Rentabilidade: {resultado_item1['rentabilidade_item']:.2f}%")
    print(f"  Total compra com ICMS: R$ {resultado_item1['total_compra_item_com_icms']:.2f}")
    print(f"  Total venda com ICMS: R$ {resultado_item1['total_venda_com_icms_item']:.2f}")
    
    # Testar cálculo completo do orçamento
    resultado_orcamento = BusinessRulesCalculator.calculate_complete_budget(
        payload['items'], outras_despesas_totais, soma_pesos_pedido
    )
    
    print(f"\nResultado BusinessRulesCalculator - Orçamento completo:")
    print(f"  Markup: {resultado_orcamento['totals']['markup_pedido']:.4f} ({resultado_orcamento['totals']['markup_pedido']*100:.2f}%)")
    
    # Calcular rentabilidade do orçamento manualmente baseada nos totais
    soma_total_venda_com_icms = resultado_orcamento['totals']['soma_total_venda_com_icms']
    soma_total_compra_com_icms = sum(item['total_compra_item_com_icms'] for item in resultado_orcamento['items'])
    
    if soma_total_compra_com_icms > 0:
        rentabilidade_orcamento = ((soma_total_venda_com_icms - soma_total_compra_com_icms) / soma_total_compra_com_icms) * 100
    else:
        rentabilidade_orcamento = 0.0
    
    print(f"  Rentabilidade calculada: {rentabilidade_orcamento:.2f}%")
    
    # Determinar taxa de comissão baseada na rentabilidade
    if rentabilidade_orcamento >= 80:
        taxa_comissao = 5
    elif rentabilidade_orcamento >= 60:
        taxa_comissao = 4
    elif rentabilidade_orcamento >= 40:
        taxa_comissao = 3
    elif rentabilidade_orcamento >= 20:
        taxa_comissao = 2
    else:
        taxa_comissao = 1
    
    print(f"  Taxa de comissão calculada: {taxa_comissao}%")
    
    print("\n=== COMPARAÇÃO ===")
    print(f"Esperado pelo usuário: 78.38%")
    print(f"Calculado pelo sistema: {rentabilidade_orcamento:.2f}%")
    print(f"Diferença: {abs(78.38 - rentabilidade_orcamento):.2f} pontos percentuais")
    
    # Verificar se está correto
    if abs(78.38 - rentabilidade_orcamento) < 0.1:
        print("✅ RENTABILIDADE CORRETA!")
    else:
        print("❌ RENTABILIDADE INCORRETA!")
        
    if taxa_comissao == 4:
        print("✅ TAXA DE COMISSÃO CORRETA!")
    else:
        print("❌ TAXA DE COMISSÃO INCORRETA!")

if __name__ == "__main__":
    test_payload_usuario()