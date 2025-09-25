# Correção do Bug de IPI na Edição - Resumo

## Problema Identificado
O valor do IPI não estava sendo exibido corretamente ao editar um orçamento. O debug mostrava que o valor original (`ipi_original`) vinha como undefined, sendo processado como 0 (`ipi_processed`).

## Diagnóstico Realizado
1. **Análise do SimplifiedBudgetForm.tsx**: Identificou que o problema estava no mapeamento dos dados do backend para o frontend
2. **Verificação dos schemas**: Confirmou que os schemas estavam corretos no backend
3. **Análise do service**: Verificou que o budgetService estava correto
4. **Identificação da causa**: O backend retorna dados com campos em inglês (ex: `ipi_percentage`), mas o frontend esperava campos em português (ex: `percentual_ipi`)

## Correção Implementada

### Arquivo Modificado: `frontend/src/components/budgets/SimplifiedBudgetForm.tsx`

1. **Adicionada interface BackendBudgetItem**:
```typescript
interface BackendBudgetItem {
  description?: string;
  weight?: number;
  sale_weight?: number;
  purchase_value_with_icms?: number;
  purchase_icms_percentage?: number;
  purchase_other_expenses?: number;
  sale_value_with_icms?: number;
  sale_icms_percentage?: number;
  ipi_percentage?: number; // CAMPO CRÍTICO
  // Campos em português (caso já estejam convertidos)
  peso_compra?: number;
  peso_venda?: number;
  // ... outros campos
}
```

2. **Corrigido o mapeamento dos dados na inicialização**:
```typescript
// ANTES (PROBLEMÁTICO)
percentual_ipi: typeof item.percentual_ipi === 'number' ? item.percentual_ipi : 0.0

// DEPOIS (CORRETO)
percentual_ipi: typeof backendItem.ipi_percentage === 'number' ? backendItem.ipi_percentage :
               typeof item.percentual_ipi === 'number' ? item.percentual_ipi : 0.0
```

3. **Mapeamento completo dos campos**:
   - `weight` → `peso_compra`
   - `sale_weight` → `peso_venda`
   - `purchase_value_with_icms` → `valor_com_icms_compra`
   - `purchase_icms_percentage` → `percentual_icms_compra`
   - `sale_value_with_icms` → `valor_com_icms_venda`
   - `sale_icms_percentage` → `percentual_icms_venda`
   - **`ipi_percentage` → `percentual_ipi`** ← **CORREÇÃO CRÍTICA**

## Código Debug Preservado
Mantido o código de debug no console para facilitar futuras investigações:
```javascript
console.log('=== DEBUG IPI - SimplifiedBudgetForm ===');
console.log('Initial data items:', initialData.items?.map(item => ({ 
  desc: item.description, 
  ipi_original: item.percentual_ipi 
})));
// ... processamento ...
console.log('Items after processing:', itemsWithPreservedIPI.map(item => ({ 
  desc: item.description, 
  ipi_processed: item.percentual_ipi 
})));
console.log('==========================================');
```

## Como a Correção Funciona

1. **Antes da correção**: 
   - Backend enviava `ipi_percentage: 0.0325` (3.25%)
   - Frontend procurava por `percentual_ipi` (undefined)
   - Resultado: IPI era definido como 0.0 (valor padrão)

2. **Após a correção**:
   - Backend envia `ipi_percentage: 0.0325` (3.25%)
   - Frontend primeiro verifica `backendItem.ipi_percentage` (encontra 0.0325)
   - Se não encontrar, verifica `item.percentual_ipi` (fallback)
   - Resultado: IPI é preservado como 0.0325

## Validação
A correção preserva o valor do IPI ao editar orçamentos existentes, solucionando o bug reportado onde o valor aparecia como 0 ao invés do valor correto salvo no banco de dados.

## Arquivos Relacionados
- ✅ `frontend/src/components/budgets/SimplifiedBudgetForm.tsx` - CORRIGIDO
- ✅ `services/budget_service/app/schemas/budget.py` - OK (não precisou alteração)
- ✅ `services/budget_service/app/services/budget_service.py` - OK (não precisou alteração)
- ✅ `frontend/src/services/budgetService.ts` - OK (não precisou alteração)

## Status: ✅ RESOLVIDO
O bug do IPI na edição foi corrigido através do mapeamento correto dos campos do backend para o frontend.
