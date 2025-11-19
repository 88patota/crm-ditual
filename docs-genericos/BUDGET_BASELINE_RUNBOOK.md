# Runbook: Baseline única do budget_service

Este documento descreve como aplicar a migration única (baseline) do **budget_service** em produção, e como realizar rollback caso necessário.

## Arquivos relevantes

- `services/budget_service/alembic/versions/0100_baseline_full_schema.py` — migration baseline
- `baseline_budget.sql` — SQL offline gerado para execução direta no banco
- Backup das migrações antigas: `migrations_backup/budget_versions_old/`

## Pré-requisitos

- Banco Postgres acessível (host, porta, usuário e base)
- Usuário com permissão de criação de tabelas, índices e constraints
- Backup do banco antes da execução

## Passos de execução (produção)

1. Copie o arquivo `baseline_budget.sql` para o servidor de banco.
2. Execute:

   - `psql -h <HOST> -U <USER> -d <DB> -f baseline_budget.sql`

3. Se o banco já contém o schema atual e você apenas está sincronizando Alembic:

   - Entre no diretório `services/budget_service/` com Python e Alembic disponíveis
   - Exporte variáveis `POSTGRES_*` para apontar ao banco
   - Rode `alembic -c alembic.ini stamp 0100`

> Observação: `stamp` marca a versão sem executar SQL — use apenas se o schema já está conforme a baseline.

## Rollback

Se a baseline foi aplicada a um banco vazio e precisa ser revertida:

- `psql -h <HOST> -U <USER> -d <DB>` e execute:

  - `DROP TABLE IF EXISTS budget_items CASCADE;`
  - `DROP TABLE IF EXISTS budgets CASCADE;`

Se a versão foi apenas marcada com `stamp` (sem executar SQL), para desfazer:

- `alembic -c alembic.ini stamp base`

## Notas técnicas

- A baseline cria integralmente as tabelas `budgets` e `budget_items`, seus índices e a FK de `budget_items.budget_id → budgets.id`.
- Defaults de tempo (`created_at`, `updated_at`) usam `server_default now()`. O comportamento de `onupdate` é tratado pela aplicação.
- Tipos numéricos seguem os modelos atuais (Float). Se desejar `Numeric(precision, scale)`, ajuste os modelos e gere nova baseline.

## Verificação pós-execução

- Confirmar existência das tabelas e índices:
  - `\d+ budgets`
  - `\d+ budget_items`
- Exercutar endpoints do serviço para validar persistência e leitura.

## Histórico

- Migrações antigas arquivadas em `migrations_backup/budget_versions_old/`
- Baseline gerada com `revision 0100` e `down_revision=None`