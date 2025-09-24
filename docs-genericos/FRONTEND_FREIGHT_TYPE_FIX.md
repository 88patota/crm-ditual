# Correção do Bug: Campo Freight Type não sendo atualizado corretamente no Frontend

## Problema Identificado

O problema estava no frontend, especificamente na forma como o campo [freight_type](file:///Users/erikpatekoski/dev/crm-ditual/services/budget_service/app/models/budget.py#L43-L43) estava sendo tratado nos formulários de orçamento. Mesmo quando o usuário não alterava o valor do campo frete, o frontend estava enviando um valor padrão, o que causava comportamentos inesperados no backend.

## Causa Raiz

### 1. Tratamento Incorreto no Serviço de Orçamento
No arquivo [frontend/src/services/budgetService.ts](file:///Users/erikpatekoski/dev/crm-ditual/frontend/src/services/budgetService.ts), o método [updateBudget](file:///Users/erikpatekoski/dev/crm-ditual/frontend/src/services/budgetService.ts#L215-L226) estava forçando a inclusão do campo [freight_type](file:///Users/erikpatekoski/dev/crm-ditual/services/budget_service/app/models/budget.py#L43-L43) nos dados de atualização, mesmo quando o valor era `undefined`:

```typescript
// Código problemático
const updateData = {
  ...budget,
  freight_type: budget.freight_type  // Isso força a inclusão mesmo quando undefined
};
```

### 2. Tratamento Incorreto nos Formulários
Nos arquivos de formulário ([BudgetForm.tsx](file:///Users/erikpatekoski/dev/crm-ditual/frontend/src/components/budgets/BudgetForm.tsx) e [SimplifiedBudgetForm.tsx](file:///Users/erikpatekoski/dev/crm-ditual/frontend/src/components/budgets/SimplifiedBudgetForm.tsx)), o código estava definindo um valor padrão para [freight_type](file:///Users/erikpatekoski/dev/crm-ditual/services/budget_service/app/models/budget.py#L43-L43) mesmo quando o campo não havia sido alterado:

```typescript
// Código problemático
freight_type: formData.freight_type || initialData?.freight_type || 'FOB',
```

Isso fazia com que o frontend sempre enviasse um valor para [freight_type](file:///Users/erikpatekoski/dev/crm-ditual/services/budget_service/app/models/budget.py#L43-L43), mesmo quando o usuário não tinha alterado o campo.

## Solução Implementada

### 1. Correção no Serviço de Orçamento
Modificamos o método [updateBudget](file:///Users/erikpatekoski/dev/crm-ditual/frontend/src/services/budgetService.ts#L215-L226) em [frontend/src/services/budgetService.ts](file:///Users/erikpatekoski/dev/crm-ditual/frontend/src/services/budgetService.ts) para apenas incluir [freight_type](file:///Users/erikpatekoski/dev/crm-ditual/services/budget_service/app/models/budget.py#L43-L43) nos dados de atualização quando ele foi explicitamente fornecido:

```typescript
// Correção
const updateData = { ...budget };

// Only add freight_type to updateData if it's explicitly provided (not undefined)
if (budget.freight_type !== undefined) {
  updateData.freight_type = budget.freight_type;
}
```

### 2. Correção nos Formulários
Modificamos ambos os formulários ([BudgetForm.tsx](file:///Users/erikpatekoski/dev/crm-ditual/frontend/src/components/budgets/BudgetForm.tsx) e [SimplifiedBudgetForm.tsx](file:///Users/erikpatekoski/dev/crm-ditual/frontend/src/components/budgets/SimplifiedBudgetForm.tsx)) para:

#### a) Apenas incluir [freight_type](file:///Users/erikpatekoski/dev/crm-ditual/services/budget_service/app/models/budget.py#L43-L43) nos dados de envio quando foi alterado:
```typescript
// Correção
...(formData.freight_type !== undefined && { freight_type: formData.freight_type }),
```

#### b) Apenas definir valores iniciais quando apropriado:
```typescript
// Correção para Form initialValues
{...(!initialData && { freight_type: 'FOB' })},

// Correção para initialData setup
...(initialData.freight_type !== undefined && { freight_type: initialData.freight_type }),
```

### 3. Correção nos Valores Iniciais do Formulário
Modificamos os valores iniciais dos formulários para apenas definir [freight_type](file:///Users/erikpatekoski/dev/crm-ditual/services/budget_service/app/models/budget.py#L43-L43) como 'FOB' para novos orçamentos, não para orçamentos existentes que estão sendo editados:

```typescript
// Correção
initialValues={{
  status: 'draft',
  // Only set freight_type default for new budgets, not for editing
  ...(!initialData && { freight_type: 'FOB' }),
}}
```

## Arquivos Modificados

1. [frontend/src/services/budgetService.ts](file:///Users/erikpatekoski/dev/crm-ditual/frontend/src/services/budgetService.ts) - Correção no método [updateBudget](file:///Users/erikpatekoski/dev/crm-ditual/frontend/src/services/budgetService.ts#L215-L226)
2. [frontend/src/components/budgets/BudgetForm.tsx](file:///Users/erikpatekoski/dev/crm-ditual/frontend/src/components/budgets/BudgetForm.tsx) - Correção na função [handleSubmit](file:///Users/erikpatekoski/dev/crm-ditual/frontend/src/components/budgets/BudgetForm.tsx#L266-L297) e no [useEffect](file:///Users/erikpatekoski/dev/crm-ditual/frontend/src/components/budgets/BudgetForm.tsx#L52-L127)
3. [frontend/src/components/budgets/SimplifiedBudgetForm.tsx](file:///Users/erikpatekoski/dev/crm-ditual/frontend/src/components/budgets/SimplifiedBudgetForm.tsx) - Correção na função [handleSubmit](file:///Users/erikpatekoski/dev/crm-ditual/frontend/src/components/budgets/SimplifiedBudgetForm.tsx#L375-L409) e no [useEffect](file:///Users/erikpatekoski/dev/crm-ditual/frontend/src/components/budgets/SimplifiedBudgetForm.tsx#L123-L312)

## Teste de Verificação

Criamos um teste específico ([tests-genericos/test_frontend_freight_type_fix.py](file:///Users/erikpatekoski/dev/crm-ditual/tests-genericos/test_frontend_freight_type_fix.py)) para verificar que a correção funciona corretamente:

- ✅ Comportamento antigo do frontend ainda funciona (compatibilidade)
- ✅ Novo comportamento apenas envia [freight_type](file:///Users/erikpatekoski/dev/crm-ditual/services/budget_service/app/models/budget.py#L43-L43) quando alterado
- ✅ Valores são corretamente atualizados quando alterados
- ✅ Valores não são alterados quando não enviados

## Validação

A correção foi testada e validada com os seguintes cenários:
- ✅ Edição de orçamento sem alterar o campo frete (não deve enviar [freight_type](file:///Users/erikpatekoski/dev/crm-ditual/services/budget_service/app/models/budget.py#L43-L43))
- ✅ Edição de orçamento alterando o campo frete (deve enviar o novo valor)
- ✅ Criação de novo orçamento (deve usar 'FOB' como padrão)
- ✅ Compatibilidade com o comportamento anterior

## Impacto

Esta correção resolve o problema relatado sem afetar outras funcionalidades do sistema. O campo [freight_type](file:///Users/erikpatekoski/dev/crm-ditual/services/budget_service/app/models/budget.py#L43-L43) agora é corretamente tratado no frontend, sendo enviado apenas quando necessário, o que previne comportamentos inesperados no backend.