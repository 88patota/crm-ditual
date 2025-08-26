#!/usr/bin/env python3
"""
Script para revisar e validar as faixas de comissão
Verifica inconsistências, gaps ou sobreposições nas faixas de porcentagem
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'budget_service'))

from services.budget_service.app.services.commission_service import CommissionService

def test_commission_brackets():
    """Testa e valida as faixas de comissão"""
    
    print("=== REVISÃO DAS FAIXAS DE COMISSÃO ===\n")
    
    # 1. Exibir faixas atuais
    print("1. FAIXAS ATUAIS:")
    brackets = CommissionService.COMMISSION_BRACKETS
    for i, bracket in enumerate(brackets):
        min_perc = bracket["min_profitability"] * 100
        max_perc = bracket["max_profitability"] * 100 if bracket["max_profitability"] != float('inf') else "∞"
        comm_perc = bracket["commission_rate"] * 100
        
        if i == 0:
            range_desc = f"< {max_perc}%"
        elif bracket["max_profitability"] == float('inf'):
            range_desc = f">= {min_perc}%"
        else:
            range_desc = f"{min_perc}% - {max_perc}%"
            
        print(f"   Faixa {i+1}: {range_desc:15} → Comissão: {comm_perc:4.1f}%")
    
    print("\n" + "="*60)
    
    # 2. Testar valores limítrofes
    print("\n2. TESTE DE VALORES LIMÍTROFES:")
    test_values = [0.19, 0.20, 0.29, 0.30, 0.39, 0.40, 0.49, 0.50, 0.59, 0.60, 0.79, 0.80, 0.99, 1.50]
    
    for rentabilidade in test_values:
        commission_perc = CommissionService.calculate_commission_percentage(rentabilidade)
        print(f"   Rentabilidade: {rentabilidade*100:6.1f}% → Comissão: {commission_perc*100:4.1f}%")
    
    print("\n" + "="*60)
    
    # 3. Verificar gaps e sobreposições
    print("\n3. VERIFICAÇÃO DE CONSISTÊNCIA:")
    
    gaps_found = False
    overlaps_found = False
    
    # Verificar se há gaps entre faixas
    for i in range(len(brackets) - 1):
        current_max = brackets[i]["max_profitability"]
        next_min = brackets[i + 1]["min_profitability"]
        
        if current_max != next_min:
            if current_max < next_min:
                print(f"   ⚠️  GAP encontrado: Entre {current_max*100}% e {next_min*100}%")
                gaps_found = True
            else:
                print(f"   ❌ SOBREPOSIÇÃO encontrada: {current_max*100}% > {next_min*100}%")
                overlaps_found = True
    
    # Verificar se a primeira faixa começa em 0
    if brackets[0]["min_profitability"] != 0.0:
        print(f"   ⚠️  PROBLEMA: Primeira faixa não começa em 0% (começa em {brackets[0]['min_profitability']*100}%)")
    
    # Verificar se a última faixa vai até infinito
    if brackets[-1]["max_profitability"] != float('inf'):
        print(f"   ⚠️  PROBLEMA: Última faixa não vai até infinito (termina em {brackets[-1]['max_profitability']*100}%)")
    
    if not gaps_found and not overlaps_found:
        print("   ✅ Todas as faixas estão corretamente conectadas")
    
    print("\n" + "="*60)
    
    # 4. Verificar lógica de negócio
    print("\n4. VERIFICAÇÃO DE LÓGICA DE NEGÓCIO:")
    
    # Verificar se comissões são crescentes
    commission_rates = [bracket["commission_rate"] for bracket in brackets]
    is_ascending = all(commission_rates[i] <= commission_rates[i+1] for i in range(len(commission_rates)-1))
    
    if is_ascending:
        print("   ✅ Taxas de comissão são crescentes (incentivo correto)")
    else:
        print("   ❌ Taxas de comissão NÃO são crescentes")
        for i in range(len(commission_rates)-1):
            if commission_rates[i] > commission_rates[i+1]:
                print(f"      Problema: Faixa {i+1} ({commission_rates[i]*100}%) > Faixa {i+2} ({commission_rates[i+1]*100}%)")
    
    print("\n" + "="*60)
    
    # 5. Exemplos práticos
    print("\n5. EXEMPLOS PRÁTICOS DE CÁLCULO:")
    
    examples = [
        {"description": "Item com baixa margem", "purchase": 1000, "sale": 1150, "expected_bracket": "< 20%"},
        {"description": "Item com margem padrão", "purchase": 1000, "sale": 1250, "expected_bracket": "20-30%"},
        {"description": "Item com boa margem", "purchase": 1000, "sale": 1350, "expected_bracket": "30-40%"},
        {"description": "Item com alta margem", "purchase": 1000, "sale": 1450, "expected_bracket": "40-50%"},
        {"description": "Item com margem premium", "purchase": 1000, "sale": 1550, "expected_bracket": "50-60%"},
        {"description": "Item com margem excelente", "purchase": 1000, "sale": 1700, "expected_bracket": "60-80%"},
        {"description": "Item com margem excepcional", "purchase": 1000, "sale": 2000, "expected_bracket": "≥ 80%"},
    ]
    
    for example in examples:
        purchase = example["purchase"]
        sale = example["sale"]
        profitability = (sale / purchase) - 1
        commission_rate = CommissionService.calculate_commission_percentage(profitability)
        commission_value = CommissionService.calculate_commission_value(sale, profitability)
        
        print(f"   {example['description']:<30}")
        print(f"      Compra: R$ {purchase:>8.2f} | Venda: R$ {sale:>8.2f}")
        print(f"      Rentabilidade: {profitability*100:>6.1f}% | Comissão: {commission_rate*100:>4.1f}% | Valor: R$ {commission_value:>6.2f}")
        print(f"      Faixa esperada: {example['expected_bracket']}")
        print()
    
    print("=" * 60)
    
    # 6. Recomendações
    print("\n6. ANÁLISE E RECOMENDAÇÕES:")
    
    print("   PONTOS POSITIVOS:")
    print("   ✅ Estrutura progressiva incentiva vendas de alta margem")
    print("   ✅ Faixas bem distribuídas entre 0% e 80% de rentabilidade")
    print("   ✅ Comissão máxima de 5% é razoável")
    print("   ✅ Faixa de 0% para itens de baixa margem protege a empresa")
    
    print("\n   POSSÍVEIS MELHORIAS:")
    print("   💡 Considerar faixa intermediária entre 0-20% (ex: 10-20% = 0.5%)")
    print("   💡 Avaliar se 1.5% na faixa 30-40% não deveria ser 2%")
    print("   💡 Considerar feedback dos vendedores sobre os incentivos")
    
    print("\n   VALIDAÇÃO TÉCNICA:")
    if not gaps_found and not overlaps_found and is_ascending:
        print("   ✅ IMPLEMENTAÇÃO CORRETA - Sem problemas técnicos identificados")
    else:
        print("   ⚠️  ATENÇÃO - Problemas técnicos identificados acima")

if __name__ == "__main__":
    test_commission_brackets()