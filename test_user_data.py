#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'budget_service'))

from app.services.business_rules_calculator import BusinessRulesCalculator
from app.services.commission_service import CommissionService

def test_user_data():
    print("=== TESTE COM DADOS DO USUÁRIO ===")
    
    # Dados fornecidos pelo usuário
    freight_value_total = 500
    peso_compra = 1000
    peso_venda = 1010
    valor_com_icms_compra = 2.11
    valor_com_icms_venda = 4.32
    
    print(f"Dados de entrada:")
    print(f"- Frete total: R$ {freight_value_total}")
    print(f"- Peso compra: {peso_compra} kg")
    print(f"- Peso venda: {peso_venda} kg")
    print(f"- Valor com ICMS compra: R$ {valor_com_icms_compra}")
    print(f"- Valor com ICMS venda: R$ {valor_com_icms_venda}")
    print()
    
    # Calcular frete distribuído por kg
    frete_distribuido_por_kg = freight_value_total / peso_compra
    print(f"Frete distribuído por kg: R$ {frete_distribuido_por_kg:.4f}")
    
    # Calcular valor unitário com frete
    valor_com_icms_compra_unitario_com_frete = valor_com_icms_compra + frete_distribuido_por_kg
    print(f"Valor unitário com frete: R$ {valor_com_icms_compra_unitario_com_frete:.4f}")
    
    # Calcular totais
    total_compra_item_com_icms = peso_compra * valor_com_icms_compra_unitario_com_frete
    total_venda_item_com_icms = peso_venda * valor_com_icms_venda
    
    print(f"Total compra COM ICMS (item): R$ {total_compra_item_com_icms:.2f}")
    print(f"Total venda COM ICMS (item): R$ {total_venda_item_com_icms:.2f}")
    
    # Calcular rentabilidade
    rentabilidade_item = ((total_venda_item_com_icms - total_compra_item_com_icms) / total_compra_item_com_icms) * 100
    print(f"Rentabilidade calculada: {rentabilidade_item:.2f}%")
    
    # Calcular markup
    markup_pedido = ((total_venda_item_com_icms - total_compra_item_com_icms) / total_venda_item_com_icms) * 100
    print(f"Markup calculado: {markup_pedido:.2f}%")
    
    print("\n=== CÁLCULO DA COMISSÃO ===")
    
    # Calcular comissão usando o serviço
    commission_service = CommissionService()
    
    # Testar o cálculo da rentabilidade unitária
    rentabilidade_unitaria = commission_service._calculate_unit_profitability_with_icms(
        valor_com_icms_venda, valor_com_icms_compra_unitario_com_frete
    )
    print(f"Rentabilidade unitária: {rentabilidade_unitaria:.2f}%")
    
    # Calcular percentual de comissão
    percentual_comissao = commission_service.calculate_commission_percentage(rentabilidade_unitaria)
    print(f"Percentual de comissão: {percentual_comissao:.2f}%")
    
    # Calcular valor da comissão
    valor_comissao = commission_service.calculate_commission_value_with_quantity_adjustment(
        total_venda_item_com_icms,
        total_compra_item_com_icms,
        peso_venda,
        peso_compra,
        valor_com_icms_venda,
        valor_com_icms_compra_unitario_com_frete
    )
    print(f"Valor da comissão: R$ {valor_comissao:.2f}")
    
    print("\n=== COMPARAÇÃO COM VALORES CORRETOS ===")
    print(f"Sistema calculou:")
    print(f"- Comissão: R$ {valor_comissao:.2f}")
    print(f"- Rentabilidade: {rentabilidade_item:.2f}%")
    print(f"- Percentual comissão: {percentual_comissao:.2f}%")
    
    print(f"\nValores corretos esperados:")
    print(f"- Comissão: R$ 130.90")
    print(f"- Rentabilidade: 56.84%")
    print(f"- Percentual comissão: 3%")
    
    print(f"\nDiferenças:")
    print(f"- Comissão: R$ {valor_comissao - 130.90:.2f}")
    print(f"- Rentabilidade: {rentabilidade_item - 56.84:.2f}%")
    print(f"- Percentual comissão: {percentual_comissao - 3:.2f}%")

if __name__ == "__main__":
    test_user_data()