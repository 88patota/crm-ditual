#!/bin/bash

# ==============================================
# 🚀 CRM SYSTEM - PRODUCTION DEPLOYMENT SCRIPT
# ==============================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Configuration
COMPOSE_FILE="docker-compose.prod.yml"
ENV_FILE=".env.prod"
BACKUP_DIR="/var/backups/crm"
SSL_DIR="nginx/ssl"

# Banner
echo -e "${BLUE}"
cat << "EOF"
  ______ _____  __  __   _____            _                 
 / _____|_____)|  \/  | / ___/           | |                
( (____  _____|| |\/| | |_____  _   _  _ | |_  ___  __  __  
 \___ \|  ___ | |  | | |  ___||| | | || ||  _)/ _ \|  \/  | 
 ____) ) |___)|_|  |_| | |___ | |_| ||_||  |_| |_||  |  | | 
(______|______|_)  (_) |____/ |_||_| (_)  \__)\___|_|  |_| 
                                                           
         🚀 PRODUCTION DEPLOYMENT SCRIPT 🚀
EOF
echo -e "${NC}"

log_info "Starting CRM System production deployment..."

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check if Docker Compose is available
    if ! docker compose version &> /dev/null; then
        log_error "Docker Compose is not available. Please install Docker Compose plugin."
        exit 1
    fi
    
    # Check if environment file exists
    if [[ ! -f "$ENV_FILE" ]]; then
        log_error "Environment file $ENV_FILE not found!"
        log_warning "Please copy .env.prod.template to .env.prod and configure it."
        exit 1
    fi
    
    log_success "Prerequisites check passed!"
}

# Create necessary directories
setup_directories() {
    log_info "Setting up directories..."
    
    sudo mkdir -p /var/log/crm
    sudo mkdir -p "$BACKUP_DIR"
    sudo mkdir -p "$SSL_DIR"
    
    # Set permissions
    sudo chown -R $USER:$USER /var/log/crm
    sudo chown -R $USER:$USER "$BACKUP_DIR"
    
    log_success "Directories setup completed!"
}

