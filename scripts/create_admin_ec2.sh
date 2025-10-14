#!/bin/bash

# Script para criar usuário admin no CRM Ditual em ambiente EC2
# Este script executa o Python script dentro do container user_service

set -e

echo "🚀 CRM Ditual - Criação de Usuário Admin (EC2)"
echo "=============================================="

# Verificar se docker-compose está disponível
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose não encontrado"
    echo "💡 Instale o docker-compose primeiro"
    exit 1
fi

# Verificar se o arquivo docker-compose.prod.yml existe
if [ ! -f "docker-compose.prod.yml" ]; then
    echo "❌ Arquivo docker-compose.prod.yml não encontrado"
    echo "💡 Execute este script a partir do diretório raiz do projeto"
    exit 1
fi

# Verificar se os containers estão rodando
echo "🔍 Verificando status dos containers..."

if ! docker-compose -f docker-compose.prod.yml ps | grep -q "crm_user_service.*Up"; then
    echo "❌ Container user_service não está rodando"
    echo "💡 Inicie os containers primeiro com:"
    echo "   docker-compose -f docker-compose.prod.yml up -d"
    exit 1
fi

if ! docker-compose -f docker-compose.prod.yml ps | grep -q "crm_postgres.*Up"; then
    echo "❌ Container postgres não está rodando"
    echo "💡 Inicie os containers primeiro com:"
    echo "   docker-compose -f docker-compose.prod.yml up -d"
    exit 1
fi

echo "✅ Containers estão rodando"

# Aguardar um pouco para garantir que os serviços estejam prontos
echo "⏳ Aguardando serviços ficarem prontos..."
sleep 5

# Executar o script Python dentro do container
echo "🔧 Executando script de criação do usuário admin..."
echo "=============================================="

docker-compose -f docker-compose.prod.yml exec user_service python create_admin_user.py

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