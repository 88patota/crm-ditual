import pytest
from app.services.business_rules_calculator import BusinessRulesCalculator


class TestWeightDifferenceDisplay:
    """Testes para a funcionalidade de exibição da diferença de peso."""

    def test_calculate_weight_difference_display_no_difference(self):
        """Testa quando não há diferença entre peso compra e venda."""
        result = BusinessRulesCalculator.calculate_weight_difference_display(100, 100)
        
        assert result['has_difference'] is False
        assert result['absolute_difference'] == 0
        assert result['percentage_difference'] == 0
        assert result['formatted_display'] == ""

    def test_calculate_weight_difference_display_positive_difference(self):
        """Testa diferença positiva (peso venda > peso compra)."""
        result = BusinessRulesCalculator.calculate_weight_difference_display(130, 100)
        
        assert result['has_difference'] is True
        assert result['absolute_difference'] == 30
        assert result['percentage_difference'] == 30.0
        assert result['formatted_display'] == "30.00 (30.0%)"

    def test_calculate_weight_difference_display_negative_difference(self):
        """Testa diferença negativa (peso venda < peso compra)."""
        result = BusinessRulesCalculator.calculate_weight_difference_display(70, 100)
        
        assert result['has_difference'] is True
        assert result['absolute_difference'] == 30
        assert result['percentage_difference'] == 30.0
        assert result['formatted_display'] == "30.00 (30.0%)"

    def test_calculate_weight_difference_display_zero_peso_compra(self):
        """Testa quando peso_compra é zero."""
        result = BusinessRulesCalculator.calculate_weight_difference_display(50, 0)
        
        assert result['has_difference'] is True
        assert result['absolute_difference'] == 50
        assert result['percentage_difference'] == 0.0
        assert result['formatted_display'] == "50.00"

    def test_calculate_weight_difference_display_decimal_values(self):
        """Testa com valores decimais."""
        result = BusinessRulesCalculator.calculate_weight_difference_display(120.75, 100.5)
        
        assert result['has_difference'] is True
        assert abs(result['absolute_difference'] - 20.25) < 0.01
        assert abs(result['percentage_difference'] - 20.15) < 0.01
        assert result['formatted_display'] == "20.25 (20.1%)"

    def test_calculate_weight_difference_display_small_difference(self):
        """Testa com diferença muito pequena."""
        result = BusinessRulesCalculator.calculate_weight_difference_display(100.1, 100)
        
        assert result['has_difference'] is True
        assert abs(result['absolute_difference'] - 0.1) < 0.01
        assert abs(result['percentage_difference'] - 0.1) < 0.01
        assert result['formatted_display'] == "0.10 (0.1%)"

    def test_calculate_weight_difference_display_large_percentage(self):
        """Testa com diferença percentual grande."""
        result = BusinessRulesCalculator.calculate_weight_difference_display(50, 10)
        
        assert result['has_difference'] is True
        assert result['absolute_difference'] == 40
        assert result['percentage_difference'] == 400.0
        assert result['formatted_display'] == "40.00 (400.0%)"

    def test_integration_with_calculate_complete_item(self):
        """Testa a integração com calculate_complete_item."""
        item_data = {
            'peso_compra': 100,
            'peso_venda': 130,
            'valor_com_icms_compra': 50.0,
            'percentual_icms_compra': 0.17,
            'outras_despesas_item': 0,
            'valor_com_icms_venda': 80.0,
            'percentual_icms_venda': 0.17,
            'percentual_ipi': 0.0
        }
        
        result = BusinessRulesCalculator.calculate_complete_item(
            item_data, 
            outras_despesas_totais=0.0, 
            soma_pesos_pedido=100.0
        )
        
        # Verifica se o campo weight_difference_display foi incluído
        assert 'weight_difference_display' in result
        
        weight_diff = result['weight_difference_display']
        assert weight_diff['has_difference'] is True
        assert weight_diff['absolute_difference'] == 30
        assert weight_diff['percentage_difference'] == 30.0
        assert weight_diff['formatted_display'] == "30.00 (30.0%)"

    def test_integration_no_difference_scenario(self):
        """Testa integração quando não há diferença de peso."""
        item_data = {
            'peso_compra': 100,
            'peso_venda': 100,
            'valor_com_icms_compra': 50.0,
            'percentual_icms_compra': 0.17,
            'outras_despesas_item': 0,
            'valor_com_icms_venda': 80.0,
            'percentual_icms_venda': 0.17,
            'percentual_ipi': 0.0
        }
        
        result = BusinessRulesCalculator.calculate_complete_item(
            item_data, 
            outras_despesas_totais=0.0, 
            soma_pesos_pedido=100.0
        )
        
        # Verifica se o campo weight_difference_display foi incluído
        assert 'weight_difference_display' in result
        
        weight_diff = result['weight_difference_display']
        assert weight_diff['has_difference'] is False
        assert weight_diff['formatted_display'] == ""