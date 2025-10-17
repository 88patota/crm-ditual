import asyncio
import sys
sys.path.append('/Users/erikpatekoski/dev/crm-ditual/services/budget_service')

from app.core.database import get_db
from app.services.budget_service import BudgetService
from app.schemas.budget import BudgetResponse
import json

async def test_api_serialization():
    async for db in get_db():
        budget = await BudgetService.get_budget_by_id(db, 132)
        if budget:
            print(f"Raw Budget payment_condition: {repr(budget.payment_condition)}")
            print(f"Raw Budget type: {type(budget)}")
            
            # Test direct Pydantic serialization (como a API faz)
            try:
                # Simular o que a API faz
                budget_response = BudgetResponse.from_orm(budget)
                print(f"BudgetResponse payment_condition: {repr(budget_response.payment_condition)}")
                
                # Test JSON serialization (como FastAPI faz)
                budget_json = budget_response.json()
                parsed_json = json.loads(budget_json)
                print(f"JSON payment_condition: {repr(parsed_json.get('payment_condition'))}")
                
                # Test dict conversion
                budget_dict = budget_response.dict()
                print(f"Dict payment_condition: {repr(budget_dict.get('payment_condition'))}")
                
                # Check if field is excluded
                print(f"All fields in dict: {list(budget_dict.keys())}")
                print(f"payment_condition in dict: {'payment_condition' in budget_dict}")
                
            except Exception as e:
                print(f"Serialization error: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("Budget not found")
        break

if __name__ == "__main__":
    asyncio.run(test_api_serialization())