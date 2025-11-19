#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'budget_service'))

from app.services.commission_service import CommissionService

print("=== FAIXAS DE COMISSÃO ===")
for bracket in CommissionService.COMMISSION_BRACKETS:
    min_perc = bracket["min_profitability"] * 100
    max_perc = bracket["max_profitability"] * 100 if bracket["max_profitability"] != float('inf') else "∞"
    comm_perc = bracket["commission_rate"] * 100
    print(f"Rentabilidade {min_perc:.2f}% - {max_perc}%: Comissão {comm_perc:.2f}%")

print("\n=== TESTE COM NOSSOS VALORES ===")
rentabilidades_teste = [1.0474, 0.8701, 0.79, 0.60, 0.50, 0.40, 0.30, 0.20, 0.10]

for rent in rentabilidades_teste:
    perc_comissao = CommissionService.calculate_commission_percentage(rent)
    print(f"Rentabilidade {rent*100:.2f}% → Comissão {perc_comissao*100:.2f}%")