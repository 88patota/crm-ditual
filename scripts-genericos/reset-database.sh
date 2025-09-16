#!/bin/bash

# ==============================================
# 🗑️ CRM SYSTEM - DATABASE RESET SCRIPT
# ==============================================

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_danger() { echo -e "${PURPLE}[DANGER]${NC} $1"; }

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
echo -e "${RED}"
cat << "EOF"
⚠️ ============================================== ⚠️
🗑️                DATABASE RESET                🗑️
⚠️ ============================================== ⚠️
                 ⚠️  CUIDADO  ⚠️
        ESTE SCRIPT VAI APAGAR TODOS OS DADOS!
EOF
echo -e "${NC}"

log_danger "Environment detected: $ENVIRONMENT"
log_danger "Compose file: $COMPOSE_FILE"

# Help function
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --force              Skip confirmation prompts"
    echo "  --no-backup          Skip backup creation"
    echo "  --keep-users         Keep user data (only clear budgets)"
    echo "  --keep-structure     Keep table structure (only clear data)"
    echo "  --reset-migrations   Reset database migrations"
    echo "  -h, --help           Show this help"
    echo ""
    echo "Reset Types:"
    echo "  1. Full Reset        (default) - Drop all data, recreate, but preserve users"
    echo "  2. Data Only         (--keep-structure) - Clear budget data, preserve users"
    echo "  3. Budgets Only      (--keep-users) - Clear only budget data"
    echo ""
    echo "Examples:"
    echo "  $0                              # Full reset with backup"
    echo "  $0 --force --no-backup          # Quick full reset"
    echo "  $0 --keep-users                 # Reset only budgets"
    echo "  $0 --keep-structure --force     # Clear data only"
}

# Parse arguments
FORCE=false
NO_BACKUP=false
KEEP_USERS=false
KEEP_STRUCTURE=false
RESET_MIGRATIONS=false

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
        --keep-users)
            KEEP_USERS=true
            shift
            ;;
        --keep-structure)
            KEEP_STRUCTURE=true
            shift
            ;;
        --reset-migrations)
            RESET_MIGRATIONS=true
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

    log_info "Creating safety backup before reset..."
    
    mkdir -p "$BACKUP_DIR"
    BACKUP_FILE="$BACKUP_DIR/pre-reset-backup-$(date +%Y%m%d-%H%M%S).sql"
    
    docker compose -f "$COMPOSE_FILE" exec -T postgres \
        pg_dump -U crm_user crm_db > "$BACKUP_FILE"
    
    gzip "$BACKUP_FILE"
    
    BACKUP_SIZE=$(du -h "${BACKUP_FILE}.gz" | cut -f1)
    log_success "Backup created: ${BACKUP_FILE}.gz ($BACKUP_SIZE)"
}

# Reset functions
reset_full() {
    log_info "Performing FULL database reset (will backup users first)..."
    
    # First, backup existing users if they exist
    TEMP_USERS_BACKUP="/tmp/users_backup_$(date +%Y%m%d_%H%M%S).sql"
    
    # Try to backup users table
    docker compose -f "$COMPOSE_FILE" exec -T postgres \
        pg_dump -U crm_user -d crm_db -t users --data-only > "$TEMP_USERS_BACKUP" 2>/dev/null || true
    
    # Drop and recreate database
    docker compose -f "$COMPOSE_FILE" exec -T postgres psql -U crm_user -d postgres << 'EOF'
DROP DATABASE IF EXISTS crm_db;
CREATE DATABASE crm_db OWNER crm_user;
EOF

    log_success "Database dropped and recreated!"
    
    # Store the backup path for later restoration
    echo "$TEMP_USERS_BACKUP" > /tmp/last_users_backup_path
}

reset_data_only() {
    log_info "Clearing data (keeping structure and users)..."
    
    # Clear only non-user data but keep structure and users
    docker compose -f "$COMPOSE_FILE" exec -T postgres psql -U crm_user -d crm_db << 'EOF'
TRUNCATE TABLE budgets CASCADE;
-- Manter tabela de usuários intacta para preservar logins
-- TRUNCATE TABLE users CASCADE;
TRUNCATE TABLE alembic_version;
EOF

    log_success "Data cleared (users preserved)!"
}

reset_budgets_only() {
    log_info "Clearing only budget data (keeping users)..."
    
    # Clear only budget-related data
    docker compose -f "$COMPOSE_FILE" exec -T postgres psql -U crm_user -d crm_db << 'EOF'
TRUNCATE TABLE budgets CASCADE;
EOF

    log_success "Budget data cleared!"
}

