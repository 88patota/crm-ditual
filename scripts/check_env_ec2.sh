#!/bin/bash

# Script para verificar se o arquivo .env.prod existe e está configurado corretamente
# Este script deve ser executado no diretório raiz do projeto na instância EC2

set -e

echo "🔍 VERIFICANDO CONFIGURAÇÃO DO AMBIENTE EC2"
echo "==========================================="

# Verificar se estamos no diretório correto
if [ ! -f "docker-compose.prod.yml" ]; then
    echo "❌ Arquivo docker-compose.prod.yml não encontrado!"
    echo "Execute este script no diretório raiz do projeto."
    exit 1
fi

echo "✅ Diretório correto identificado"

# Verificar se o arquivo .env.prod existe
if [ ! -f ".env.prod" ]; then
    echo "❌ PROBLEMA IDENTIFICADO: Arquivo .env.prod não encontrado!"
    echo ""
    echo "🔧 SOLUÇÕES:"
    echo "1. Copie o arquivo .env.prod para a instância EC2:"
    echo "   scp .env.prod ec2-user@SEU_IP_EC2:/caminho/para/projeto/"
    echo ""
    echo "2. Ou crie o arquivo .env.prod manualmente:"
    echo "   nano .env.prod"
    echo ""
    echo "3. Conteúdo mínimo necessário:"
    echo "   POSTGRES_PASSWORD=crm_strong_password_2024"
    echo "   REDIS_PASSWORD=redis_strong_password_2024"
    echo "   SECRET_KEY=9372b96b078a8471d27f3cf16ad4834bf6b49a987b9b68a0bd0bd2686ae160cc"
    echo "   DOMAIN=loen.digital"
    echo ""
    exit 1
fi

echo "✅ Arquivo .env.prod encontrado!"

# Verificar variáveis críticas
echo ""
echo "🔍 Verificando variáveis críticas..."

CRITICAL_VARS=("POSTGRES_PASSWORD" "REDIS_PASSWORD" "SECRET_KEY" "DOMAIN")
MISSING_VARS=()

for var in "${CRITICAL_VARS[@]}"; do
    if ! grep -q "^${var}=" .env.prod; then
        MISSING_VARS+=("$var")
    fi
done

if [ ${#MISSING_VARS[@]} -ne 0 ]; then
    echo "❌ Variáveis críticas ausentes no .env.prod:"
    for var in "${MISSING_VARS[@]}"; do
        echo "  - $var"
    done
    echo ""
    echo "🔧 Adicione essas variáveis ao arquivo .env.prod"
    exit 1
fi

echo "✅ Todas as variáveis críticas estão presentes!"

# Testar carregamento das variáveis
echo ""
echo "🔧 Testando carregamento das variáveis..."
set -a  # Automatically export all variables
source .env.prod
set +a  # Stop automatically exporting

if [ -z "$POSTGRES_PASSWORD" ]; then
    echo "❌ Erro ao carregar POSTGRES_PASSWORD"
    exit 1
fi

if [ -z "$REDIS_PASSWORD" ]; then
    echo "❌ Erro ao carregar REDIS_PASSWORD"
    exit 1
fi

echo "✅ Variáveis carregadas com sucesso!"

# Verificar conectividade com containers
echo ""
echo "🔍 Verificando containers Docker..."

if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose não está instalado!"
    exit 1
fi

# Verificar se os containers estão rodando
REQUIRED_SERVICES=("postgres" "redis")
MISSING_SERVICES=()

for service in "${REQUIRED_SERVICES[@]}"; do
    if ! docker-compose -f docker-compose.prod.yml ps | grep -q "$service"; then
        MISSING_SERVICES+=("$service")
    fi
done

if [ ${#MISSING_SERVICES[@]} -ne 0 ]; then
    echo "⚠️ Os seguintes containers não estão rodando: ${MISSING_SERVICES[*]}"
    echo "Execute: docker-compose -f docker-compose.prod.yml up -d"
else
    echo "✅ Todos os containers necessários estão rodando!"
fi

# Testar conectividade com PostgreSQL
echo ""
echo "🔗 Testando conectividade com PostgreSQL..."
if docker-compose -f docker-compose.prod.yml exec postgres pg_isready -U crm_user -d crm_ditual; then
    echo "✅ PostgreSQL acessível!"
else
    echo "❌ PostgreSQL não está acessível!"
    echo "Verifique os logs: docker-compose -f docker-compose.prod.yml logs postgres"
fi

echo ""
echo "🎉 VERIFICAÇÃO CONCLUÍDA!"
echo "========================"
echo ""
echo "📋 Status:"
echo "  ✅ Arquivo .env.prod: OK"
echo "  ✅ Variáveis críticas: OK"
echo "  ✅ Carregamento de variáveis: OK"
echo ""
echo "🚀 Próximos passos:"
echo "  1. Execute as migrações: ./scripts/run_all_migrations_ec2.sh"
echo "  2. Crie o usuário admin: ./scripts/create_admin_ec2.sh"