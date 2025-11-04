#!/usr/bin/env python3
"""
Análise das diferenças entre BudgetCalculatorService e BusinessRulesCalculator
para identificar por que os cálculos de comissão estão divergentes.
"""

from app.services.budget_calculator import BudgetCalculatorService
from app.services.business_rules_calculator import BusinessRulesCalculator
from app.schemas.budget import BudgetItemSimplified

def analyze_calculators_difference():
    """Analisa as diferenças entre os dois calculadores"""
    
    # Dados do usuário
    item_data = BudgetItemSimplified(
        description="item",
        delivery_time="0",
        peso_compra=1000,
        peso_venda=1010,
        valor_com_icms_compra=2.11,
        percentual_icms_compra=0.18,
        outras_despesas_item=0,
        valor_com_icms_venda=4.32,
        percentual_icms_venda=0.18,
        percentual_ipi=0
    )
    
    # Frete total
    freight_value_total = 500
    
    print("=== ANÁLISE DAS DIFERENÇAS ENTRE CALCULADORES ===\n")
    
    # 1. BudgetCalculatorService (usado na API)
    print("1. BudgetCalculatorService (usado na API):")
    budget_result = BudgetCalculatorService.calculate_simplified_item(item_data)
    
    print(f"   - Total Purchase: R$ {budget_result['total_purchase']:.2f}")
    print(f"   - Total Sale: R$ {budget_result['total_sale']:.2f}")
    print(f"   - Profitability: {budget_result['profitability']*100:.2f}%")
    print(f"   - Commission: R$ {budget_result['commission_value']:.2f}")
    print(f"   - Purchase without taxes: R$ {budget_result['purchase_value_without_taxes']:.6f}")
    print(f"   - Sale without taxes: R$ {budget_result['sale_value_without_taxes']:.6f}")
    
    # 2. BusinessRulesCalculator (com frete)
    print("\n2. BusinessRulesCalculator (com frete):")
    
    # Preparar dados do item para BusinessRulesCalculator
    item_dict = {
        'peso_compra': item_data.peso_compra,
        'peso_venda': item_data.peso_venda,
        'valor_com_icms_compra': item_data.valor_com_icms_compra,
        'percentual_icms_compra': item_data.percentual_icms_compra,
        'outras_despesas_item': item_data.outras_despesas_item,
        'valor_com_icms_venda': item_data.valor_com_icms_venda,
        'percentual_icms_venda': item_data.percentual_icms_venda,
        'percentual_ipi': item_data.percentual_ipi
    }
    
    business_result = BusinessRulesCalculator.calculate_complete_item(
        item_data=item_dict,
        outras_despesas_totais=0.0,  # Não há outras despesas totais neste caso
        soma_pesos_pedido=item_data.peso_compra,  # Peso total do pedido
        freight_value_total=freight_value_total
    )
    
    print(f"   - Total Purchase: R$ {business_result['total_compra_item_com_icms']:.2f}")
    print(f"   - Total Sale: R$ {business_result['total_venda_com_icms_item']:.2f}")
    print(f"   - Profitability: {business_result['rentabilidade_item']*100:.2f}%")
    print(f"   - Commission: R$ {business_result['valor_comissao']:.2f}")
    print(f"   - Commission %: {business_result['percentual_comissao']*100:.2f}%")
    
    # 3. Análise das diferenças
    print("\n3. ANÁLISE DAS DIFERENÇAS:")
    
    total_purchase_diff = business_result['total_compra_item_com_icms'] - budget_result['total_purchase']
    profitability_diff = business_result['rentabilidade_item'] - budget_result['profitability']
    commission_diff = business_result['valor_comissao'] - budget_result['commission_value']
    
    print(f"   - Diferença Total Purchase: R$ {total_purchase_diff:.2f}")
    print(f"   - Diferença Profitability: {profitability_diff*100:.2f}%")
    print(f"   - Diferença Commission: R$ {commission_diff:.2f}")
    
    # 4. Explicação das diferenças
    print("\n4. EXPLICAÇÃO DAS DIFERENÇAS:")
    freight_per_kg = freight_value_total / item_data.peso_compra
    valor_com_icms_compra_unitario_com_frete = item_data.valor_com_icms_compra + freight_per_kg
    
    print(f"   - Frete por kg: R$ {freight_per_kg:.2f}")
    print(f"   - Valor compra sem frete: R$ {item_data.valor_com_icms_compra:.2f}")
    print(f"   - Valor compra com frete: R$ {valor_com_icms_compra_unitario_com_frete:.2f}")
    
    print("\n   PROBLEMA IDENTIFICADO:")
    print("   - BudgetCalculatorService NÃO considera frete no cálculo")
    print("   - BusinessRulesCalculator considera frete corretamente")
    print("   - Isso resulta em rentabilidade e comissão diferentes")
    
    # 5. Valores esperados pelo usuário
    print("\n5. VALORES ESPERADOS PELO USUÁRIO:")
    print("   - Comissão: R$ 130.90")
    print("   - Rentabilidade: 56.84%")
    print("   - Percentual comissão: 3%")
    
    print("\n6. CONCLUSÃO:")
    print("   - BusinessRulesCalculator está mais próximo dos valores esperados")
    print("   - BudgetCalculatorService precisa ser corrigido para incluir frete")
    print("   - A API está usando BudgetCalculatorService, por isso os valores estão errados")

if __name__ == "__main__":
    analyze_calculators_difference()