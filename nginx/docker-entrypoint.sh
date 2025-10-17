#!/bin/bash

# Função para configurar SSL
setup_ssl() {
    echo "Configurando SSL..."
    
    # Criar diretório SSL se não existir
    mkdir -p /etc/nginx/ssl
    
    # Gerar parâmetros DH se não existirem ou se for placeholder
    if [ ! -f /etc/nginx/ssl/dhparam.pem ] || [ "$(cat /etc/nginx/ssl/dhparam.pem 2>/dev/null)" = "placeholder" ]; then
        echo "Gerando parâmetros DH..."
        openssl dhparam -out /etc/nginx/ssl/dhparam.pem 2048
    fi
    
    # Tentar localizar certificados Let's Encrypt (considerando sufixos -0001, -0002, etc.)
    CERT_DIR="/etc/letsencrypt/live/${DOMAIN}"
    if [ ! -f "$CERT_DIR/fullchain.pem" ] || [ ! -f "$CERT_DIR/privkey.pem" ]; then
        ALT_DIR=$(ls -d /etc/letsencrypt/live/${DOMAIN}-* 2>/dev/null | sort -V | tail -n 1)
        if [ -n "$ALT_DIR" ] && [ -f "$ALT_DIR/fullchain.pem" ] && [ -f "$ALT_DIR/privkey.pem" ]; then
            echo "Certificados encontrados em lineage alternativa: $ALT_DIR"
            CERT_DIR="$ALT_DIR"
        fi
    fi

    # Linkar certificados se encontrados; caso contrário, gerar autoassinado
    if [ -f "$CERT_DIR/fullchain.pem" ] && [ -f "$CERT_DIR/privkey.pem" ]; then
        echo "Certificados Let's Encrypt encontrados em $CERT_DIR. Criando links simbólicos..."
        ln -sf "$CERT_DIR/fullchain.pem" /etc/nginx/ssl/fullchain.pem
        ln -sf "$CERT_DIR/privkey.pem" /etc/nginx/ssl/privkey.pem
        if [ -f "$CERT_DIR/chain.pem" ]; then
            ln -sf "$CERT_DIR/chain.pem" /etc/nginx/ssl/chain.pem
        else
            # Caso 'chain.pem' não exista, usar o próprio fullchain como chain
            cp /etc/nginx/ssl/fullchain.pem /etc/nginx/ssl/chain.pem
        fi
    else
        echo "Certificados Let's Encrypt não encontrados. Gerando certificados auto-assinados temporários..."
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout /etc/nginx/ssl/privkey.pem \
            -out /etc/nginx/ssl/fullchain.pem \
            -subj "/C=BR/ST=State/L=City/O=Organization/CN=${DOMAIN:-localhost}"
        cp /etc/nginx/ssl/fullchain.pem /etc/nginx/ssl/chain.pem
    fi
}

# Verificar se a variável DOMAIN está definida
if [ -z "$DOMAIN" ]; then
    echo "AVISO: Variável DOMAIN não definida! Usando 'localhost' como padrão."
    export DOMAIN="localhost"
fi

# Determinar qual configuração usar
if [ "$ENVIRONMENT" = "production" ]; then
    echo "Usando configuração de produção..."
    CONFIG_FILE="/etc/nginx/nginx.prod.conf"
    setup_ssl
    # Substituir variáveis de ambiente no template (DOMAIN)
    echo "Gerando nginx.conf com DOMAIN=$DOMAIN via envsubst..."
    envsubst '${DOMAIN}' < "$CONFIG_FILE" > /etc/nginx/nginx.conf
else
    echo "Usando configuração de desenvolvimento..."
    CONFIG_FILE="/etc/nginx/nginx.dev.conf"
    # Copiar configuração de desenvolvimento diretamente
    cp "$CONFIG_FILE" /etc/nginx/nginx.conf
fi

# Aguardar serviços dependentes estarem disponíveis (apenas em produção)
if [ "$ENVIRONMENT" = "production" ]; then
    echo "Aguardando serviços dependentes..."
    
    # Aguardar user_service
    until nc -z crm_user_service 8000 2>/dev/null; do
        echo "Aguardando user_service..."
        sleep 2
    done
    
    # Aguardar budget_service  
    until nc -z crm_budget_service 8002 2>/dev/null; do
        echo "Aguardando budget_service..."
        sleep 2
    done
    
    # Tentar aguardar frontend (opcional)
    timeout 30 bash -c 'until nc -z crm_frontend 80 2>/dev/null; do echo "Aguardando frontend..."; sleep 2; done' || echo "Frontend não disponível, continuando..."
fi

# Testar configuração do nginx
echo "Testando configuração do nginx..."
nginx -t

if [ $? -eq 0 ]; then
    echo "Configuração válida. Iniciando nginx..."
    exec nginx -g "daemon off;"
else
    echo "ERRO: Configuração do nginx inválida!"
    exit 1
fi