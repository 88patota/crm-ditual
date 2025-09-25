import pytest
from decimal import Decimal
from app.services.commission_service import CommissionService
from app.services.business_rules_calculator import BusinessRulesCalculator

class TestCommissionServiceWithQuantityAdjustment:
    """Test the new commission calculation rules with quantity/weight adjustments"""
    
    def test_commission_same_weight(self):
        """Test commission calculation when peso_venda equals peso_compra"""
        total_venda = 1000.0
        total_compra = 800.0
        peso_venda = 100.0
        peso_compra = 100.0
        valor_sem_impostos_venda = 10.0
        valor_sem_impostos_compra = 8.0
        
        result = CommissionService.calculate_commission_value_with_quantity_adjustment(
            total_venda, total_compra, peso_venda, peso_compra,
            valor_sem_impostos_venda, valor_sem_impostos_compra
        )
        
        # Should use unit profitability: (10/8 - 1) = 0.25 = 25%
        # 25% profitability -> 1% commission rate
        # Commission = 1000 * 0.01 = 10.0
        assert result == 10.0
    
    def test_commission_higher_sale_weight(self):
        """Test commission calculation when peso_venda > peso_compra"""
        total_venda = 1200.0  # Selling more quantity
        total_compra = 800.0  # Same purchase cost
        peso_venda = 120.0    # Selling 120kg
        peso_compra = 100.0   # Bought 100kg
        valor_sem_impostos_venda = 10.0
        valor_sem_impostos_compra = 8.0
        
        result = CommissionService.calculate_commission_value_with_quantity_adjustment(
            total_venda, total_compra, peso_venda, peso_compra,
            valor_sem_impostos_venda, valor_sem_impostos_compra
        )
        
        # Should use total profitability: (1200/800 - 1) = 0.5 = 50%
        # 50% profitability -> 3% commission rate
        # Commission = 1200 * 0.03 = 36.0
        assert result == 36.0
    
    def test_commission_lower_sale_weight(self):
        """Test commission calculation when peso_venda < peso_compra"""
        total_venda = 800.0   # Selling less quantity
        total_compra = 800.0  # Same purchase cost
        peso_venda = 80.0     # Selling 80kg
        peso_compra = 100.0   # Bought 100kg
        valor_sem_impostos_venda = 10.0
        valor_sem_impostos_compra = 8.0
        
        result = CommissionService.calculate_commission_value_with_quantity_adjustment(
            total_venda, total_compra, peso_venda, peso_compra,
            valor_sem_impostos_venda, valor_sem_impostos_compra
        )
        
        # Should use total profitability: (800/800 - 1) = 0 = 0%
        # 0% profitability -> 0% commission rate
        # Commission = 800 * 0.0 = 0.0
        assert result == 0.0
    
    def test_unit_profitability_calculation(self):
        """Test internal unit profitability calculation"""
        valor_venda = 12.0
        valor_compra = 10.0
        
        result = CommissionService._calculate_unit_profitability(valor_venda, valor_compra)
        
        # (12/10 - 1) = 0.2 = 20%
        assert abs(result - 0.2) < 0.001
    
    def test_total_profitability_calculation(self):
        """Test internal total profitability calculation"""
        total_venda = 1500.0
        total_compra = 1000.0
        
        result = CommissionService._calculate_total_profitability(total_venda, total_compra)
        
        # (1500/1000 - 1) = 0.5 = 50%
        assert abs(result - 0.5) < 0.001
    
    def test_complete_item_calculation_with_new_commission(self):
        """Test complete item calculation using the new commission rule"""
        item_data = {
            'description': 'Test Product',
            'peso_compra': 100.0,
            'peso_venda': 120.0,  # Selling more than purchased
            'valor_com_icms_compra': 10.0,
            'percentual_icms_compra': 0.18,
            'valor_com_icms_venda': 15.0,
            'percentual_icms_venda': 0.18,
        }
        
        result = BusinessRulesCalculator.calculate_complete_item(
            item_data, outras_despesas_totais=0.0, soma_pesos_pedido=100.0
        )
        
        # Verify that commission was calculated
        assert result['valor_comissao'] > 0
        assert result['peso_venda'] == 120.0
        assert result['peso_compra'] == 100.0
        assert result['diferenca_peso'] == 20.0
        
        # Verify commission reflects the increased sale quantity
        # Total sale should be higher due to increased weight
        assert result['total_venda_item'] > result['total_compra_item']
    
    def test_commission_brackets_still_work(self):
        """Ensure commission brackets are still properly applied"""
        # Test various profitability levels
        test_cases = [
            (0.15, 0.0),   # 15% -> 0% commission
            (0.25, 0.01),  # 25% -> 1% commission
            (0.35, 0.015), # 35% -> 1.5% commission
            (0.45, 0.025), # 45% -> 2.5% commission
            (0.55, 0.03),  # 55% -> 3% commission
            (0.70, 0.04),  # 70% -> 4% commission
            (0.90, 0.05),  # 90% -> 5% commission
        ]
        
        for profitability, expected_rate in test_cases:
            result_rate = CommissionService.calculate_commission_percentage(profitability)
            assert abs(result_rate - expected_rate) < 0.001, f"Failed for profitability {profitability}"
    
    def test_zero_purchase_cost_handling(self):
        """Test handling of edge case where purchase cost is zero"""
        result = CommissionService._calculate_total_profitability(1000.0, 0.0)
        assert result == 0.0
        
        result = CommissionService._calculate_unit_profitability(10.0, 0.0)
        assert result == 0.0
    
    def test_backward_compatibility(self):
        """Ensure the original commission calculation method still works"""
        total_venda = 1000.0
        rentabilidade = 0.30  # 30%
        
        result = CommissionService.calculate_commission_value(total_venda, rentabilidade)
        
        # 30% profitability -> 1.5% commission rate
        # Commission = 1000 * 0.015 = 15.0
        assert result == 15.0