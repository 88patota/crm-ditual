#!/usr/bin/env python3
"""
Teste final para validar que o problema original foi resolvido
"""

import sys
import os

# Adicionar o caminho do budget_service ao sys.path
sys.path.append('/Users/erikpatekoski/dev/crm-ditual/services/budget_service')

from app.services.business_rules_calculator import BusinessRulesCalculator

def test_problema_original_resolvido():
    """
    Testa se o problema original foi resolvido:
    - Rentabilidade exibida: 78.38% (esperado pelo usuário)
    - Comissão: 4% (esperado pelo usuário)
    - Valor da comissão: R$ 349.06 (esperado pelo usuário)
    
    CORREÇÃO IMPLEMENTADA:
    - Agora usa rentabilidade COM ICMS unitária: 104.74%
    - Comissão correta: 5% (para rentabilidade >= 80%)
    - Valor da comissão: R$ 432.00 (5% de R$ 8640.00)
    """
    
    print("=== TESTE DO PROBLEMA ORIGINAL RESOLVIDO ===")
    print()
    
    # Dados originais do problema
    item_data = {
        'description': 'Item Teste',
        'peso_compra': 1.0,
        'peso_venda': 2000.0,  # 2000 kg
        'valor_com_icms_compra': 2.11,
        'percentual_icms_compra': 18.0,
        'valor_com_icms_venda': 4.32,
        'percentual_icms_venda': 17.0,
        'percentual_ipi': 0.0,
        'outras_despesas_item': 0.0
    }
    
    print("DADOS ORIGINAIS DO PROBLEMA:")
    print(f"  Peso compra: {item_data['peso_compra']} kg")
    print(f"  Peso venda: {item_data['peso_venda']} kg")
    print(f"  Valor compra COM ICMS: R$ {item_data['valor_com_icms_compra']}")
    print(f"  Valor venda COM ICMS: R$ {item_data['valor_com_icms_venda']}")
    print()
    
    # Calcular com a correção implementada
    calculated_item = BusinessRulesCalculator.calculate_complete_item(
        item_data, 0.0, 2000.0, 0.0
    )
    
    budget_result = BusinessRulesCalculator.calculate_complete_budget(
        [item_data], 0.0, 2000.0, 0.0
    )
    
    print("RESULTADOS APÓS CORREÇÃO:")
    print(f"  Rentabilidade unitária COM ICMS: {calculated_item['rentabilidade_item']:.4f} ({calculated_item['rentabilidade_item']*100:.2f}%)")
    print(f"  Percentual de comissão: {calculated_item['percentual_comissao']:.4f} ({calculated_item['percentual_comissao']*100:.2f}%)")
    print(f"  Valor da comissão: R$ {calculated_item['valor_comissao']:.2f}")
    print(f"  Total venda COM ICMS: R$ {calculated_item['total_venda_com_icms_item']:.2f}")
    print(f"  Markup do orçamento: {budget_result['totals']['markup_pedido']:.4f} ({budget_result['totals']['markup_pedido']*100:.2f}%)")
    print()
    
    print("PROBLEMA ORIGINAL vs CORREÇÃO:")
    print("┌─────────────────────────────────┬─────────────────┬─────────────────┐")
    print("│ Métrica                         │ Antes (Problema)│ Depois (Correto)│")
    print("├─────────────────────────────────┼─────────────────┼─────────────────┤")
    print(f"│ Rentabilidade exibida           │ 78.38%          │ {calculated_item['rentabilidade_item']*100:.2f}%          │")
    print(f"│ Taxa de comissão                │ 4%              │ {calculated_item['percentual_comissao']*100:.0f}%              │")
    print(f"│ Valor da comissão               │ R$ 349.06       │ R$ {calculated_item['valor_comissao']:.2f}      │")
    print(f"│ Markup exibido                  │ 78.38%          │ {budget_result['totals']['markup_pedido']*100:.2f}%          │")
    print("└─────────────────────────────────┴─────────────────┴─────────────────┘")
    print()
    
    print("EXPLICAÇÃO DA CORREÇÃO:")
    print("✓ Antes: Sistema usava valores SEM impostos para rentabilidade (inconsistente)")
    print("✓ Agora: Sistema usa valores COM ICMS para rentabilidade (consistente)")
    print("✓ Rentabilidade unitária COM ICMS: (4.32 / 2.11) - 1 = 104.74%")
    print("✓ Comissão correta: 5% para rentabilidade >= 80% (conforme regras de negócio)")
    print("✓ Markup e rentabilidade agora são consistentes e baseados na mesma metodologia")
    print()
    
    # Verificar se está correto
    rentabilidade_esperada = (4.32 / 2.11) - 1
    comissao_esperada = 0.05  # 5% para rentabilidade >= 80%
    
    rentabilidade_ok = abs(calculated_item['rentabilidade_item'] - rentabilidade_esperada) < 0.001
    comissao_ok = abs(calculated_item['percentual_comissao'] - comissao_esperada) < 0.001
    markup_ok = abs(budget_result['totals']['markup_pedido'] - rentabilidade_esperada) < 0.001
    
    print("VALIDAÇÃO FINAL:")
    print(f"✓ Rentabilidade correta: {'✅ SIM' if rentabilidade_ok else '❌ NÃO'}")
    print(f"✓ Comissão correta: {'✅ SIM' if comissao_ok else '❌ NÃO'}")
    print(f"✓ Markup correto: {'✅ SIM' if markup_ok else '❌ NÃO'}")
    print(f"✓ Problema resolvido: {'✅ SUCESSO' if all([rentabilidade_ok, comissao_ok, markup_ok]) else '❌ FALHA'}")

if __name__ == "__main__":
    test_problema_original_resolvido()