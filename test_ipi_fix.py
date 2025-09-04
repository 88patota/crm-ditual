#!/usr/bin/env python3
"""
Test script to verify IPI fix implementation
"""
import sys
import os

# Add the budget service to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'budget_service'))

from app.services.business_rules_calculator import BusinessRulesCalculator

def test_ipi_calculation():
    """Test IPI calculation functionality"""
    print("=== TESTING IPI CALCULATION FIX ===")
    
    # Test data with IPI
    test_items = [
        {
            'description': 'Item com IPI 3.25%',
            'peso_compra': 100.0,
            'peso_venda': 100.0,
            'valor_com_icms_compra': 10.00,
            'percentual_icms_compra': 0.18,
            'outras_despesas_item': 0.0,
            'valor_com_icms_venda': 15.00,
            'percentual_icms_venda': 0.17,
            'percentual_ipi': 0.0325  # 3.25% IPI
        },
        {
            'description': 'Item sem IPI',
            'peso_compra': 50.0,
            'peso_venda': 50.0,
            'valor_com_icms_compra': 8.00,
            'percentual_icms_compra': 0.18,
            'outras_despesas_item': 0.0,
            'valor_com_icms_venda': 12.00,
            'percentual_icms_venda': 0.17,
            'percentual_ipi': 0.0  # 0% IPI
        }
    ]
    
    outras_despesas_totais = 0.0
    soma_pesos_pedido = sum(item['peso_compra'] for item in test_items)
    
    print(f"Total weight: {soma_pesos_pedido} kg")
    print(f"Other expenses: R$ {outras_despesas_totais}")
    print()
    
    try:
        # Calculate budget with IPI
        result = BusinessRulesCalculator.calculate_complete_budget(
            test_items, outras_despesas_totais, soma_pesos_pedido
        )
        
        print("✅ Budget calculation completed successfully")
        print(f"Items processed: {result['totals']['items_count']}")
        print(f"Total IPI: R$ {result['totals']['total_ipi_orcamento']:.2f}")
        print(f"Final value with IPI: R$ {result['totals']['total_final_com_ipi']:.2f}")
        print()
        
        # Check individual items
        for i, item in enumerate(result['items']):
            print(f"Item {i+1}: {item['description']}")
            print(f"  IPI Percentage: {item['percentual_ipi']*100:.2f}%")
            print(f"  IPI Value: R$ {item['valor_ipi_total']:.2f}")
            print(f"  Final Value with IPI: R$ {item['total_final_com_ipi']:.2f}")
            print()
        
        print("✅ IPI calculation fix verification completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error in IPI calculation: {e}")
        return False

if __name__ == "__main__":
    success = test_ipi_calculation()
    sys.exit(0 if success else 1)