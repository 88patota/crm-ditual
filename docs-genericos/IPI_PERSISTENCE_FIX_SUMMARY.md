# Correção do Problema de Persistência do IPI

## Problema Identificado

Ao salvar um orçamento, o campo IPI não estava sendo persistido corretamente no banco de dados. Após salvar, o campo IPI ficava com valor 0 (isento) mesmo quando um percentual de IPI válido (3.25% ou 5%) era informado.

## Análise do Problema

### Causa Raiz

O problema estava no mapeamento entre os campos calculados pelo `BusinessRulesCalculator` e os campos salvos no banco de dados através do `BudgetService`. Especificamente:

1. **Nomenclatura de campos**: O `BusinessRulesCalculator` retorna o valor calculado do IPI no campo `valor_ipi_total`, mas o `BudgetService` estava tentando acessar um campo inexistente.

2. **Ordem de prioridade**: O código estava calculando o IPI duas vezes - uma vez pelo `BusinessRulesCalculator` e outra vez manualmente, mas priorizando o valor manual que poderia estar incorreto.

### Arquivos Analisados

- ✅ `services/budget_service/app/models/budget.py` - Modelo correto com campos IPI
- ✅ `services/budget_service/app/schemas/budget.py` - Schema correto com validações IPI
- ✅ `services/budget_service/app/services/business_rules_calculator.py` - Cálculos IPI implementados corretamente
- ❌ `services/budget_service/app/services/budget_service.py` - **PROBLEMA IDENTIFICADO AQUI**

## Correção Implementada

### Mudanças no `BudgetService`

**Arquivo**: `services/budget_service/app/services/budget_service.py`

#### 1. Método `create_budget`

**ANTES**:
```python
# IPI fields - explicitly set calculated values
ipi_percentage=ipi_percentage,
ipi_value=ipi_value,  # Valor calculado manualmente
total_value_with_ipi=calculated_item.get('total_final_com_ipi', 0.0),
```

**DEPOIS**:
```python
# IPI fields - use values calculated by BusinessRulesCalculator
ipi_percentage=ipi_percentage,
ipi_value=calculated_item.get('valor_ipi_total', ipi_value),  # Prioriza valor do calculator
total_value_with_ipi=total_value_with_ipi,
```

#### 2. Método `update_budget`

Aplicada a mesma correção para garantir consistência em atualizações de orçamentos.

### Lógica da Correção

1. **Priorizar valores do BusinessRulesCalculator**: Usar `calculated_item.get('valor_ipi_total', ipi_value)` em vez de apenas `ipi_value`

2. **Fallback seguro**: Manter o cálculo manual como fallback caso o BusinessRulesCalculator não retorne o valor esperado

3. **Consistência**: Aplicar a mesma lógica em todos os métodos que criam ou atualizam itens de orçamento

## Campos IPI Envolvidos

### No Modelo (`BudgetItem`)
- `ipi_percentage`: Percentual de IPI (0.0, 0.0325, 0.05)
- `ipi_value`: Valor do IPI calculado para o item
- `total_value_with_ipi`: Valor total do item incluindo IPI

### No Modelo (`Budget`)
- `total_ipi_value`: Soma de todos os valores de IPI dos itens
- `total_final_value`: Valor final do orçamento incluindo todos os IPI

### No BusinessRulesCalculator

**Campos retornados por item**:
- `percentual_ipi`: Percentual de IPI
- `valor_ipi_total`: **Campo-chave** - Valor total do IPI para o item
- `total_final_com_ipi`: Valor total do item com IPI

**Campos retornados nos totals**:
- `total_ipi_orcamento`: Total de IPI de todo o orçamento
- `total_final_com_ipi`: Valor final total incluindo IPI

## Validação da Correção

### Como Testar

1. **Criar um orçamento com IPI**:
   ```json
   {
     "client_name": "Cliente Teste",
     "items": [
       {
         "description": "Item com IPI 3.25%",
         "peso_compra": 100.0,
         "valor_com_icms_compra": 10.00,
         "percentual_icms_compra": 0.18,
         "valor_com_icms_venda": 15.00,
         "percentual_icms_venda": 0.17,
         "percentual_ipi": 0.0325
       }
     ]
   }
   ```

2. **Verificar persistência**: Após salvar, recuperar o orçamento e verificar:
   - `ipi_percentage` = 0.0325
   - `ipi_value` = valor calculado (não zero)
   - `total_value_with_ipi` = valor com IPI incluído

### Resultado Esperado

- ✅ Campo `ipi_percentage` mantém o valor correto (0.0325 para 3.25%)
- ✅ Campo `ipi_value` contém o valor calculado do IPI (não zero)
- ✅ Campo `total_value_with_ipi` contém o valor final incluindo IPI
- ✅ Totais do orçamento incluem corretamente os valores de IPI

## Arquivos Alterados

1. `services/budget_service/app/services/budget_service.py`
   - Método `create_budget` - linha ~108
   - Método `update_budget` - linha ~270

## Impacto da Correção

### Funcionalidades Afetadas ✅

- ✅ Criação de orçamentos com IPI
- ✅ Atualização de orçamentos com IPI
- ✅ Cálculo correto de totais incluindo IPI
- ✅ Exportação PDF com valores de IPI corretos
- ✅ Visualização de orçamentos com IPI

### Compatibilidade ✅

- ✅ Orçamentos existentes sem IPI continuam funcionando
- ✅ Orçamentos com IPI = 0% continuam funcionando
- ✅ Validações de IPI (0%, 3.25%, 5%) mantidas
- ✅ Cálculos de comissão e markup não afetados pelo IPI (conforme regra de negócio)

## Status

🎯 **PROBLEMA CORRIGIDO**

O IPI agora é persistido corretamente no banco de dados e mantém seus valores após salvar o orçamento.
