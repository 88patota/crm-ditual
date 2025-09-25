#!/usr/bin/env python3
"""
Test to verify that the frontend freight_type fix works correctly
This test simulates the frontend behavior before and after the fix
"""
import requests
import json

def test_frontend_freight_type_fix():
    """Test that the frontend correctly handles freight_type updates"""
    
    base_url = "http://localhost:8002"
    budget_id = None
    
    print("=== TESTING FRONTEND FREIGHT TYPE FIX ===")
    print()
    
    # First, create a test budget with FOB freight type
    print("🔄 Creating test budget with FOB freight type...")
    
    create_data = {
        "order_number": "TEST-FRONTEND-001",
        "client_name": "Test Client",
        "notes": "Test budget for frontend freight type fix",
        "freight_type": "FOB",
        "items": [{
            "description": "Test Item",
            "weight": 100.0,
            "sale_weight": 100.0,
            "purchase_value_with_icms": 100.0,
            "purchase_icms_percentage": 0.18,
            "purchase_other_expenses": 0.0,
            "sale_value_with_icms": 150.0,
            "sale_icms_percentage": 0.17,
            "ipi_percentage": 0.0
        }]
    }
    
    try:
        # Create the budget
        create_response = requests.post(f"{base_url}/budgets/", json=create_data)
        if create_response.status_code != 201:
            print(f"❌ Failed to create budget: {create_response.status_code}")
            print(f"Response: {create_response.text}")
            return False
            
        created_budget = create_response.json()
        budget_id = created_budget["id"]
        print(f"✅ Budget created successfully with ID: {budget_id}")
        print(f"   Initial freight_type: {created_budget.get('freight_type', 'NOT SET')}")
        print()
        
        # Verify initial freight_type
        if created_budget.get('freight_type') != 'FOB':
            print(f"❌ Initial freight_type is incorrect: {created_budget.get('freight_type')}")
            return False
        
        # Test 1: Simulate the OLD frontend behavior (incorrect)
        # This would send freight_type even when not changed
        print("🔄 Testing OLD frontend behavior (should still work)...")
        
        old_update_data = {
            "client_name": "Updated Client Name",
            "freight_type": "FOB"  # This would be sent even if not changed
        }
        
        old_update_response = requests.put(f"{base_url}/budgets/{budget_id}", json=old_update_data)
        if old_update_response.status_code != 200:
            print(f"❌ Failed OLD frontend update test: {old_update_response.status_code}")
            print(f"Response: {old_update_response.text}")
            return False
            
        old_updated_budget = old_update_response.json()
        print(f"✅ OLD frontend behavior still works")
        print(f"   Freight type after OLD update: {old_updated_budget.get('freight_type', 'NOT SET')}")
        print()
        
        # Test 2: Simulate the NEW frontend behavior (correct)
        # This should only send freight_type when it's actually changed
        print("🔄 Testing NEW frontend behavior (correct)...")
        
        # First update without freight_type (should not change it)
        new_update_data_1 = {
            "client_name": "Updated Client Name Again",
            "notes": "Updated notes without changing freight type"
            # Note: freight_type is NOT included, simulating that it wasn't changed
        }
        
        new_update_response_1 = requests.put(f"{base_url}/budgets/{budget_id}", json=new_update_data_1)
        if new_update_response_1.status_code != 200:
            print(f"❌ Failed NEW frontend update test 1: {new_update_response_1.status_code}")
            print(f"Response: {new_update_response_1.text}")
            return False
            
        new_updated_budget_1 = new_update_response_1.json()
        print(f"✅ NEW frontend update 1 successful (no freight_type sent)")
        print(f"   Freight type after NEW update 1: {new_updated_budget_1.get('freight_type', 'NOT SET')}")
        print(f"   Client name after NEW update 1: {new_updated_budget_1.get('client_name', 'NOT SET')}")
        print()
        
        # Verify freight_type is still FOB
        if new_updated_budget_1.get('freight_type') != 'FOB':
            print(f"❌ Freight type was incorrectly changed: {new_updated_budget_1.get('freight_type')}")
            return False
        
        # Test 3: Update freight_type to CIF (should change it)
        print("🔄 Testing freight_type change to CIF...")
        
        new_update_data_2 = {
            "freight_type": "CIF"
        }
        
        new_update_response_2 = requests.put(f"{base_url}/budgets/{budget_id}", json=new_update_data_2)
        if new_update_response_2.status_code != 200:
            print(f"❌ Failed freight_type change test: {new_update_response_2.status_code}")
            print(f"Response: {new_update_response_2.text}")
            return False
            
        new_updated_budget_2 = new_update_response_2.json()
        print(f"✅ Freight type change to CIF successful")
        print(f"   Freight type after change: {new_updated_budget_2.get('freight_type', 'NOT SET')}")
        print()
        
        # Verify freight_type is now CIF
        if new_updated_budget_2.get('freight_type') != 'CIF':
            print(f"❌ Freight type was not changed to CIF: {new_updated_budget_2.get('freight_type')}")
            return False
        
        # Test 4: Update back to FOB
        print("🔄 Testing freight_type change back to FOB...")
        
        new_update_data_3 = {
            "freight_type": "FOB"
        }
        
        new_update_response_3 = requests.put(f"{base_url}/budgets/{budget_id}", json=new_update_data_3)
        if new_update_response_3.status_code != 200:
            print(f"❌ Failed freight_type change back test: {new_update_response_3.status_code}")
            print(f"Response: {new_update_response_3.text}")
            return False
            
        new_updated_budget_3 = new_update_response_3.json()
        print(f"✅ Freight type change back to FOB successful")
        print(f"   Freight type after change back: {new_updated_budget_3.get('freight_type', 'NOT SET')}")
        print()
        
        # Verify freight_type is now FOB again
        if new_updated_budget_3.get('freight_type') != 'FOB':
            print(f"❌ Freight type was not changed back to FOB: {new_updated_budget_3.get('freight_type')}")
            return False
        
        print("🎉 ALL FRONTEND FREIGHT TYPE TESTS PASSED!")
        print("   The fix correctly handles freight_type updates")
        return True
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False
    finally:
        # Clean up - delete the test budget if it was created
        try:
            if budget_id is not None:
                requests.delete(f"{base_url}/budgets/{budget_id}")
                print(f"🧹 Cleaned up test budget {budget_id}")
        except:
            pass

if __name__ == "__main__":
    success = test_frontend_freight_type_fix()
    if success:
        print("\n✅ FRONTEND FREIGHT TYPE FIX TEST PASSED")
    else:
        print("\n❌ FRONTEND FREIGHT TYPE FIX TEST FAILED")