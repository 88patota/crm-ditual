#!/bin/bash
set -e

# Função para substituir variáveis de ambiente no arquivo de configuração
envsubst_config() {
    local config_file="$1"
    local temp_file="/tmp/nginx_config_temp"
    
    # Substitui as variáveis de ambiente
    envsubst '${DOMAIN}' < "$config_file" > "$temp_file"
    
    # Move o arquivo temporário para o local correto
    mv "$temp_file" "$config_file"
}

# Função para configurar SSL
setup_ssl() {
    echo "Configurando SSL..."
    
    # Cria diretório SSL se não existir
    mkdir -p /etc/nginx/ssl
    
    # Gera DH parameters se não existir (apenas se não for um placeholder)
    if [ ! -f /etc/nginx/ssl/dhparam.pem ] || grep -q "Placeholder" /etc/nginx/ssl/dhparam.pem; then
        echo "Gerando DH parameters (isso pode demorar alguns minutos)..."
        openssl dhparam -out /etc/nginx/ssl/dhparam.pem 2048
        echo "DH parameters gerados com sucesso."
    fi
    
    # Verifica se os certificados Let's Encrypt existem
    if [ -f /etc/letsencrypt/live/${DOMAIN}/fullchain.pem ] && [ -f /etc/letsencrypt/live/${DOMAIN}/privkey.pem ]; then
        echo "Certificados Let's Encrypt encontrados. Criando links simbólicos..."
        ln -sf /etc/letsencrypt/live/${DOMAIN}/fullchain.pem /etc/nginx/ssl/fullchain.pem
        ln -sf /etc/letsencrypt/live/${DOMAIN}/privkey.pem /etc/nginx/ssl/privkey.pem
        ln -sf /etc/letsencrypt/live/${DOMAIN}/chain.pem /etc/nginx/ssl/chain.pem
    else
        echo "AVISO: Certificados Let's Encrypt não encontrados em /etc/letsencrypt/live/${DOMAIN}/"
        echo "Criando certificados auto-assinados temporários..."
        
        # Gera certificado auto-assinado temporário
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout /etc/nginx/ssl/privkey.pem \
            -out /etc/nginx/ssl/fullchain.pem \
            -subj "/C=BR/ST=State/L=City/O=Organization/CN=${DOMAIN}"
        
        # Cria chain.pem (mesmo que fullchain para certificados auto-assinados)
        cp /etc/nginx/ssl/fullchain.pem /etc/nginx/ssl/chain.pem
        
        echo "Certificados temporários criados. Configure Let's Encrypt para certificados válidos."
    fi
}

# Determina qual configuração usar baseado na variável ENVIRONMENT
if [ "${ENVIRONMENT:-production}" = "development" ]; then
    echo "Usando configuração de desenvolvimento..."
    cp /etc/nginx/nginx.dev.conf /etc/nginx/nginx.conf
else
    echo "Usando configuração de produção..."
    cp /etc/nginx/nginx.prod.conf /etc/nginx/nginx.conf
    
    # Substitui variáveis de ambiente apenas em produção
    if [ -n "${DOMAIN}" ]; then
        echo "Substituindo DOMAIN=${DOMAIN} na configuração..."
        envsubst_config /etc/nginx/nginx.conf
        
        # Configura SSL para produção
        setup_ssl
    else
        echo "AVISO: Variável DOMAIN não definida!"
    fi
fi

# Cria diretório de logs se não existir
mkdir -p /var/log/nginx

# Testa a configuração do nginx
echo "Testando configuração do nginx..."
nginx -t

if [ $? -eq 0 ]; then
    echo "Configuração do nginx válida. Iniciando servidor..."
    # Inicia o nginx em modo foreground
    exec nginx -g "daemon off;"
else
    echo "ERRO: Configuração do nginx inválida!"
    exit 1
fi