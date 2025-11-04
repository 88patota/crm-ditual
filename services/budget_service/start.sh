#!/bin/bash

# Script de inicialização do budget_service
# Executa migração do banco antes de iniciar o serviço

echo "Iniciando budget_service..."

# Aguardar o banco de dados estar disponível
echo "Aguardando banco de dados..."
while ! nc -z postgres 5432; do
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
