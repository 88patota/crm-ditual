# 🚀 Passo a Passo - Aplicação da Refatoração de Migrações em Produção

## ✅ Status da Refatoração
- **Ambiente de Desenvolvimento**: ✅ TESTADO E FUNCIONANDO
- **Migrações Criadas**: ✅ COMPLETO
- **Sistema Validado**: ✅ FUNCIONANDO

## 📋 Pré-requisitos
- Acesso SSH à instância EC2
- Backup completo do banco de dados
- Acesso aos arquivos do projeto na EC2

## 🔧 Passo a Passo para Produção

### 1. 📥 Fazer Backup Completo
```bash
# Conectar na EC2
ssh -i sua-chave.pem ubuntu@seu-ip-ec2

# Navegar para o diretório do projeto
cd /caminho/para/crm-ditual

# Fazer backup do banco de dados
docker compose exec postgres pg_dump -U crm_user -d crm_ditual > backup_pre_migration_$(date +%Y%m%d_%H%M%S).sql

# Fazer backup das migrações atuais
cp -r services/budget_service/alembic/versions migrations_backup_prod_$(date +%Y%m%d_%H%M%S)/budget_versions
cp -r services/user_service/alembic/versions migrations_backup_prod_$(date +%Y%m%d_%H%M%S)/user_versions
```

### 2. ⏹️ Parar Todos os Serviços
```bash
# Parar todos os serviços
docker compose -f docker-compose.prod.yml down

# Verificar que todos os containers foram parados
docker ps -a
```

### 3. 🧹 Limpar Tabela alembic_version
```bash
# Iniciar apenas o PostgreSQL
docker compose -f docker-compose.prod.yml up -d postgres

# Aguardar PostgreSQL ficar pronto (30 segundos)
sleep 30

# Limpar tabela alembic_version
docker compose exec postgres psql -U crm_user -d crm_ditual -c "DELETE FROM alembic_version;"

# Verificar que foi limpa
docker compose exec postgres psql -U crm_user -d crm_ditual -c "SELECT * FROM alembic_version;"
```

### 4. 🗂️ Atualizar Arquivos de Migração
```bash
# Remover migrações antigas do budget_service
rm -f services/budget_service/alembic/versions/*.py

# Remover migrações antigas do user_service  
rm -f services/user_service/alembic/versions/*.py
```

### 5. 📁 Copiar Novas Migrações
Copie os seguintes arquivos do ambiente de desenvolvimento para produção:

**Budget Service:**
```bash
# Criar arquivo: services/budget_service/alembic/versions/001_initial_migration.py
# (Conteúdo já criado e testado)
```

**User Service:**
```bash
# Criar arquivo: services/user_service/alembic/versions/001_initial_migration.py
# (Conteúdo já criado e testado)
```

### 6. 🚀 Iniciar Serviços e Aplicar Migrações
```bash
# Iniciar todos os serviços
docker compose -f docker-compose.prod.yml up -d

# Aguardar serviços ficarem prontos (60 segundos)
sleep 60

# Marcar migrações como aplicadas (sem executar DDL)
docker compose exec budget_service alembic stamp 001
docker compose exec user_service alembic stamp 001
```

### 7. ✅ Validar Sistema
```bash
# Verificar status das migrações
docker compose exec budget_service alembic current
docker compose exec user_service alembic current

# Verificar tabela alembic_version
docker compose exec postgres psql -U crm_user -d crm_ditual -c "SELECT * FROM alembic_version;"

# Testar endpoints de saúde
curl -f https://seu-dominio.com/api/users/health
curl -f https://seu-dominio.com/api/budgets/health

# Verificar logs dos serviços
docker compose logs budget_service --tail=50
docker compose logs user_service --tail=50
```

### 8. 🧪 Teste Funcional
```bash
# Testar criação de usuário (se aplicável)
# Testar criação de orçamento (se aplicável)
# Verificar se o frontend está carregando corretamente
```

## 🚨 Plano de Rollback (Se Necessário)

### Se algo der errado:
```bash
# 1. Parar serviços
docker compose -f docker-compose.prod.yml down

# 2. Restaurar backup do banco
docker compose -f docker-compose.prod.yml up -d postgres
sleep 30
docker compose exec -T postgres psql -U crm_user -d crm_ditual < backup_pre_migration_YYYYMMDD_HHMMSS.sql

# 3. Restaurar migrações antigas
cp -r migrations_backup_prod_YYYYMMDD_HHMMSS/budget_versions/* services/budget_service/alembic/versions/
cp -r migrations_backup_prod_YYYYMMDD_HHMMSS/user_versions/* services/user_service/alembic/versions/

# 4. Reiniciar serviços
docker compose -f docker-compose.prod.yml up -d
```

## 📊 Resultados Esperados

Após a execução bem-sucedida:
- ✅ Tabela `alembic_version` com apenas uma entrada: `001`
- ✅ Ambos os serviços com migração `001 (head)`
- ✅ Sistema funcionando normalmente
- ✅ Estrutura de migrações limpa e organizada
- ✅ Sem conflitos de numeração
- ✅ Base sólida para futuras migrações

## 📞 Suporte
Em caso de problemas durante a execução, documente:
1. Passo onde ocorreu o erro
2. Mensagem de erro completa
3. Logs dos serviços
4. Status dos containers

**Tempo estimado total: 15-20 minutos**
**Downtime estimado: 10-15 minutos**