.PHONY: setup dev stop clean test lint migrate

# Setup do ambiente de desenvolvimento
setup:
	@echo "🔧 Configurando ambiente de desenvolvimento..."
	@chmod +x scripts/setup_dev.sh
	@./scripts/setup_dev.sh

# Iniciar ambiente de desenvolvimento
dev:
	@echo "🚀 Iniciando ambiente de desenvolvimento..."
	@chmod +x scripts/run_dev.sh
	@./scripts/run_dev.sh

# Parar todos os serviços
stop:
	@echo "⏹️ Parando serviços..."
	@docker compose down

# Limpar ambiente (volumes, containers, etc.)
clean:
	@echo "🧹 Limpando ambiente..."
	@docker compose down -v
	@docker system prune -f

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
	@docker compose logs -f

# Status dos serviços
status:
	@docker compose ps