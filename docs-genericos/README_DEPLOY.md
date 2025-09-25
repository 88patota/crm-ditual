# 🚀 CRM System - Guia de Deploy Rápido

## 📋 Resumo Executivo

Este sistema CRM possui **deploy completo automatizado** com scripts prontos para produção. Escolha sua opção de hospedagem e siga os passos abaixo.

## ⚡ Deploy Rápido (5 minutos)

### 1. **Escolha sua Hospedagem**

| Opção | Custo/mês | Dificuldade | Recomendado para |
|-------|-----------|-------------|------------------|
| 🌊 **DigitalOcean Droplet** | $5-12 | ⭐⭐ | Pequenas empresas |
| ☁️ **AWS EC2** | $15-25 | ⭐⭐⭐ | Médias empresas |
| 🛡️ **VPS Dedicado** | $20-50 | ⭐⭐ | Grandes empresas |

### 2. **Configuração do Servidor**

```bash
# Ubuntu/Debian (recomendado)
sudo apt update
sudo apt install -y docker.io docker-compose-plugin nginx git

# Clonar o projeto
git clone https://github.com/seu-usuario/crm-ditual.git
cd crm-ditual
```

### 3. **Configurar Ambiente**

```bash
# Copiar template de configuração
cp .env.prod.template .env.prod

# Editar configurações (IMPORTANTE!)
nano .env.prod
```

**Variáveis obrigatórias no .env.prod:**
```bash
POSTGRES_PASSWORD=sua_senha_super_forte_123
REDIS_PASSWORD=sua_senha_redis_456
SECRET_KEY=sua_chave_jwt_muito_longa_e_aleatoria
DOMAIN=seu-dominio.com
EMAIL=seu-email@dominio.com
```

### 4. **Deploy Automático**

```bash
# Executar script de deploy (faz tudo automaticamente)
./deploy.sh
```

O script irá:
- ✅ Verificar pré-requisitos
- ✅ Configurar SSL (Let's Encrypt)
- ✅ Fazer backup do banco (se existir)
- ✅ Buildar e iniciar todos os serviços
- ✅ Executar health checks
- ✅ Configurar monitoramento automático

### 5. **Verificar Deploy**

```bash
# Monitorar sistema
./monitor.sh

# Ver logs
docker compose -f docker-compose.prod.yml logs -f
```

---

## 🌍 Opções de Hospedagem Detalhadas

### 🌊 DigitalOcean (Recomendado para iniciantes)

1. **Criar Droplet:**
   - Tamanho: Basic $5/mês (1GB RAM)
   - Imagem: Ubuntu 22.04 LTS
   - Datacenter: Mais próximo dos usuários

2. **Configurar DNS:**
   ```
   A     @       IP_DO_DROPLET
   A     www     IP_DO_DROPLET
   ```

3. **Deploy:**
   ```bash
   ssh root@seu-ip
   # Seguir passos de configuração acima
   ```

### ☁️ AWS EC2

1. **Criar instância:**
   - Tipo: t3.small (2 vCPU, 2GB RAM)
   - AMI: Ubuntu Server 22.04 LTS
   - Security Group: Portas 22, 80, 443

2. **RDS + ElastiCache (opcional):**
   ```bash
   # Para alta disponibilidade
   # Usar managed database e cache
   ```

### 🛡️ VPS Tradicional (Vultr, Linode, etc.)

1. **Especificações mínimas:**
   - CPU: 1-2 cores
   - RAM: 2GB
   - Storage: 20GB SSD
   - Banda: 1TB/mês

---

## 🔧 Scripts de Manutenção

### Deploy e Atualizações
```bash
# Deploy inicial completo
./deploy.sh

# Atualização rápida (sem downtime)
./update.sh

# Atualizar serviço específico
./update.sh --service frontend
```

### Monitoramento e Backup
```bash
# Status do sistema
./monitor.sh

# Backup manual
./backup.sh

# Logs em tempo real
docker compose -f docker-compose.prod.yml logs -f
```

### Comandos Úteis
```bash
# Parar tudo
docker compose -f docker-compose.prod.yml down

# Reiniciar serviço específico
docker compose -f docker-compose.prod.yml restart user_service

# Ver uso de recursos
docker stats

# Limpar sistema
docker system prune -af
```

---

## 🌐 URLs de Acesso

Após o deploy bem-sucedido:

- **Frontend:** https://seu-dominio.com
- **Health Check:** https://seu-dominio.com/health
- **API Base:** https://seu-dominio.com/api

---

## 🆘 Problemas Comuns

### 1. **Erro de SSL**
```bash
# Gerar certificados manualmente
sudo certbot --nginx -d seu-dominio.com
```

### 2. **Serviços não iniciam**
```bash
# Verificar logs
./monitor.sh
docker compose -f docker-compose.prod.yml logs

# Reiniciar tudo
docker compose -f docker-compose.prod.yml down
./deploy.sh
```

### 3. **Falta de memória**
```bash
# Verificar uso
free -h
docker stats

# Adicionar swap se necessário
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### 4. **Porta ocupada**
```bash
# Verificar portas em uso
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :443

# Parar nginx do sistema se necessário
sudo systemctl stop nginx
sudo systemctl disable nginx
```

---

## 📞 Suporte e Próximos Passos

### Após Deploy Bem-Sucedido:

1. **✅ Configurar backup automático** (já incluído no script)
2. **✅ Configurar monitoramento** (já incluído no script)
3. **🔄 Testar processo de atualização**
4. **📊 Configurar alertas** (opcional)
5. **🔒 Configurar firewall** (recomendado)

### Firewall Básico:
```bash
# Ubuntu UFW
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### Monitoramento Avançado (Opcional):
- **Uptime Kuma:** Para monitoramento de uptime
- **Grafana + Prometheus:** Para métricas detalhadas
- **ELK Stack:** Para análise de logs

---

## 💡 Dicas de Otimização

### Performance:
- Use SSD storage
- Configure Redis para cache
- Otimize imagens Docker
- Configure CDN para assets estáticos

### Segurança:
- Troque senhas padrão
- Configure backup regular
- Monitore logs de acesso
- Use certificados SSL

### Escalabilidade:
- Docker Swarm para múltiplos servidores
- Load balancer para alto tráfego
- Database read replicas
- Microservices separation

---

**🎉 Seu CRM está pronto para produção!**

Para dúvidas específicas, consulte o [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) completo ou entre em contato com a equipe técnica.
