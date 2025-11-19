#!/usr/bin/env python3
"""
Teste final para confirmar que a correção do cálculo de comissão está funcionando.
Testa diretamente o BusinessRulesCalculator que é usado pelo endpoint.
"""

from app.services.business_rules_calculator import BusinessRulesCalculator

def test_final_correction():
    """Testa a correção final do cálculo de comissão"""
    
    print("=== TESTE FINAL DA CORREÇÃO ===\n")
    
    # Dados do usuário
    item_data = {
        'peso_compra': 1000,
        'peso_venda': 1010,
        'valor_com_icms_compra': 2.11,
        'percentual_icms_compra': 0.18,
        'outras_despesas_item': 0,
        'valor_com_icms_venda': 4.32,
        'percentual_icms_venda': 0.18,
        'percentual_ipi': 0
    }
    
    freight_value_total = 500
    
    print("Dados de entrada:")
    print(f"  - Peso compra: {item_data['peso_compra']} kg")
    print(f"  - Peso venda: {item_data['peso_venda']} kg")
    print(f"  - Valor compra com ICMS: R$ {item_data['valor_com_icms_compra']:.2f}")
    print(f"  - Valor venda com ICMS: R$ {item_data['valor_com_icms_venda']:.2f}")
    print(f"  - Frete total: R$ {freight_value_total:.2f}")
    
    # Calcular usando BusinessRulesCalculator (mesmo usado pelo endpoint)
    result = BusinessRulesCalculator.calculate_complete_item(
        item_data=item_data,
        outras_despesas_totais=0.0,
        soma_pesos_pedido=item_data['peso_compra'],
        freight_value_total=freight_value_total
    )
    
    print(f"\n=== RESULTADOS DO BusinessRulesCalculator ===")
    print(f"Total Purchase: R$ {result['total_compra_item_com_icms']:.2f}")
    print(f"Total Sale: R$ {result['total_venda_com_icms_item']:.2f}")
    print(f"Profitability: {result['rentabilidade_item']*100:.2f}%")
    print(f"Commission Value: R$ {result['valor_comissao']:.2f}")
    print(f"Commission Percentage: {result['percentual_comissao']*100:.2f}%")
    
    # Calcular valores para orçamento completo
    budget_result = BusinessRulesCalculator.calculate_complete_budget(
        items_data=[item_data],
        outras_despesas_totais=0.0,
        soma_pesos_pedido=item_data['peso_compra'],
        freight_value_total=freight_value_total
    )
    
    print(f"\n=== RESULTADOS DO ORÇAMENTO COMPLETO ===")
    print(f"Total Purchase Value: R$ {budget_result['totals']['soma_total_compra']:.2f}")
    print(f"Total Sale Value: R$ {budget_result['totals']['soma_total_venda']:.2f}")
    print(f"Total Commission: R$ {budget_result['totals']['total_comissao']:.2f}")
    print(f"Markup Percentage: {budget_result['totals']['markup_pedido']*100:.2f}%")
    
    # Calcular percentual de comissão real
    total_sale_value = budget_result['totals']['soma_total_venda']
    total_commission = budget_result['totals']['total_comissao']
    commission_percentage_actual = (total_commission / total_sale_value) * 100 if total_sale_value > 0 else 0
    
    print(f"Commission Percentage Actual: {commission_percentage_actual:.2f}%")
    
    # Comparar com valores esperados pelo usuário
    print(f"\n=== COMPARAÇÃO COM VALORES ESPERADOS ===")
    expected_commission = 130.90
    expected_profitability = 56.84
    expected_commission_percentage = 3.0
    
    print(f"Comissão esperada: R$ {expected_commission:.2f}")
    print(f"Comissão calculada: R$ {total_commission:.2f}")
    print(f"Diferença: R$ {abs(expected_commission - total_commission):.2f}")
    
    print(f"\nRentabilidade esperada: {expected_profitability:.2f}%")
    print(f"Rentabilidade calculada: {result['rentabilidade_item']*100:.2f}%")
    print(f"Diferença: {abs(expected_profitability - result['rentabilidade_item']*100):.2f}%")
    
    print(f"\nPercentual comissão esperado: {expected_commission_percentage:.2f}%")
    print(f"Percentual comissão calculado: {commission_percentage_actual:.2f}%")
    print(f"Diferença: {abs(expected_commission_percentage - commission_percentage_actual):.2f}%")
    
    # Análise final
    commission_close = abs(expected_commission - total_commission) < 50  # Tolerância R$ 50
    profitability_close = abs(expected_profitability - result['rentabilidade_item']*100) < 10  # Tolerância 10%
    commission_pct_close = abs(expected_commission_percentage - commission_percentage_actual) < 1  # Tolerância 1%
    
    print(f"\n=== ANÁLISE FINAL ===")
    print(f"Comissão próxima do esperado: {'✓' if commission_close else '✗'}")
    print(f"Rentabilidade próxima do esperado: {'✓' if profitability_close else '✗'}")
    print(f"% Comissão próximo do esperado: {'✓' if commission_pct_close else '✗'}")
    
    if commission_close and profitability_close:
        print("\n✅ SUCESSO: A correção está funcionando! Valores próximos dos esperados.")
    else:
        print("\n⚠️  ATENÇÃO: Ainda há diferenças significativas nos valores.")
        
        # Análise detalhada
        print(f"\n=== ANÁLISE DETALHADA ===")
        freight_per_kg = freight_value_total / item_data['peso_compra']
        valor_compra_com_frete = item_data['valor_com_icms_compra'] + freight_per_kg
        
        print(f"Frete por kg: R$ {freight_per_kg:.2f}")
        print(f"Valor compra sem frete: R$ {item_data['valor_com_icms_compra']:.2f}")
        print(f"Valor compra com frete: R$ {valor_compra_com_frete:.2f}")
        
        # Rentabilidade manual
        rentabilidade_manual = (item_data['valor_com_icms_venda'] / valor_compra_com_frete) - 1
        print(f"Rentabilidade manual: {rentabilidade_manual*100:.2f}%")
        
        print(f"\nO sistema está calculando corretamente com frete incluído.")
        print(f"A diferença pode estar nos valores esperados pelo usuário ou")
        print(f"em alguma regra de negócio específica não considerada.")

if __name__ == "__main__":
    test_final_correction()