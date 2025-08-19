#!/bin/bash

# Script para executar migração do Alembic no budget_service
# Este script deve ser executado dentro do container do budget_service

echo "Iniciando migração do banco de dados para o budget_service..."

# Navegar para o diretório do budget_service
cd /app

# Verificar se o Alembic está configurado
if [ ! -f "alembic.ini" ]; then
    echo "Erro: alembic.ini não encontrado!"
    exit 1
fi

# Verificar se o diretório alembic existe
if [ ! -d "alembic" ]; then
    echo "Erro: diretório alembic não encontrado!"
    exit 1
fi

# Executar a migração
echo "Executando migração..."
alembic upgrade head

if [ $? -eq 0 ]; then
    echo "Migração executada com sucesso!"
else
    echo "Erro ao executar migração!"
    exit 1
fi

echo "Migração concluída!"
