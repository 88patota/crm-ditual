#!/bin/bash

# Script para corrigir problemas de banco de dados no ambiente EC2
# Este script deve ser executado ANTES das migrações se houver problemas de autenticação

set -e

echo "🔧 Corrigindo problemas de banco de dados no ambiente EC2..."
echo "=========================================================="

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
echo "  - Host: ${POSTGRES_HOST}"
echo ""

# Parar containers se estiverem rodando
echo "🛑 Parando containers..."
docker-compose -f docker-compose.prod.yml down

# Remover volumes do PostgreSQL (CUIDADO: isso apaga todos os dados!)
echo "⚠️  Removendo volumes do PostgreSQL (dados serão perdidos)..."
docker volume rm crm-ditual_postgres_data 2>/dev/null || true

# Recriar containers
echo "🚀 Recriando containers..."
docker-compose -f docker-compose.prod.yml up -d postgres

# Aguardar PostgreSQL estar pronto
echo "⏳ Aguardando PostgreSQL estar pronto..."
sleep 20

# Verificar se o PostgreSQL está rodando
echo "🔍 Verificando status do PostgreSQL..."
docker-compose -f docker-compose.prod.yml exec postgres pg_isready -U postgres
if [ $? -ne 0 ]; then
    echo "❌ PostgreSQL não está respondendo!"
    exit 1
fi

# Criar usuário e banco manualmente
echo "👤 Criando usuário e banco de dados..."
docker-compose -f docker-compose.prod.yml exec postgres psql -U postgres -c "
    DROP DATABASE IF EXISTS ${POSTGRES_DB};
    DROP USER IF EXISTS ${POSTGRES_USER};
    CREATE USER ${POSTGRES_USER} WITH PASSWORD '${POSTGRES_PASSWORD}';
    CREATE DATABASE ${POSTGRES_DB} OWNER ${POSTGRES_USER};
    GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_USER};
"

# Testar conexão
echo "🔐 Testando autenticação..."
docker-compose -f docker-compose.prod.yml exec postgres psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "SELECT 'Conexão OK' as status;"

if [ $? -eq 0 ]; then
    echo "✅ Banco de dados corrigido com sucesso!"
    echo ""
    echo "🚀 Agora você pode subir os outros serviços:"
    echo "   docker-compose -f docker-compose.prod.yml up -d"
    echo ""
    echo "📋 E executar as migrações:"
    echo "   ./scripts/run_all_migrations_ec2.sh"
else
    echo "❌ Ainda há problemas com a autenticação!"
    exit 1
fi