# 🚀 Guia de Deploy - CRM System

Este guia apresenta diferentes opções para hospedar e configurar a aplicação CRM em produção.

## 📋 Índice
- [Opções de Hospedagem](#opções-de-hospedagem)
- [Deploy em VPS/Servidor Linux](#deploy-em-vpsservidor-linux)
- [Deploy com Docker Swarm](#deploy-com-docker-swarm)
- [Deploy na AWS](#deploy-na-aws)
- [Deploy no DigitalOcean](#deploy-no-digitalocean)
- [Configurações de Produção](#configurações-de-produção)
- [SSL/HTTPS](#sslhttps)
- [Monitoramento](#monitoramento)

## 🎯 Opções de Hospedagem

### 1. **VPS/Servidor Dedicado** (Recomendado)
- **Custo**: $5-20/mês
- **Controle total**: ✅
- **Escalabilidade**: ✅
- **Exemplos**: DigitalOcean Droplets, AWS EC2, Vultr, Linode

### 2. **Cloud Containers**
- **Custo**: $10-50/mês
- **Managed**: ✅
- **Auto-scaling**: ✅
- **Exemplos**: AWS ECS, Google Cloud Run, Azure Container Instances

### 3. **Platform as a Service**
- **Custo**: $7-25/mês
- **Deploy simples**: ✅
- **Menos controle**: ❌
- **Exemplos**: Heroku, Railway, Render

---

## 🐧 Deploy em VPS/Servidor Linux

### Pré-requisitos
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y docker.io docker-compose-plugin nginx certbot python3-certbot-nginx

# CentOS/RHEL
sudo yum install -y docker docker-compose nginx certbot python3-certbot-nginx
```

### 1. Configuração do Servidor

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/crm-ditual.git
cd crm-ditual

# Criar diretórios necessários
sudo mkdir -p /var/log/crm
sudo mkdir -p /var/backups/crm

# Dar permissões
sudo chown -R $USER:$USER /var/log/crm
sudo chown -R $USER:$USER /var/backups/crm
```

### 2. Configurar Variáveis de Ambiente

```bash
# Criar arquivo de produção
cp docker-compose.yml docker-compose.prod.yml
```

### 3. Docker Compose para Produção

```yaml
# docker-compose.prod.yml
services:
  postgres:
    image: postgres:14
    container_name: crm_postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: crm_db
      POSTGRES_USER: crm_user
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-strong_password_here}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - /var/backups/crm:/backups
    networks:
      - crm_network
    # Remove porta pública em produção
    
  redis:
    image: redis:7-alpine
    container_name: crm_redis
    restart: unless-stopped
    command: redis-server --requirepass ${REDIS_PASSWORD:-redis_strong_password}
    volumes:
      - redis_data:/data
    networks:
      - crm_network
    
  user_service:
    build: ./services/user_service
    container_name: crm_user_service
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgresql+asyncpg://crm_user:${POSTGRES_PASSWORD}@postgres:5432/crm_db
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379
      - ENVIRONMENT=production
      - SECRET_KEY=${SECRET_KEY}
      - ACCESS_TOKEN_EXPIRE_MINUTES=30
    depends_on:
      - postgres
      - redis
    networks:
      - crm_network
    
  budget_service:
    build: ./services/budget_service
    container_name: crm_budget_service
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgresql+asyncpg://crm_user:${POSTGRES_PASSWORD}@postgres:5432/crm_db
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379
      - ENVIRONMENT=production
    depends_on:
      - postgres
      - redis
    networks:
      - crm_network
    
  frontend:
    build: ./frontend
    container_name: crm_frontend
    restart: unless-stopped
    depends_on:
      - user_service
      - budget_service
    networks:
      - crm_network
    
  nginx:
    image: nginx:alpine
    container_name: crm_nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - /var/log/crm:/var/log/nginx
    depends_on:
      - frontend
      - user_service
      - budget_service
    networks:
      - crm_network

volumes:
  postgres_data:
  redis_data:

networks:
  crm_network:
    driver: bridge
```

### 4. Arquivo .env para Produção

```bash
# .env.prod
POSTGRES_PASSWORD=sua_senha_super_forte_postgres
REDIS_PASSWORD=sua_senha_super_forte_redis
SECRET_KEY=sua_chave_secreta_jwt_muito_longa_e_segura
DOMAIN=seu-dominio.com
EMAIL=seu-email@dominio.com
```

---

## 🌊 Deploy com Docker Swarm

```bash
# Inicializar swarm
docker swarm init

# Deploy
docker stack deploy -c docker-compose.prod.yml crm

# Verificar status
docker stack services crm
```

---

## ☁️ Deploy na AWS

### Usando EC2 + RDS + ElastiCache

```bash
# 1. Criar instância EC2 (t3.medium recomendado)
# 2. Criar RDS PostgreSQL
# 3. Criar ElastiCache Redis
# 4. Configurar Security Groups
# 5. Deploy da aplicação
```

### docker-compose.aws.yml
```yaml
services:
  user_service:
    environment:
      - DATABASE_URL=postgresql+asyncpg://usuario:senha@rds-endpoint:5432/crm_db
      - REDIS_URL=redis://elasticache-endpoint:6379
  
  budget_service:
    environment:
      - DATABASE_URL=postgresql+asyncpg://usuario:senha@rds-endpoint:5432/crm_db
      - REDIS_URL=redis://elasticache-endpoint:6379
```

---

## 🌊 Deploy no DigitalOcean

### Usando App Platform
```yaml
# .do/app.yaml
name: crm-system
services:
- name: frontend
  source_dir: frontend
  build_command: npm run build
  run_command: serve -s dist
- name: user-service
  source_dir: services/user_service
  build_command: pip install -r requirements.txt
  run_command: uvicorn app.main:app --host 0.0.0.0
databases:
- name: postgres
  engine: PG
- name: redis
  engine: REDIS
```

---

## ⚙️ Configurações de Produção

### 1. Criar Nginx Reverso Proxy

```bash
mkdir nginx
```

```nginx
# nginx/nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream frontend {
        server crm_frontend:80;
    }
    
    upstream api {
        server crm_user_service:8000;
        server crm_budget_service:8002;
    }
    
    server {
        listen 80;
        server_name seu-dominio.com;
        
        # Redirecionar para HTTPS
        return 301 https://$server_name$request_uri;
    }
    
    server {
        listen 443 ssl http2;
        server_name seu-dominio.com;
        
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        
        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        
        # API
        location /api {
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

### 2. Script de Deploy Automatizado

```bash
# deploy.sh
#!/bin/bash

# Criar script de deploy
```

---

## 🔒 SSL/HTTPS

### Usando Let's Encrypt (Gratuito)

```bash
# Instalar certificado SSL
sudo certbot --nginx -d seu-dominio.com

# Auto-renovação
sudo crontab -e
# Adicionar: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Usando certificado próprio

```bash
# Copiar certificados
sudo mkdir -p nginx/ssl
sudo cp seu-certificado.crt nginx/ssl/cert.pem
sudo cp sua-chave-privada.key nginx/ssl/key.pem
```

---

## 📊 Monitoramento

### 1. Logs Centralizados

```yaml
# docker-compose.monitoring.yml
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.14.0
  
  logstash:
    image: docker.elastic.co/logstash/logstash:7.14.0
  
  kibana:
    image: docker.elastic.co/kibana/kibana:7.14.0
```

### 2. Health Checks

```bash
# Criar script de health check
#!/bin/bash
curl -f http://localhost:3000/health || exit 1
curl -f http://localhost:8001/health || exit 1
curl -f http://localhost:8002/health || exit 1
```

---

## 🚀 Scripts Úteis

### Backup Automático
```bash
#!/bin/bash
# backup.sh
docker exec crm_postgres pg_dump -U crm_user crm_db > /var/backups/crm/backup-$(date +%Y%m%d).sql
```

### Atualização da Aplicação
```bash
#!/bin/bash
# update.sh
git pull origin main
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

---

## 💰 Estimativa de Custos Mensais

| Opção | Custo | Recursos | Adequado para |
|-------|-------|----------|---------------|
| DigitalOcean Droplet | $5-12 | 1-2GB RAM | Pequenas empresas |
| AWS EC2 t3.small | $15-25 | 2GB RAM | Médias empresas |
| VPS Dedicado | $20-50 | 4-8GB RAM | Grandes empresas |

---

## 🎯 Próximos Passos

1. **Escolher opção de hospedagem**
2. **Configurar domínio**
3. **Configurar SSL**
4. **Configurar backups**
5. **Configurar monitoramento**
6. **Testar em produção**

## 📞 Suporte

Para dúvidas sobre o deploy, consulte a documentação específica de cada provedor ou entre em contato com a equipe técnica.
