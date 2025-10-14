#!/bin/bash

# Script para executar migrações do user_service no ambiente EC2
# Este script deve ser executado no diretório raiz do projeto

set -e

echo "🗄️ Executando migrações do user_service no ambiente EC2..."

# Verificar se docker-compose está disponível
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose não está instalado!"
    exit 1
fi

# Verificar se o arquivo docker-compose.prod.yml existe
if [ ! -f "docker-compose.prod.yml" ]; then
    echo "❌ Arquivo docker-compose.prod.yml não encontrado!"
    echo "Execute este script no diretório raiz do projeto."
    exit 1
fi

# Verificar se os containers estão rodando
echo "🔍 Verificando status dos containers..."
if ! docker-compose -f docker-compose.prod.yml ps | grep -q "user_service"; then
    echo "❌ Container user_service não está rodando!"
    echo "Execute: docker-compose -f docker-compose.prod.yml up -d"
    exit 1
fi

if ! docker-compose -f docker-compose.prod.yml ps | grep -q "postgres"; then
    echo "❌ Container postgres não está rodando!"
    echo "Execute: docker-compose -f docker-compose.prod.yml up -d"
    exit 1
fi

# Aguardar serviços estarem prontos
echo "⏳ Aguardando serviços estarem prontos..."
sleep 5

# Verificar conectividade com o banco
echo "🔗 Testando conectividade com o banco de dados..."
docker-compose -f docker-compose.prod.yml exec postgres pg_isready -U crm_user -d crm_db
if [ $? -ne 0 ]; then
    echo "❌ Banco de dados não está acessível!"
    exit 1
fi

echo "✅ Banco de dados acessível!"

# Executar migrações do user_service
echo "🚀 Executando migrações do user_service..."
docker-compose -f docker-compose.prod.yml exec user_service alembic upgrade head

if [ $? -eq 0 ]; then
    echo "✅ Migrações do user_service executadas com sucesso!"
    echo ""
    echo "📋 Resumo:"
    echo "  - Serviço: user_service"
    echo "  - Migração executada: 23b3c1dada96_initial_migration.py"
    echo "  - Tabela criada: users (com campos id, email, username, full_name, hashed_password, role, is_active, created_at, updated_at)"
    echo ""
else
    echo "❌ Erro ao executar migrações do user_service!"
    echo ""
    echo "🔧 Troubleshooting:"
    echo "  1. Verifique se o container user_service está rodando:"
    echo "     docker-compose -f docker-compose.prod.yml ps"
    echo ""
    echo "  2. Verifique os logs do user_service:"
    echo "     docker-compose -f docker-compose.prod.yml logs user_service"
    echo ""
    echo "  3. Verifique a conectividade com o banco:"
    echo "     docker-compose -f docker-compose.prod.yml exec postgres psql -U crm_user -d crm_db -c '\\dt'"
    echo ""
    exit 1
fi

echo "🎉 Migrações do user_service concluídas!"