# 🔐 Criação de Usuário Admin - CRM Ditual

Este documento explica como criar o usuário administrador no sistema CRM Ditual rodando em ambiente EC2 com Docker.

## 📋 Pré-requisitos

- ✅ Sistema rodando em EC2 com Docker
- ✅ Containers do CRM Ditual em execução
- ✅ Acesso SSH à instância EC2
- ✅ Docker e docker-compose instalados

## 🚀 Métodos de Execução

### Método 1: Script Automatizado (Recomendado)

O método mais simples é usar o script bash que automatiza todo o processo:

```bash
# 1. Conectar na EC2 via SSH
ssh -i sua-chave.pem ec2-user@seu-ip-ec2

# 2. Navegar para o diretório do projeto
cd /caminho/para/crm-ditual

# 3. Executar o script automatizado
./scripts/create_admin_ec2.sh
```

### Método 2: Execução Manual via Docker

Se preferir executar manualmente:

```bash
# 1. Verificar se os containers estão rodando
docker-compose -f docker-compose.prod.yml ps

# 2. Executar o script Python dentro do container
docker-compose -f docker-compose.prod.yml exec user_service python create_admin_user.py
```

### Método 3: Execução Direta (Se não estiver usando Docker)

Se o sistema estiver rodando diretamente no EC2 sem Docker:

```bash
# 1. Navegar para o diretório do user_service
cd services/user_service

# 2. Executar o script Python
python create_admin_user.py
```

## 🔧 Troubleshooting

### Problema: "Container não está rodando"

```bash
# Verificar status dos containers
docker-compose -f docker-compose.prod.yml ps

# Iniciar os containers se necessário
docker-compose -f docker-compose.prod.yml up -d

# Aguardar containers ficarem prontos
docker-compose -f docker-compose.prod.yml logs -f
```

### Problema: "Erro de conexão com banco"

```bash
# Verificar logs do PostgreSQL
docker-compose -f docker-compose.prod.yml logs postgres

# Verificar se o banco está respondendo
docker-compose -f docker-compose.prod.yml exec postgres pg_isready -U crm_user -d crm_ditual
```

### Problema: "Usuário já existe"

Se o usuário admin já existir, o script informará e não criará duplicata. Para redefinir:

```bash
# Conectar ao banco e deletar o usuário existente
docker-compose -f docker-compose.prod.yml exec postgres psql -U crm_user -d crm_ditual -c "DELETE FROM users WHERE username = 'admin';"

# Executar o script novamente
./scripts/create_admin_ec2.sh
```

### Problema: "Módulo não encontrado"

```bash
# Verificar se está executando dentro do container correto
docker-compose -f docker-compose.prod.yml exec user_service ls -la

# Verificar se o arquivo existe
docker-compose -f docker-compose.prod.yml exec user_service ls -la create_admin_user.py
```

## 📊 Verificação do Sucesso

Após executar o script, você deve ver uma saída similar a:

```
🎉 USUÁRIO ADMIN CRIADO COM SUCESSO!
==================================================
👤 Username: admin
📧 Email: admin@crmditual.com
🏷️  Nome: Administrador do Sistema
🔑 Role: admin
🆔 ID: 1
📅 Criado em: 2024-01-15 10:30:00
==================================================
🔐 CREDENCIAIS DE ACESSO:
   Username: admin
   Password: admin102030
==================================================
```

## 🌐 Testando o Login

Após criar o usuário, teste o login:

1. **Via Frontend**: Acesse a URL do seu sistema e faça login com:
   - Username: `admin`
   - Password: `admin102030`

2. **Via API**: Teste o endpoint de login:
   ```bash
   curl -X POST "http://seu-ip-ec2/api/v1/users/login" \
        -H "Content-Type: application/json" \
        -d '{"username": "admin", "password": "admin102030"}'
   ```

## 🔒 Segurança

⚠️ **IMPORTANTE**: Após criar o usuário admin:

1. **Altere a senha padrão** imediatamente após o primeiro login
2. **Use uma senha forte** com pelo menos 12 caracteres
3. **Configure 2FA** se disponível no sistema
4. **Monitore os logs** de acesso do usuário admin

## 📁 Arquivos Criados

Este processo cria os seguintes arquivos:

- `services/user_service/create_admin_user.py` - Script Python principal
- `scripts/create_admin_ec2.sh` - Script bash para EC2
- `CREATE_ADMIN_README.md` - Esta documentação

## 🆘 Suporte

Se encontrar problemas:

1. Verifique os logs dos containers
2. Confirme que todos os serviços estão rodando
3. Verifique as variáveis de ambiente
4. Consulte a documentação do projeto

---

**✨ Criado para CRM Ditual - Sistema de Gestão Comercial**