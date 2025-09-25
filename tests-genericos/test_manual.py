#!/usr/bin/env python3
"""
Teste manual dos cálculos após correção
"""

def test_calculations():
    """Teste manual baseado nos dados fornecidos"""
    
    # Dados de entrada
    quantity = 10
    purchase_value_with_icms = 12.45
    purchase_icms_percentage = 12
    purchase_other_expenses = 100
    sale_value_with_icms = 43.10
    sale_icms_percentage = 12
    
    print("=== DADOS DE ENTRADA ===")
    print(f"Quantidade: {quantity}")
    print(f"Valor compra c/ICMS: R$ {purchase_value_with_icms:.2f}")
    print(f"ICMS compra: {purchase_icms_percentage}%")
    print(f"Outras despesas: R$ {purchase_other_expenses:.2f}")
    print(f"Valor venda c/ICMS: R$ {sale_value_with_icms:.2f}")
    print(f"ICMS venda: {sale_icms_percentage}%")
    print()
    
    # Cálculos
    purchase_value_without_taxes = purchase_value_with_icms * (1 - purchase_icms_percentage / 100)
    sale_value_without_taxes = sale_value_with_icms * (1 - sale_icms_percentage / 100)
    
    print("=== VALORES SEM IMPOSTOS (UNITÁRIOS) ===")
    print(f"Compra s/ICMS: R$ {purchase_value_without_taxes:.3f}")
    print(f"Venda s/ICMS: R$ {sale_value_without_taxes:.3f}")
    print()
    
    # Custo total unitário
    total_unit_cost = purchase_value_without_taxes + purchase_other_expenses
    print(f"Custo total unitário: R$ {total_unit_cost:.3f}")
    print()
    
    # Markup individual
    markup_percentage = ((sale_value_without_taxes - total_unit_cost) / total_unit_cost) * 100
    print(f"Markup individual: {markup_percentage:.2f}%")
    print()
    
    # Totais
    total_purchase = total_unit_cost * quantity
    total_sale_without_taxes = sale_value_without_taxes * quantity
    total_sale_with_taxes = sale_value_with_icms * quantity
    
    print("=== TOTAIS ===")
    print(f"Total compra: R$ {total_purchase:.2f}")
    print(f"Total venda s/ICMS: R$ {total_sale_without_taxes:.2f}")
    print(f"Total venda c/ICMS: R$ {total_sale_with_taxes:.2f}")
    print()
    
    # Rentabilidade geral (usando valores sem ICMS para consistência)
    profitability_percentage = ((total_sale_without_taxes - total_purchase) / total_purchase) * 100
    print(f"Rentabilidade geral (s/ICMS): {profitability_percentage:.2f}%")
    
    # Comissão (sobre valor COM ICMS)
    commission_percentage = 1.5
    commission_value = total_sale_with_taxes * (commission_percentage / 100)
    print(f"Comissão (1,5% sobre venda c/ICMS): R$ {commission_value:.3f}")
    print()
    
    print("=== VALORES ESPERADOS ===")
    print(f"total_purchase_value: {total_purchase:.2f}")
    print(f"total_sale_value: {total_sale_without_taxes:.2f}")  # SEM ICMS para consistência
    print(f"total_commission: {commission_value:.3f}")
    print(f"profitability_percentage: {profitability_percentage:.2f}")
    print(f"markup_percentage: {markup_percentage:.2f}")

if __name__ == "__main__":
    test_calculations()
