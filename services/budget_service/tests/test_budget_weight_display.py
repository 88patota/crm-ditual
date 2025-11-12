import pytest
from app.models.budget import BudgetItem
from app.services.business_rules_calculator import BusinessRulesCalculator


class TestBudgetWeightDisplay:
    """Testes para verificar se o peso exibido no orçamento corresponde ao peso de venda."""

    def test_budget_item_weight_display_uses_sale_weight(self):
        """Testa se o peso exibido no orçamento usa o peso de venda."""
        # Arrange
        item_data = {
            'description': 'Item de teste',
            'peso_compra': 10.0,  # Peso de compra
            'peso_venda': 12.0,   # Peso de venda (diferente do peso de compra)
            'valor_com_icms_compra': 100.0,
            'percentual_icms_compra': 0.17,
            'outras_despesas_item': 5.0,
            'valor_com_icms_venda': 150.0,
            'percentual_icms_venda': 0.17,
            'percentual_ipi': 0.0
        }
        
        calculator = BusinessRulesCalculator()
        
        # Act
        result = calculator.calculate_complete_item(item_data, 0.0, 10.0)
        
        # Assert
        assert 'peso_venda' in result, "Resultado deve conter peso_venda"
        assert result['peso_venda'] == 12.0, f"Peso da venda deve ser 12.0, mas foi {result['peso_venda']}"
        assert result['peso_compra'] == 10.0, f"Peso de compra deve ser 10.0, mas foi {result['peso_compra']}"
        
        # Verificar que o peso de venda é diferente do peso de compra
        assert result['peso_venda'] != result['peso_compra'], "Peso de venda deve ser diferente do peso de compra"

    def test_budget_item_weight_display_same_values(self):
        """Testa quando peso de compra e venda são iguais."""
        # Arrange
        item_data = {
            'description': 'Item com pesos iguais',
            'peso_compra': 10.0,
            'peso_venda': 10.0,   # Mesmo valor do peso de compra
            'valor_com_icms_compra': 100.0,
            'percentual_icms_compra': 0.17,
            'outras_despesas_item': 5.0,
            'valor_com_icms_venda': 150.0,
            'percentual_icms_venda': 0.17,
            'percentual_ipi': 0.0
        }
        
        calculator = BusinessRulesCalculator()
        
        # Act
        result = calculator.calculate_complete_item(item_data, 0.0, 10.0)
        
        # Assert
        assert result['peso_venda'] == 10.0, "O peso de venda deve ser 10.0"
        assert result['peso_compra'] == 10.0, "O peso de compra deve ser 10.0"
        assert result['peso_venda'] == result['peso_compra'], "Pesos devem ser iguais quando configurados com o mesmo valor"

    def test_budget_item_weight_display_zero_sale_weight(self):
        """Testa o comportamento quando peso de venda é zero - deve usar peso de compra"""
        # Arrange
        item_data = {
            'description': 'Item com peso de venda zero',
            'peso_compra': 10.0,
            'peso_venda': 0.0,  # Zero será substituído pelo peso de compra
            'valor_com_icms_compra': 100.0,
            'percentual_icms_compra': 0.17,
            'outras_despesas_item': 5.0,
            'valor_com_icms_venda': 150.0,
            'percentual_icms_venda': 0.17,
            'percentual_ipi': 0.0
        }
        
        calculator = BusinessRulesCalculator()
        
        # Act
        result = calculator.calculate_complete_item(item_data, 0.0, 10.0)
        
        # Assert
        # Quando peso_venda é 0, o sistema usa peso_compra
        assert result['peso_venda'] == 10.0, "O peso de venda deve ser igual ao peso de compra quando é zero"
        assert result['peso_compra'] == 10.0, "O peso de compra deve ser 10.0"

    def test_budget_item_weight_calculations_consistency(self):
        """Testa se os cálculos são consistentes com os pesos corretos"""
        # Arrange
        item_data = {
            'peso_compra': 10.0,
            'peso_venda': 10.0,  # Mesmo peso para simplificar o teste
            'valor_com_icms_compra': 100.0,
            'valor_com_icms_venda': 120.0,
            'percentual_icms_compra': 0.18,
            'percentual_icms_venda': 0.18,
            'outras_despesas_item': 0.0
        }
        
        calculator = BusinessRulesCalculator()
        
        # Act
        result = calculator.calculate_complete_item(item_data, 0.0, 18.0)
        
        # Assert
        assert 'total_compra_item' in result, "Deve calcular total de compra"
        assert 'total_venda_item' in result, "Deve calcular total de venda"
        assert result['peso_venda'] == 10.0, "Peso de venda deve ser 10.0"
        assert result['peso_compra'] == 10.0, "Peso de compra deve ser 10.0"
        
        # Verificar que a diferença de peso é calculada corretamente
        assert result['diferenca_peso'] == 0.0, "Diferença de peso deve ser 0.0 quando os pesos são iguais"