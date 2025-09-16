#!/usr/bin/env python3
"""
Test script to verify IPI persistence using simplified endpoint
"""
import requests
import json

# Configuration
BASE_URL = "http://localhost:8002"  # Budget service port
API_PREFIX = "/api/v1"

def test_ipi_simplified_save():
    """Test IPI persistence using simplified endpoint"""
    print("=== TESTING IPI SAVE WITH SIMPLIFIED ENDPOINT ===")

    # Test data using simplified format (Portuguese field names)
    test_data = {
        "client_name": "Cliente Teste IPI Simplificado",
        "items": [
            {
                "description": "Item com IPI 3.25%",
                "peso_compra": 100.0,
                "peso_venda": 100.0,
                "valor_com_icms_compra": 10.00,
                "percentual_icms_compra": 0.18,
                "outras_despesas_item": 0.0,
                "valor_com_icms_venda": 15.00,
                "percentual_icms_venda": 0.17,
                "percentual_ipi": 0.0325  # 3.25% IPI
            }
        ]
    }

    # Step 1: Create budget using simplified endpoint
    create_url = f"{BASE_URL}{API_PREFIX}/budgets/simplified"
    print(f"Step 1: Creating simplified budget at: {create_url}")

    try:
        response = requests.post(create_url, json=test_data, headers={"Content-Type": "application/json"})
        print(f"Create response status: {response.status_code}")

        if response.status_code == 201:
            budget_data = response.json()
            print("✅ Simplified budget created successfully!")
            
            budget_id = budget_data.get('id')
            order_number = budget_data.get('order_number')
            
            print(f"Budget ID: {budget_id}")
            print(f"Order Number: {order_number}")
            
            # Check IPI values in creation response
            total_ipi = budget_data.get('total_ipi_value', 0)
            total_final = budget_data.get('total_final_value', 0)
            
            print(f"Created - Total IPI: R$ {total_ipi:.2f}")
            print(f"Created - Total Final Value: R$ {total_final:.2f}")
            
            # Check item level IPI
            items = budget_data.get('items', [])
            if items:
                item = items[0]
                item_ipi_percentage = item.get('ipi_percentage', 0)
                item_ipi_value = item.get('ipi_value', 0)
                item_total_with_ipi = item.get('total_value_with_ipi', 0)
                
                print(f"Item - IPI Percentage: {item_ipi_percentage}")
                print(f"Item - IPI Value: R$ {item_ipi_value:.2f}")
                print(f"Item - Total with IPI: R$ {item_total_with_ipi:.2f}")
                
                # Expected values calculation
                expected_ipi_value = 100.0 * 15.00 * 0.0325  # peso * valor_venda * percentual_ipi
                print(f"Expected IPI Value: R$ {expected_ipi_value:.2f}")
                
                # Verification
                print(f"\n=== IPI CALCULATION VERIFICATION ===")
                
                tolerance = 0.01
                ipi_percentage_correct = abs(item_ipi_percentage - 0.0325) < tolerance
                ipi_value_correct = abs(item_ipi_value - expected_ipi_value) < tolerance
                
                print(f"IPI Percentage correct: {ipi_percentage_correct} ({item_ipi_percentage} should be 0.0325)")
                print(f"IPI Value correct: {ipi_value_correct} (R$ {item_ipi_value:.2f} should be R$ {expected_ipi_value:.2f})")
                
                if item_ipi_percentage == 0.0 or item_ipi_value == 0.0:
                    print("❌ PROBLEM FOUND: IPI values are zero after saving!")
                    print("This confirms the reported issue - IPI is not being saved correctly.")
                    return False
                elif ipi_percentage_correct and ipi_value_correct:
                    print("✅ IPI values are correct after saving!")
                    return True
                else:
                    print("❌ IPI values are incorrect after saving!")
                    return False
            else:
                print("❌ No items found in created budget")
                return False
                
        else:
            print(f"❌ Failed to create budget: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"Error details: {error_detail}")
            except:
                print(f"Raw response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Make sure the budget service is running on http://localhost:8002")
    print("This test will create a simplified budget with IPI and verify if it's saved correctly")
    print()

    success = test_ipi_simplified_save()
    if success:
        print("\n🎉 IPI simplified save test completed successfully!")
    else:
        print("\n❌ IPI simplified save test failed!")
        print("This confirms the reported issue with IPI not being saved correctly.")
