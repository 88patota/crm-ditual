#!/bin/bash

# Script unificado para executar todas as migrações no ambiente EC2
# Este script executa migrações do user_service e budget_service em sequência
# Deve ser executado no diretório raiz do projeto

set -e

echo "🚀 Executando todas as migrações do CRM no ambiente EC2..."
echo "=================================================="

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
export $(grep -v '^#' .env.prod | xargs)

# Verificar se todos os containers necessários estão rodando
echo "🔍 Verificando status dos containers..."
REQUIRED_SERVICES=("postgres" "user_service" "budget_service")
MISSING_SERVICES=()

for service in "${REQUIRED_SERVICES[@]}"; do
    if ! docker-compose -f docker-compose.prod.yml ps | grep -q "$service"; then
        MISSING_SERVICES+=("$service")
    fi
done

if [ ${#MISSING_SERVICES[@]} -ne 0 ]; then
    echo "❌ Os seguintes containers não estão rodando: ${MISSING_SERVICES[*]}"
    echo "Execute: docker-compose -f docker-compose.prod.yml up -d"
    exit 1
fi

echo "✅ Todos os containers necessários estão rodando!"

# Aguardar serviços estarem prontos
echo "⏳ Aguardando serviços estarem prontos..."
sleep 10

# Verificar conectividade com o banco
echo "🔗 Testando conectividade com o banco de dados..."
docker-compose -f docker-compose.prod.yml exec postgres pg_isready -U crm_user -d crm_db
if [ $? -ne 0 ]; then
    echo "❌ Banco de dados não está acessível!"
    exit 1
fi

echo "✅ Banco de dados acessível!"
echo ""

# Executar migrações do user_service
echo "👤 EXECUTANDO MIGRAÇÕES DO USER_SERVICE"
echo "======================================="
docker-compose -f docker-compose.prod.yml exec user_service alembic upgrade head

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
docker-compose -f docker-compose.prod.yml exec budget_service alembic upgrade head

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
docker-compose -f docker-compose.prod.yml exec user_service alembic current

echo ""
echo "📊 Estado das migrações do budget_service:"
docker-compose -f docker-compose.prod.yml exec budget_service alembic current

echo ""
echo "🗄️ Verificando tabelas criadas no banco de dados:"
docker-compose -f docker-compose.prod.yml exec postgres psql -U crm_user -d crm_db -c "\\dt"

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
echo "  3. Verificar logs dos serviços: docker-compose -f docker-compose.prod.yml logs"
echo ""
echo "📚 Para mais informações, consulte:"
echo "  - CREATE_ADMIN_README.md (criação de usuário admin)"
echo "  - docker-compose -f docker-compose.prod.yml logs [service_name] (logs específicos)"