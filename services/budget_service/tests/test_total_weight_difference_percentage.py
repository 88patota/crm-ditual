import pytest
from app.services.business_rules_calculator import BusinessRulesCalculator

class TestTotalWeightDifferencePercentage:
    """Testes unitários para validar a fórmula de cálculo da diferença percentual de peso total"""

    def test_calculate_total_weight_difference_percentage_normal_case(self):
        """Teste caso normal: peso de venda maior que peso de compra"""
        # Cenário: 120kg venda vs 100kg compra = 20% de diferença
        total_sale_weight = 120.0
        total_purchase_weight = 100.0
        
        result = BusinessRulesCalculator.calculate_total_weight_difference_percentage(
            total_sale_weight, total_purchase_weight
        )
        
        expected = ((120.0 - 100.0) / 100.0) * 100  # 20.0%
        assert result == expected
        assert result == 20.0

    def test_calculate_total_weight_difference_percentage_negative_difference(self):
        """Teste caso com diferença negativa: peso de venda menor que peso de compra"""
        # Cenário: 80kg venda vs 100kg compra = -20% de diferença
        total_sale_weight = 80.0
        total_purchase_weight = 100.0
        
        result = BusinessRulesCalculator.calculate_total_weight_difference_percentage(
            total_sale_weight, total_purchase_weight
        )
        
        expected = ((80.0 - 100.0) / 100.0) * 100  # -20.0%
        assert result == expected
        assert result == -20.0

    def test_calculate_total_weight_difference_percentage_zero_difference(self):
        """Teste caso sem diferença: pesos iguais"""
        # Cenário: 100kg venda vs 100kg compra = 0% de diferença
        total_sale_weight = 100.0
        total_purchase_weight = 100.0
        
        result = BusinessRulesCalculator.calculate_total_weight_difference_percentage(
            total_sale_weight, total_purchase_weight
        )
        
        expected = ((100.0 - 100.0) / 100.0) * 100  # 0.0%
        assert result == expected
        assert result == 0.0

    def test_calculate_total_weight_difference_percentage_zero_purchase_weight(self):
        """Teste validação: peso de compra zero deve retornar 0.0"""
        total_sale_weight = 100.0
        total_purchase_weight = 0.0
        
        result = BusinessRulesCalculator.calculate_total_weight_difference_percentage(
            total_sale_weight, total_purchase_weight
        )
        
        assert result == 0.0

    def test_calculate_total_weight_difference_percentage_negative_sale_weight(self):
        """Teste validação: peso de venda negativo deve gerar ValueError"""
        total_sale_weight = -50.0
        total_purchase_weight = 100.0
        
        with pytest.raises(ValueError, match="Total sale weight cannot be negative"):
            BusinessRulesCalculator.calculate_total_weight_difference_percentage(
                total_sale_weight, total_purchase_weight
            )

    def test_calculate_total_weight_difference_percentage_negative_purchase_weight(self):
        """Teste validação: peso de compra negativo deve gerar ValueError"""
        total_sale_weight = 100.0
        total_purchase_weight = -50.0
        
        with pytest.raises(ValueError, match="Total purchase weight cannot be negative"):
            BusinessRulesCalculator.calculate_total_weight_difference_percentage(
                total_sale_weight, total_purchase_weight
            )

    def test_calculate_total_weight_difference_percentage_decimal_precision(self):
        """Teste com números decimais para verificar precisão"""
        # Cenário: 12.345kg venda vs 10.012kg compra
        total_sale_weight = 12.345
        total_purchase_weight = 10.012
        
        result = BusinessRulesCalculator.calculate_total_weight_difference_percentage(
            total_sale_weight, total_purchase_weight
        )
        
        expected = ((12.345 - 10.012) / 10.012) * 100  # ~23.30%
        # Usando tolerância para comparação de floats
        assert abs(result - expected) < 0.01  # Tolerância de 0.01%

    def test_calculate_total_weight_difference_percentage_large_numbers(self):
        """Teste com números grandes"""
        # Cenário: 10000kg venda vs 8000kg compra = 25% de diferença
        total_sale_weight = 10000.0
        total_purchase_weight = 8000.0
        
        result = BusinessRulesCalculator.calculate_total_weight_difference_percentage(
            total_sale_weight, total_purchase_weight
        )
        
        expected = ((10000.0 - 8000.0) / 8000.0) * 100  # 25.0%
        assert result == expected
        assert result == 25.0

    def test_calculate_total_weight_difference_percentage_small_numbers(self):
        """Teste com números pequenos"""
        # Cenário: 0.5kg venda vs 0.4kg compra = 25% de diferença
        total_sale_weight = 0.5
        total_purchase_weight = 0.4
        
        result = BusinessRulesCalculator.calculate_total_weight_difference_percentage(
            total_sale_weight, total_purchase_weight
        )
        
        expected = ((0.5 - 0.4) / 0.4) * 100  # 25.0%
        # Usando tolerância para comparação de floats
        assert abs(result - expected) < 0.01  # Tolerância de 0.01%