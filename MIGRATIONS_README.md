# Guia de Migrações do Banco de Dados - Ambiente EC2

Este guia explica como executar as migrações do banco de dados no ambiente EC2 com Docker.

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
# Testar conectividade
docker-compose -f docker-compose.prod.yml exec postgres pg_isready -U crm_user -d crm_db

# Verificar logs do PostgreSQL
docker-compose -f docker-compose.prod.yml logs postgres
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