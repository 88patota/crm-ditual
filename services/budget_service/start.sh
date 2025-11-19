#!/bin/bash

# Script de inicialização do budget_service
# Executa migração do banco antes de iniciar o serviço

echo "Iniciando budget_service..."

# Carregar variáveis locais, se existir
if [ -f ".env.local" ]; then
  set -a
  . ./.env.local
  set +a
fi

# Garantir binários da venv no PATH
if [ -d ".venv/bin" ]; then
  export PATH=".venv/bin:$PATH"
fi

# Aguardar o banco de dados estar disponível
echo "Aguardando banco de dados..."
# Usar variáveis de ambiente com defaults locais
POSTGRES_HOST=${POSTGRES_HOST:-localhost}
POSTGRES_PORT=${POSTGRES_PORT:-5432}
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done
echo "Banco de dados disponível!"

# Executar migração do Alembic
echo "Executando migração do banco..."
alembic upgrade head

if [ $? -eq 0 ]; then
    echo "Migração executada com sucesso!"
else
    echo "Erro ao executar migração!"
    exit 1
fi

# Iniciar o serviço
echo "Iniciando serviço..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
