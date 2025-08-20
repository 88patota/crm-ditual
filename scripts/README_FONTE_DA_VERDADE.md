# Script de Drop e Recriação do Banco - Fonte da Verdade

## Visão Geral

Este conjunto de scripts foi criado para dropar o banco de dados atual e recriá-lo com uma **fonte da verdade** baseada nos campos que estão efetivamente sendo utilizados na aplicação.

## Arquivos Criados

### 1. `drop_and_recreate_db.py`
Script Python que automatiza todo o processo de:
- Backup das migrations existentes
- Drop das tabelas atuais
- Criação de nova migration com fonte da verdade
- Aplicação da nova estrutura
- Verificação dos resultados

### 2. `007_fonte_da_verdade_inicial.py`
Migration manual que contém TODOS os campos utilizados na aplicação:

#### Tabela `budgets`:
- **Campos obrigatórios**: id, order_number, client_name, created_by, status
- **Campos financeiros**: total_purchase_value, total_sale_value, total_commission, markup_percentage, profitability_percentage
- **Campos de metadados**: notes, client_id, expires_at
- **Timestamps**: created_at, updated_at
- **Campos dos schemas**: prazo_medio, outras_despesas_totais

#### Tabela `budget_items`:
- **Identificação**: id, budget_id, description
- **Campos do frontend simplificado** (português): peso_compra, valor_com_icms_compra, percentual_icms_compra, outras_despesas_item, peso_venda, valor_com_icms_venda, percentual_icms_venda
- **Campos do modelo SQLAlchemy** (inglês): purchase_*, sale_*, weight, weight_difference
- **Campos calculados**: profitability, total_purchase, total_sale, unit_value, total_value
- **Comissão**: commission_percentage, commission_value
- **Referência externa**: dunamis_cost
- **Compatibilidade**: quantity, purchase_value_with_icms, sale_value_with_icms

## Como Usar

### Pré-requisitos
- Docker e docker-compose funcionando
- Serviços rodando (banco PostgreSQL ativo)
- Backup dos dados importantes (se houver)

### Execução

1. **Navegue até o diretório raiz do projeto:**
   ```bash
   cd /Users/erikpatekoski/dev/crm-ditual
   ```

2. **Torne o script executável:**
   ```bash
   chmod +x scripts/drop_and_recreate_db.py
   ```

3. **Execute o script:**
   ```bash
   python scripts/drop_and_recreate_db.py
   ```

### O que o script faz:

1. **Backup das migrations**: Copia migrations antigas para `alembic/versions_backup/`
2. **Drop das tabelas**: Remove todas as tabelas via `alembic downgrade base`
3. **Reset do Alembic**: Limpa histórico com `alembic stamp base`
4. **Nova migration**: Gera migration com `alembic revision --autogenerate`
5. **Aplicação**: Executa `alembic upgrade head`
6. **Verificação**: Confere se tabelas foram criadas corretamente

### Saída Esperada

```
🚀 Iniciando processo de drop e recriação do banco de dados
============================================================
📁 Diretório de trabalho: /Users/erikpatekoski/dev/crm-ditual/services/budget_service

1. Fazendo backup das migrations atuais...
✅ Backup das migrations - Sucesso

🔄 Remoção das migrations existentes...
✅ Remoção das migrations existentes - Sucesso

🔄 Drop das tabelas via Alembic downgrade...
✅ Drop das tabelas via Alembic downgrade - Sucesso

🔄 Reset do histórico Alembic...
✅ Reset do histórico Alembic - Sucesso

🔄 Geração da migration fonte da verdade...
✅ Geração da migration fonte da verdade - Sucesso

🔄 Aplicação da migration fonte da verdade...
✅ Aplicação da migration fonte da verdade - Sucesso

7. Verificando estrutura das tabelas criadas...
📊 Tabelas criadas:
   - budgets
   - budget_items

📋 Estrutura da tabela 'budgets':
   - id: integer (NOT NULL)
   - order_number: character varying (NOT NULL)
   - client_name: character varying (NOT NULL)
   - client_id: integer (NULL)
   - total_purchase_value: double precision (NULL)
   - total_sale_value: double precision (NULL)
   - total_commission: double precision (NULL)
   - markup_percentage: double precision (NULL)
   - profitability_percentage: double precision (NULL)
   - status: character varying (NOT NULL)
   - notes: text (NULL)
   - created_by: character varying (NOT NULL)
   - created_at: timestamp with time zone (NULL)
   - updated_at: timestamp with time zone (NULL)
   - expires_at: timestamp with time zone (NULL)
   - prazo_medio: integer (NULL)
   - outras_despesas_totais: double precision (NULL)

📋 Estrutura da tabela 'budget_items':
   [Lista completa de campos]

✅ Verificação das tabelas concluída com sucesso!

============================================================
🎉 Processo concluído com sucesso!

📝 Resumo:
   - Banco de dados dropado
   - Nova migration criada com fonte da verdade
   - Tabelas recriadas com estrutura atual
   - Backup das migrations antigas em alembic/versions_backup/

💡 Próximos passos:
   - Verificar se a aplicação está funcionando corretamente
   - Executar testes para validar a integridade
   - Popular dados de teste se necessário
```

## Verificações Pós-Execução

### 1. Testar a aplicação
```bash
# Verificar se o budget service sobe corretamente
cd services/budget_service
python -m app.main
```

### 2. Verificar endpoints
```bash
# Testar criação de orçamento simplificado
curl -X POST http://localhost:8001/budgets/simplified \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "Cliente Teste",
    "items": [
      {
        "description": "Produto Teste",
        "peso_compra": 100.0,
        "valor_com_icms_compra": 1000.0,
        "percentual_icms_compra": 0.17,
        "peso_venda": 100.0,
        "valor_com_icms_venda": 1200.0,
        "percentual_icms_venda": 0.17
      }
    ]
  }'
```

### 3. Verificar no banco
```sql
-- Conectar no banco e verificar estrutura
\d budgets;
\d budget_items;

-- Verificar se os dados estão sendo inseridos
SELECT COUNT(*) FROM budgets;
SELECT COUNT(*) FROM budget_items;
```

## Rollback (se necessário)

Se algo der errado, você pode:

1. **Restaurar migrations antigas:**
   ```bash
   cd services/budget_service
   rm alembic/versions/*.py
   cp alembic/versions_backup/*.py alembic/versions/
   ```

2. **Voltar para estrutura anterior:**
   ```bash
   alembic upgrade head
   ```

## Campos Mapeados

Esta migration foi criada baseada na análise de:

- ✅ **Modelo SQLAlchemy** (`app/models/budget.py`)
- ✅ **Schemas Pydantic** (`app/schemas/budget.py`)
- ✅ **Frontend TypeScript** (`frontend/src/services/budgetService.ts`)
- ✅ **Formulários React** (`frontend/src/components/budgets/`)
- ✅ **Migrations existentes** (`alembic/versions/`)

## Suporte

Se encontrar problemas:

1. Verifique os logs detalhados do script
2. Confirme se o PostgreSQL está rodando
3. Verifique se não há conexões ativas no banco
4. Consulte o backup em `alembic/versions_backup/`

---

**⚠️ IMPORTANTE**: Este script fará DROP de todas as tabelas. Certifique-se de ter backup dos dados importantes antes de executar.
