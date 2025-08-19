#!/bin/bash

# ==============================================
# 🔄 CRM SYSTEM - QUICK UPDATE SCRIPT
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

COMPOSE_FILE="docker-compose.prod.yml"
ENV_FILE=".env.prod"

echo -e "${BLUE}"
echo "=============================================="
echo "🔄 CRM SYSTEM - QUICK UPDATE"
echo "=============================================="
echo -e "${NC}"

# Check if git repo
if [[ ! -d ".git" ]]; then
    log_warning "Not a git repository. Skipping source update."
    SOURCE_UPDATE=false
else
    SOURCE_UPDATE=true
fi

# Check if environment file exists
if [[ ! -f "$ENV_FILE" ]]; then
    log_error "Environment file $ENV_FILE not found!"
    exit 1
fi

# Options
while [[ $# -gt 0 ]]; do
    case $1 in
        --no-backup)
            NO_BACKUP=true
            shift
            ;;
        --force)
            FORCE_UPDATE=true
            shift
            ;;
        --service)
            SPECIFIC_SERVICE="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --no-backup    Skip database backup"
            echo "  --force        Force update without confirmation"
            echo "  --service NAME Update specific service only"
            echo "  -h, --help     Show this help"
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Confirmation if not forced
if [[ "$FORCE_UPDATE" != "true" ]]; then
    echo -e "${YELLOW}This will update and restart the CRM system.${NC}"
    read -p "Continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Update cancelled."
        exit 0
    fi
fi

# Backup database unless skipped
if [[ "$NO_BACKUP" != "true" ]]; then
    log_info "Creating backup before update..."
    if [[ -f "backup.sh" ]]; then
        ./backup.sh
    else
        log_warning "Backup script not found, skipping backup."
    fi
fi

# Update source code
if $SOURCE_UPDATE; then
    log_info "Updating source code..."
    
    # Stash any local changes
    if ! git diff-index --quiet HEAD --; then
        log_warning "Local changes detected, stashing..."
        git stash push -m "Auto-stash before update $(date)"
    fi
    
    # Pull latest changes
    git pull origin main
    log_success "Source code updated!"
fi

# Update specific service or all services
if [[ -n "$SPECIFIC_SERVICE" ]]; then
    log_info "Updating service: $SPECIFIC_SERVICE"
    
    # Build and restart specific service
    docker compose -f "$COMPOSE_FILE" build "$SPECIFIC_SERVICE"
    docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" up -d "$SPECIFIC_SERVICE"
    
    # Wait a moment for service to start
    sleep 5
    
    # Check service status
    if docker compose -f "$COMPOSE_FILE" ps "$SPECIFIC_SERVICE" | grep -q "Up"; then
        log_success "Service $SPECIFIC_SERVICE updated successfully!"
    else
        log_error "Service $SPECIFIC_SERVICE failed to start!"
        log_info "Checking logs..."
        docker compose -f "$COMPOSE_FILE" logs --tail=20 "$SPECIFIC_SERVICE"
        exit 1
    fi
    
else
    log_info "Updating all services..."
    
    # Build all services
    log_info "Building updated images..."
    docker compose -f "$COMPOSE_FILE" build
    
    # Rolling update (restart services one by one to minimize downtime)
    SERVICES=("user_service" "budget_service" "frontend" "nginx")
    
    for service in "${SERVICES[@]}"; do
        log_info "Updating $service..."
        docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" up -d "$service"
        sleep 5
        
        # Quick health check
        if docker compose -f "$COMPOSE_FILE" ps "$service" | grep -q "Up"; then
            log_success "$service updated successfully!"
        else
            log_error "$service failed to start!"
            log_info "Rolling back..."
            docker compose -f "$COMPOSE_FILE" restart "$service"
            exit 1
        fi
    done
fi

# Clean up unused Docker resources
log_info "Cleaning up unused Docker resources..."
docker system prune -f
docker image prune -f

# Final health check
log_info "Performing post-update health check..."
sleep 10

# Check if monitoring script exists and run it
if [[ -f "monitor.sh" ]]; then
    ./monitor.sh
else
    # Simple health check
    SERVICES=("postgres" "redis" "user_service" "budget_service" "frontend" "nginx")
    ALL_HEALTHY=true
    
    for service in "${SERVICES[@]}"; do
        if docker compose -f "$COMPOSE_FILE" ps "$service" | grep -q "Up"; then
            log_success "$service: Running"
        else
            log_error "$service: Not running"
            ALL_HEALTHY=false
        fi
    done
    
    if $ALL_HEALTHY; then
        log_success "All services are running!"
    else
        log_error "Some services are not running. Check logs."
        exit 1
    fi
fi

echo ""
log_success "🎉 Update completed successfully!"
echo ""
echo -e "${BLUE}📊 Quick Status:${NC}"
docker compose -f "$COMPOSE_FILE" ps
echo ""
echo -e "${BLUE}🔗 Application Access:${NC}"
if [[ -f "$ENV_FILE" ]]; then
    source "$ENV_FILE"
    if [[ -n "$DOMAIN" ]]; then
        echo -e "  - Website: https://$DOMAIN"
        echo -e "  - Health: https://$DOMAIN/health"
    else
        echo -e "  - Website: http://localhost:3000"
    fi
else
    echo -e "  - Website: http://localhost:3000"
fi
echo ""
echo -e "${BLUE}📋 Useful commands:${NC}"
echo -e "  - View logs: docker compose -f $COMPOSE_FILE logs -f [service]"
echo -e "  - Monitor: ./monitor.sh"
echo -e "  - Backup: ./backup.sh"
