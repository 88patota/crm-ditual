#!/bin/bash

# ==============================================
# 📊 CRM SYSTEM - MONITORING SCRIPT
# ==============================================

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

# Banner
echo -e "${BLUE}"
echo "=============================================="
echo "📊 CRM SYSTEM - STATUS MONITOR"
echo "=============================================="
echo -e "${NC}"

# Check Docker daemon
if ! docker info >/dev/null 2>&1; then
    log_error "Docker daemon is not running!"
    exit 1
fi

log_info "Docker daemon: OK"

# Check services status
log_info "Checking services status..."
echo ""

SERVICES=("postgres" "redis" "user_service" "budget_service" "frontend" "nginx")
ALL_HEALTHY=true

for service in "${SERVICES[@]}"; do
    if docker compose -f "$COMPOSE_FILE" ps "$service" | grep -q "Up"; then
        # Check if container is healthy
        HEALTH=$(docker compose -f "$COMPOSE_FILE" ps "$service" --format "table {{.State}}")
        if echo "$HEALTH" | grep -q "healthy"; then
            echo -e "  ✅ ${service}: ${GREEN}Healthy${NC}"
        elif echo "$HEALTH" | grep -q "Up"; then
            echo -e "  🟡 ${service}: ${YELLOW}Running${NC}"
        else
            echo -e "  ❌ ${service}: ${RED}Unhealthy${NC}"
            ALL_HEALTHY=false
        fi
    else
        echo -e "  ❌ ${service}: ${RED}Down${NC}"
        ALL_HEALTHY=false
    fi
done

echo ""

# System resources
log_info "System resources:"
echo ""

# Memory usage
MEMORY_USAGE=$(free -h | awk 'NR==2{printf "%.1f%%", $3/$2*100}')
echo -e "  💾 Memory Usage: $MEMORY_USAGE"

# Disk usage
DISK_USAGE=$(df -h / | awk 'NR==2{print $5}')
echo -e "  💿 Disk Usage: $DISK_USAGE"

# Docker system info
echo -e "  🐳 Docker containers: $(docker ps -q | wc -l) running"
echo -e "  🖼️  Docker images: $(docker images -q | wc -l) total"

# Container resource usage
echo ""
log_info "Container resource usage:"
echo ""
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" | head -10

echo ""

# Recent logs check for errors
log_info "Recent error check (last 100 lines)..."
ERROR_COUNT=$(docker compose -f "$COMPOSE_FILE" logs --tail=100 | grep -i "error\|exception\|fatal" | wc -l)
if [[ $ERROR_COUNT -gt 0 ]]; then
    log_warning "Found $ERROR_COUNT recent errors in logs"
    echo ""
    echo -e "${YELLOW}Recent errors:${NC}"
    docker compose -f "$COMPOSE_FILE" logs --tail=100 | grep -i "error\|exception\|fatal" | tail -5
else
    log_success "No recent errors found"
fi

echo ""

# Database connection test
log_info "Testing database connection..."
if docker compose -f "$COMPOSE_FILE" exec -T postgres pg_isready -U crm_user >/dev/null 2>&1; then
    log_success "Database connection: OK"
    
    # Show database size
    DB_SIZE=$(docker compose -f "$COMPOSE_FILE" exec -T postgres psql -U crm_user -d crm_db -t -c "SELECT pg_size_pretty(pg_database_size('crm_db'));" | tr -d ' ')
    echo -e "  📊 Database size: $DB_SIZE"
else
    log_error "Database connection: FAILED"
    ALL_HEALTHY=false
fi

# Redis connection test
log_info "Testing Redis connection..."
if docker compose -f "$COMPOSE_FILE" exec -T redis redis-cli ping >/dev/null 2>&1; then
    log_success "Redis connection: OK"
else
    log_error "Redis connection: FAILED"
    ALL_HEALTHY=false
fi

# Network connectivity test
log_info "Testing network connectivity..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200\|301\|302"; then
    log_success "Frontend accessible: OK"
else
    log_warning "Frontend accessibility: Check required"
fi

echo ""

# Summary
if $ALL_HEALTHY; then
    echo -e "${GREEN}🎉 SYSTEM STATUS: ALL SERVICES HEALTHY${NC}"
    echo ""
    echo -e "${BLUE}📈 Quick Stats:${NC}"
    echo -e "  - All services: Running"
    echo -e "  - Memory usage: $MEMORY_USAGE"
    echo -e "  - Disk usage: $DISK_USAGE"
    echo -e "  - Recent errors: $ERROR_COUNT"
    echo ""
    echo -e "${BLUE}🔗 Access URLs:${NC}"
    echo -e "  - Frontend: http://localhost:3000"
    echo -e "  - Health Check: http://localhost:3000/health"
else
    echo -e "${RED}🚨 SYSTEM STATUS: ISSUES DETECTED${NC}"
    echo ""
    echo -e "${YELLOW}🔧 Troubleshooting commands:${NC}"
    echo -e "  - Check logs: docker compose -f $COMPOSE_FILE logs [service_name]"
    echo -e "  - Restart service: docker compose -f $COMPOSE_FILE restart [service_name]"
    echo -e "  - Full restart: docker compose -f $COMPOSE_FILE down && docker compose -f $COMPOSE_FILE up -d"
fi

echo ""
echo -e "${BLUE}=============================================="
echo "📊 Monitoring completed at $(date)"
echo -e "===============================================${NC}"
