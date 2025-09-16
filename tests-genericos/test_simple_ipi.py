#!/usr/bin/env python3
"""
Simple test to debug IPI calculation issues
"""
import sys
import os

# Add the budget service to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'budget_service'))

from app.services.business_rules_calculator import BusinessRulesCalculator

def test_simple_ipi():
    """Test simple IPI calculation"""
    print("=== TESTING SIMPLE IPI CALCULATION ===")

    # Simple test data
    test_item = {
        'description': 'Item Teste',
        'peso_compra': 100.0,
        'peso_venda': 100.0,
        'valor_com_icms_compra': 10.00,
        'percentual_icms_compra': 0.18,
        'outras_despesas_item': 0.0,
        'valor_com_icms_venda': 15.00,
        'percentual_icms_venda': 0.17,
        'percentual_ipi': 0.0325
    }

    print(f"Test item: {test_item}")

    try:
        # Test validation
        print("Testing validation...")
        errors = BusinessRulesCalculator.validate_item_data(test_item)
        if errors:
            print(f"Validation errors: {errors}")
            return False

        print("✅ Validation passed")

        # Test calculation
        print("Testing calculation...")
        result = BusinessRulesCalculator.calculate_complete_item(test_item, 0.0, 100.0)
        print("✅ Calculation successful")
        print(f"IPI Percentage: {result['percentual_ipi']}")
        print(f"IPI Value: R$ {result['valor_ipi_total']:.2f}")
        print(f"Final Value with IPI: R$ {result['total_final_com_ipi']:.2f}")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_simple_ipi()
    if success:
        print("\n✅ Simple IPI test passed!")
    else:
        print("\n❌ Simple IPI test failed!")
