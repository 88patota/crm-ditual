# Funcionalidade de Tipo de Frete (CIF/FOB)

## Resumo da Implementação

Foi implementada uma nova funcionalidade que permite aos vendedores selecionar o tipo de frete (CIF ou FOB) ao criar ou editar orçamentos. Esta informação é exibida na visualização do orçamento e também é incluída no PDF da proposta comercial.

## Funcionalidades Implementadas

### 1. Backend

#### Banco de Dados
- Adicionada coluna `freight_type` na tabela `budgets` com tipo VARCHAR(10)
- Valores permitidos: "CIF" ou "FOB"
- Valor padrão: "FOB"

#### Modelo de Dados
- Atualizado o modelo [Budget](file:///Users/erikpatekoski/dev/crm-ditual/frontend/src/services/budgetService.ts#L136-L162) para incluir o campo `freight_type`
- Tipo: String, obrigatório, valor padrão "FOB"

#### Schemas Pydantic
- Atualizados os schemas para incluir o campo `freight_type`:
  - [BudgetBase](file:///Users/erikpatekoski/dev/crm-ditual/services/budget_service/app/schemas/budget.py#L178-L200)
  - [BudgetSimplifiedCreate](file:///Users/erikpatekoski/dev/crm-ditual/services/budget_service/app/schemas/budget.py#L55-L80)
  - [BudgetCreate](file:///Users/erikpatekoski/dev/crm-ditual/frontend/src/pages/BudgetCreate.tsx#L7-L51)
  - [BudgetUpdate](file:///Users/erikpatekoski/dev/crm-ditual/services/budget_service/app/schemas/budget.py#L207-L214)
  - [BudgetResponse](file:///Users/erikpatekoski/dev/crm-ditual/services/budget_service/app/schemas/budget.py#L217-L239)

### 2. Frontend

#### Formulário de Orçamento
- Adicionado campo de seleção "Frete" no formulário de criação/edição de orçamentos
- Opções: "CIF" ou "FOB"
- Posicionado na seção de informações gerais do orçamento
- Valor padrão: "FOB"

#### Visualização de Orçamento
- Adicionada exibição do tipo de frete na seção de informações gerais
- Exibido como tag colorida (azul para CIF, laranja para FOB)

#### Tipos TypeScript
- Atualizados os tipos [Budget](file:///Users/erikpatekoski/dev/crm-ditual/frontend/src/services/budgetService.ts#L136-L162) e [BudgetSimplified](file:///Users/erikpatekoski/dev/crm-ditual/frontend/src/services/budgetService.ts#L21-L32) para incluir o campo `freight_type`

### 3. PDF Export

#### Template de Proposta
- Atualizada a seção "Demais condições" no PDF para exibir o tipo de frete selecionado
- Substituído o valor fixo "FOB" pelo valor dinâmico do orçamento

## Como Usar

### Para o Vendedor

1. **Ao criar um novo orçamento:**
   - Na seção de informações gerais, selecione o tipo de frete desejado (CIF ou FOB)
   - O valor padrão é FOB
   - Preencha os demais campos do orçamento normalmente

2. **Ao editar um orçamento existente:**
   - O campo de frete estará disponível para alteração
   - Após salvar, a nova informação será refletida na visualização e no PDF

3. **Ao visualizar um orçamento:**
   - O tipo de frete será exibido na seção de informações gerais
   - Será mostrado como uma tag colorida para fácil identificação

4. **Ao exportar para PDF:**
   - O tipo de frete selecionado será incluído na seção "Demais condições" do PDF
   - Substitui o valor fixo anterior de "FOB"

## Considerações Técnicas

### Migração de Banco de Dados
- Nome do arquivo: `010_add_freight_type_to_budgets.py`
- Tipo de coluna: VARCHAR(10)
- Valor padrão: "FOB"
- Não permite valores nulos

### Validação
- O campo é obrigatório no frontend e backend
- Valores aceitos: "CIF" ou "FOB"
- Valor padrão quando não especificado: "FOB"

### Compatibilidade
- Totalmente retrocompatível com orçamentos existentes
- Orçamentos criados antes desta implementação terão o valor padrão "FOB"

## Benefícios

1. **Melhor informação ao cliente:** O tipo de frete é claramente indicado na proposta
2. **Flexibilidade:** Os vendedores podem escolher entre CIF e FOB conforme a negociação
3. **Consistência:** A informação é mantida em todos os pontos do sistema (formulário, visualização e PDF)
4. **Facilidade de uso:** Interface simples e intuitiva

## Próximos Passos

1. **Testes completos:** Verificar o funcionamento em diferentes cenários
2. **Feedback dos usuários:** Coletar impressões dos vendedores sobre a nova funcionalidade
3. **Expansão:** Considerar adicionar mais opções de frete no futuro, se necessário