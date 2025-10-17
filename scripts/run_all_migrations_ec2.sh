#!/bin/bash

# Script unificado para executar todas as migrações no ambiente EC2
# Este script executa migrações do user_service e budget_service em sequência
# Deve ser executado no diretório raiz do projeto

set -e

echo "🚀 Executando todas as migrações do CRM no ambiente EC2..."
echo "=================================================="

# Verificar se docker-compose está disponível
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
elif docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    echo "❌ docker-compose ou docker compose não está instalado!"
    exit 1
fi

# Verificar se o arquivo docker-compose.prod.yml existe
if [ ! -f "docker-compose.prod.yml" ]; then
    echo "❌ Arquivo docker-compose.prod.yml não encontrado!"
    echo "Execute este script no diretório raiz do projeto."
    exit 1
fi

# Verificar se o arquivo .env.prod existe
if [ ! -f ".env.prod" ]; then
    echo "❌ Arquivo .env.prod não encontrado!"
    echo "Este arquivo é necessário para as variáveis de ambiente."
    echo "Certifique-se de que o arquivo .env.prod está presente no diretório raiz."
    exit 1
fi

echo "✅ Arquivo .env.prod encontrado!"

# Carregar variáveis de ambiente do .env.prod
echo "🔧 Carregando variáveis de ambiente..."
set -a  # Automatically export all variables
source .env.prod
set +a  # Stop automatically exporting

# Verificar se todos os containers necessários estão rodando
echo "🔍 Verificando status dos containers..."
REQUIRED_SERVICES=("postgres" "user_service" "budget_service")
MISSING_SERVICES=()

for service in "${REQUIRED_SERVICES[@]}"; do
    if ! ${DOCKER_COMPOSE} -f docker-compose.prod.yml ps | grep -q "$service"; then
        MISSING_SERVICES+=("$service")
    fi
done

if [ ${#MISSING_SERVICES[@]} -ne 0 ]; then
    echo "❌ Os seguintes containers não estão rodando: ${MISSING_SERVICES[*]}"
    echo "Execute: ${DOCKER_COMPOSE} -f docker-compose.prod.yml up -d"
    exit 1
fi

echo "✅ Todos os containers necessários estão rodando!"

# Aguardar serviços estarem prontos
echo "⏳ Aguardando serviços estarem prontos..."
sleep 15

# Verificar conectividade com o banco usando as variáveis corretas
echo "🔗 Testando conectividade com o banco de dados..."
${DOCKER_COMPOSE} -f docker-compose.prod.yml exec postgres pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}
if [ $? -ne 0 ]; then
    echo "❌ Banco de dados não está acessível!"
    echo "🔧 Tentando recriar o banco de dados..."
    
    # Recriar banco se necessário
    ${DOCKER_COMPOSE} -f docker-compose.prod.yml exec postgres psql -U postgres -c "DROP DATABASE IF EXISTS ${POSTGRES_DB};"
    ${DOCKER_COMPOSE} -f docker-compose.prod.yml exec postgres psql -U postgres -c "CREATE DATABASE ${POSTGRES_DB} OWNER ${POSTGRES_USER};"
    ${DOCKER_COMPOSE} -f docker-compose.prod.yml exec postgres psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_USER};"
    
    # Testar novamente
    ${DOCKER_COMPOSE} -f docker-compose.prod.yml exec postgres pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}
    if [ $? -ne 0 ]; then
        echo "❌ Ainda não foi possível conectar ao banco!"
        exit 1
    fi
fi

echo "✅ Banco de dados acessível!"

# Verificar se o usuário e senha estão corretos
echo "🔐 Verificando autenticação do usuário..."
${DOCKER_COMPOSE} -f docker-compose.prod.yml exec postgres psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "SELECT 1;" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Falha na autenticação! Corrigindo senha do usuário..."
    ${DOCKER_COMPOSE} -f docker-compose.prod.yml exec postgres psql -U postgres -c "ALTER USER ${POSTGRES_USER} WITH PASSWORD '${POSTGRES_PASSWORD}';"
    
    # Testar novamente
    ${DOCKER_COMPOSE} -f docker-compose.prod.yml exec postgres psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "SELECT 1;" > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "❌ Ainda há problemas de autenticação!"
        exit 1
    fi
fi

echo "✅ Autenticação funcionando corretamente!"
echo ""

# Executar migrações do user_service
echo "👤 EXECUTANDO MIGRAÇÕES DO USER_SERVICE"
echo "======================================="
${DOCKER_COMPOSE} -f docker-compose.prod.yml exec user_service alembic upgrade head

if [ $? -eq 0 ]; then
    echo "✅ Migrações do user_service executadas com sucesso!"
    echo ""
else
    echo "❌ Erro ao executar migrações do user_service!"
    echo "Abortando execução das demais migrações."
    exit 1
fi

# Executar migrações do budget_service
echo "💰 EXECUTANDO MIGRAÇÕES DO BUDGET_SERVICE"
echo "========================================="
${DOCKER_COMPOSE} -f docker-compose.prod.yml exec budget_service alembic upgrade head

if [ $? -eq 0 ]; then
    echo "✅ Migrações do budget_service executadas com sucesso!"
    echo ""
else
    echo "❌ Erro ao executar migrações do budget_service!"
    exit 1
fi

# Verificar estado final das migrações
echo "🔍 VERIFICANDO ESTADO FINAL DAS MIGRAÇÕES"
echo "========================================"

echo "📊 Estado das migrações do user_service:"
${DOCKER_COMPOSE} -f docker-compose.prod.yml exec user_service alembic current

echo ""
echo "📊 Estado das migrações do budget_service:"
${DOCKER_COMPOSE} -f docker-compose.prod.yml exec budget_service alembic current

echo ""
echo "🗄️ Verificando tabelas criadas no banco de dados:"
${DOCKER_COMPOSE} -f docker-compose.prod.yml exec postgres psql -U crm_user -d crm_ditual -c "\\dt"

echo ""
echo "🎉 TODAS AS MIGRAÇÕES EXECUTADAS COM SUCESSO!"
echo "============================================="
echo ""
echo "📋 Resumo do que foi executado:"
echo "  ✅ user_service: Tabela 'users' criada com campos de autenticação e autorização"
echo "  ✅ budget_service: Tabelas 'budgets' e 'budget_items' criadas com todas as funcionalidades"
echo ""
echo "🔧 Próximos passos:"
echo "  1. Criar usuário admin: ./scripts/create_admin_ec2.sh"
echo "  2. Testar acesso ao sistema via frontend"
echo "  3. Verificar logs dos serviços: ${DOCKER_COMPOSE} -f docker-compose.prod.yml logs"
echo ""
echo "📚 Para mais informações, consulte:"
echo "  - CREATE_ADMIN_README.md (criação de usuário admin)"
echo "  - ${DOCKER_COMPOSE} -f docker-compose.prod.yml logs [service_name] (logs específicos)"