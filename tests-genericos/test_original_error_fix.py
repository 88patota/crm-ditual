#!/usr/bin/env python3

import requests
import json

# Test data with Portuguese field names (as used in the system)
# This is the exact data that was causing the validation error originally
test_data = {
    'items': [
        {
            'description': 'item',
            'peso_compra': 100,
            'peso_venda': 100,
            'valor_com_icms_compra': 3.22,
            'percentual_icms_compra': 0.12,
            'outras_despesas_item': 0,
            'valor_com_icms_venda': 22.12,
            'percentual_icms_venda': 0.15
        }
    ]
}

print('=== TESTING ORIGINAL ERROR DATA ===')
print('Testing with the exact data that was causing the validation error...')
print()
print('Data being sent:')
print(json.dumps(test_data, indent=2))
print()

try:
    response = requests.post('http://localhost:8002/api/v1/budgets/calculate-simplified', 
                           json=test_data,
                           headers={'Content-Type': 'application/json'})
    
    print(f'Status Code: {response.status_code}')
    
    if response.status_code == 200:
        result = response.json()
        print('✅ SUCCESS: No more validation errors!')
        print('✅ The endpoint now accepts Portuguese field names correctly!')
        print()
        print('Response summary:')
        print(f"  - Total Purchase Value: R$ {result['total_purchase_value']}")
        print(f"  - Total Sale Value: R$ {result['total_sale_value']}")
        print(f"  - Profitability: {result['profitability_percentage']:.2f}%")
        print(f"  - Items calculated: {len(result['items_calculations'])}")
    else:
        print('❌ ERROR Response:')
        print(response.text)
        
except Exception as e:
    print(f'❌ Connection error: {e}')
