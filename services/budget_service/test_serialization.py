import asyncio
import sys
sys.path.append('/Users/erikpatekoski/dev/crm-ditual/services/budget_service')

from app.core.database import get_db
from app.services.budget_service import BudgetService
from app.schemas.budget import BudgetResponse

async def test_serialization():
    async for db in get_db():
        budget = await BudgetService.get_budget_by_id(db, 132)
        if budget:
            print(f"Raw Budget payment_condition: {repr(budget.payment_condition)}")
            
            # Test Pydantic serialization
            try:
                budget_response = BudgetResponse.from_orm(budget)
                print(f"Serialized payment_condition: {repr(budget_response.payment_condition)}")
                
                # Test dict conversion
                budget_dict = budget_response.dict()
                print(f"Dict payment_condition: {repr(budget_dict.get('payment_condition'))}")
                
                # Test JSON serialization
                import json
                budget_json = budget_response.json()
                parsed_json = json.loads(budget_json)
                print(f"JSON payment_condition: {repr(parsed_json.get('payment_condition'))}")
                
            except Exception as e:
                print(f"Serialization error: {e}")
        else:
            print("Budget not found")
        break

if __name__ == "__main__":
    asyncio.run(test_serialization())