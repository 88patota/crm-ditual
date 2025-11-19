# PLANO DE REFATORAÇÃO - SISTEMA DE MIGRAÇÕES
## CRM Ditual - Solução Definitiva para Problemas de Banco de Dados

### 🔍 DIAGNÓSTICO DOS PROBLEMAS IDENTIFICADOS

#### 1. **Conflitos de Numeração de Migrações**
- **Problema**: Duas migrações com ID `005` no budget_service:
  - `005_add_commission_percentage_actual.py`
  - `005_remove_quantity_column.py`
- **Impacto**: Conflito de dependências e ordem de execução

#### 2. **Referências Cruzadas Entre Serviços**
- **Problema**: Migrações do budget_service referenciam revisões do user_service
- **Evidência**: Scripts de correção múltiplos (`fix_*.py`) indicam problema recorrente
- **Impacto**: Falhas na aplicação de migrações e inconsistências

#### 3. **Estrutura de Migrações Desorganizada**
- **Problema**: Mistura de formatos de ID (numéricas vs hash)
- **Evidência**: 
  - IDs sequenciais: `001`, `002`, `003`...
  - IDs hash: `1f4f4176aeb7`, `c0eefe7ade9c`
  - IDs timestamp: `20250915_124515`

#### 4. **Múltiplas Heads Não Resolvidas**
- **Problema**: Arquivo de merge `c0eefe7ade9c_merge_multiple_heads.py` indica heads divergentes
- **Impacto**: Estado inconsistente do banco

---

## 🎯 OPÇÕES DE SOLUÇÃO

### **OPÇÃO 1: RESET COMPLETO COM MIGRAÇÃO ÚNICA (RECOMENDADA)**

#### **Vantagens:**
- ✅ Elimina todos os conflitos existentes
- ✅ Estrutura limpa e organizada
- ✅ Fácil manutenção futura
- ✅ Sem dependências cruzadas

#### **Desvantagem:**
- ⚠️ Requer backup e restauração de dados

#### **Passos:**
1. **Backup dos dados**
2. **Criar migração única por serviço**
3. **Limpar histórico de migrações**
4. **Aplicar nova estrutura**
5. **Restaurar dados**

---

### **OPÇÃO 2: CORREÇÃO INCREMENTAL (MAIS ARRISCADA)**

#### **Vantagens:**
- ✅ Mantém histórico existente
- ✅ Não requer backup/restore

#### **Desvantagens:**
- ❌ Complexa de implementar
- ❌ Pode gerar novos conflitos
- ❌ Difícil de manter

#### **Passos:**
1. **Renumerar migrações conflitantes**
2. **Corrigir dependências**
3. **Resolver múltiplas heads**

---

### **OPÇÃO 3: MIGRAÇÃO HÍBRIDA (EQUILIBRADA)**

#### **Vantagens:**
- ✅ Preserva dados importantes
- ✅ Estrutura mais limpa
- ✅ Risco controlado

#### **Desvantagem:**
- ⚠️ Complexidade média

#### **Passos:**
1. **Backup seletivo**
2. **Reset apenas das migrações problemáticas**
3. **Manter migrações estáveis**

---

## 🚀 IMPLEMENTAÇÃO RECOMENDADA - OPÇÃO 1

### **FASE 1: PREPARAÇÃO**

```bash
# 1. Backup completo do banco
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U crm_user crm_ditual > backup_pre_migration.sql

# 2. Backup dos dados críticos
python scripts/backup_critical_data.py
```

### **FASE 2: LIMPEZA**

```bash
# 1. Parar serviços
docker-compose -f docker-compose.prod.yml down

# 2. Limpar tabela alembic_version
python fix_cross_contamination.py

# 3. Remover migrações conflitantes
rm -rf services/*/alembic/versions/*
```

### **FASE 3: NOVA ESTRUTURA**

