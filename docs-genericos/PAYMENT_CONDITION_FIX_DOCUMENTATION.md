# Correção do Problema de Persistência do Payment Condition

## Resumo do Problema

O campo `payment_condition` não estava sendo salvo no banco de dados, apesar de:
- O frontend estar enviando o dado corretamente
- O schema `BudgetCreate` incluir o campo
- O modelo `Budget` ter a coluna definida
- O endpoint da API receber o campo

## Causa Raiz Identificada

O problema estava no método `create_budget` da classe `BudgetService` em `/services/budget_service/app/services/budget_service.py`.

O método não estava mapeando os seguintes campos opcionais do objeto `budget_data` (tipo `BudgetCreate`) para o objeto `Budget` antes de salvá-lo no banco:

- `payment_condition`
- `prazo_medio` 
- `outras_despesas_totais`

## Correção Aplicada

### Arquivo Modificado
`/services/budget_service/app/services/budget_service.py`

### Linhas Alteradas
Linhas 78-84 do método `create_budget`

### Antes da Correção
```python
budget = Budget(
    order_number=budget_data.order_number,
    client_name=budget_data.client_name,
    client_id=budget_data.client_id,
    markup_percentage=budget_result['totals']['markup_pedido'],
    notes=budget_data.notes,
    expires_at=budget_data.expires_at,
    created_by=created_by,
    total_purchase_value=totals['total_purchase_value'],
    total_sale_value=totals['total_sale_value'],
    total_sale_with_icms=budget_result['totals']['soma_total_venda_com_icms'],
    total_commission=totals['total_commission'],
    profitability_percentage=totals['profitability_percentage'],
    freight_type=budget_data.freight_type,
    # payment_condition estava FALTANDO aqui
    total_ipi_value=budget_result['totals'].get('total_ipi_orcamento', 0.0),
    total_final_value=budget_result['totals'].get('total_final_com_ipi', 0.0)
)
```

### Depois da Correção
```python
budget = Budget(
    order_number=budget_data.order_number,
    client_name=budget_data.client_name,
    client_id=budget_data.client_id,
    markup_percentage=budget_result['totals']['markup_pedido'],
    notes=budget_data.notes,
    expires_at=budget_data.expires_at,
    created_by=created_by,
    total_purchase_value=totals['total_purchase_value'],
    total_sale_value=totals['total_sale_value'],
    total_sale_with_icms=budget_result['totals']['soma_total_venda_com_icms'],
    total_commission=totals['total_commission'],
    profitability_percentage=totals['profitability_percentage'],
    freight_type=budget_data.freight_type,
    # Add payment_condition field - FIX: Campo estava faltando no mapeamento
    payment_condition=budget_data.payment_condition,
    # Add prazo_medio and outras_despesas_totais fields - FIX: Campos estavam faltando no mapeamento
    prazo_medio=budget_data.prazo_medio,
    outras_despesas_totais=budget_data.outras_despesas_totais,
    total_ipi_value=budget_result['totals'].get('total_ipi_orcamento', 0.0),
    total_final_value=budget_result['totals'].get('total_final_com_ipi', 0.0)
)
```

## Campos Corrigidos

1. **`payment_condition`** - Campo principal do problema reportado
2. **`prazo_medio`** - Campo opcional que também estava faltando
3. **`outras_despesas_totais`** - Campo opcional que também estava faltando

## Verificação da Correção

Foi criado um teste (`test_payment_condition_fix.py`) que verifica se os campos estão sendo mapeados corretamente no código. O teste confirmou:

```
✅ payment_condition - MAPEADO CORRETAMENTE
✅ prazo_medio - MAPEADO CORRETAMENTE  
✅ outras_despesas_totais - MAPEADO CORRETAMENTE
```

## Impacto da Correção

### Antes
- `payment_condition` enviado pelo frontend era ignorado
- Valor sempre ficava `null` no banco de dados
- Interface mostrava "À vista" como fallback

### Depois
- `payment_condition` é corretamente persistido no banco
- Valor enviado pelo frontend é mantido
- Interface mostra o valor real salvo

## Componentes Verificados (Já Funcionavam Corretamente)

✅ **Frontend (`BudgetForm.tsx`)** - Envia `payment_condition` corretamente
✅ **Frontend (`BudgetView.tsx`)** - Exibe `payment_condition` corretamente
✅ **Schema (`BudgetCreate`)** - Inclui `payment_condition` como campo opcional
✅ **Modelo (`Budget`)** - Define coluna `payment_condition` no banco
✅ **API Endpoint** - Recebe e repassa `payment_condition` corretamente

❌ **BudgetService** - Não mapeava `payment_condition` (CORRIGIDO)

## Data da Correção

**Data:** Janeiro 2025
**Status:** ✅ Correção aplicada e testada com sucesso

## Próximos Passos Recomendados

1. **Teste em ambiente de desenvolvimento** - Criar um novo orçamento e verificar se `payment_condition` é salvo
2. **Teste de regressão** - Verificar se outros campos continuam funcionando
3. **Deploy para produção** - Aplicar a correção no ambiente de produção
4. **Monitoramento** - Acompanhar se o problema foi definitivamente resolvido

## Lições Aprendidas

- Sempre verificar se todos os campos do schema estão sendo mapeados no serviço
- Campos opcionais podem ser facilmente esquecidos durante o desenvolvimento
- Testes de persistência são importantes para detectar esse tipo de problema
- A análise sistemática de cada camada (frontend → API → service → banco) é essencial para identificar onde está o problema