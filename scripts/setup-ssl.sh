#!/bin/bash

# Script para configurar SSL com Let's Encrypt
# Uso: ./setup-ssl.sh seu-dominio.com

set -e

DOMAIN=$1
EMAIL=${2:-"admin@${DOMAIN}"}

if [ -z "$DOMAIN" ]; then
    echo "Uso: $0 <dominio> [email]"
    echo "Exemplo: $0 loen.digital admin@loen.digital"
    exit 1
fi

echo "Configurando SSL para o domínio: $DOMAIN"
echo "Email para notificações: $EMAIL"

# Verifica se o certbot está instalado
if ! command -v certbot &> /dev/null; then
    echo "Instalando certbot..."
    
    # Para Ubuntu/Debian
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y certbot python3-certbot-nginx
    # Para CentOS/RHEL
    elif command -v yum &> /dev/null; then
        sudo yum install -y certbot python3-certbot-nginx
    # Para Amazon Linux
    elif command -v amazon-linux-extras &> /dev/null; then
        sudo amazon-linux-extras install -y epel
        sudo yum install -y certbot python3-certbot-nginx
    else
        echo "Sistema operacional não suportado. Instale o certbot manualmente."
        exit 1
    fi
fi

# Para o nginx se estiver rodando
echo "Parando nginx temporariamente..."
sudo docker stop crm_nginx 2>/dev/null || true

# Gera certificado Let's Encrypt
echo "Gerando certificado Let's Encrypt..."
sudo certbot certonly \
    --standalone \
    --email "$EMAIL" \
    --agree-tos \
    --no-eff-email \
    --domains "$DOMAIN" \
    --non-interactive

# Verifica se o certificado foi criado
if [ -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]; then
    echo "Certificado SSL criado com sucesso!"
    
    # Configura renovação automática
    echo "Configurando renovação automática..."
    
    # Cria script de renovação
    sudo tee /etc/cron.d/certbot-renew > /dev/null <<EOF
# Renova certificados Let's Encrypt automaticamente
0 12 * * * root certbot renew --quiet --deploy-hook "docker restart crm_nginx"
EOF
    
    echo "Renovação automática configurada."
    
    # Reinicia o nginx
    echo "Reiniciando nginx..."
    sudo docker start crm_nginx
    
    echo ""
    echo "✅ SSL configurado com sucesso!"
    echo "Seu site agora está disponível em: https://$DOMAIN"
    echo ""
    echo "Para verificar o status do certificado:"
    echo "sudo certbot certificates"
    echo ""
    echo "Para renovar manualmente:"
    echo "sudo certbot renew"
    
else
    echo "❌ Erro ao gerar certificado SSL"
    exit 1
fi