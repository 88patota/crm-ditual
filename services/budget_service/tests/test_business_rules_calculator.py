import pytest
from decimal import Decimal
from app.services.business_rules_calculator import BusinessRulesCalculator

def test_calculate_purchase_value_with_weight_correction():
    result = BusinessRulesCalculator.calculate_purchase_value_with_weight_correction(100.0, 50.0, 10.0)
    assert result == 120.0

def test_calculate_distributed_other_expenses():
    result = BusinessRulesCalculator.calculate_distributed_other_expenses(10.0, 100.0, 50.0)
    assert result == 5.0

def test_calculate_purchase_value_without_taxes():
    result = BusinessRulesCalculator.calculate_purchase_value_without_taxes(100.0, 0.18, 10.0)
    assert round(result, 6) == 84.415000

def test_calculate_sale_value_without_taxes():
    result = BusinessRulesCalculator.calculate_sale_value_without_taxes(100.0, 0.18)
    assert round(result, 6) == 74.415000

def test_calculate_weight_difference():
    result = BusinessRulesCalculator.calculate_weight_difference(50.0, 40.0)
    assert result == 10.0

def test_calculate_unit_sale_value():
    result = BusinessRulesCalculator.calculate_unit_sale_value(100.0, 50.0)
    assert round(result, 6) == 2.000000

def test_calculate_item_profitability():
    result = BusinessRulesCalculator.calculate_item_profitability(120.0, 100.0)
    assert round(result, 6) == 0.200000

def test_calculate_budget_markup():
    result = BusinessRulesCalculator.calculate_budget_markup(120.0, 100.0)
    assert round(result, 6) == 0.200000

def test_calculate_dunamis_cost_v1():
    result = BusinessRulesCalculator.calculate_dunamis_cost_v1(100.0, 0.18)
    assert round(result, 6) == 134.381509

def test_calculate_dunamis_cost_v2():
    result = BusinessRulesCalculator.calculate_dunamis_cost_v2(100.0, 0.18)
    assert round(result, 6) == 121.951220

def test_calculate_total_purchase_item():
    result = BusinessRulesCalculator.calculate_total_purchase_item(10.0, 20.0)
    assert round(result, 6) == 200.000000
