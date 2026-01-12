#!/bin/bash

set -Eeuo pipefail

echo "🗄️ CRM Ditual - Restore de Backup no PostgreSQL (DEV)"
echo "===================================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.yml}"
POSTGRES_DB="${POSTGRES_DB:-crm_ditual}"
POSTGRES_USER="${POSTGRES_USER:-crm_user}"
POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-crm_strong_password_2024}"
RESET_SCHEMA="${RESET_SCHEMA:-true}"

BACKUP_FILE="${1:-/Users/erikpatekoski/dev/crm-ditual/backup-crm_ditual-20260105-042151.sql}"

if command -v docker-compose >/dev/null 2>&1; then
  COMPOSE_CMD=(docker-compose)
elif docker compose version >/dev/null 2>&1; then
  COMPOSE_CMD=(docker compose)
else
  echo "❌ Docker Compose não encontrado (docker-compose ou docker compose)"
  exit 1
fi

if [ ! -f "$COMPOSE_FILE" ]; then
  echo "❌ Arquivo $COMPOSE_FILE não encontrado em $PROJECT_ROOT"
  exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
  echo "❌ Backup não encontrado: $BACKUP_FILE"
  exit 1
fi

echo "📄 Backup: $BACKUP_FILE"
echo "🐘 Banco:  $POSTGRES_DB (usuário: $POSTGRES_USER)"
echo "🧩 Compose: $COMPOSE_FILE"

echo "🔍 Verificando container do banco..."
if ! "${COMPOSE_CMD[@]}" -f "$COMPOSE_FILE" ps postgres 2>/dev/null | grep -Eiq "(Up|running)"; then
  echo "❌ Container postgres não está rodando"
  echo "💡 Inicie com: ${COMPOSE_CMD[*]} -f $COMPOSE_FILE up -d postgres"
  exit 1
fi

psql_env=()
if [ -n "${POSTGRES_PASSWORD:-}" ]; then
  psql_env=(-e "PGPASSWORD=${POSTGRES_PASSWORD}")
fi

if [ "${RESET_SCHEMA}" = "true" ] || [ "${RESET_SCHEMA}" = "1" ]; then
  echo "🧨 Limpando schema public (RESET_SCHEMA=$RESET_SCHEMA)..."
  "${COMPOSE_CMD[@]}" -f "$COMPOSE_FILE" exec -T "${psql_env[@]}" postgres \
    psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -v ON_ERROR_STOP=1 \
    -c "DROP SCHEMA IF EXISTS public CASCADE;" \
    -c "CREATE SCHEMA public;" \
    -c "GRANT ALL ON SCHEMA public TO ${POSTGRES_USER};" \
    -c "GRANT ALL ON SCHEMA public TO public;"
else
  echo "↪️ Mantendo schema atual (RESET_SCHEMA=$RESET_SCHEMA)"
fi

echo "🚀 Restaurando backup..."
if [[ "$BACKUP_FILE" == *.gz ]]; then
  gunzip -c "$BACKUP_FILE" | "${COMPOSE_CMD[@]}" -f "$COMPOSE_FILE" exec -T "${psql_env[@]}" postgres \
    psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -v ON_ERROR_STOP=1 -1
else
  cat "$BACKUP_FILE" | "${COMPOSE_CMD[@]}" -f "$COMPOSE_FILE" exec -T "${psql_env[@]}" postgres \
    psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -v ON_ERROR_STOP=1 -1
fi

echo "📦 Tabelas no banco após restore:"
"${COMPOSE_CMD[@]}" -f "$COMPOSE_FILE" exec -T "${psql_env[@]}" postgres \
  psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -v ON_ERROR_STOP=1 \
  -c "SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename;"

echo "🎉 Restore concluído"
