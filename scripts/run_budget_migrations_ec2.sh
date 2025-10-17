#!/bin/bash

# Script para executar migrações do budget_service no ambiente EC2
# Este script deve ser executado no diretório raiz do projeto

set -e

echo "🗄️ Executando migrações do budget_service no ambiente EC2..."

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
set -a  # Automatically export all variables
source .env.prod
set +a  # Stop automatically exporting

# Verificar se os containers estão rodando
echo "🔍 Verificando status dos containers..."
if ! docker-compose -f docker-compose.prod.yml ps | grep -q "budget_service"; then
    echo "❌ Container budget_service não está rodando!"
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

# Executar migrações do budget_service
echo "🚀 Executando migrações do budget_service..."
docker-compose -f docker-compose.prod.yml exec budget_service alembic upgrade head

if [ $? -eq 0 ]; then
    echo "✅ Migrações do budget_service executadas com sucesso!"
    echo ""
    echo "📋 Resumo das migrações aplicadas:"
    echo "  - Serviço: budget_service"
    echo "  - 001_convert_to_numeric.py: Conversão de campos Float para Numeric (precisão monetária)"
    echo "  - 002_create_budget_status_enum.py: Criação do enum BudgetStatus"
    echo "  - 003_convert_status_to_string.py: Conversão do status de enum para string"
    echo "  - 004_add_business_rules_fields.py: Adição de campos de regras de negócio"
    echo "  - 005_add_commission_percentage_actual.py: Adição de percentual de comissão atual"
    echo "  - 005_remove_quantity_column.py: Remoção da coluna quantity"
    echo "  - 006_add_ipi_fields_to_budgets.py: Adição de campos IPI aos orçamentos"
    echo "  - 006_rename_columns_to_english.py: Renomeação de colunas para inglês"
    echo "  - 007_fonte_da_verdade_inicial.py: Configuração inicial da fonte da verdade"
    echo "  - 008_add_ipi_fields_to_budget_items.py: Adição de campos IPI aos itens do orçamento"
    echo "  - 009_add_delivery_time_to_budget_items.py: Adição de tempo de entrega aos itens"
    echo "  - 010_add_freight_type_to_budgets.py: Adição de tipo de frete aos orçamentos"
    echo "  - 20250915_124515_add_total_sale_with_icms.py: Adição de total de venda com ICMS"
    echo ""
    echo "📊 Tabelas criadas/modificadas:"
    echo "  - budgets: Tabela principal de orçamentos"
    echo "  - budget_items: Itens dos orçamentos"
    echo ""
else
    echo "❌ Erro ao executar migrações do budget_service!"
    echo ""
    echo "🔧 Troubleshooting:"
    echo "  1. Verifique se o container budget_service está rodando:"
    echo "     docker-compose -f docker-compose.prod.yml ps"
    echo ""
    echo "  2. Verifique os logs do budget_service:"
    echo "     docker-compose -f docker-compose.prod.yml logs budget_service"
    echo ""
    echo "  3. Verifique a conectividade com o banco:"
    echo "     docker-compose -f docker-compose.prod.yml exec postgres psql -U crm_user -d crm_db -c '\\dt'"
    echo ""
    echo "  4. Verifique se há conflitos de migração:"
    echo "     docker-compose -f docker-compose.prod.yml exec budget_service alembic current"
    echo "     docker-compose -f docker-compose.prod.yml exec budget_service alembic history"
    echo ""
    exit 1
fi

echo "🎉 Migrações do budget_service concluídas!"