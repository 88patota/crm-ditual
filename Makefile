.PHONY: help setup backend frontend all dev stop clean test lint migrate health rebuild install

# Mostrar ajuda
help:
	@echo "CRM Ditual - Comandos disponíveis:"
	@echo ""
	@echo "  setup      - Configurar ambiente de desenvolvimento"
	@echo "  backend    - Iniciar apenas serviços backend"
	@echo "  frontend   - Iniciar apenas frontend"
	@echo "  all        - Iniciar todos os serviços (backend + frontend)"
	@echo "  dev        - Alias para 'all'"
	@echo "  stop       - Parar todos os serviços"
	@echo "  logs       - Mostrar logs dos serviços"
	@echo "  status     - Verificar status dos serviços"
	@echo "  health     - Verificar saúde dos serviços"
	@echo "  clean      - Limpar containers e volumes"
	@echo "  rebuild    - Rebuild de todos os serviços"
	@echo "  test       - Executar testes"
	@echo "  lint       - Verificar código"
	@echo "  migrate    - Executar migrações"
	@echo "  install    - Instalar dependências do frontend"

# Setup do ambiente de desenvolvimento
setup:
	@echo "🔧 Configurando ambiente de desenvolvimento..."
	@chmod +x scripts/setup_dev.sh
	@./scripts/setup_dev.sh

# Iniciar apenas serviços backend
backend:
	@echo "🔥 Iniciando serviços backend..."
	@docker compose up -d postgres redis user_service budget_service api_gateway
	@echo "✅ Backend iniciado!"
	@echo "🔧 API Gateway: http://localhost:8000"
	@echo "👥 User Service: http://localhost:8001" 
	@echo "💰 Budget Service: http://localhost:8002"

# Iniciar apenas frontend
frontend:
	@echo "🎨 Iniciando frontend..."
	@cd frontend && npm run dev

# Iniciar todos os serviços (backend + frontend)
all:
	@echo "🚀 Iniciando todos os serviços..."
	@make backend
	@echo "⏳ Aguardando serviços backend ficarem prontos..."
	@sleep 15
	@echo "🎨 Iniciando frontend..."
	@cd frontend && npm run dev &
	@echo "🎉 Todos os serviços iniciados!"
	@echo "📊 Dashboard: http://localhost:5173"
	@echo "🔧 API Gateway: http://localhost:8000"

# Alias para desenvolvimento
dev:
	@make all

# Parar todos os serviços
stop:
	@echo "⏹️ Parando serviços..."
	@docker compose down
	@pkill -f "npm run dev" || true

# Limpar ambiente (volumes, containers, etc.)
clean:
	@echo "🧹 Limpando ambiente..."
	@docker compose down -v
	@docker system prune -f

# Verificar saúde dos serviços
health:
	@echo "🏥 Verificando saúde dos serviços..."
	@echo "PostgreSQL:"
	@docker compose exec postgres pg_isready -U crm_user -d crm_db 2>/dev/null && echo "✅ PostgreSQL OK" || echo "❌ PostgreSQL não está saudável"
	@echo "Redis:"
	@docker compose exec redis redis-cli ping 2>/dev/null && echo "✅ Redis OK" || echo "❌ Redis não está saudável"
	@echo "User Service:"
	@curl -s http://localhost:8001/health >/dev/null 2>&1 && echo "✅ User Service OK" || echo "❌ User Service não está saudável"
	@echo "Budget Service:"
	@curl -s http://localhost:8002/health >/dev/null 2>&1 && echo "✅ Budget Service OK" || echo "❌ Budget Service não está saudável"
	@echo "API Gateway:"
	@curl -s http://localhost:8000/health >/dev/null 2>&1 && echo "✅ API Gateway OK" || echo "❌ API Gateway não está saudável"

# Rebuild de todos os serviços
rebuild:
	@echo "🔨 Rebuilding serviços..."
	@docker compose build --no-cache
	@make backend

# Executar testes
test:
	@echo "🧪 Executando testes..."
	@cd services/user_service && source venv/bin/activate && python -m pytest

# Verificar linting
lint:
	@echo "🔍 Verificando código..."
	@cd services/user_service && source venv/bin/activate && flake8 app/

# Executar migrações
migrate:
	@echo "🗄️ Executando migrações..."
	@cd services/user_service && source venv/bin/activate && alembic upgrade head

# Criar nova migração
migration:
	@echo "📝 Criando nova migração..."
	@cd services/user_service && source venv/bin/activate && alembic revision --autogenerate

# Logs dos serviços
logs:
	@docker compose logs -f --tail=100

# Status dos serviços
status:
	@docker compose ps

# Instalar dependências do frontend
install:
	@echo "📦 Instalando dependências do frontend..."
	@cd frontend && npm install