#!/usr/bin/env python3
"""
Test script to verify IPI persistence when saving and retrieving budgets
"""
import requests
import json

# Configuration
BASE_URL = "http://localhost:8002"  # Budget service port
API_PREFIX = "/api/v1"

def test_ipi_save_and_retrieve():
    """Test IPI persistence in budget save/retrieve operations"""
    print("=== TESTING IPI SAVE AND RETRIEVE ===")

    # Test data with IPI
    test_data = {
        "order_number": "TEST-IPI-SAVE-001",
        "client_name": "Cliente Teste Persistência IPI",
        "items": [
            {
                "description": "Item com IPI 3.25%",
                "weight": 100.0,
                "purchase_value_with_icms": 10.00,
                "purchase_icms_percentage": 0.18,
                "purchase_other_expenses": 0.0,
                "purchase_value_without_taxes": 8.00,
                "sale_weight": 100.0,
                "sale_value_with_icms": 15.00,
                "sale_icms_percentage": 0.17,
                "sale_value_without_taxes": 12.45,
                "ipi_percentage": 0.0325,  # 3.25% IPI
                "commission_percentage": 0.0
            }
        ]
    }

    # Step 1: Create budget
    create_url = f"{BASE_URL}{API_PREFIX}/budgets/"
    print(f"Step 1: Creating budget at: {create_url}")

    try:
        # Add auth headers (assuming demo user)
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer demo_token"  # Replace with actual token if needed
        }

        response = requests.post(create_url, json=test_data, headers=headers)
        print(f"Create response status: {response.status_code}")

        if response.status_code == 201:
            budget_data = response.json()
            print("✅ Budget created successfully!")
            
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
            
            # Step 2: Retrieve budget by ID
            print(f"\nStep 2: Retrieving budget by ID...")
            get_url = f"{BASE_URL}{API_PREFIX}/budgets/{budget_id}"
            
            get_response = requests.get(get_url, headers=headers)
            print(f"Get response status: {get_response.status_code}")
            
            if get_response.status_code == 200:
                retrieved_data = get_response.json()
                print("✅ Budget retrieved successfully!")
                
                # Check IPI values in retrieved data
                retrieved_total_ipi = retrieved_data.get('total_ipi_value', 0)
                retrieved_total_final = retrieved_data.get('total_final_value', 0)
                
                print(f"Retrieved - Total IPI: R$ {retrieved_total_ipi:.2f}")
                print(f"Retrieved - Total Final Value: R$ {retrieved_total_final:.2f}")
                
                # Check item level IPI
                retrieved_items = retrieved_data.get('items', [])
                if retrieved_items:
                    retrieved_item = retrieved_items[0]
                    retrieved_ipi_percentage = retrieved_item.get('ipi_percentage', 0)
                    retrieved_ipi_value = retrieved_item.get('ipi_value', 0)
                    retrieved_total_with_ipi = retrieved_item.get('total_value_with_ipi', 0)
                    
                    print(f"Retrieved Item - IPI Percentage: {retrieved_ipi_percentage}")
                    print(f"Retrieved Item - IPI Value: R$ {retrieved_ipi_value:.2f}")
                    print(f"Retrieved Item - Total with IPI: R$ {retrieved_total_with_ipi:.2f}")
                    
                    # Verification
                    print(f"\n=== PERSISTENCE VERIFICATION ===")
                    
                    # Check if values match
                    tolerance = 0.01
                    
                    ipi_percentage_match = abs(item_ipi_percentage - retrieved_ipi_percentage) < tolerance
                    ipi_value_match = abs(item_ipi_value - retrieved_ipi_value) < tolerance
                    total_ipi_match = abs(total_ipi - retrieved_total_ipi) < tolerance
                    
                    print(f"IPI Percentage matches: {ipi_percentage_match} ({item_ipi_percentage} vs {retrieved_ipi_percentage})")
                    print(f"IPI Value matches: {ipi_value_match} (R$ {item_ipi_value:.2f} vs R$ {retrieved_ipi_value:.2f})")
                    print(f"Total IPI matches: {total_ipi_match} (R$ {total_ipi:.2f} vs R$ {retrieved_total_ipi:.2f})")
                    
                    if ipi_percentage_match and ipi_value_match and total_ipi_match:
                        print("✅ IPI persistence test PASSED!")
                        return True
                    else:
                        print("❌ IPI persistence test FAILED!")
                        print("Problem: IPI values are not being persisted correctly")
                        return False
                else:
                    print("❌ No items found in retrieved budget")
                    return False
            else:
                print(f"❌ Failed to retrieve budget: {get_response.text}")
                return False
        else:
            print(f"❌ Failed to create budget: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("Make sure the budget service is running on http://localhost:8002")
    print("This test will create a budget with IPI and verify persistence")
    print()

    success = test_ipi_save_and_retrieve()
    if success:
        print("\n🎉 IPI persistence test completed successfully!")
    else:
        print("\n❌ IPI persistence test failed!")
        print("Check the budget service logs for more details.")
