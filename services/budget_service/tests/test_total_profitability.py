import pytest
from app.services.business_rules_calculator import BusinessRulesCalculator


def test_rentabilidade_item_total_calculation_basic():
    item_data = {
        'description': 'Produto Teste',
        'peso_compra': 10.0,
        'peso_venda': 12.0,
        'valor_com_icms_compra': 100.0,
        'valor_com_icms_venda': 150.0,
        'percentual_icms_compra': 0.18,
        'percentual_icms_venda': 0.18,
        'percentual_ipi': 0.0,
        'outras_despesas_item': 0.0,
    }

    outras_despesas_totais = 0.0
    soma_pesos_pedido = item_data['peso_compra']

    result = BusinessRulesCalculator.calculate_complete_item(
        item_data, outras_despesas_totais, soma_pesos_pedido, freight_value_total=0.0
    )

    total_compra_item = result['total_compra_item']
    total_venda_item = result['total_venda_item']
    expected_total_profitability = (total_venda_item / total_compra_item) - 1 if total_compra_item > 0 else 0.0

    assert 'rentabilidade_item_total' in result
    assert result['rentabilidade_item_total'] == pytest.approx(expected_total_profitability, rel=1e-6, abs=1e-6)


def test_complete_budget_returns_rentabilidade_item_total():
    items_data = [
        {
            'description': 'Produto A',
            'peso_compra': 5.0,
            'peso_venda': 6.0,
            'valor_com_icms_compra': 80.0,
            'valor_com_icms_venda': 120.0,
            'percentual_icms_compra': 0.18,
            'percentual_icms_venda': 0.18,
            'percentual_ipi': 0.0,
            'outras_despesas_item': 0.0,
        },
        {
            'description': 'Produto B',
            'peso_compra': 3.0,
            'peso_venda': 2.5,
            'valor_com_icms_compra': 60.0,
            'valor_com_icms_venda': 90.0,
            'percentual_icms_compra': 0.18,
            'percentual_icms_venda': 0.18,
            'percentual_ipi': 0.0,
            'outras_despesas_item': 0.0,
        }
    ]

    soma_pesos_pedido = sum(i['peso_compra'] for i in items_data)
    outras_despesas_totais = 0.0
    freight_value_total = 0.0

    calc = BusinessRulesCalculator.calculate_complete_budget(
        items_data, outras_despesas_totais, soma_pesos_pedido, freight_value_total
    )

    assert 'items' in calc
    assert len(calc['items']) == 2

    for item in calc['items']:
        assert 'rentabilidade_item_total' in item
        total_compra_item = item['total_compra_item']
        total_venda_item = item['total_venda_item']
        expected_total_profitability = (total_venda_item / total_compra_item) - 1 if total_compra_item > 0 else 0.0
        assert item['rentabilidade_item_total'] == pytest.approx(expected_total_profitability, rel=1e-6, abs=1e-6)