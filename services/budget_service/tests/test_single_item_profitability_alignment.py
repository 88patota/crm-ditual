import pytest
from app.services.business_rules_calculator import BusinessRulesCalculator


def test_single_item_budget_profitability_equals_item_total_profitability():
    """
    Com apenas 1 item e diferença de peso, a rentabilidade do orçamento
    (markup_pedido_sem_impostos) deve ser igual à rentabilidade total do item.
    """
    item_data = {
        'description': 'Produto Único',
        'peso_compra': 10.0,
        'peso_venda': 12.0,
        'valor_com_icms_compra': 100.0,
        'valor_com_icms_venda': 150.0,
        'percentual_icms_compra': 0.18,
        'percentual_icms_venda': 0.18,
        'percentual_ipi': 0.0,
        'outras_despesas_item': 0.0,
    }

    soma_pesos_pedido = item_data['peso_compra']
    outras_despesas_totais = 0.0
    freight_value_total = 0.0

    calc = BusinessRulesCalculator.calculate_complete_budget(
        [item_data], outras_despesas_totais, soma_pesos_pedido, freight_value_total
    )

    assert 'items' in calc and len(calc['items']) == 1
    item = calc['items'][0]

    # Orçamento vs item total
    markup_pedido_sem_impostos = calc['totals']['markup_pedido_sem_impostos']
    assert 'rentabilidade_item_total' in item
    assert markup_pedido_sem_impostos == pytest.approx(item['rentabilidade_item_total'], rel=1e-6, abs=1e-6)


def test_unit_profitability_uses_weight_corrected_purchase():
    """
    A rentabilidade unitária deve usar a compra corrigida por peso:
    rentabilidade_item = valor_sem_impostos_venda / valor_corrigido_peso - 1
    """
    item_data = {
        'description': 'Produto Único',
        'peso_compra': 10.0,
        'peso_venda': 12.0,
        'valor_com_icms_compra': 100.0,
        'valor_com_icms_venda': 150.0,
        'percentual_icms_compra': 0.18,
        'percentual_icms_venda': 0.18,
        'percentual_ipi': 0.0,
        'outras_despesas_item': 0.0,
    }

    soma_pesos_pedido = item_data['peso_compra']
    outras_despesas_totais = 0.0
    freight_value_total = 0.0

    result = BusinessRulesCalculator.calculate_complete_item(
        item_data, outras_despesas_totais, soma_pesos_pedido, freight_value_total
    )

    valor_sem_impostos_venda = result['valor_sem_impostos_venda']
    valor_corrigido_peso = result['valor_corrigido_peso']

    expected_unit_profitability = (valor_sem_impostos_venda / valor_corrigido_peso) - 1
    assert 'rentabilidade_item' in result
    assert result['rentabilidade_item'] == pytest.approx(expected_unit_profitability, rel=1e-6, abs=1e-6)