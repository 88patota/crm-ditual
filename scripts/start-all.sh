#!/bin/bash

# CRM Ditual - Script de inicialização completa
# Este script inicia todos os serviços backend e aguarda que estejam prontos

set -e

echo "🚀 Iniciando CRM Ditual - Todos os Serviços"
echo "=========================================="

# Função para verificar se um serviço está rodando
check_service() {
    local service_name=$1
    local url=$2
    local max_attempts=30
    local attempt=0

    echo "⏳ Aguardando $service_name ficar disponível..."
    
    while [ $attempt -lt $max_attempts ]; do
        if curl -s "$url" > /dev/null 2>&1; then
            echo "✅ $service_name está rodando!"
            return 0
        fi
        
        echo "🔄 Tentativa $((attempt + 1))/$max_attempts para $service_name..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo "❌ $service_name não ficou disponível após $max_attempts tentativas"
    return 1
}

# Função para verificar PostgreSQL
check_postgres() {
    echo "⏳ Aguardando PostgreSQL ficar disponível..."
    local max_attempts=30
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if docker compose exec -T postgres pg_isready -U crm_user -d crm_db > /dev/null 2>&1; then
            echo "✅ PostgreSQL está rodando!"
            return 0
        fi
        
        echo "🔄 Tentativa $((attempt + 1))/$max_attempts para PostgreSQL..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo "❌ PostgreSQL não ficou disponível"
    return 1
}

# Função para verificar Redis
check_redis() {
    echo "⏳ Aguardando Redis ficar disponível..."
    local max_attempts=30
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if docker compose exec -T redis redis-cli ping > /dev/null 2>&1; then
            echo "✅ Redis está rodando!"
            return 0
        fi
        
        echo "🔄 Tentativa $((attempt + 1))/$max_attempts para Redis..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo "❌ Redis não ficou disponível"
    return 1
}

# Parar serviços existentes
echo "🧹 Parando serviços existentes..."
docker compose down

# Iniciar infraestrutura (PostgreSQL e Redis)
echo "🗄️ Iniciando infraestrutura..."
docker compose up -d postgres redis

# Aguardar infraestrutura
check_postgres
check_redis

# Iniciar serviços de aplicação
echo "🚀 Iniciando serviços de aplicação..."
docker compose up -d user_service budget_service

# Aguardar serviços de aplicação
check_service "User Service" "http://localhost:8001/health"
check_service "Budget Service" "http://localhost:8002/health"

# Iniciar API Gateway
echo "🌐 Iniciando API Gateway..."
docker compose up -d api_gateway

# Aguardar API Gateway
check_service "API Gateway" "http://localhost:8000/health"

# Mostrar status final
echo ""
echo "🎉 Todos os serviços backend estão rodando!"
echo "=========================================="
echo "📊 Serviços disponíveis:"
echo "  🔧 API Gateway:    http://localhost:8000"
echo "  👥 User Service:   http://localhost:8001"
echo "  💰 Budget Service: http://localhost:8002"
echo "  🗄️ PostgreSQL:     localhost:5432"
echo "  🔴 Redis:          localhost:6379"
echo ""
echo "📖 Documentação da API:"
echo "  👥 User Service:   http://localhost:8001/docs"
echo "  💰 Budget Service: http://localhost:8002/docs"
echo ""
echo "🎨 Para iniciar o frontend:"
echo "  cd frontend && npm run dev"
echo ""
echo "📊 Dashboard estará em: http://localhost:5173"
echo ""

# Verificar saúde final
echo "🏥 Verificação final de saúde:"
docker compose ps

echo "✅ Inicialização completa!"