# 📘 Guia de Uso - CRM Microserviços

Este guia mostra como usar o sistema CRM após o setup inicial.

## 🚀 Início Rápido

### 1. Configurar Ambiente
```bash
# Configuração inicial (apenas uma vez)
make setup

# Iniciar serviços
make dev
```

### 2. Verificar Serviços
```bash
# Ver status dos containers
make status

# Ver logs em tempo real
make logs
```

## 👤 Gerenciamento de Usuários

### Criar Usuário Admin
```bash
curl -X POST "http://localhost:8001/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@crm.com",
    "username": "admin",
    "full_name": "Administrador",
    "password": "admin123456",
    "role": "admin"
  }'
```

### Criar Usuário de Vendas
```bash
curl -X POST "http://localhost:8001/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "vendedor@crm.com",
    "username": "vendedor",
    "full_name": "João Vendedor",
    "password": "venda123456",
    "role": "vendas"
  }'
```

### Fazer Login
```bash
curl -X POST "http://localhost:8001/api/v1/users/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123456"
  }'
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Listar Usuários
```bash
curl -X GET "http://localhost:8001/api/v1/users/" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

## 🌐 Usando a Interface Web

Acesse a documentação interativa da API:
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

### Testando via Interface

1. Acesse http://localhost:8001/docs
2. Clique em "POST /api/v1/users/" para criar usuário
3. Clique em "Try it out"
4. Preencha o JSON de exemplo
5. Execute e veja a resposta

## 📊 Monitoramento

### Health Checks
```bash
# Verificar saúde do serviço de usuários
curl http://localhost:8001/health

# Verificar PostgreSQL
docker exec crm_postgres pg_isready -U crm_user -d crm_db

# Verificar Redis
docker exec crm_redis redis-cli ping
```

### Logs dos Serviços
```bash
# Logs de todos os serviços
make logs

# Logs específicos
docker-compose logs user_service
docker-compose logs postgres
docker-compose logs redis
```

## 🔄 Eventos do Sistema

O sistema publica eventos no Redis quando ações ocorrem:

### Monitorar Eventos
```bash
# Conectar ao Redis CLI
docker exec -it crm_redis redis-cli

# Assinar canal de eventos de usuário
SUBSCRIBE user_events
```

### Tipos de Eventos
- `user.created` - Novo usuário criado
- `user.updated` - Usuário atualizado
- `user.deleted` - Usuário removido
- `user.login` - Login realizado

## 🗄️ Banco de Dados

### Conectar ao PostgreSQL
```bash
# Via Docker
docker exec -it crm_postgres psql -U crm_user -d crm_db

# Via cliente local (se instalado)
psql -h localhost -p 5432 -U crm_user -d crm_db
```

### Comandos Úteis no psql
```sql
-- Listar tabelas
\dt

-- Ver estrutura da tabela users
\d users

-- Consultar usuários
SELECT id, username, email, role, is_active FROM users;

-- Sair
\q
```

### Migrações
```bash
# Criar nova migração
make migration

# Aplicar migrações
make migrate

# Ver histórico de migrações
cd services/user_service && source venv/bin/activate && alembic history
```

## 🧪 Testes

### Executar Testes
```bash
# Todos os testes
make test

# Testes específicos
cd services/user_service
source venv/bin/activate
python -m pytest tests/test_users.py -v
```

### Testes de Carga
```bash
# Instalar Apache Bench (se não tiver)
brew install httpd  # macOS
# ou
sudo apt install apache2-utils  # Ubuntu

# Teste de carga no endpoint de health
ab -n 1000 -c 10 http://localhost:8001/health
```

## 🔧 Troubleshooting

### Problemas Comuns

#### Porto já em uso
```bash
# Ver processos usando portas
lsof -i :8001
lsof -i :5432
lsof -i :6379

# Parar serviços conflitantes
make stop
```

#### Erro de conexão com banco
```bash
# Verificar se PostgreSQL está rodando
docker-compose ps postgres

# Reiniciar PostgreSQL
docker-compose restart postgres

# Ver logs do PostgreSQL
docker-compose logs postgres
```

#### Erro de permissão nos scripts
```bash
# Dar permissão de execução
chmod +x scripts/*.sh
```

#### Limpar ambiente completamente
```bash
# Remove containers, volumes e networks
make clean

# Reconfigurar tudo
make setup
make dev
```

## 📈 Próximos Passos

### Adicionar Novos Serviços
1. Criar diretório em `services/`
2. Seguir estrutura similar ao `user_service`
3. Adicionar ao `docker-compose.yml`
4. Atualizar documentação

### Configuração de Produção
1. Alterar configurações de CORS
2. Usar variáveis de ambiente para senhas
3. Configurar HTTPS
4. Implementar rate limiting
5. Adicionar monitoramento (Prometheus, Grafana)

### Integração com Frontend
1. Configurar CORS adequadamente
2. Implementar refresh tokens
3. Criar middleware de autenticação
4. Documentar endpoints para o frontend

## 🆘 Suporte

Para problemas ou dúvidas:
1. Verificar logs: `make logs`
2. Consultar documentação: http://localhost:8001/docs
3. Verificar issues no repositório
4. Criar nova issue com detalhes do problema