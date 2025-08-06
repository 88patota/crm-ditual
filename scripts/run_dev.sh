#!/bin/bash

echo "🚀 Iniciando ambiente de desenvolvimento CRM..."

# Verificar se o setup já foi executado
if [ ! -d "services/user_service/venv" ]; then
    echo "❌ Ambiente não configurado. Execute primeiro: ./scripts/setup_dev.sh"
    exit 1
fi

# Subir todos os serviços
echo "🐳 Iniciando todos os serviços..."
docker compose up -d

echo "⏳ Aguardando serviços estarem prontos..."
sleep 15

echo "✅ Todos os serviços estão rodando!"
echo ""
echo "🌐 Serviços disponíveis:"
echo "  - User Service: http://localhost:8001"
echo "  - API Docs: http://localhost:8001/docs"
echo "  - PostgreSQL: localhost:5432"
echo "  - Redis: localhost:6379"
echo ""
echo "Para parar os serviços: docker compose down"