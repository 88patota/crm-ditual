"""
Testes unitários para a funcionalidade de cálculo de frete
"""
import pytest
from app.services.business_rules_calculator import BusinessRulesCalculator


class TestFreightCalculation:
    """Testes para o cálculo de valor de frete por kg"""

    def test_calculate_freight_value_per_kg_basic(self):
        """Teste básico do cálculo de frete por kg"""
        valor_frete_total = 100.0
        peso_total = 50.0
        
        result = BusinessRulesCalculator.calculate_freight_value_per_kg(
            valor_frete_total, peso_total
        )
        
        assert result == 2.0

    def test_calculate_freight_value_per_kg_decimal_precision(self):
        """Teste de precisão decimal no cálculo de frete"""
        valor_frete_total = 33.33
        peso_total = 10.0
        
        result = BusinessRulesCalculator.calculate_freight_value_per_kg(
            valor_frete_total, peso_total
        )
        
        assert result == 3.333

    def test_calculate_freight_value_per_kg_zero_weight_error(self):
        """Teste de erro quando peso total é zero"""
        valor_frete_total = 100.0
        peso_total = 0.0
        
        with pytest.raises(ValueError, match="Peso total deve ser maior que zero"):
            BusinessRulesCalculator.calculate_freight_value_per_kg(
                valor_frete_total, peso_total
            )

    def test_calculate_freight_value_per_kg_negative_weight_error(self):
        """Teste de erro quando peso total é negativo"""
        valor_frete_total = 100.0
        peso_total = -10.0
        
        with pytest.raises(ValueError, match="Peso total deve ser maior que zero"):
            BusinessRulesCalculator.calculate_freight_value_per_kg(
                valor_frete_total, peso_total
            )

    def test_complete_budget_with_freight_calculation(self):
        """Teste do cálculo completo de orçamento incluindo frete"""
        items_data = [
            {
                'description': 'Produto Teste',
                'quantity': 10,
                'peso_compra': 2.5,
                'peso_venda': 2.5,
                'valor_com_icms_compra': 100.0,
                'valor_com_icms_venda': 150.0,
                'percentual_icms_compra': 18.0,
                'percentual_icms_venda': 18.0,
                'percentual_ipi': 0.0,
                'outras_despesas_item': 0.0
            }
        ]
        
        peso_total = sum(item['peso_compra'] * item['quantity'] for item in items_data)
        outras_despesas_totais = 0.0
        freight_value_total = 50.0
        
        result = BusinessRulesCalculator.calculate_complete_budget(
            items_data, 
            outras_despesas_totais, 
            peso_total, 
            freight_value_total
        )
        
        # Verificar se o valor do frete por kg foi calculado corretamente
        expected_freight_per_kg = freight_value_total / peso_total
        assert result['totals']['valor_frete_compra'] == expected_freight_per_kg
        assert result['totals']['valor_frete_compra'] == 2.0

    def test_complete_budget_zero_freight_value(self):
        """Teste do cálculo completo com valor de frete zero"""
        items_data = [
            {
                'description': 'Produto Teste',
                'quantity': 5,
                'peso_compra': 1.0,
                'peso_venda': 1.0,
                'valor_com_icms_compra': 50.0,
                'valor_com_icms_venda': 75.0,
                'percentual_icms_compra': 18.0,
                'percentual_icms_venda': 18.0,
                'percentual_ipi': 0.0,
                'outras_despesas_item': 0.0
            }
        ]
        
        peso_total = sum(item['peso_compra'] * item['quantity'] for item in items_data)
        outras_despesas_totais = 0.0
        freight_value_total = 0.0
        
        result = BusinessRulesCalculator.calculate_complete_budget(
            items_data, 
            outras_despesas_totais, 
            peso_total, 
            freight_value_total
        )
        
        # Com frete zero, o valor por kg deve ser zero
        assert result['totals']['valor_frete_compra'] == 0.0

    def test_complete_budget_negative_freight_error(self):
        """Teste de erro com valor de frete negativo"""
        items_data = [
            {
                'description': 'Produto Teste',
                'quantity': 1,
                'peso_compra': 1.0,
                'peso_venda': 1.0,
                'valor_com_icms_compra': 50.0,
                'valor_com_icms_venda': 75.0,
                'percentual_icms_compra': 18.0,
                'percentual_icms_venda': 18.0,
                'percentual_ipi': 0.0,
                'outras_despesas_item': 0.0
            }
        ]
        
        peso_total = 1.0
        outras_despesas_totais = 0.0
        freight_value_total = -10.0
        
        with pytest.raises(ValueError, match="Valor do frete não pode ser negativo"):
            BusinessRulesCalculator.calculate_complete_budget(
                items_data, 
                outras_despesas_totais, 
                peso_total, 
                freight_value_total
            )

    def test_complete_budget_multiple_items_freight(self):
        """Teste com múltiplos itens para verificar cálculo de frete"""
        items_data = [
            {
                'description': 'Produto A',
                'quantity': 5,
                'peso_compra': 2.0,
                'peso_venda': 2.0,
                'valor_com_icms_compra': 100.0,
                'valor_com_icms_venda': 150.0,
                'percentual_icms_compra': 18.0,
                'percentual_icms_venda': 18.0,
                'percentual_ipi': 0.0,
                'outras_despesas_item': 0.0
            },
            {
                'description': 'Produto B',
                'quantity': 3,
                'peso_compra': 1.5,
                'peso_venda': 1.5,
                'valor_com_icms_compra': 80.0,
                'valor_com_icms_venda': 120.0,
                'percentual_icms_compra': 18.0,
                'percentual_icms_venda': 18.0,
                'percentual_ipi': 0.0,
                'outras_despesas_item': 0.0
            }
        ]
        
        # Peso total: (5 * 2.0) + (3 * 1.5) = 10 + 4.5 = 14.5 kg
        peso_total = sum(item['peso_compra'] * item['quantity'] for item in items_data)
        outras_despesas_totais = 0.0
        freight_value_total = 72.5
        
        result = BusinessRulesCalculator.calculate_complete_budget(
            items_data, 
            outras_despesas_totais, 
            peso_total, 
            freight_value_total
        )
        
        # Verificar se o valor do frete por kg foi calculado corretamente
        expected_freight_per_kg = freight_value_total / peso_total  # 72.5 / 14.5 = 5.0
        assert result['totals']['valor_frete_compra'] == expected_freight_per_kg
        assert result['totals']['valor_frete_compra'] == 5.0