#!/bin/bash

# ==============================================
# 🗄️ CRM SYSTEM - BACKUP SCRIPT
# ==============================================

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

COMPOSE_FILE="docker-compose.prod.yml"
BACKUP_DIR="/var/backups/crm"
ENV_FILE=".env.prod"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Source environment variables
if [[ -f "$ENV_FILE" ]]; then
    source "$ENV_FILE"
fi

log_info "Starting backup process..."

# Database backup
log_info "Creating database backup..."
BACKUP_FILE="$BACKUP_DIR/backup-$(date +%Y%m%d-%H%M%S).sql"

if docker compose -f "$COMPOSE_FILE" ps postgres | grep -q "Up"; then
    docker compose -f "$COMPOSE_FILE" exec -T postgres \
        pg_dump -U crm_user crm_db > "$BACKUP_FILE"
    
    # Compress backup
    gzip "$BACKUP_FILE"
    
    log_success "Database backup created: ${BACKUP_FILE}.gz"
    
    # Show backup size
    BACKUP_SIZE=$(du -h "${BACKUP_FILE}.gz" | cut -f1)
    log_info "Backup size: $BACKUP_SIZE"
    
    # Clean old backups (keep last 30 days)
    log_info "Cleaning old backups (keeping last 30 days)..."
    find "$BACKUP_DIR" -name "backup-*.sql.gz" -mtime +30 -delete
    
    # List recent backups
    log_info "Recent backups:"
    ls -lah "$BACKUP_DIR"/backup-*.sql.gz | tail -10
    
else
    log_error "Database container is not running!"
    exit 1
fi

log_success "Backup process completed!"
