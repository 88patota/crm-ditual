#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'budget_service'))

from app.services.commission_service import CommissionService

def debug_calculation():
    print("=== DEBUG DETALHADO DO CÁLCULO ===")
    
    # Dados do usuário
    valor_com_icms_venda = 4.32
    valor_com_icms_compra = 2.11
    frete_por_kg = 0.5
    valor_com_icms_compra_com_frete = valor_com_icms_compra + frete_por_kg
    
    print(f"Valor venda unitário: {valor_com_icms_venda}")
    print(f"Valor compra unitário SEM frete: {valor_com_icms_compra}")
    print(f"Frete por kg: {frete_por_kg}")
    print(f"Valor compra unitário COM frete: {valor_com_icms_compra_com_frete}")
    print()
    
    # Teste manual da fórmula de rentabilidade
    print("=== CÁLCULO MANUAL DA RENTABILIDADE ===")
    rentabilidade_manual = (valor_com_icms_venda / valor_com_icms_compra_com_frete) - 1
    print(f"Rentabilidade manual: {rentabilidade_manual:.6f} ({rentabilidade_manual*100:.2f}%)")
    
    # Teste usando o método do sistema
    print("=== CÁLCULO USANDO MÉTODO DO SISTEMA ===")
    rentabilidade_sistema = CommissionService._calculate_unit_profitability_with_icms(
        valor_com_icms_venda, valor_com_icms_compra_com_frete
    )
    print(f"Rentabilidade sistema: {rentabilidade_sistema:.6f} ({rentabilidade_sistema*100:.2f}%)")
    
    # Verificar se são iguais
    if abs(rentabilidade_manual - rentabilidade_sistema) < 0.0001:
        print("✓ Cálculos são consistentes")
    else:
        print("✗ Há diferença entre os cálculos!")
    
    print()
    
    # Testar percentual de comissão
    print("=== CÁLCULO DO PERCENTUAL DE COMISSÃO ===")
    percentual_comissao = CommissionService.calculate_commission_percentage(rentabilidade_sistema)
    print(f"Percentual de comissão: {percentual_comissao:.6f} ({percentual_comissao*100:.2f}%)")
    
    # Verificar faixas de comissão
    print("\n=== FAIXAS DE COMISSÃO ===")
    for bracket in CommissionService.COMMISSION_BRACKETS:
        min_val = bracket["min_profitability"]
        max_val = bracket["max_profitability"]
        rate = bracket["commission_rate"]
        print(f"Faixa: {min_val:.2f} - {max_val:.2f} = {rate:.3f} ({rate*100:.1f}%)")
        
        if rentabilidade_sistema >= min_val and rentabilidade_sistema <= max_val:
            print(f"  ✓ Rentabilidade {rentabilidade_sistema:.4f} está nesta faixa!")
    
    print()
    
    # Calcular valor da comissão
    total_venda = 4363.20
    valor_comissao = total_venda * percentual_comissao
    print(f"Valor da comissão: R$ {valor_comissao:.2f}")
    
    print("\n=== COMPARAÇÃO COM VALORES ESPERADOS ===")
    print(f"Esperado: Rentabilidade ~56.84%, Comissão 3%, Valor R$ 130.90")
    print(f"Calculado: Rentabilidade {rentabilidade_sistema*100:.2f}%, Comissão {percentual_comissao*100:.2f}%, Valor R$ {valor_comissao:.2f}")
    
    # Calcular qual rentabilidade daria 3% de comissão
    print("\n=== ANÁLISE REVERSA ===")
    print("Para ter 3% de comissão, a rentabilidade deveria estar na faixa 50-59.99%")
    rentabilidade_para_3_porcento = 0.55  # 55% está na faixa de 3%
    valor_compra_necessario = valor_com_icms_venda / (1 + rentabilidade_para_3_porcento)
    frete_necessario = valor_compra_necessario - valor_com_icms_compra
    
    print(f"Para rentabilidade de 55% (3% comissão):")
    print(f"- Valor compra COM frete deveria ser: R$ {valor_compra_necessario:.4f}")
    print(f"- Frete necessário seria: R$ {frete_necessario:.4f} por kg")
    print(f"- Frete atual é: R$ {frete_por_kg:.4f} por kg")

if __name__ == "__main__":
    debug_calculation()