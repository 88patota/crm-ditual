# Guia de Deploy na AWS - CRM Ditual

## Problema Resolvido: SSL na AWS

A AWS não permite certificados SSL autoassinados em produção. Este guia apresenta **2 soluções simples** para gerenciar certificados SSL manualmente.

## 🚀 Soluções para SSL na AWS

### Opção 1: Let's Encrypt com Certbot - **RECOMENDADA**

Certificados SSL gratuitos e automáticos:

```bash
# 1. Instale certbot no servidor EC2
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# 2. Gere certificado para seu domínio
sudo certbot --nginx -d seu-dominio.com

# 3. Use a configuração normal
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

**Vantagens:**
- ✅ Certificado SSL gratuito
- ✅ Renovação automática (cron job)
- ✅ Reconhecido por todos os navegadores
- ✅ Simples de configurar

### Opção 2: Certificado SSL Comercial

```bash
# 1. Compre certificado SSL de uma CA (GoDaddy, Namecheap, etc.)
# 2. Faça upload dos arquivos para o servidor
# 3. Substitua os certificados no diretório nginx/ssl/
cp seu-certificado.crt nginx/ssl/cert.pem
cp sua-chave-privada.key nginx/ssl/key.pem

# 4. Use a configuração normal
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

**Vantagens:**
- ✅ Certificado profissional
- ✅ Suporte técnico da CA
- ✅ Certificados wildcard disponíveis
- ✅ Validação estendida (EV) disponível

## 📁 Arquivos Disponíveis

### `docker-compose.prod.yml`
- Configuração completa com SSL
- Nginx com HTTPS (porta 443)
- Certificados SSL no diretório `nginx/ssl/`

### `nginx/nginx.prod.conf`
- Configuração nginx com SSL
- Redirecionamento HTTP → HTTPS
- Headers de segurança configurados

### `nginx/ssl/`
- `cert.pem`: Certificado SSL (substitua pelo seu)
- `key.pem`: Chave privada (substitua pela sua)

## 🔧 Como Usar

### Para produção com Let's Encrypt:

```bash
# 1. Configure seu domínio apontando para o servidor
# 2. Instale certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# 3. Pare o nginx temporariamente
docker compose -f docker-compose.prod.yml stop nginx

# 4. Gere o certificado
sudo certbot certonly --standalone -d seu-dominio.com

# 5. Copie os certificados para o projeto
sudo cp /etc/letsencrypt/live/seu-dominio.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/seu-dominio.com/privkey.pem nginx/ssl/key.pem
sudo chown $USER:$USER nginx/ssl/*.pem

# 6. Inicie a aplicação
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

### Para certificado comercial:

```bash
# 1. Substitua os certificados
cp seu-certificado.crt nginx/ssl/cert.pem
cp sua-chave-privada.key nginx/ssl/key.pem

# 2. Inicie a aplicação
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

## 🔍 Verificações de Saúde

### Endpoints de Verificação:
- **Aplicação**: `https://seu-dominio.com` → Interface do CRM
- **User Service**: `https://seu-dominio.com/api/users/health` → `200`
- **Budget Service**: `https://seu-dominio.com/api/budgets/health` → `200`
- **PostgreSQL**: Health check interno do Docker
- **Redis**: Health check interno do Docker

### Monitoramento:
```bash
# Logs em tempo real
docker compose -f docker-compose.prod.yml logs -f

# Status dos containers
docker compose -f docker-compose.prod.yml ps

# Verificar SSL
curl -I https://seu-dominio.com
openssl s_client -connect seu-dominio.com:443 -servername seu-dominio.com
```

## 🚨 Troubleshooting

### Problema: "SSL certificate error"
**Causa**: Certificado inválido ou expirado
**Solução**: 
```bash
# Verificar certificado
openssl x509 -in nginx/ssl/cert.pem -text -noout

# Renovar Let's Encrypt
sudo certbot renew
sudo cp /etc/letsencrypt/live/seu-dominio.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/seu-dominio.com/privkey.pem nginx/ssl/key.pem
docker compose -f docker-compose.prod.yml restart nginx
```

### Problema: "host not found in upstream"
**Causa**: Nginx iniciando antes dos outros serviços
**Solução**: Use `docker compose up` (todos os serviços juntos)