#### **Budget Service - Migração Única**
```python
# services/budget_service/alembic/versions/001_initial_schema.py
"""Initial schema for budget service

Revision ID: 001_initial_schema
Revises: 
Create Date: 2025-01-XX XX:XX:XX.XXXXXX
"""

def upgrade() -> None:
    # Criar todas as tabelas de uma vez
    # budgets + budget_items com TODOS os campos atuais
    pass
```

#### **User Service - Migração Única**
```python
# services/user_service/alembic/versions/001_initial_schema.py
"""Initial schema for user service

Revision ID: 001_initial_schema
Revises: 
Create Date: 2025-01-XX XX:XX:XX.XXXXXX
"""

def upgrade() -> None:
    # Criar tabela users com todos os campos
    pass
```

### **FASE 4: APLICAÇÃO**

```bash
# 1. Subir apenas o banco
docker-compose -f docker-compose.prod.yml up -d postgres redis

# 2. Aplicar migrações
docker-compose -f docker-compose.prod.yml exec user_service alembic upgrade head
docker-compose -f docker-compose.prod.yml exec budget_service alembic upgrade head

# 3. Restaurar dados
python scripts/restore_critical_data.py

# 4. Subir todos os serviços
docker-compose -f docker-compose.prod.yml up -d
```

---

## 📋 SCRIPTS NECESSÁRIOS

### **1. Script de Backup de Dados Críticos**
```python
# scripts/backup_critical_data.py
# - Exportar usuários
# - Exportar orçamentos
# - Exportar itens de orçamento
# - Salvar em JSON/CSV
```

### **2. Script de Restauração**
```python
# scripts/restore_critical_data.py
# - Importar usuários
# - Importar orçamentos
# - Importar itens
# - Validar integridade
```

### **3. Script de Validação**
```python
# scripts/validate_migration.py
# - Verificar estrutura das tabelas
# - Contar registros
# - Validar relacionamentos
```

---

## ⚡ EXECUÇÃO RÁPIDA - COMANDOS PRONTOS

### **Para Ambiente de Desenvolvimento:**
```bash
# Reset completo (CUIDADO: apaga dados!)
./scripts/reset_dev_database.sh
```

### **Para Ambiente de Produção:**
```bash
# Backup + Reset + Restore
./scripts/production_migration_reset.sh
```

---

## 🔒 PREVENÇÃO DE PROBLEMAS FUTUROS

### **1. Convenções de Nomenclatura**
- **User Service**: `user_001_`, `user_002_`, etc.
- **Budget Service**: `budget_001_`, `budget_002_`, etc.

### **2. Processo de Criação de Migrações**
```bash
# Sempre usar comando específico por serviço
cd services/user_service
alembic revision --autogenerate -m "description"

cd services/budget_service  
alembic revision --autogenerate -m "description"
```

### **3. Validação Automática**
- Script de CI/CD para validar migrações
- Testes automatizados de migração
- Verificação de dependências cruzadas

---

## 📊 CRONOGRAMA ESTIMADO

| Fase | Tempo Estimado | Risco |
|------|----------------|-------|
| Backup | 30 min | Baixo |
| Limpeza | 15 min | Baixo |
| Nova Estrutura | 2 horas | Médio |
| Aplicação | 1 hora | Alto |
| Validação | 30 min | Baixo |
| **TOTAL** | **4 horas** | **Médio** |

---

## ⚠️ RISCOS E MITIGAÇÕES

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Perda de dados | Baixa | Alto | Backup completo + validação |
| Falha na migração | Média | Alto | Rollback automático |
| Downtime prolongado | Baixa | Médio | Ambiente de teste |
| Inconsistências | Baixa | Médio | Scripts de validação |

---

## 🎯 RECOMENDAÇÃO FINAL

**EXECUTAR OPÇÃO 1 (Reset Completo)** pelos seguintes motivos:

1. **Solução definitiva** - Elimina todos os problemas atuais
2. **Manutenibilidade** - Estrutura limpa para o futuro
3. **Tempo de execução** - 4 horas vs semanas de correções incrementais
4. **Confiabilidade** - Menor chance de problemas futuros

**Próximo passo:** Confirmar a abordagem e executar o backup inicial.