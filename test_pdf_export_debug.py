#!/usr/bin/env python3

import asyncio
import sys
import os

# Add the budget service to sys.path
sys.path.insert(0, '/Users/erikpatekoski/dev/crm-ditual/services/budget_service')

# Set environment variables
os.environ['DATABASE_URL'] = 'postgresql+asyncpg://postgres:postgres@localhost:5433/crm_ditual'

async def test_pdf_export():
    """Test PDF export functionality to identify the 500 error"""
    from app.core.database import get_db
    from app.services.budget_service import BudgetService
    from app.services.pdf_export_service import pdf_export_service
    
    try:
        # Get database session
        async for db in get_db():
            # Fetch budget ID 72
            budget = await BudgetService.get_budget_by_id(db, 72)
            
            if not budget:
                print("❌ Budget 72 not found")
                return False
            
            print(f"✅ Found budget: {budget.order_number}")
            print(f"   Client: {budget.client_name}")
            print(f"   Items count: {len(budget.items) if budget.items else 0}")
            
            # Check if budget has items
            if not budget.items or len(budget.items) == 0:
                print("❌ Budget has no items - this could cause PDF generation issues")
                return False
            
            # Examine first item to check field availability
            first_item = budget.items[0]
            print(f"\n🔍 Checking first item fields:")
            
            # Check for fields used in PDF generation
            required_fields = [
                'description', 'weight', 'purchase_value_with_icms', 
                'purchase_icms_percentage', 'purchase_other_expenses',
                'purchase_value_without_taxes', 'sale_weight', 'sale_value_with_icms',
                'sale_icms_percentage', 'sale_value_without_taxes', 'profitability',
                'total_purchase', 'total_sale', 'unit_value', 'total_value',
                'commission_percentage', 'commission_value'
            ]
            
            missing_fields = []
            for field in required_fields:
                if not hasattr(first_item, field):
                    missing_fields.append(field)
                    print(f"   ❌ Missing field: {field}")
                else:
                    value = getattr(first_item, field)
                    print(f"   ✅ {field}: {value}")
            
            # Check if model has quantity field (used in simplified PDF)
            if not hasattr(first_item, 'quantity'):
                print("   ❌ Missing field: quantity (used in simplified PDF)")
                missing_fields.append('quantity')
            else:
                print(f"   ✅ quantity: {getattr(first_item, 'quantity')}")
            
            if missing_fields:
                print(f"\n❌ Found {len(missing_fields)} missing fields that could cause PDF generation to fail")
                return False
            
            # Try to generate simplified PDF
            print(f"\n🧪 Testing simplified PDF generation...")
            
            try:
                pdf_content = pdf_export_service.generate_simplified_proposal_pdf(budget)
                print(f"✅ Simplified PDF generated successfully! Size: {len(pdf_content)} bytes")
            except Exception as pdf_error:
                print(f"❌ Simplified PDF generation failed: {str(pdf_error)}")
                print(f"   Error type: {type(pdf_error).__name__}")
                import traceback
                traceback.print_exc()
                return False
            
            # Try to generate full PDF
            print(f"\n🧪 Testing full PDF generation...")
            
            try:
                pdf_content = pdf_export_service.generate_proposal_pdf(budget)
                print(f"✅ Full PDF generated successfully! Size: {len(pdf_content)} bytes")
            except Exception as pdf_error:
                print(f"❌ Full PDF generation failed: {str(pdf_error)}")
                print(f"   Error type: {type(pdf_error).__name__}")
                import traceback
                traceback.print_exc()
                return False
            
            print(f"\n✅ All PDF tests passed!")
            return True
            
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Testing PDF Export Functionality...")
    success = asyncio.run(test_pdf_export())
    
    if success:
        print("\n✅ Test completed successfully")
    else:
        print("\n❌ Test failed - this explains the 500 error")
