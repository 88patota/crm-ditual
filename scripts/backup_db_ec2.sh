#!/bin/bash

set -Eeuo pipefail

echo "🗄️ CRM Ditual - Backup do PostgreSQL (EC2)"
echo "========================================="

COMPOSE_FILE="docker-compose.prod.yml"
ENV_FILE=".env.prod"
BACKUP_DIR="${BACKUP_DIR:-/var/backups/crm}"
LOG_FILE="${LOG_FILE:-/var/log/crm/db-backup.log}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
BACKUP_S3_BUCKET="${BACKUP_S3_BUCKET:-s3-bkp-ditual}"

if command -v docker-compose >/dev/null 2>&1; then
  COMPOSE_CMD=(docker-compose)
elif docker compose version >/dev/null 2>&1; then
  COMPOSE_CMD=(docker compose)
else
  echo "❌ Docker Compose não encontrado (docker-compose ou docker compose)"
  exit 1
fi

if [ ! -f "$COMPOSE_FILE" ]; then
  echo "❌ Arquivo $COMPOSE_FILE não encontrado"
  echo "💡 Execute este script a partir do diretório raiz do projeto"
  exit 1
fi

if [ ! -f "$ENV_FILE" ]; then
  echo "❌ Arquivo $ENV_FILE não encontrado"
  echo "💡 Crie/ajuste o $ENV_FILE com POSTGRES_PASSWORD e demais variáveis"
  exit 1
fi

set -a
source "$ENV_FILE"
set +a

POSTGRES_DB="${POSTGRES_DB:-crm_ditual}"
POSTGRES_USER="${POSTGRES_USER:-crm_user}"

mkdir -p "$BACKUP_DIR"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
  local msg="$1"
  local ts
  ts="$(date '+%Y-%m-%d %H:%M:%S')"
  echo "$ts $msg" | tee -a "$LOG_FILE"
}

on_error() {
  local exit_code="$1"
  local line_no="$2"
  log "❌ Falha (exit=$exit_code) na linha $line_no"
  exit "$exit_code"
}

trap 'on_error $? $LINENO' ERR

log "🔍 Verificando container do banco..."
if ! "${COMPOSE_CMD[@]}" -f "$COMPOSE_FILE" ps postgres 2>/dev/null | grep -Eiq "(Up|running)"; then
  log "❌ Container postgres não está rodando"
  log "💡 Inicie com: ${COMPOSE_CMD[*]} -f $COMPOSE_FILE up -d"
  exit 1
fi

ts="$(date '+%Y%m%d-%H%M%S')"
backup_base="backup-${POSTGRES_DB}-${ts}.sql"
backup_sql="$BACKUP_DIR/$backup_base"
backup_gz="${backup_sql}.gz"

log "🚀 Iniciando backup do banco '$POSTGRES_DB'..."

"${COMPOSE_CMD[@]}" -f "$COMPOSE_FILE" exec -T \
  -e "PGPASSWORD=${POSTGRES_PASSWORD:-}" \
  postgres pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" > "$backup_sql"

gzip -f "$backup_sql"

backup_size="$(du -h "$backup_gz" | awk '{print $1}')"
log "✅ Backup criado: $backup_gz ($backup_size)"

if [ -n "${BACKUP_S3_BUCKET:-}" ]; then
  if command -v aws >/dev/null 2>&1; then
    s3_prefix="${BACKUP_S3_PREFIX:-crm-ditual/postgres/${POSTGRES_DB}}"
    s3_uri="s3://${BACKUP_S3_BUCKET%/}/${s3_prefix%/}/$(basename "$backup_gz")"
    log "☁️ Enviando backup para S3: $s3_uri"
    aws s3 cp "$backup_gz" "$s3_uri" ${BACKUP_S3_STORAGE_CLASS:+--storage-class "$BACKUP_S3_STORAGE_CLASS"} ${BACKUP_S3_SSE:+--sse "$BACKUP_S3_SSE"}
    log "✅ Upload no S3 concluído"
  else
    log "⚠️ BACKUP_S3_BUCKET definido, mas aws cli não está instalado; pulando upload"
  fi
fi

log "🧹 Limpando backups antigos (>$RETENTION_DAYS dias)..."
find "$BACKUP_DIR" -name "backup-${POSTGRES_DB}-*.sql.gz" -type f -mtime +"$RETENTION_DAYS" -delete

log "📦 Últimos backups:"
ls -lah "$BACKUP_DIR"/backup-"${POSTGRES_DB}"-*.sql.gz 2>/dev/null | tail -10 | tee -a "$LOG_FILE" >/dev/null || true

log "🎉 Backup concluído"
