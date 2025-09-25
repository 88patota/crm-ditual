#!/usr/bin/env python3
"""
Test to verify that freight_type is properly updated when editing a budget
"""
import requests
import json

def test_freight_type_update():
    """Test that freight_type is properly updated when editing a budget"""
    
    base_url = "http://localhost:8002"
    budget_id = None
    
    print("=== TESTING FREIGHT TYPE UPDATE ===")
    print()
    
    # First, create a test budget
    print("🔄 Creating test budget...")
    
    create_data = {
        "order_number": "TEST-FREIGHT-001",
        "client_name": "Test Client",
        "notes": "Test budget for freight type update",
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
        
        # Now update the freight_type to CIF
        print("🔄 Updating freight_type to CIF...")
        
        update_data = {
            "freight_type": "CIF"
        }
        
        update_response = requests.put(f"{base_url}/budgets/{budget_id}", json=update_data)
        if update_response.status_code != 200:
            print(f"❌ Failed to update budget: {update_response.status_code}")
            print(f"Response: {update_response.text}")
            return False
            
        updated_budget = update_response.json()
        print(f"✅ Budget updated successfully")
        print(f"   Updated freight_type: {updated_budget.get('freight_type', 'NOT SET')}")
        print()
        
        # Verify the freight_type was updated
        if updated_budget.get('freight_type') != 'CIF':
            print(f"❌ freight_type was not updated correctly: {updated_budget.get('freight_type')}")
            return False
        
        # Also test updating both freight_type and other fields
        print("🔄 Updating freight_type and other fields...")
        
        update_data_2 = {
            "freight_type": "FOB",
            "notes": "Updated notes with freight type change"
        }
        
        update_response_2 = requests.put(f"{base_url}/budgets/{budget_id}", json=update_data_2)
        if update_response_2.status_code != 200:
            print(f"❌ Failed to update budget (2nd update): {update_response_2.status_code}")
            print(f"Response: {update_response_2.text}")
            return False
            
        updated_budget_2 = update_response_2.json()
        print(f"✅ Budget updated successfully (2nd update)")
        print(f"   Updated freight_type: {updated_budget_2.get('freight_type', 'NOT SET')}")
        print(f"   Updated notes: {updated_budget_2.get('notes', 'NOT SET')}")
        print()
        
        # Verify both fields were updated
        if updated_budget_2.get('freight_type') != 'FOB':
            print(f"❌ freight_type was not updated correctly in 2nd update: {updated_budget_2.get('freight_type')}")
            return False
            
        if updated_budget_2.get('notes') != 'Updated notes with freight type change':
            print(f"❌ Notes were not updated correctly: {updated_budget_2.get('notes')}")
            return False
        
        print("🎉 ALL TESTS PASSED!")
        print("   Freight type is properly updated when editing budgets")
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
    success = test_freight_type_update()
    if success:
        print("\n✅ FREIGHT TYPE UPDATE TEST PASSED")
    else:
        print("\n❌ FREIGHT TYPE UPDATE TEST FAILED")