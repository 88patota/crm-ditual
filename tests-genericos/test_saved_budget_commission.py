#!/usr/bin/env python3
"""
Test saved budget commission percentage display
"""
import requests
import json

def test_saved_budget_commission_display():
    print("🧪 TESTING: Saved budget commission percentage display")
    print("=" * 60)
    
    base_url = "http://localhost:8002/api/v1"
    
    # First, create a budget using simplified endpoint
    budget_data = {
        "order_number": "PED-TEST-SAVED",
        "client_name": "Test Saved Budget Commission",
        "notes": "Test commission percentage after save",
        "items": [{
            "description": "Test Item Saved 1050kg",
            "peso_compra": 1000,
            "peso_venda": 1050,  # Different weight to get 3% commission
            "valor_com_icms_compra": 6,
            "percentual_icms_compra": 0.18,
            "outras_despesas_item": 0,
            "valor_com_icms_venda": 8,
            "percentual_icms_venda": 0.12
        }]
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        # Create the budget
        print("🌐 Creating budget...")
        response = requests.post(f"{base_url}/budgets/simplified", json=budget_data, headers=headers)
        
        if response.status_code == 201:
            created_budget = response.json()
            budget_id = created_budget.get('id')
            print(f"✅ Budget created with ID: {budget_id}")
            
            # Now fetch the budget to check commission_percentage_actual
            print(f"🌐 Fetching budget {budget_id}...")
            response = requests.get(f"{base_url}/budgets/{budget_id}", headers=headers)
            
            if response.status_code == 200:
                fetched_budget = response.json()
                items = fetched_budget.get('items', [])
                
                if items:
                    item = items[0]
                    commission_value = item.get('commission_value', 0)
                    commission_percentage_actual = item.get('commission_percentage_actual')
                    
                    print(f"  Commission value: R$ {commission_value:.2f}")
                    
                    if commission_percentage_actual is not None:
                        print(f"  Commission percentage (backend): {commission_percentage_actual * 100:.1f}%")
                        
                        # Expected results
                        if abs(commission_value - 252.0) < 0.01:
                            print("  ✅ Commission value correct: R$ 252.00")
                        else:
                            print(f"  ❌ Commission value incorrect: Expected R$ 252.00, got R$ {commission_value:.2f}")
                            
                        if abs(commission_percentage_actual - 0.03) < 0.001:  # 3% = 0.03
                            print("  ✅ Commission percentage correct: 3.0%")
                            print("\n  🎉 Saved budgets now display correct commission percentage!")
                        else:
                            print(f"  ❌ Commission percentage incorrect: Expected 3.0%, got {commission_percentage_actual * 100:.1f}%")
                            
                    else:
                        print("  ❌ commission_percentage_actual field not found in saved budget")
                        print("  Available fields:", list(item.keys()))
                        
                else:
                    print("  ❌ No items found in fetched budget")
                    
            else:
                print(f"❌ Error fetching budget: {response.status_code}")
                print(f"   Response: {response.text}")
                
        else:
            print(f"❌ Error creating budget: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR: Service not running")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_saved_budget_commission_display()