import asyncio
import sys
sys.path.append('/Users/erikpatekoski/dev/crm-ditual/services/budget_service')

from app.core.database import get_db
from app.services.budget_service import BudgetService

async def test_payment_condition():
    async for db in get_db():
        budget = await BudgetService.get_budget_by_id(db, 132)
        if budget:
            print(f"Budget ID: {budget.id}")
            print(f"Order Number: {budget.order_number}")
            print(f"Payment Condition: {repr(budget.payment_condition)}")
            print(f"Payment Condition Type: {type(budget.payment_condition)}")
        else:
            print("Budget not found")
        break

if __name__ == "__main__":
    asyncio.run(test_payment_condition())