#!/bin/bash

# ==============================================
# 🗑️ CRM SYSTEM - CLEAN BUDGETS ONLY SCRIPT
# ==============================================

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Configuration
COMPOSE_FILE_DEV="docker-compose.yml"
COMPOSE_FILE_PROD="docker-compose.prod.yml"
BACKUP_DIR="/var/backups/crm"
ENV_FILE=".env.prod"

# Detect environment
if [[ -f "$ENV_FILE" ]]; then
    COMPOSE_FILE="$COMPOSE_FILE_PROD"
    ENVIRONMENT="production"
else
    COMPOSE_FILE="$COMPOSE_FILE_DEV"
    ENVIRONMENT="development"
fi

# Banner
echo -e "${BLUE}"
cat << "EOF"
🗑️ =============================================
   LIMPEZA SEGURA DE ORÇAMENTOS
   (USUÁRIOS SEMPRE PRESERVADOS)
🗑️ =============================================
EOF
echo -e "${NC}"

log_info "Environment: $ENVIRONMENT"
log_info "Compose file: $COMPOSE_FILE"

# Help function
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Este script limpa APENAS os dados de orçamentos."
    echo "Os usuários e logins são SEMPRE preservados!"
    echo ""
    echo "Options:"
    echo "  --force              Skip confirmation prompts"
    echo "  --no-backup          Skip backup creation"
    echo "  -h, --help           Show this help"
    echo ""
    echo "Examples:"
    echo "  $0                   # Clean budgets with backup"
    echo "  $0 --force           # Quick clean without prompts"
    echo "  $0 --no-backup       # Clean without backup"
}

# Parse arguments
FORCE=false
NO_BACKUP=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --force)
            FORCE=true
            shift
            ;;
        --no-backup)
            NO_BACKUP=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Check if database is running
check_database() {
    if ! docker compose -f "$COMPOSE_FILE" ps postgres | grep -q "Up"; then
        log_error "Database container is not running!"
        log_info "Start the system first with: docker compose -f $COMPOSE_FILE up -d"
        exit 1
    fi
}

# Create backup
create_backup() {
    if [[ "$NO_BACKUP" == "true" ]]; then
        log_warning "Skipping backup creation (--no-backup flag used)"
        return 0
    fi

    log_info "Creating backup of budget data..."
    
    mkdir -p "$BACKUP_DIR"
    BACKUP_FILE="$BACKUP_DIR/budgets-backup-$(date +%Y%m%d-%H%M%S).sql"
    
    # Backup only budgets table
    docker compose -f "$COMPOSE_FILE" exec -T postgres \
        pg_dump -U crm_user -d crm_db -t budgets > "$BACKUP_FILE"
    
    gzip "$BACKUP_FILE"
    
    BACKUP_SIZE=$(du -h "${BACKUP_FILE}.gz" | cut -f1)
    log_success "Budget backup created: ${BACKUP_FILE}.gz ($BACKUP_SIZE)"
}

# Show current data counts
show_current_data() {
    log_info "Current database status:"
    echo ""
    
    # Count users
    USER_COUNT=$(docker compose -f "$COMPOSE_FILE" exec -T postgres \
        psql -U crm_user -d crm_db -t -c "SELECT COUNT(*) FROM users;" 2>/dev/null | tr -d ' ' || echo "0")
    
    # Count budgets
    BUDGET_COUNT=$(docker compose -f "$COMPOSE_FILE" exec -T postgres \
        psql -U crm_user -d crm_db -t -c "SELECT COUNT(*) FROM budgets;" 2>/dev/null | tr -d ' ' || echo "0")
    
    echo -e "  👥 Usuários: ${GREEN}$USER_COUNT${NC} (serão preservados)"
    echo -e "  📊 Orçamentos: ${YELLOW}$BUDGET_COUNT${NC} (serão removidos)"
    echo ""
}

# Clean only budgets
clean_budgets() {
    log_info "Limpando APENAS dados de orçamentos..."
    log_warning "Usuários e logins serão PRESERVADOS!"
    
    # Clear only budget-related data, preserve users completely
    docker compose -f "$COMPOSE_FILE" exec -T postgres psql -U crm_user -d crm_db << 'EOF'
-- Limpar apenas orçamentos
TRUNCATE TABLE budgets CASCADE;

-- IMPORTANTE: NÃO tocar na tabela users!
-- A tabela users é mantida intacta para preservar todos os logins

-- Opcional: Limpar apenas versões de migração relacionadas ao budget service
-- DELETE FROM alembic_version WHERE version_num LIKE '%budget%';
EOF

    log_success "Orçamentos removidos com sucesso!"
    log_success "Todos os usuários foram preservados!"
}

# Show final status
show_final_status() {
    log_info "Status após limpeza:"
    echo ""
    
    # Count users again
    USER_COUNT=$(docker compose -f "$COMPOSE_FILE" exec -T postgres \
        psql -U crm_user -d crm_db -t -c "SELECT COUNT(*) FROM users;" 2>/dev/null | tr -d ' ' || echo "0")
    
    # Count budgets again
    BUDGET_COUNT=$(docker compose -f "$COMPOSE_FILE" exec -T postgres \
        psql -U crm_user -d crm_db -t -c "SELECT COUNT(*) FROM budgets;" 2>/dev/null | tr -d ' ' || echo "0")
    
    echo -e "  👥 Usuários: ${GREEN}$USER_COUNT${NC} ✅ Preservados"
    echo -e "  📊 Orçamentos: ${GREEN}$BUDGET_COUNT${NC} ✅ Limpos"
    echo ""
    
    if [[ "$USER_COUNT" -gt "0" ]]; then
        log_success "✅ Usuários preservados com sucesso!"
    fi
    
    if [[ "$BUDGET_COUNT" -eq "0" ]]; then
        log_success "✅ Orçamentos limpos com sucesso!"
    fi
}

# Main execution
main() {
    check_database
    
    echo -e "${GREEN}🛡️  SCRIPT SEGURO - USUÁRIOS SEMPRE PRESERVADOS 🛡️${NC}"
    echo ""
    
    show_current_data
    
    # Confirmation
    if [[ "$FORCE" != "true" ]]; then
        echo -e "${YELLOW}Este script vai remover APENAS os orçamentos.${NC}"
        echo -e "${GREEN}Os usuários e logins serão mantidos intactos.${NC}"
        echo ""
        
        if [[ "$ENVIRONMENT" == "production" ]]; then
            echo -e "${RED}🚨 PRODUCTION ENVIRONMENT DETECTED! 🚨${NC}"
            read -p "Digite 'CLEAN BUDGETS' para confirmar: " -r confirmation
            if [[ "$confirmation" != "CLEAN BUDGETS" ]]; then
                log_info "Operação cancelada."
                exit 0
            fi
        else
            read -p "Confirmar limpeza de orçamentos? (Y/n): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Nn]$ ]]; then
                log_info "Operação cancelada."
                exit 0
            fi
        fi
    fi
    
    # Create backup
    create_backup
    
    # Clean budgets only
    clean_budgets
    
    # Show final status
    show_final_status
    
    echo ""
    log_success "🎉 Limpeza de orçamentos concluída!"
    log_success "🛡️ Todos os usuários foram preservados!"
    echo ""
    echo -e "${BLUE}🔗 Próximos passos:${NC}"
    echo -e "  - Os usuários podem fazer login normalmente"
    echo -e "  - Novos orçamentos podem ser criados"
    echo -e "  - Acesso: http://localhost:3000"
}

# Run main function
main "$@"