# Run migrations
run_migrations() {
    log_info "Running database migrations..."
    
    # Run user service migrations
    if docker compose -f "$COMPOSE_FILE" ps user_service | grep -q "Up"; then
        docker compose -f "$COMPOSE_FILE" exec user_service alembic upgrade head
        log_success "User service migrations completed!"
    fi
    
    # Run budget service migrations
    if docker compose -f "$COMPOSE_FILE" ps budget_service | grep -q "Up"; then
        docker compose -f "$COMPOSE_FILE" exec budget_service alembic upgrade head
        log_success "Budget service migrations completed!"
    fi
    
    # Try to restore users if we have a backup from full reset
    if [[ -f "/tmp/last_users_backup_path" ]]; then
        USERS_BACKUP=$(cat /tmp/last_users_backup_path)
        if [[ -f "$USERS_BACKUP" ]] && [[ -s "$USERS_BACKUP" ]]; then
            log_info "Restoring existing users from backup..."
            docker compose -f "$COMPOSE_FILE" exec -T postgres \
                psql -U crm_user -d crm_db < "$USERS_BACKUP" 2>/dev/null || true
            log_success "Existing users restored!"
            rm -f "$USERS_BACKUP" /tmp/last_users_backup_path
        fi
    fi
}

# Seed demo data
seed_demo_data() {
    log_info "Would you like to seed demo data? (admin user + sample budgets)"
    read -p "Seed demo data? (Y/n): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        log_info "Seeding demo data..."
        
        # Run demo user script if available
        if docker compose -f "$COMPOSE_FILE" ps user_service | grep -q "Up"; then
            if [[ -f "services/user_service/init_demo_users.py" ]]; then
                docker compose -f "$COMPOSE_FILE" exec user_service python init_demo_users.py
                log_success "Demo users created!"
            fi
        fi
        
        log_success "Demo data seeded!"
    fi
}

# Main execution
main() {
    check_database
    
    # Show reset type
    if [[ "$KEEP_USERS" == "true" ]]; then
        RESET_TYPE="Budgets Only (Users Preserved)"
    elif [[ "$KEEP_STRUCTURE" == "true" ]]; then
        RESET_TYPE="Data Reset (Users Preserved)"
    else
        RESET_TYPE="Full Reset (Users Will Be Backed Up and Restored)"
    fi
    
    echo ""
    log_danger "Reset Type: $RESET_TYPE"
    log_danger "Environment: $ENVIRONMENT"
    echo ""
    
    # Confirmation
    if [[ "$FORCE" != "true" ]]; then
        if [[ "$ENVIRONMENT" == "production" ]]; then
            echo -e "${RED}🚨 PRODUCTION ENVIRONMENT DETECTED! 🚨${NC}"
            echo -e "${YELLOW}This will permanently delete production data!${NC}"
            echo ""
            echo "Type 'RESET PRODUCTION DATABASE' to confirm:"
            read -r confirmation
            if [[ "$confirmation" != "RESET PRODUCTION DATABASE" ]]; then
                log_info "Reset cancelled."
                exit 0
            fi
        else
            echo -e "${YELLOW}This will permanently delete all database data!${NC}"
            read -p "Are you absolutely sure? Type 'yes' to continue: " -r confirmation
            if [[ "$confirmation" != "yes" ]]; then
                log_info "Reset cancelled."
                exit 0
            fi
        fi
    fi
    
    # Create backup
    create_backup
    
    # Perform reset based on options
    if [[ "$KEEP_USERS" == "true" ]]; then
        reset_budgets_only
    elif [[ "$KEEP_STRUCTURE" == "true" ]]; then
        reset_data_only
    else
        reset_full
    fi
    
    # Run migrations if needed
    if [[ "$KEEP_STRUCTURE" != "true" ]] || [[ "$RESET_MIGRATIONS" == "true" ]]; then
        run_migrations
    fi
    
    # Offer to seed demo data
    if [[ "$FORCE" != "true" ]] && [[ "$ENVIRONMENT" != "production" ]]; then
        seed_demo_data
    fi
    
    echo ""
    log_success "🎉 Database reset completed successfully!"
    echo ""
    echo -e "${BLUE}📊 Database Status:${NC}"
    docker compose -f "$COMPOSE_FILE" exec -T postgres psql -U crm_user -d crm_db -c "\dt"
    echo ""
    echo -e "${BLUE}🔗 Next Steps:${NC}"
    echo -e "  - Restart services: docker compose -f $COMPOSE_FILE restart"
    echo -e "  - Check logs: docker compose -f $COMPOSE_FILE logs"
    echo -e "  - Access frontend: http://localhost:3000"
}

# Run main function
main "$@"
