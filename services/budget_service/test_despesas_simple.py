#!/usr/bin/env python3
"""
Teste simples para validar a correção das despesas (R$/kg)
"""

import os
import sys

# Garantir que o pacote "app" esteja no PYTHONPATH
BASE_DIR = os.path.dirname(__file__)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.services.budget_calculator import BudgetCalculatorService
from app.schemas.budget import BudgetItemSimplified


def test_despesas_simplificadas_r_por_kg():
    """Valida que outras_despesas_item (R$/kg) é somada ao custo por kg."""
    # Dados de teste
    test_data = BudgetItemSimplified(
        description='Item de Teste',
        peso_compra=10.0,
        peso_venda=10.0,
        valor_com_icms_compra=100.0,
        percentual_icms_compra=0.18,  # formato decimal
        outras_despesas_item=20.0,    # R$/kg
        valor_com_icms_venda=120.0,
        percentual_icms_venda=0.17,   # formato decimal
        percentual_ipi=0.0
    )

    # Executar cálculo simplificado
    result = BudgetCalculatorService.calculate_simplified_item(test_data)
    valor_sem_impostos_por_kg = result.get('purchase_value_without_taxes', 0)
    valor_total_sem_impostos = valor_sem_impostos_por_kg * test_data.peso_compra

    # Esperados com regra R$/kg:
    # Base sem impostos: 100 * (1-0.18) * (1-0.0925) = 74.415
    # Soma outras despesas: 74.415 + 20 = 94.415 por kg
    esperado_por_kg = 94.415
    esperado_total = 944.15  # 94.415 * 10 kg

    tolerancia = 0.01
    assert abs(valor_sem_impostos_por_kg - esperado_por_kg) <= tolerancia
    assert abs(valor_total_sem_impostos - esperado_total) <= tolerancia