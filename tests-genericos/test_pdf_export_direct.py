#!/usr/bin/env python3

import sys
import os
import traceback

# Add the budget service to sys.path
sys.path.insert(0, '/Users/erikpatekoski/dev/crm-ditual/services/budget_service')

def test_pdf_direct():
    """Test PDF generation directly without database to isolate the issue"""
    try:
        from app.services.pdf_export_service import PDFExportService
        from app.models.budget import Budget, BudgetItem, BudgetStatus
        from datetime import datetime
        
        print("🔍 Testing PDF generation directly...")
        
        # Create a mock budget item with all required fields
        mock_item = type('MockBudgetItem', (), {
            'description': 'Test Item',
            'weight': 10.0,
            'purchase_value_with_icms': 100.0,
            'purchase_icms_percentage': 17.0,
            'purchase_other_expenses': 5.0,
            'purchase_value_without_taxes': 83.0,
            'sale_weight': 10.0,
            'sale_value_with_icms': 150.0,
            'sale_icms_percentage': 17.0,
            'sale_value_without_taxes': 124.5,
            'profitability': 50.0,
            'total_purchase': 1000.0,
            'total_sale': 1500.0,
            'unit_value': 150.0,
            'total_value': 1500.0,
            'commission_percentage': 1.5,
            'commission_value': 22.5
        })()
        
        # Create a mock budget with all required fields
        mock_budget = type('MockBudget', (), {
            'id': 1,
            'order_number': 'PED-0001',
            'client_name': 'Test Client',
            'markup_percentage': 50.0,
            'total_purchase_value': 1000.0,
            'total_sale_value': 1500.0,
            'total_commission': 22.5,
            'profitability_percentage': 50.0,
            'notes': 'Test notes',
            'created_by': 'test_user',
            'created_at': datetime.now(),
            'expires_at': None,
            'status': type('MockStatus', (), {'value': 'draft'})(),
            'items': [mock_item]
        })()
        
        # Test PDF service initialization
        pdf_service = PDFExportService()
        print("✅ PDF service initialized successfully")
        
        # Test simplified PDF generation
        print("\n🧪 Testing simplified PDF generation...")
        try:
            pdf_content = pdf_service.generate_simplified_proposal_pdf(mock_budget)
            print(f"✅ Simplified PDF generated successfully! Size: {len(pdf_content)} bytes")
        except Exception as e:
            print(f"❌ Simplified PDF generation failed: {str(e)}")
            print(f"   Error type: {type(e).__name__}")
            traceback.print_exc()
            return False
        
        # Test full PDF generation
        print("\n🧪 Testing full PDF generation...")
        try:
            pdf_content = pdf_service.generate_proposal_pdf(mock_budget)
            print(f"✅ Full PDF generated successfully! Size: {len(pdf_content)} bytes")
        except Exception as e:
            print(f"❌ Full PDF generation failed: {str(e)}")
            print(f"   Error type: {type(e).__name__}")
            traceback.print_exc()
            return False
        
        print(f"\n✅ All PDF tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        print(f"   Error type: {type(e).__name__}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Testing PDF Export Direct Generation...")
    success = test_pdf_direct()
    
    if success:
        print("\n✅ Direct test completed successfully")
    else:
        print("\n❌ Direct test failed - this shows the root cause of the 500 error")