### Problema: 502 Bad Gateway
**Causa**: Serviços backend não estão saudáveis
**Solução**: 
```bash
docker compose -f docker-compose.prod.yml logs user_service
docker compose -f docker-compose.prod.yml logs budget_service
```

## 🔄 Renovação Automática (Let's Encrypt)

### Configure cron job para renovação automática:

```bash
# Edite o crontab
sudo crontab -e

# Adicione esta linha (verifica renovação todo dia às 2h)
0 2 * * * /usr/bin/certbot renew --quiet && /usr/local/bin/docker-compose -f /caminho/para/seu/projeto/docker-compose.prod.yml restart nginx
```

### Script de renovação personalizado:

```bash
# Crie o script
sudo nano /usr/local/bin/renew-ssl.sh

#!/bin/bash
cd /caminho/para/seu/projeto
certbot renew --quiet
if [ $? -eq 0 ]; then
    cp /etc/letsencrypt/live/seu-dominio.com/fullchain.pem nginx/ssl/cert.pem
    cp /etc/letsencrypt/live/seu-dominio.com/privkey.pem nginx/ssl/key.pem
    docker compose -f docker-compose.prod.yml restart nginx
    echo "$(date): SSL certificate renewed successfully" >> /var/log/ssl-renewal.log
fi

# Torne executável
sudo chmod +x /usr/local/bin/renew-ssl.sh

# Adicione ao cron
0 2 * * * /usr/local/bin/renew-ssl.sh
```

## 💰 Estimativa de Custos

### Custos Mensais Estimados (AWS):

#### Opção 1: Let's Encrypt (Gratuito)
- **EC2 t3.micro**: ~$8.50/mês
- **EBS 20GB**: ~$2.00/mês
- **Transferência de dados**: ~$1.00/mês (1GB)
- **Total**: ~$11.50/mês

#### Opção 2: Certificado Comercial
- **EC2 t3.micro**: ~$8.50/mês
- **EBS 20GB**: ~$2.00/mês
- **Transferência de dados**: ~$1.00/mês
- **Certificado SSL**: $50-200/ano
- **Total**: ~$15.67-28.17/mês

### Comparação com outras soluções:
- **Heroku**: $25-50/mês (com SSL gratuito)
- **DigitalOcean**: $12-24/mês (com SSL gratuito)
- **Vercel/Netlify**: $0-20/mês (com SSL gratuito)

## 🔒 Configurações de Segurança

### Headers de Segurança (já configurados no nginx.prod.conf):
```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

### Configurações SSL Recomendadas:
```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers off;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
```

### Firewall AWS (Security Groups):
```
Inbound Rules:
- HTTP (80): 0.0.0.0/0
- HTTPS (443): 0.0.0.0/0
- SSH (22): Seu IP específico

Outbound Rules:
- All traffic: 0.0.0.0/0
```

## 📋 Checklist de Deploy

### Pré-Deploy:
- [ ] Domínio configurado e apontando para o servidor
- [ ] Certificado SSL obtido e copiado para `nginx/ssl/`
- [ ] Variáveis de ambiente configuradas em `.env.prod`
- [ ] Backup do banco de dados (se aplicável)
- [ ] Teste local da aplicação

### Deploy:
- [ ] Upload dos arquivos para o servidor
- [ ] Configuração das permissões dos certificados SSL
- [ ] Execução do `docker compose -f docker-compose.prod.yml up -d`
- [ ] Verificação dos logs dos containers
- [ ] Teste de conectividade HTTPS

### Pós-Deploy:
- [ ] Configuração da renovação automática do SSL
- [ ] Configuração de backups automáticos
- [ ] Monitoramento configurado
- [ ] Documentação atualizada
- [ ] Teste de todos os endpoints da aplicação

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs: `docker compose -f docker-compose.prod.yml logs`
2. Consulte a seção de troubleshooting acima
3. Verifique a configuração do SSL e certificados
4. Teste a conectividade dos serviços individualmente

**Última atualização**: $(date)
**Versão**: 2.0 - SSL Manual (sem Load Balancer)

---

**Próximos passos**: Configure o ALB na AWS e aponte para sua instância EC2 na porta 80.