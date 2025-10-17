#!/bin/bash

# Script para criar usuário admin no CRM Ditual em ambiente LOCAL
# Este script executa o Python script dentro do container user_service (dev)

set -e

echo "🚀 CRM Ditual - Criação de Usuário Admin (Local)"
echo "=============================================="

# Detectar comando docker compose (plugin) ou docker-compose (standalone)
COMPOSE_CMD=""
if docker compose version >/dev/null 2>&1; then
  COMPOSE_CMD="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE_CMD="docker-compose"
else
  echo "❌ Docker Compose não encontrado"
  echo "💡 Instale Docker Compose ou o plugin 'docker compose'"
  exit 1
fi

# Verificar se o arquivo docker-compose.yml existe
if [ ! -f "docker-compose.yml" ]; then
  echo "❌ Arquivo docker-compose.yml não encontrado"
  echo "💡 Execute este script a partir do diretório raiz do projeto"
  exit 1
fi

# Verificar se os containers estão rodando
echo "🔍 Verificando status dos containers..."

if ! $COMPOSE_CMD ps | grep -q "crm_user_service.*Up"; then
  echo "❌ Container user_service não está rodando"
  echo "💡 Inicie os containers primeiro com:"
  echo "   $COMPOSE_CMD up -d"
  exit 1
fi

if ! $COMPOSE_CMD ps | grep -q "crm_postgres.*Up"; then
  echo "❌ Container postgres não está rodando"
  echo "💡 Inicie os containers primeiro com:"
  echo "   $COMPOSE_CMD up -d"
  exit 1
fi

echo "✅ Containers estão rodando"

# Aguardar um pouco para garantir que os serviços estejam prontos
echo "⏳ Aguardando serviços ficarem prontos..."
sleep 5

# Executar o script Python dentro do container
echo "🔧 Executando script de criação do usuário admin..."
echo "=============================================="

$COMPOSE_CMD exec user_service python create_admin_user.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 SUCESSO!"
    echo "=============================================="
    echo "✅ Usuário admin criado com sucesso"
    echo "🔐 Credenciais:"
    echo "   Username: admin"
    echo "   Password: admin102030"
    echo ""
    echo "🌐 Você pode agora fazer login no sistema!"
    echo "=============================================="
else
    echo ""
    echo "❌ ERRO!"
    echo "=============================================="
    echo "Falha ao criar usuário admin"
    echo "Verifique os logs acima para mais detalhes"
    exit 1
fi