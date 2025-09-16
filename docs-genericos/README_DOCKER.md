# 🐳 CRM Ditual - Guia Docker Completo

Este guia contém todas as instruções para rodar o CRM Ditual usando Docker com todos os serviços backend.

## 🏗️ Arquitetura dos Serviços

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │  API Gateway    │    │   PostgreSQL    │
│   React + Vite  │◄──►│     Nginx       │    │   Database      │
│   Port: 5173    │    │   Port: 8000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │  User Service   │    │     Redis       │
                       │     FastAPI     │◄──►│     Cache       │
                       │   Port: 8001    │    │   Port: 6379    │
                       └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ Budget Service  │
                       │     FastAPI     │
                       │   Port: 8002    │
                       └─────────────────┘
```

## 🚀 Comandos Rápidos

### ⚡ Iniciar Tudo
```bash
# Opção 1: Usar Makefile (recomendado)
make all

# Opção 2: Script direto
./scripts/start-all.sh

# Opção 3: Docker Compose
docker compose up -d
```

### 🔧 Apenas Backend
```bash
make backend
```

### 🎨 Apenas Frontend
```bash
make frontend
```

### ⏹️ Parar Tudo
```bash
make stop
```

### 🏥 Verificar Saúde
```bash
make health
```

## 📋 Comandos Disponíveis

| Comando | Descrição |
|---------|-----------|
| `make help` | Mostrar todos os comandos |
| `make setup` | Configurar ambiente de desenvolvimento |
| `make backend` | Iniciar apenas serviços backend |
| `make frontend` | Iniciar apenas frontend |
| `make all` | Iniciar todos os serviços |
| `make dev` | Alias para 'all' |
| `make stop` | Parar todos os serviços |
| `make logs` | Mostrar logs dos serviços |
| `make status` | Verificar status dos serviços |
| `make health` | Verificar saúde dos serviços |
| `make clean` | Limpar containers e volumes |
| `make rebuild` | Rebuild de todos os serviços |
| `make install` | Instalar dependências do frontend |

## 🌐 URLs dos Serviços

### 🎯 Produção
- **Dashboard Frontend**: http://localhost:5173
- **API Gateway**: http://localhost:8000

### 🔧 Desenvolvimento
- **User Service**: http://localhost:8001
- **Budget Service**: http://localhost:8002
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

### 📖 Documentação
- **User Service API**: http://localhost:8001/docs
- **Budget Service API**: http://localhost:8002/docs

## 🔧 Configuração dos Serviços

### 📊 PostgreSQL
- **Database**: `crm_db`
- **User**: `crm_user`
- **Password**: `crm_password`
- **Port**: `5432`

### 🔴 Redis
- **Port**: `6379`
- **Memory**: `256MB`
- **Policy**: `allkeys-lru`

### 🌐 API Gateway (Nginx)
- **Port**: `8000`
- **CORS**: Habilitado
- **Routes**: 
  - `/api/v1/users/*` → User Service
  - `/api/v1/budgets/*` → Budget Service

## 🛠️ Desenvolvimento

### 📦 Primeira Instalação
```bash
# 1. Clonar o repositório
git clone <repository-url>
cd crm-ditual

# 2. Instalar dependências do frontend
make install

# 3. Configurar ambiente
make setup

# 4. Iniciar todos os serviços
make all
```

### 🔄 Uso Diário
```bash
# Iniciar desenvolvimento
make dev

# Ver logs
make logs

# Verificar status
make status

# Parar ao final do dia
make stop
```

### 🧹 Limpeza
```bash
# Limpar containers e volumes
make clean

# Rebuild completo
make rebuild
```

## 🐛 Troubleshooting

### ❌ Serviços não iniciam
```bash
# Verificar logs
make logs

# Verificar status
make status

# Limpar e tentar novamente
make clean
make rebuild
```

### 🔍 Debug de Serviços Específicos
```bash
# Logs de um serviço específico
docker compose logs user_service
docker compose logs budget_service
docker compose logs postgres

# Acessar container
docker compose exec user_service bash
docker compose exec postgres psql -U crm_user -d crm_db
```

### 🏥 Health Checks
```bash
# Verificar saúde de todos os serviços
make health

# Verificar individualmente
curl http://localhost:8001/health  # User Service
curl http://localhost:8002/health  # Budget Service
curl http://localhost:8000/health  # API Gateway
```

### 🔧 Problemas de Porta
Se alguma porta estiver ocupada:

```bash
# Verificar portas em uso
lsof -i :8000  # API Gateway
lsof -i :8001  # User Service
lsof -i :8002  # Budget Service
lsof -i :5432  # PostgreSQL
lsof -i :6379  # Redis

# Matar processo na porta
sudo kill -9 $(lsof -t -i:PORTA)
```

## 📊 Monitoramento

### 📈 Métricas dos Containers
```bash
# Uso de recursos
docker stats

# Logs em tempo real
docker compose logs -f

# Status detalhado
docker compose ps -a
```

### 🔍 Verificação de Banco
```bash
# Conectar ao PostgreSQL
docker compose exec postgres psql -U crm_user -d crm_db

# Verificar tabelas
\dt

# Verificar dados de usuários
SELECT * FROM users;
```

### 🔴 Verificação do Redis
```bash
# Conectar ao Redis
docker compose exec redis redis-cli

# Verificar keys
KEYS *

# Info do servidor
INFO
```

## 🚀 Deploy

### 🐳 Build para Produção
```bash
# Build todas as imagens
docker compose build

# Push para registry (configurar primeiro)
docker compose push
```

### ⚙️ Variáveis de Ambiente
Principais variáveis que podem ser configuradas:

```env
# Database
DATABASE_URL=postgresql+asyncpg://crm_user:crm_password@postgres:5432/crm_db

# Redis
REDIS_URL=redis://redis:6379

# JWT
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Environment
ENVIRONMENT=development|production
```

## 📝 Logs e Debugging

### 📋 Tipos de Logs
- **Application Logs**: Logs dos serviços Python
- **Access Logs**: Logs do Nginx (API Gateway)
- **Database Logs**: Logs do PostgreSQL
- **Cache Logs**: Logs do Redis

### 🔍 Comandos de Log
```bash
# Todos os logs
make logs

# Logs específicos com tail
docker compose logs -f --tail=100 user_service

# Logs por timestamp
docker compose logs --since="2024-01-01T00:00:00Z"
```

---

## 🎉 Pronto!

Com este setup, você tem um ambiente completo de desenvolvimento rodando em containers Docker, com:
- ✅ API Gateway para roteamento
- ✅ Serviços de microservices independentes  
- ✅ Banco de dados PostgreSQL
- ✅ Cache Redis
- ✅ Health checks automatizados
- ✅ Hot reload para desenvolvimento
- ✅ Logs centralizados

**Happy coding! 🚀**