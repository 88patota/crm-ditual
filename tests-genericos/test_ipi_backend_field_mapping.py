import asyncio
import httpx

async def test_ipi_backend_field_mapping():
    """Test to understand the actual field names returned by the backend when editing budgets"""
    
    # First, create a budget with IPI
    budget_data = {
        "order_number": "TEST-IPI-FIELD-001",
        "client_name": "Cliente Teste IPI Field",
        "status": "draft",
        "items": [
            {
                "description": "Item com IPI 3.25%",
                "peso_compra": 10.0,
                "peso_venda": 10.0,
                "valor_com_icms_compra": 100.0,
                "percentual_icms_compra": 0.18,
                "outras_despesas_item": 0.0,
                "valor_com_icms_venda": 150.0,
                "percentual_icms_venda": 0.18,
                "percentual_ipi": 0.0325  # 3.25%
            }
        ]
    }
    
    async with httpx.AsyncClient() as client:
        # Login first
        login_response = await client.post(
            "http://localhost:8001/api/v1/auth/login",
            data={"username": "admin", "password": "admin123"}
        )
        
        if login_response.status_code != 200:
            print(f"Login failed: {login_response.status_code}")
            return
        
        login_data = login_response.json()
        token = login_data["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create the budget
        print("=== Creating budget with IPI ===")
        create_response = await client.post(
            "http://localhost:8001/api/v1/budgets/simplified",
            json=budget_data,
            headers=headers
        )
        
        if create_response.status_code != 201:
            print(f"Failed to create budget: {create_response.status_code}")
            print(f"Response: {create_response.text}")
            return
        
        created_budget = create_response.json()
        budget_id = created_budget["id"]
        print(f"Created budget ID: {budget_id}")
        print(f"Created budget order number: {created_budget['order_number']}")
        
        # Now retrieve the budget (simulate editing)
        print("\n=== Retrieving budget for editing ===")
        get_response = await client.get(
            f"http://localhost:8001/api/v1/budgets/{budget_id}",
            headers=headers
        )
        
        if get_response.status_code != 200:
            print(f"Failed to retrieve budget: {get_response.status_code}")
            return
        
        retrieved_budget = get_response.json()
        
        print("\n=== ANALYZING BACKEND RESPONSE STRUCTURE ===")
        print("Budget basic fields:")
        for key in retrieved_budget.keys():
            if key != "items":
                print(f"  {key}: {retrieved_budget[key]}")
        
        print("\nItems structure:")
        if retrieved_budget.get("items"):
            for i, item in enumerate(retrieved_budget["items"]):
                print(f"\nItem {i+1}:")
                for key, value in item.items():
                    print(f"  {key}: {value}")
                    if "ipi" in key.lower():
                        print(f"  >>> FOUND IPI FIELD: {key} = {value} <<<")
        
        # Test the mapping logic
        print("\n=== TESTING FIELD MAPPING LOGIC ===")
        if retrieved_budget.get("items"):
            item = retrieved_budget["items"][0]
            
            print(f"Raw item data: {item}")
            
            # Test different field name possibilities
            ipi_fields_to_check = [
                'ipi_percentage',
                'percentual_ipi', 
                'ipi_value',
                'ipi_original'
            ]
            
            for field_name in ipi_fields_to_check:
                if field_name in item:
                    print(f"FOUND: {field_name} = {item[field_name]}")
                else:
                    print(f"NOT FOUND: {field_name}")
            
            # Test the current mapping logic from SimplifiedBudgetForm
            backend_item = item
            
            print("\n=== CURRENT MAPPING LOGIC TEST ===")
            # This is the exact logic from the current SimplifiedBudgetForm.tsx
            percentual_ipi_mapped = (
                backend_item.get('ipi_percentage') if isinstance(backend_item.get('ipi_percentage'), (int, float)) else
                backend_item.get('percentual_ipi') if isinstance(backend_item.get('percentual_ipi'), (int, float)) else
                0.0
            )
            
            print(f"Mapped percentual_ipi value: {percentual_ipi_mapped}")
            print(f"Original IPI from creation: 0.0325 (3.25%)")
            print(f"Mapping successful: {percentual_ipi_mapped == 0.0325}")
        
        print("\n=== CLEANUP ===")
        # Clean up - delete the test budget
        delete_response = await client.delete(
            f"http://localhost:8001/api/v1/budgets/{budget_id}",
            headers=headers
        )
        print(f"Cleanup delete status: {delete_response.status_code}")

if __name__ == "__main__":
    asyncio.run(test_ipi_backend_field_mapping())