# SSL Certificate setup
setup_ssl() {
    log_info "Setting up SSL certificates..."
    
    # Source environment variables
    source "$ENV_FILE"
    
    if [[ -z "$DOMAIN" ]]; then
        log_error "DOMAIN not set in environment file!"
        exit 1
    fi
    
    # Check if certificates exist
    if [[ -f "$SSL_DIR/cert.pem" ]] && [[ -f "$SSL_DIR/key.pem" ]]; then
        log_success "SSL certificates already exist!"
        return 0
    fi
    
    log_info "SSL certificates not found. Setting up Let's Encrypt..."
    
    # Install certbot if not present
    if ! command -v certbot &> /dev/null; then
        log_info "Installing certbot..."
        sudo apt update
        sudo apt install -y certbot python3-certbot-nginx
    fi
    
    # Stop nginx if running
    sudo systemctl stop nginx 2>/dev/null || true
    
    # Get certificate
    log_info "Obtaining SSL certificate for $DOMAIN..."
    sudo certbot certonly --standalone \
        --email "$EMAIL" \
        --agree-tos \
        --no-eff-email \
        -d "$DOMAIN" \
        -d "www.$DOMAIN"
    
    # Copy certificates to nginx directory
    sudo cp "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" "$SSL_DIR/cert.pem"
    sudo cp "/etc/letsencrypt/live/$DOMAIN/privkey.pem" "$SSL_DIR/key.pem"
    
    # Set proper permissions
    sudo chown $USER:$USER "$SSL_DIR"/*
    sudo chmod 644 "$SSL_DIR/cert.pem"
    sudo chmod 600 "$SSL_DIR/key.pem"
    
    log_success "SSL certificates configured!"
}

# Database backup
backup_database() {
    log_info "Creating database backup..."
    
    # Check if database container is running
    if docker compose -f "$COMPOSE_FILE" ps postgres | grep -q "Up"; then
        BACKUP_FILE="$BACKUP_DIR/backup-$(date +%Y%m%d-%H%M%S).sql"
        
        # Source environment to get password
        source "$ENV_FILE"
        
        docker compose -f "$COMPOSE_FILE" exec -T postgres \
            pg_dump -U crm_user crm_db > "$BACKUP_FILE"
        
        # Compress backup
        gzip "$BACKUP_FILE"
        
        log_success "Database backup created: ${BACKUP_FILE}.gz"
        
        # Clean old backups (keep last 30 days)
        find "$BACKUP_DIR" -name "backup-*.sql.gz" -mtime +30 -delete
    else
        log_warning "Database container not running, skipping backup..."
    fi
}

# Deploy application
deploy_application() {
    log_info "Deploying application..."
    
    # Pull latest changes (if git repo)
    if [[ -d ".git" ]]; then
        log_info "Updating source code..."
        git pull origin main
    fi
    
    # Build and deploy
    log_info "Building and starting services..."
    
    # Stop existing services
    docker compose -f "$COMPOSE_FILE" down
    
    # Build images
    docker compose -f "$COMPOSE_FILE" build --no-cache
    
    # Start services
    docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" up -d
    
    log_success "Services started!"
}

# Health check
health_check() {
    log_info "Performing health checks..."
    
    # Wait for services to start
    log_info "Waiting for services to be ready..."
    sleep 30
    
    # Check services status
    local services=("postgres" "redis" "user_service" "budget_service" "frontend" "nginx")
    local failed_services=()
    
    for service in "${services[@]}"; do
        if docker compose -f "$COMPOSE_FILE" ps "$service" | grep -q "Up"; then
            log_success "$service is running"
        else
            log_error "$service is not running"
            failed_services+=("$service")
        fi
    done
    
    if [[ ${#failed_services[@]} -eq 0 ]]; then
        log_success "All services are healthy!"
        
        # Show access information
        source "$ENV_FILE"
        echo ""
        echo -e "${GREEN}🎉 DEPLOYMENT SUCCESSFUL! 🎉${NC}"
        echo ""
        echo -e "${BLUE}📊 Service Status:${NC}"
        docker compose -f "$COMPOSE_FILE" ps
        echo ""
        echo -e "${BLUE}🌐 Access Information:${NC}"
        echo -e "   Website: https://$DOMAIN"
        echo -e "   Health Check: https://$DOMAIN/health"
        echo ""
        echo -e "${BLUE}📋 Useful Commands:${NC}"
        echo -e "   View logs: docker compose -f $COMPOSE_FILE logs -f [service_name]"
        echo -e "   Restart: docker compose -f $COMPOSE_FILE restart [service_name]"
        echo -e "   Stop all: docker compose -f $COMPOSE_FILE down"
        echo ""
        
    else
        log_error "Some services failed to start: ${failed_services[*]}"
        echo ""
        echo -e "${RED}🚨 DEPLOYMENT ISSUES DETECTED 🚨${NC}"
        echo ""
        echo -e "${YELLOW}Debug commands:${NC}"
        echo -e "   Check logs: docker compose -f $COMPOSE_FILE logs"
        echo -e "   Check status: docker compose -f $COMPOSE_FILE ps"
        echo ""
        exit 1
    fi
}

# Setup monitoring
setup_monitoring() {
    log_info "Setting up monitoring and maintenance..."
    
    # Create backup cron job
    CRON_JOB="0 2 * * * /usr/bin/docker compose -f $(pwd)/$COMPOSE_FILE exec -T postgres pg_dump -U crm_user crm_db | gzip > $BACKUP_DIR/backup-\$(date +\\%Y\\%m\\%d).sql.gz"
    
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    
    # Setup SSL renewal
    SSL_RENEWAL="0 0,12 * * * /usr/bin/certbot renew --quiet --deploy-hook 'docker compose -f $(pwd)/$COMPOSE_FILE restart nginx'"
    (crontab -l 2>/dev/null; echo "$SSL_RENEWAL") | crontab -
    
    log_success "Monitoring and maintenance configured!"
}

# Main deployment flow
main() {
    log_info "Starting production deployment process..."
    
    check_prerequisites
    setup_directories
    
    # Ask for SSL setup
    read -p "Setup SSL certificates with Let's Encrypt? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        setup_ssl
    else
        log_warning "Skipping SSL setup. Make sure you have valid certificates in $SSL_DIR/"
    fi
    
    # Ask for database backup
    read -p "Create database backup before deployment? (Y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        backup_database
    fi
    
    deploy_application
    health_check
    
    # Ask for monitoring setup
    read -p "Setup automated monitoring and backups? (Y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        setup_monitoring
    fi
    
    log_success "🎉 Production deployment completed successfully! 🎉"
}

# Run main function
main "$@"
