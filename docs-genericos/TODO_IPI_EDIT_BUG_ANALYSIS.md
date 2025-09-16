# TODO LIST: IPI Edit Bug Analysis and Fix

## 🔍 PROBLEM IDENTIFIED

**Root Cause:** Field name inconsistency between backend and frontend causing IPI values to not display when editing budgets.

### Backend Response (Correct):
```json
{
  "ipi_percentage": 0.0325,  // Backend uses English field name
  "ipi_value": 10.14,
  "total_ipi_value": 10.14
}
```

### Frontend Interface (Problematic):
```typescript
// BudgetItemSimplified uses Portuguese field names
export interface BudgetItemSimplified {
  percentual_ipi?: number;  // Frontend expects Portuguese field name
}

// But BudgetItem uses English field names  
export interface BudgetItem {
  ipi_percentage?: number;  // English field name
}
```

### Current Mapping Logic Issues:
1. Complex field mapping in SimplifiedBudgetForm.tsx with multiple fallback attempts
2. Language inconsistency between interfaces (`percentual_ipi` vs `ipi_percentage`)
3. Overly complex useEffect logic that fails to properly map `ipi_percentage` to `percentual_ipi`

## 📋 TODO LIST

### Phase 1: Interface Standardization
- [ ] **1.1** Update `BudgetItemSimplified` interface in `budgetService.ts`
  - [ ] Change `percentual_ipi?: number` to `ipi_percentage?: number`
  - [ ] Ensure consistency with backend field naming
  
- [ ] **1.2** Update all Portuguese field names to English in `BudgetItemSimplified`
  - [ ] `peso_compra` → `weight` (or keep as is if backend expects Portuguese)
  - [ ] `peso_venda` → `sale_weight` 
  - [ ] `valor_com_icms_compra` → `purchase_value_with_icms`
  - [ ] `percentual_icms_compra` → `purchase_icms_percentage`
  - [ ] `outras_despesas_item` → `purchase_other_expenses`
  - [ ] `valor_com_icms_venda` → `sale_value_with_icms`
  - [ ] `percentual_icms_venda` → `sale_icms_percentage`
  - [ ] `percentual_ipi` → `ipi_percentage`

### Phase 2: Form Component Updates
- [ ] **2.1** Update `SimplifiedBudgetForm.tsx` field references
  - [ ] Update all form field names to match new interface
  - [ ] Update `updateItem` function calls
  - [ ] Update table column `dataIndex` properties
  - [ ] Update `initialBudgetItem` object

- [ ] **2.2** Simplify useEffect mapping logic
  - [ ] Remove complex field name fallback logic
  - [ ] Use direct field mapping: `item.ipi_percentage`
  - [ ] Remove Portuguese field name mapping
  - [ ] Remove debug console logs

- [ ] **2.3** Update form validation and submission
  - [ ] Ensure `handleSubmit` uses correct field names
  - [ ] Update field parsing logic for numeric values
  - [ ] Test form submission with IPI values

### Phase 3: Testing and Validation
- [ ] **3.1** Test IPI value display in edit mode
  - [ ] Create budget with IPI = 3.25%
  - [ ] Edit budget and verify IPI displays correctly
  - [ ] Test with IPI = 5% and IPI = 0%

- [ ] **3.2** Test form functionality
  - [ ] Test adding/removing items
  - [ ] Test IPI dropdown selection
  - [ ] Test calculation preview
  - [ ] Test budget saving

- [ ] **3.3** Test backend integration
  - [ ] Verify data is sent with correct field names
  - [ ] Verify backend responses are properly mapped
  - [ ] Test complete create/edit/view cycle

### Phase 4: Cleanup and Documentation
- [ ] **4.1** Remove unused interfaces and types
  - [ ] Remove `BackendBudgetItem` interface if no longer needed
  - [ ] Remove `BudgetItemWithBackendFields` interface if no longer needed
  - [ ] Clean up import statements

- [ ] **4.2** Add proper TypeScript typing
  - [ ] Ensure all form fields have proper types
  - [ ] Add type safety for field updates
  - [ ] Fix any TypeScript errors

- [ ] **4.3** Document the fix
  - [ ] Update README with field naming conventions
  - [ ] Add comments explaining IPI field mapping
  - [ ] Document the interface standardization

## 🎯 EXPECTED OUTCOME

After completing this TODO list:

1. ✅ IPI values will display correctly when editing budgets
2. ✅ Frontend and backend will use consistent English field names
3. ✅ Complex field mapping logic will be simplified
4. ✅ Form functionality will be more reliable and maintainable
5. ✅ TypeScript type safety will be improved

## 🚨 CRITICAL PRIORITY

**Immediate Fix Needed:**
- Update `BudgetItemSimplified.percentual_ipi` to `ipi_percentage`
- Update `SimplifiedBudgetForm.tsx` to use `ipi_percentage` consistently
- Test IPI display in edit mode

This is a **HIGH PRIORITY** bug affecting core budget editing functionality.

## ⏱️ ESTIMATED TIME

- **Phase 1:** 30 minutes (Interface updates)
- **Phase 2:** 45 minutes (Form component updates) 
- **Phase 3:** 30 minutes (Testing)
- **Phase 4:** 15 minutes (Cleanup)

**Total Estimated Time:** ~2 hours

---

## 📝 NOTES

- The backend correctly returns `ipi_percentage: 0.0325`
- The issue is purely frontend field mapping
- Solution: Standardize all field names to English (matching backend)
- Keep it simple - avoid complex field name fallback logic
