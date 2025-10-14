#!/bin/bash

# Script simples para corrigir problemas de banco de dados no ambiente EC2
# Este script funciona com a configuração atual do PostgreSQL

set -e

echo "🔧 Correção simples do banco de dados no ambiente EC2..."
echo "====================================================="

# Verificar se o arquivo .env.prod existe
if [ ! -f ".env.prod" ]; then
    echo "❌ Arquivo .env.prod não encontrado!"
    exit 1
fi

# Carregar variáveis de ambiente
echo "🔧 Carregando variáveis de ambiente..."
set -a
source .env.prod
set +a

echo "📋 Configurações carregadas:"
echo "  - Database: ${POSTGRES_DB}"
echo "  - User: ${POSTGRES_USER}"
echo ""

# Parar todos os containers
echo "🛑 Parando todos os containers..."
docker-compose -f docker-compose.prod.yml down

# Remover volumes (CUIDADO: apaga dados!)
echo "⚠️  Removendo volumes do PostgreSQL..."
docker volume rm crm-ditual_postgres_data 2>/dev/null || true
docker volume rm crm-ditual_redis_data 2>/dev/null || true

# Subir apenas o PostgreSQL primeiro
echo "🚀 Subindo PostgreSQL..."
docker-compose -f docker-compose.prod.yml up -d postgres

# Aguardar PostgreSQL estar pronto
echo "⏳ Aguardando PostgreSQL estar pronto (30 segundos)..."
sleep 30

# Verificar se está funcionando
echo "🔍 Verificando se PostgreSQL está respondendo..."
docker-compose -f docker-compose.prod.yml exec postgres pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}

if [ $? -eq 0 ]; then
    echo "✅ PostgreSQL está funcionando!"
    
    # Testar conexão ao banco
    echo "🔐 Testando conexão ao banco..."
    docker-compose -f docker-compose.prod.yml exec postgres psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "SELECT 'Banco funcionando!' as status;"
    
    if [ $? -eq 0 ]; then
        echo "✅ Banco de dados está funcionando perfeitamente!"
        echo ""
        echo "🚀 Próximos passos:"
        echo "1. Subir todos os serviços:"
        echo "   docker-compose -f docker-compose.prod.yml up -d"
        echo ""
        echo "2. Executar migrações:"
        echo "   ./scripts/run_all_migrations_ec2.sh"
    else
        echo "❌ Problema na conexão com o banco!"
        exit 1
    fi
else
    echo "❌ PostgreSQL não está respondendo!"
    echo "📋 Verificando logs do container:"
    docker-compose -f docker-compose.prod.yml logs postgres
    exit 1
fi