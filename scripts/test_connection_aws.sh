#!/bin/bash

# Script para testar conexão PostgreSQL na AWS
# Carrega variáveis do .env.prod e executa o teste

echo "🚀 Testando conexão PostgreSQL na AWS..."
echo "================================================"

# Verificar se .env.prod existe
if [ ! -f ".env.prod" ]; then
    echo "❌ Arquivo .env.prod não encontrado!"
    echo "💡 Certifique-se de que o arquivo .env.prod está presente"
    exit 1
fi

# Carregar variáveis do .env.prod
echo "📁 Carregando variáveis do .env.prod..."
export $(grep -v '^#' .env.prod | xargs)

# Verificar se Python está disponível
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado!"
    echo "💡 Instale Python3 para executar o teste"
    exit 1
fi

# Verificar se asyncpg está instalado
echo "🔍 Verificando dependências..."
python3 -c "import asyncpg" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  asyncpg não encontrado, instalando..."
    pip3 install asyncpg
fi

# Executar teste de conexão
echo "🔄 Executando teste de conexão..."
python3 scripts/verify_db_connection.py

# Capturar código de saída
exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo ""
    echo "✅ Teste concluído com sucesso!"
    echo "💡 A conexão PostgreSQL está funcionando corretamente"
else
    echo ""
    echo "❌ Teste falhou!"
    echo "💡 Verifique os logs acima para identificar o problema"
    echo ""
    echo "🔧 Passos para debug:"
    echo "   1. Verifique se o PostgreSQL está rodando"
    echo "   2. Confirme as credenciais no .env.prod"
    echo "   3. Teste a conectividade de rede"
    echo "   4. Verifique os logs do container PostgreSQL"
fi

exit $exit_code