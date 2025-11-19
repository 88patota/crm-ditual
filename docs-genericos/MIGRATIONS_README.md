# Guia de Migrações do Banco de Dados

Este guia explica como executar as migrações do banco de dados em dois cenários:
- Ambiente EC2 com Docker (produção)
- Ambiente local no Mac, sem Docker (desenvolvimento)

## 📋 Pré-requisitos

- Docker e Docker Compose instalados na instância EC2
- Containers do projeto rodando (`docker-compose -f docker-compose.prod.yml up -d`)
- Acesso SSH à instância EC2
- Banco PostgreSQL configurado e acessível

### ⚠️ IMPORTANTE: Configuração do .env.prod

Antes de executar as migrações, certifique-se de que o arquivo `.env.prod` existe e contém as seguintes variáveis:

```bash
# Verificar se o arquivo .env.prod está configurado
./scripts/check_env_ec2.sh
```

**Variáveis obrigatórias no .env.prod:**
- `POSTGRES_PASSWORD`: Senha do PostgreSQL
- `REDIS_PASSWORD`: Senha do Redis  
- `SECRET_KEY`: Chave secreta da aplicação
- `DOMAIN`: Domínio da aplicação
- `POSTGRES_DB`: Nome do banco de dados
- `POSTGRES_USER`: Usuário do PostgreSQL

## 🗄️ Estrutura das Migrações

O projeto possui dois serviços com migrações independentes:

### User Service
- **Arquivo de migração**: `23b3c1dada96_initial_migration.py`
- **Tabela criada**: `users`
- **Campos**: id, email, username, full_name, hashed_password, role, is_active, created_at, updated_at

### Budget Service
- **12 arquivos de migração** (001 a 010 + 20250915_124515)
- **Tabelas criadas**: `budgets`, `budget_items`
- **Funcionalidades**: Orçamentos, itens, regras de negócio, comissões, IPI, frete, etc.

## 🚀 Métodos de Execução

### 1. Método Recomendado - Script Unificado

Execute todas as migrações de uma vez:

```bash
# Tornar o script executável
chmod +x scripts/run_all_migrations_ec2.sh

# 1. Primeiro, verificar se o ambiente está configurado
./scripts/check_env_ec2.sh

# 2. Executar todas as migrações
./scripts/run_all_migrations_ec2.sh
```

### 2. Execução Individual por Serviço

#### User Service
```bash
chmod +x scripts/run_user_migrations_ec2.sh
./scripts/run_user_migrations_ec2.sh
```

#### Budget Service
```bash
chmod +x scripts/run_budget_migrations_ec2.sh
./scripts/run_budget_migrations_ec2.sh
```

### 3. Execução Manual via Docker

#### User Service
```bash
docker-compose -f docker-compose.prod.yml exec user_service alembic upgrade head
```

#### Budget Service
```bash
docker-compose -f docker-compose.prod.yml exec budget_service alembic upgrade head
```

### 4. Ambiente Local (Mac, sem Docker)

Para desenvolvimento local sem Docker, use uma instância PostgreSQL local (Postgres.app ou Homebrew) e configure a URL do Alembic.

#### Pré-requisitos
- PostgreSQL disponível em `localhost:5432` (via Postgres.app ou `brew services start postgresql`)
- Banco de dados `crm_ditual` criado e acessível

#### Variáveis de Ambiente
Você pode usar uma URL dedicada ao Alembic ou aproveitar a `DATABASE_URL` convertida automaticamente:

```bash
# Opção A: definir URL síncrona dedicada ao Alembic
export ALEMBIC_DATABASE_URL="postgresql://crm_user:crm_password@localhost:5432/crm_ditual"

# Opção B: usar a mesma URL do runtime (async) e deixar o Alembic converter
export DATABASE_URL="postgresql+asyncpg://crm_user:crm_password@localhost:5432/crm_ditual"
```

#### Executar Migrações
No diretório do serviço de orçamento:

```bash
cd services/budget_service
alembic upgrade head
```

O arquivo `alembic/env.py` foi ajustado para:
- Sobrescrever `sqlalchemy.url` quando `ALEMBIC_DATABASE_URL` ou `DATABASE_URL` estiver definida.
- Converter automaticamente `postgresql+asyncpg` para `postgresql` quando necessário.
- Usar defaults locais (`POSTGRES_HOST=localhost`) quando não houver URL explícita.

#### User Service (local)

Variáveis de ambiente (exemplo `.env.local`):
```bash
ALEMBIC_DATABASE_URL=postgresql://crm_user:crm_strong_password_2024@localhost:5432/crm_db
USER_SERVICE_DATABASE_URL=postgresql+asyncpg://crm_user:crm_strong_password_2024@localhost:5432/crm_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=crm_db
```

