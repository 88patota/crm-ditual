# TODO: Corrigir problema do campo PRAZO (delivery_time) não salvando na criação de orçamento

## Problema Identificado
Ao criar um novo orçamento, o campo PRAZO (delivery_time) não está sendo salvo corretamente. Ao visualizar o orçamento posteriormente, o campo aparece zerado. No entanto, ao editar o orçamento e adicionar novamente o valor do campo PRAZO, ele salva corretamente.

## Análise do Problema
1. O frontend está usando o endpoint simplificado para criação de orçamentos (`/budgets/simplified`)
2. Na função [mapToSimplifiedItems](file:///Users/erikpatekoski/dev/crm-ditual/frontend/src/components/budgets/BudgetForm.tsx#L278-L292) do componente [BudgetForm](file:///Users/erikpatekoski/dev/crm-ditual/frontend/src/components/budgets/BudgetForm.tsx#L59-L359), os itens são mapeados para o formato [BudgetItemSimplified](file:///Users/erikpatekoski/dev/crm-ditual/frontend/src/services/budgetService.ts#L13-L26)
3. O campo `delivery_time` não está sendo incluído no mapeamento para o formato simplificado
4. No backend, no endpoint [create_simplified_budget](file:///Users/erikpatekoski/dev/crm-ditual/services/budget_service/app/api/v1/endpoints/budgets.py#L494-L569), ao converter de [BudgetItemSimplified](file:///Users/erikpatekoski/dev/crm-ditual/services/budget_service/app/schemas/budget.py#L12-L37) para [BudgetItemCreate](file:///Users/erikpatekoski/dev/crm-ditual/services/budget_service/app/schemas/budget.py#L79-L81), o campo `delivery_time` está sendo definido com um valor padrão (`'0'`) em vez de usar o valor real do item

## Solução Proposta

### Parte 1: Frontend - Adicionar delivery_time ao mapeamento
1. Modificar a função [mapToSimplifiedItems](file:///Users/erikpatekoski/dev/crm-ditual/frontend/src/components/budgets/BudgetForm.tsx#L278-L292) no componente [BudgetForm.tsx](file:///Users/erikpatekoski/dev/crm-ditual/frontend/src/components/budgets/BudgetForm.tsx) para incluir o campo `delivery_time` no mapeamento

### Parte 2: Backend - Corrigir tratamento do delivery_time
1. Modificar o schema [BudgetItemSimplified](file:///Users/erikpatekoski/dev/crm-ditual/services/budget_service/app/schemas/budget.py#L12-L37) para incluir o campo `delivery_time`
2. Atualizar o endpoint [create_simplified_budget](file:///Users/erikpatekoski/dev/crm-ditual/services/budget_service/app/api/v1/endpoints/budgets.py#L494-L569) para usar o valor real de `delivery_time` ao criar os itens

## Implementação Detalhada

### Parte 1: Frontend
Arquivo: [frontend/src/components/budgets/BudgetForm.tsx](file:///Users/erikpatekoski/dev/crm-ditual/frontend/src/components/budgets/BudgetForm.tsx)

```typescript
// Na função mapToSimplifiedItems, adicionar delivery_time:
const mapToSimplifiedItems = () => {
  return items.map(item => ({
    description: item.description,
    peso_compra: item.weight ?? 0,
    valor_com_icms_compra: item.purchase_value_with_icms ?? 0,
    percentual_icms_compra: item.purchase_icms_percentage ?? 0,
    outras_despesas_item: item.purchase_other_expenses ?? 0,
    peso_venda: item.sale_weight ?? item.weight ?? 0,
    valor_com_icms_venda: item.sale_value_with_icms ?? 0,
    percentual_icms_venda: item.sale_icms_percentage ?? 0,
    percentual_ipi: item.ipi_percentage ?? 0.0,
    delivery_time: item.delivery_time ?? "0" // Adicionar esta linha
  }));
};
```

### Parte 2: Backend
Arquivo: [services/budget_service/app/schemas/budget.py](file:///Users/erikpatekoski/dev/crm-ditual/services/budget_service/app/schemas/budget.py)

```python
# No schema BudgetItemSimplified, adicionar delivery_time:
class BudgetItemSimplified(BaseModel):
    """Schema com apenas os campos obrigatórios conforme especificado (nomes em português)"""
    # Campos obrigatórios
    description: str
    peso_compra: Optional[float] = 1.0  # Peso de compra, padrão 1.0
    peso_venda: Optional[float] = None  # Se não fornecido, usa peso_compra
    valor_com_icms_compra: float  # Valor de compra com ICMS
    percentual_icms_compra: float = 0.18  # Percentual ICMS compra (formato decimal 0.18 = 18%)
    outras_despesas_item: Optional[float] = 0.0  # Outras despesas do item
    valor_com_icms_venda: float  # Valor de venda com ICMS
    percentual_icms_venda: float = 0.18  # Percentual ICMS venda (formato decimal 0.18 = 18%)
    percentual_ipi: float = 0.0  # Percentual IPI (formato decimal: 0.0, 0.0325, 0.05)
    delivery_time: Optional[str] = "0"  # Adicionar esta linha - Prazo de entrega em dias (0 = imediato)
    
    # ... restante do código
```

Arquivo: [services/budget_service/app/api/v1/endpoints/budgets.py](file:///Users/erikpatekoski/dev/crm-ditual/services/budget_service/app/api/v1/endpoints/budgets.py)

```python
# No endpoint create_simplified_budget, ao criar os BudgetItemCreate, usar o delivery_time real:
# Converter resultados para formato BudgetItemCreate
items_for_creation = []
for calculated_item in budget_result['items']:
    # Obter delivery_time do item original
    original_item = items_data[len(items_for_creation)] if len(items_data) > len(items_for_creation) else {}
    
    items_for_creation.append(BudgetItemCreate(
        description=calculated_item['description'],
        weight=calculated_item['peso_compra'],
        delivery_time=original_item.get('delivery_time', '0'),  # Usar delivery_time do item original
        purchase_value_with_icms=calculated_item['valor_com_icms_compra'],
        purchase_icms_percentage=calculated_item['percentual_icms_compra'],
        purchase_other_expenses=calculated_item['outras_despesas_distribuidas'],
        purchase_value_without_taxes=calculated_item['valor_sem_impostos_compra'],
        purchase_value_with_weight_diff=calculated_item.get('valor_corrigido_peso'),
        sale_weight=calculated_item['peso_venda'],
        sale_value_with_icms=calculated_item['valor_com_icms_venda'],
        sale_icms_percentage=calculated_item['percentual_icms_venda'],
        sale_value_without_taxes=calculated_item['valor_sem_impostos_venda'],
        weight_difference=calculated_item.get('diferenca_peso'),
        ipi_percentage=calculated_item['percentual_ipi'],
        commission_percentage=0
    ))
```

## Testes Necessários
1. Criar um novo orçamento com valores de PRAZO preenchidos
2. Verificar se os valores de PRAZO são salvos corretamente
3. Visualizar o orçamento criado e confirmar que os valores de PRAZO estão presentes
4. Editar o orçamento e verificar que os valores de PRAZO continuam corretos

## Observações
Esta correção resolve o problema de inconsistência entre a criação e edição de orçamentos em relação ao campo PRAZO.