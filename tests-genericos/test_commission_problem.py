#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'budget_service'))

from app.services.commission_service import CommissionService

def test_commission_problem():
    print("=== TESTE DETALHADO DO PROBLEMA DA COMISSÃO ===")
    
    # Dados do usuário
    valor_com_icms_venda = 4.32
    valor_com_icms_compra = 2.11  # SEM frete
    frete_por_kg = 0.5
    valor_com_icms_compra_com_frete = valor_com_icms_compra + frete_por_kg  # COM frete = 2.61
    
    print(f"Valor venda unitário: R$ {valor_com_icms_venda}")
    print(f"Valor compra unitário SEM frete: R$ {valor_com_icms_compra}")
    print(f"Valor compra unitário COM frete: R$ {valor_com_icms_compra_com_frete}")
    print()
    
    # Teste 1: Rentabilidade SEM considerar frete (INCORRETO)
    rentabilidade_sem_frete = CommissionService._calculate_unit_profitability_with_icms(
        valor_com_icms_venda, valor_com_icms_compra
    )
    print(f"Rentabilidade SEM frete: {rentabilidade_sem_frete:.4f} ({rentabilidade_sem_frete*100:.2f}%)")
    
    # Teste 2: Rentabilidade COM frete (CORRETO)
    rentabilidade_com_frete = CommissionService._calculate_unit_profitability_with_icms(
        valor_com_icms_venda, valor_com_icms_compra_com_frete
    )
    print(f"Rentabilidade COM frete: {rentabilidade_com_frete:.4f} ({rentabilidade_com_frete*100:.2f}%)")
    print()
    
    # Percentuais de comissão
    percentual_sem_frete = CommissionService.calculate_commission_percentage(rentabilidade_sem_frete)
    percentual_com_frete = CommissionService.calculate_commission_percentage(rentabilidade_com_frete)
    
    print(f"Percentual comissão SEM frete: {percentual_sem_frete:.4f} ({percentual_sem_frete*100:.2f}%)")
    print(f"Percentual comissão COM frete: {percentual_com_frete:.4f} ({percentual_com_frete*100:.2f}%)")
    print()
    
    # Valores de comissão sobre total de venda
    total_venda = 4363.20  # Do exemplo do usuário
    comissao_sem_frete = total_venda * percentual_sem_frete
    comissao_com_frete = total_venda * percentual_com_frete
    
    print(f"Comissão SEM frete: R$ {comissao_sem_frete:.2f}")
    print(f"Comissão COM frete: R$ {comissao_com_frete:.2f}")
    print()
    
    print("=== COMPARAÇÃO COM VALORES ESPERADOS ===")
    print(f"Valor esperado da comissão: R$ 130.90")
    print(f"Percentual esperado: 3%")
    print(f"Rentabilidade esperada: 56.84%")
    print()
    
    print("=== ANÁLISE ===")
    print(f"O sistema está usando valor SEM frete ({valor_com_icms_compra}) para calcular rentabilidade")
    print(f"Deveria usar valor COM frete ({valor_com_icms_compra_com_frete})")
    print(f"Rentabilidade correta seria: {rentabilidade_com_frete*100:.2f}%")
    print(f"Comissão correta seria: R$ {comissao_com_frete:.2f}")
    
    # Verificar se a rentabilidade COM frete está próxima da esperada
    if abs(rentabilidade_com_frete * 100 - 56.84) < 5:
        print("✓ Rentabilidade COM frete está próxima do valor esperado!")
    else:
        print("✗ Rentabilidade COM frete ainda não está correta")
        
    # Verificar se a comissão COM frete está próxima da esperada
    if abs(comissao_com_frete - 130.90) < 10:
        print("✓ Comissão COM frete está próxima do valor esperado!")
    else:
        print("✗ Comissão COM frete ainda não está correta")

if __name__ == "__main__":
    test_commission_problem()