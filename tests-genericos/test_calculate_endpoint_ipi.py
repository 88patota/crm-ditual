#!/usr/bin/env python3
"""
Test script to verify the /budgets/calculate endpoint includes IPI calculations
"""
import requests
import json

# Configuration
BASE_URL = "http://localhost:8002"  # Budget service port
API_PREFIX = "/api/v1"

def test_calculate_endpoint_with_ipi():
    """Test the /budgets/calculate endpoint with IPI data"""
    print("=== TESTING /budgets/calculate ENDPOINT WITH IPI ===")

    # Test data with IPI - matching BudgetCreate schema
    test_data = {
        "order_number": "TEST-IPI-001",
        "client_name": "Cliente Teste IPI",
        "items": [
            {
                "description": "Item com IPI 3.25%",
                "weight": 100.0,
                "purchase_value_with_icms": 10.00,
                "purchase_icms_percentage": 0.18,
                "purchase_other_expenses": 0.0,
                "purchase_value_without_taxes": 8.00,  # Required field
                "sale_weight": 100.0,  # Add sale_weight
                "sale_value_with_icms": 15.00,
                "sale_icms_percentage": 0.17,
                "sale_value_without_taxes": 12.45,  # Required field
                "ipi_percentage": 0.0325,  # 3.25% IPI
                "commission_percentage": 0.0
            },
            {
                "description": "Item sem IPI",
                "weight": 50.0,
                "purchase_value_with_icms": 8.00,
                "purchase_icms_percentage": 0.18,
                "purchase_other_expenses": 0.0,
                "purchase_value_without_taxes": 6.40,  # Required field
                "sale_weight": 50.0,  # Add sale_weight
                "sale_value_with_icms": 12.00,
                "sale_icms_percentage": 0.17,
                "sale_value_without_taxes": 9.90,  # Required field
                "ipi_percentage": 0.0,  # 0% IPI
                "commission_percentage": 0.0
            }
        ]
    }

    url = f"{BASE_URL}{API_PREFIX}/budgets/calculate"
    print(f"Making request to: {url}")
    print(f"Request data: {json.dumps(test_data, indent=2)}")

    try:
        response = requests.post(url, json=test_data, headers={"Content-Type": "application/json"})

        print(f"Response status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("✅ Calculation successful!")
            print(f"Total Purchase Value: R$ {result.get('total_purchase_value', 0):.2f}")
            print(f"Total Sale Value: R$ {result.get('total_sale_value', 0):.2f}")
            print(f"Total Commission: R$ {result.get('total_commission', 0):.2f}")
            print(f"Profitability: {result.get('profitability_percentage', 0):.2f}%")

            # Check IPI values
            total_ipi = result.get('total_ipi_value', 0)
            total_final = result.get('total_final_value', 0)

            if total_ipi > 0:
                print(f"✅ Total IPI: R$ {total_ipi:.2f}")
                print(f"✅ Total Final Value with IPI: R$ {total_final:.2f}")
            else:
                print("❌ No IPI values found in response")

            # Check items
            items = result.get('items_calculations', [])
            print(f"\nItems processed: {len(items)}")
            for i, item in enumerate(items):
                print(f"Item {i+1}: {item.get('description', '')}")
                print(f"  IPI %: {item.get('ipi_percentage', 0)*100:.2f}%")
                print(f"  IPI Value: R$ {item.get('ipi_value', 0):.2f}")
                print(f"  Final Value with IPI: R$ {item.get('total_value_with_ipi', 0):.2f}")

            return True
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("Make sure the budget service is running on http://localhost:8000")
    print("If it's running on a different port, update BASE_URL in this script")
    print()

    success = test_calculate_endpoint_with_ipi()
    if success:
        print("\n✅ /budgets/calculate endpoint is working correctly with IPI!")
    else:
        print("\n❌ /budgets/calculate endpoint has issues with IPI")
        print("Check if the service is running and the endpoint is properly updated.")