Observação: o `user_service` usa uma tabela de versão própria do Alembic (`alembic_version_user`) para evitar conflito com o `budget_service`.

Executar migrações:
```bash
cd services/user_service
alembic upgrade head
```

Se as tabelas já existirem e você quiser apenas alinhar o estado do Alembic, faça o stamp:
```bash
cd services/user_service
alembic stamp 001
```

Ou inicie o serviço local carregando `.env.local` e executando migrações automaticamente:
```bash
cd services/user_service
bash start.sh
```

## 🔍 Verificação das Migrações

### Verificar estado atual das migrações
```bash
# User Service
docker-compose -f docker-compose.prod.yml exec user_service alembic current

# Budget Service
docker-compose -f docker-compose.prod.yml exec budget_service alembic current
```

### Verificar histórico de migrações
```bash
# User Service
docker-compose -f docker-compose.prod.yml exec user_service alembic history

# Budget Service
docker-compose -f docker-compose.prod.yml exec budget_service alembic history
```

### Verificar tabelas criadas no banco
```bash
docker-compose -f docker-compose.prod.yml exec postgres psql -U crm_user -d crm_db -c "\\dt"
```

## 🔧 Troubleshooting

### Problema: Container não está rodando
```bash
# Verificar status dos containers
docker-compose -f docker-compose.prod.yml ps

# Iniciar containers se necessário
docker-compose -f docker-compose.prod.yml up -d
```

### Problema: Banco de dados não acessível
```bash
# Testar conectividade (local)
pg_isready -h localhost -p 5432 -U crm_user -d crm_ditual

# Verificar serviço (Homebrew)
brew services list | grep postgres
```

### Problema: Erro de migração
```bash
# Verificar logs do serviço específico
docker-compose -f docker-compose.prod.yml logs user_service
docker-compose -f docker-compose.prod.yml logs budget_service

# Verificar estado atual da migração
docker-compose -f docker-compose.prod.yml exec [service_name] alembic current

# Forçar migração para uma versão específica (cuidado!)
docker-compose -f docker-compose.prod.yml exec [service_name] alembic upgrade [revision_id]
```

### Problema: Conflito de migrações
```bash
# Ver histórico completo
docker-compose -f docker-compose.prod.yml exec [service_name] alembic history --verbose

# Resolver conflitos manualmente (avançado)
docker-compose -f docker-compose.prod.yml exec [service_name] alembic merge [revision1] [revision2]
```

## 📊 Detalhes das Migrações do Budget Service

| Migração | Descrição |
|----------|-----------|
| 001 | Conversão de campos Float para Numeric (precisão monetária) |
| 002 | Criação do enum BudgetStatus |
| 003 | Conversão do status de enum para string |
| 004 | Adição de campos de regras de negócio |
| 005 (commission) | Adição de percentual de comissão atual |
| 005 (quantity) | Remoção da coluna quantity |
| 006 (ipi) | Adição de campos IPI aos orçamentos |
| 006 (rename) | Renomeação de colunas para inglês |
| 007 | Configuração inicial da fonte da verdade |
| 008 | Adição de campos IPI aos itens do orçamento |
| 009 | Adição de tempo de entrega aos itens |
| 010 | Adição de tipo de frete aos orçamentos |
| 20250915 | Adição de total de venda com ICMS |

## 🔐 Segurança

- As migrações são executadas dentro dos containers Docker
- Credenciais do banco são gerenciadas via variáveis de ambiente
- Não há exposição de senhas nos scripts
- Logs podem conter informações sensíveis - revisar antes de compartilhar

## 📝 Próximos Passos

Após executar as migrações com sucesso:

1. **Criar usuário admin**: Execute `./scripts/create_admin_ec2.sh`
2. **Testar acesso**: Acesse o frontend e teste o login
3. **Verificar logs**: Monitore os logs dos serviços
4. **Backup**: Considere fazer backup do banco após as migrações

## 📚 Arquivos Relacionados

- `scripts/check_env_ec2.sh` - Script para verificar configuração do ambiente
- `scripts/run_all_migrations_ec2.sh` - Script unificado
- `scripts/run_user_migrations_ec2.sh` - Migrações do user_service
- `scripts/run_budget_migrations_ec2.sh` - Migrações do budget_service
- `CREATE_ADMIN_README.md` - Guia para criar usuário admin
- `docker-compose.prod.yml` - Configuração de produção

## ⚠️ Avisos Importantes

- **Sempre faça backup** do banco antes de executar migrações em produção
- **Teste as migrações** em ambiente de desenvolvimento primeiro
- **Monitore os logs** durante e após a execução
- **Não execute migrações** em paralelo nos mesmos serviços
- **Verifique o estado** das migrações antes de executar novamente