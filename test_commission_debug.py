#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'budget_service'))

from app.services.commission_service import CommissionService

# Dados do teste
valor_com_icms_venda = 4.32
valor_com_icms_compra_sem_frete = 2.11
valor_com_icms_compra_com_frete = 2.31  # 2.11 + 0.20 de frete
total_venda_item_com_icms = 4363.20
total_compra_item_com_icms_sem_frete = 2110.00
total_compra_item_com_icms_com_frete = 2310.00
peso_venda = 1010.0
peso_compra = 1000.0

print("=== TESTE DE COMISSÃO ===")

# Teste 1: Sem frete
print("\n--- SEM FRETE ---")
rentabilidade_sem_frete = CommissionService._calculate_unit_profitability_with_icms(
    valor_com_icms_venda, valor_com_icms_compra_sem_frete
)
print(f"Rentabilidade unitária sem frete: {rentabilidade_sem_frete:.4f} ({rentabilidade_sem_frete*100:.2f}%)")

percentual_comissao_sem_frete = CommissionService.calculate_commission_percentage(rentabilidade_sem_frete)
print(f"Percentual comissão sem frete: {percentual_comissao_sem_frete:.4f} ({percentual_comissao_sem_frete*100:.2f}%)")

valor_comissao_sem_frete = CommissionService.calculate_commission_value_with_quantity_adjustment(
    total_venda_item_com_icms, total_compra_item_com_icms_sem_frete, peso_venda, peso_compra, 
    valor_com_icms_venda, valor_com_icms_compra_sem_frete
)
print(f"Valor comissão sem frete: R$ {valor_comissao_sem_frete:.2f}")

# Teste 2: Com frete
print("\n--- COM FRETE ---")
rentabilidade_com_frete = CommissionService._calculate_unit_profitability_with_icms(
    valor_com_icms_venda, valor_com_icms_compra_com_frete
)
print(f"Rentabilidade unitária com frete: {rentabilidade_com_frete:.4f} ({rentabilidade_com_frete*100:.2f}%)")

percentual_comissao_com_frete = CommissionService.calculate_commission_percentage(rentabilidade_com_frete)
print(f"Percentual comissão com frete: {percentual_comissao_com_frete:.4f} ({percentual_comissao_com_frete*100:.2f}%)")

# PROBLEMA: Estamos passando valor_com_icms_compra_com_frete, mas o método usa o último parâmetro
valor_comissao_com_frete = CommissionService.calculate_commission_value_with_quantity_adjustment(
    total_venda_item_com_icms, total_compra_item_com_icms_com_frete, peso_venda, peso_compra, 
    valor_com_icms_venda, valor_com_icms_compra_com_frete  # Este é o valor que deveria ser usado
)
print(f"Valor comissão com frete: R$ {valor_comissao_com_frete:.2f}")

print(f"\n=== DIFERENÇA ===")
print(f"Diferença na rentabilidade: {(rentabilidade_com_frete - rentabilidade_sem_frete)*100:.2f}%")
print(f"Diferença na comissão: R$ {valor_comissao_com_frete - valor_comissao_sem_frete:.2f}")