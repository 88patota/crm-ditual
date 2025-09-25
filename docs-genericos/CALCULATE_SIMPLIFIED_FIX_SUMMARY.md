# Fix for /calculate-simplified Endpoint

## Problem Description

The `/calculate-simplified` endpoint was returning validation errors for missing required fields:

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "items", 0, "quantity"],
      "msg": "Field required"
    },
    {
      "type": "missing", 
      "loc": ["body", "items", 0, "purchase_value_with_icms"],
      "msg": "Field required"
    },
    {
      "type": "missing",
      "loc": ["body", "items", 0, "sale_value_with_icms"], 
      "msg": "Field required"
    }
  ]
}
```

## Root Causes

1. **Quantity field requirement**: The system was still requiring a `quantity` field, but per user requirements, this field should no longer be used.

2. **Field name mismatch**: Test files were using old Portuguese field names that didn't match the current schema:
   - `valor_com_icms_compra` → should be `purchase_value_with_icms`
   - `valor_com_icms_venda` → should be `sale_value_with_icms`

## Changes Made

### 1. Schema Updates (`services/budget_service/app/schemas/budget.py`)

- **Removed `quantity` field** from `BudgetItemSimplified` schema
- **Removed quantity validation** that required quantity > 0
- Made `weight` field optional with default value of 1.0

### 2. Calculator Service Updates (`services/budget_service/app/services/budget_calculator.py`)

- **Updated `calculate_simplified_item()`** to not depend on quantity field
- **Updated `calculate_simplified_budget()`** to not access `item_input.quantity`
- **Updated `validate_simplified_budget_data()`** to remove quantity validation
- Set default quantity to 1.0 in calculations for backward compatibility

### 3. Test Files Updated

- Fixed field names in test files to use current schema:
  - `peso_compra` → `weight`
  - `valor_com_icms_compra` → `purchase_value_with_icms` 
  - `valor_com_icms_venda` → `sale_value_with_icms`
  - `percentual_icms_compra` → `purchase_icms_percentage`
  - `percentual_icms_venda` → `sale_icms_percentage`

## Current Working Schema

The `/calculate-simplified` endpoint now expects this structure:

```json
{
  "client_name": "Test Client",
  "items": [{
    "description": "Test Item",
    "weight": 10.0,                          // Optional, defaults to 1.0
    "purchase_value_with_icms": 100.0,       // Required
    "purchase_icms_percentage": 18.0,        // Required, percentage format (0-100)
    "purchase_other_expenses": 0.0,          // Optional, defaults to 0.0
    "sale_value_with_icms": 150.0,           // Required  
    "sale_icms_percentage": 17.0             // Required, percentage format (0-100)
  }],
  "notes": "Optional notes"                  // Optional
}
```

## Test Results

✅ **SUCCESS**: Endpoint now returns 200 OK with expected response:

```json
{
  "total_purchase_value": 744.15,
  "total_sale_value": 1129.84, 
  "total_commission": 22.5,
  "profitability_percentage": 51.83,
  "markup_percentage": 51.83,
  "items_calculations": [
    {
      "description": "Test Item",
      "quantity": 1.0,
      "total_purchase": 744.15,
      "total_sale": 1129.84,
      "profitability": 51.83,
      "commission_value": 22.5
    }
  ]
}
```

## Key Points

1. **Quantity field removed**: No longer required in requests, defaults to 1.0 internally
2. **Field names standardized**: All field names now match the English schema
3. **Backward compatibility**: Calculations still work correctly without quantity
4. **Weight-based calculations**: System uses `weight` field for calculations instead of quantity

The endpoint is now fully functional and matches the current system architecture.
