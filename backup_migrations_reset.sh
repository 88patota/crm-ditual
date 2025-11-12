#!/bin/bash

# Script de Backup Completo - Reset de Migrações
# Data: $(date)

echo "🔄 INICIANDO BACKUP COMPLETO..."

# Criar diretório de backup com timestamp
BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "📁 Diretório de backup: $BACKUP_DIR"

# Backup do banco user_service
echo "💾 Fazendo backup do banco crm_ditual..."
docker compose -f docker-compose.prod.yml --env-file .env.prod exec -T postgres pg_dump -U crm_user -d crm_ditual > "$BACKUP_DIR/crm_ditual_backup.sql"

# Backup das migrações atuais
echo "📋 Fazendo backup das migrações atuais..."
cp -r services/budget_service/alembic/versions "$BACKUP_DIR/budget_migrations_old"
cp -r services/user_service/alembic/versions "$BACKUP_DIR/user_migrations_old"

# Backup dos arquivos de configuração
echo "⚙️ Fazendo backup das configurações..."
cp services/budget_service/alembic.ini "$BACKUP_DIR/budget_alembic.ini"
cp services/user_service/alembic.ini "$BACKUP_DIR/user_alembic.ini"

# Verificar se os backups foram criados
echo "✅ VERIFICANDO BACKUPS..."
if [ -f "$BACKUP_DIR/crm_ditual_backup.sql" ]; then
    echo "✅ Backups criados com sucesso!"
    echo "📊 Tamanhos dos arquivos:"
    ls -lh "$BACKUP_DIR"/*.sql
    echo ""
    echo "🎯 BACKUP COMPLETO FINALIZADO!"
    echo "📁 Localização: $(pwd)/$BACKUP_DIR"
else
    echo "❌ ERRO: Falha na criação dos backups!"
    exit 1
fi