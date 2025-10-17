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

# Verificar se o banco foi criado automaticamente pelo init script
echo "🔍 Verificando se o banco foi criado automaticamente..."
sleep 5

# Testar conexão direta (o usuário e banco devem ter sido criados pelo init-db.sql)
echo "🔐 Testando autenticação com configurações do .env.prod..."
docker-compose -f docker-compose.prod.yml exec postgres psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "SELECT 'Conexão OK' as status;"

# Se falhar, tentar criar manualmente usando o usuário que foi criado
if [ $? -ne 0 ]; then
    echo "⚠️  Conexão falhou, tentando corrigir..."
    
    # Usar o usuário criado pelo POSTGRES_USER para criar o banco
    echo "🔧 Criando banco usando o usuário configurado..."
    docker-compose -f docker-compose.prod.yml exec postgres createdb -U ${POSTGRES_USER} ${POSTGRES_DB} 2>/dev/null || true
    
    # Testar novamente
    echo "🔐 Testando autenticação novamente..."
    docker-compose -f docker-compose.prod.yml exec postgres psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "SELECT 'Conexão OK' as status;"
fi

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