#!/bin/bash

echo "🚀 Configurando ambiente de desenvolvimento CRM..."

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não está instalado. Por favor, instale Python 3.11 ou superior."
    exit 1
fi

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Por favor, instale Docker."
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker compose &> /dev/null; then
    echo "❌ Docker Compose não está instalado. Por favor, instale Docker Compose."
    exit 1
fi

echo "✅ Dependências verificadas"

# Criar ambiente virtual para o serviço de usuário
echo "🔧 Criando ambiente virtual..."
cd services/user_service
python3 -m venv venv
source venv/bin/activate

# Instalar dependências Python
echo "📦 Instalando dependências Python..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Ambiente virtual configurado"

# Voltar para o diretório raiz
cd ../../

# Subir serviços de infraestrutura (PostgreSQL e Redis)
echo "🐳 Iniciando serviços de infraestrutura..."
docker compose up -d postgres redis

# Aguardar serviços estarem prontos
echo "⏳ Aguardando serviços estarem prontos..."
sleep 10

# Executar migrações do banco de dados
echo "🗄️ Executando migrações do banco de dados..."
cd services/user_service
source venv/bin/activate
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

echo "✅ Setup completo!"
echo ""
echo "🎉 Ambiente de desenvolvimento configurado com sucesso!"
echo ""
echo "Para iniciar os serviços:"
echo "  docker compose up"
echo ""
echo "Para acessar o serviço de usuário:"
echo "  http://localhost:8001"
echo ""
echo "Para acessar a documentação da API:"
echo "  http://localhost:8001/docs"