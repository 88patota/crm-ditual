#!/usr/bin/env python3

import requests
import sys
import json

def test_pdf_export_fix():
    """Test both simplified and full PDF export to verify the fix"""
    
    base_url = "http://localhost:3000/api/v1"
    
    print("🔍 Testing PDF Export Fix...")
    
    # Test data for creating a budget (we'll create a test budget to export)
    test_budget = {
        "order_number": "PDF-TEST-001",
        "client_name": "Test Client for PDF",
        "markup_percentage": 50.0,
        "notes": "Test budget for PDF export fix verification",
        "items": [
            {
                "description": "Test Item 1",
                "weight": 10.0,
                "purchase_value_with_icms": 100.0,
                "purchase_icms_percentage": 17.0,
                "purchase_other_expenses": 5.0,
                "purchase_value_without_taxes": 83.0,
                "sale_weight": 10.0,
                "sale_value_with_icms": 150.0,
                "sale_icms_percentage": 17.0,
                "sale_value_without_taxes": 124.5,
                "profitability": 50.0,
                "total_purchase": 1000.0,
                "total_sale": 1500.0,
                "unit_value": 150.0,
                "total_value": 1500.0,
                "commission_percentage": 1.5,
                "commission_value": 22.5
            }
        ]
    }
    
    print("\n🧪 Step 1: Creating test budget...")
    
    try:
        # Create budget
        response = requests.post(f"{base_url}/budgets/", json=test_budget)
        
        if response.status_code == 201:
            budget = response.json()
            budget_id = budget["id"]
            print(f"✅ Created test budget with ID: {budget_id}")
        else:
            print(f"❌ Failed to create budget: {response.status_code} - {response.text}")
            # Try with existing budget ID 72 instead
            budget_id = 72
            print(f"🔄 Using existing budget ID: {budget_id}")
    
    except Exception as e:
        print(f"❌ Error creating budget: {str(e)}")
        # Use known budget ID
        budget_id = 72
        print(f"🔄 Using existing budget ID: {budget_id}")
    
    print(f"\n🧪 Step 2: Testing simplified PDF export...")
    
    try:
        # Test simplified PDF export
        response = requests.get(f"{base_url}/budgets/{budget_id}/export-pdf?simplified=true")
        
        if response.status_code == 200:
            print(f"✅ Simplified PDF export successful! Size: {len(response.content)} bytes")
            print(f"   Content-Type: {response.headers.get('content-type', 'unknown')}")
        else:
            print(f"❌ Simplified PDF export failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ Error during simplified PDF test: {str(e)}")
        return False
    
    print(f"\n🧪 Step 3: Testing full PDF export...")
    
    try:
        # Test full PDF export (this was the failing one)
        response = requests.get(f"{base_url}/budgets/{budget_id}/export-pdf?simplified=false")
        
        if response.status_code == 200:
            print(f"✅ Full PDF export successful! Size: {len(response.content)} bytes")
            print(f"   Content-Type: {response.headers.get('content-type', 'unknown')}")
        else:
            print(f"❌ Full PDF export failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ Error during full PDF test: {str(e)}")
        return False
    
    print(f"\n✅ All PDF export tests passed! The fix is working correctly.")
    return True

if __name__ == "__main__":
    print("🔍 Verifying PDF Export Fix...")
    success = test_pdf_export_fix()
    
    if success:
        print("\n🎉 PDF export fix verified successfully!")
        print("   Both simplified and full PDF generation are working.")
    else:
        print("\n❌ PDF export fix verification failed!")
        print("   There are still issues with the PDF export functionality.")
        sys.exit(1)
