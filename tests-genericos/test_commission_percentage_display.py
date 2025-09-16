#!/usr/bin/env python3
"""
Test commission percentage display fix
"""
import requests
import json

def test_commission_percentage_display():
    print("🧪 TESTING: Commission percentage display")
    print("=" * 60)
    
    # Test data with different weight to trigger 3% commission
    test_data = {
        "order_number": "PED-TEST-DISPLAY",
        "client_name": "Test Commission Display",
        "status": "draft",
        "prazo_medio": 30,
        "outras_despesas_totais": 0,
        "notes": None,
        "items": [{
            "description": "Test Item 1050kg",
            "peso_compra": 1000,
            "peso_venda": 1050,  # Different weight to get 3% commission
            "valor_com_icms_compra": 6,
            "percentual_icms_compra": 0.18,
            "outras_despesas_item": 0,
            "valor_com_icms_venda": 8,
            "percentual_icms_venda": 0.12
        }]
    }
    
    url = "http://localhost:8002/api/v1/budgets/calculate-simplified"
    headers = {"Content-Type": "application/json"}
    
    try:
        print("🌐 Calling API to calculate budget...")
        response = requests.post(url, json=test_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ API Response received")
            
            # Check the items_calculations field
            items = result.get('items_calculations', [])
            if items:
                item = items[0]
                commission_value = item.get('commission_value', 0)
                
                # Check if the new field is present
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
                    else:
                        print(f"  ❌ Commission percentage incorrect: Expected 3.0%, got {commission_percentage_actual * 100:.1f}%")
                        
                    print("\n  🎉 Frontend should now display the correct commission percentage!")
                else:
                    print("  ❌ commission_percentage_actual field not found in response")
                    print("  Available fields:", list(item.keys()))
            else:
                print("  ❌ No items found in response")
                
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR: Service not running")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_commission_percentage_display()