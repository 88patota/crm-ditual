#!/bin/sh

# Verificar se o template existe
if [ ! -f /etc/nginx/nginx.conf.template ]; then
    echo "ERRO: Template nginx.conf.template não encontrado!"
    exit 1
fi

# Verificar se a variável DOMAIN está definida
if [ -z "$DOMAIN" ]; then
    echo "AVISO: Variável DOMAIN não definida, usando localhost como padrão"
    export DOMAIN="localhost"
fi

# Substituir variáveis de ambiente no template
echo "Substituindo variáveis no template nginx..."
envsubst '${DOMAIN}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

# Verificar se a substituição foi bem-sucedida
if [ ! -f /etc/nginx/nginx.conf ]; then
    echo "ERRO: Falha ao gerar nginx.conf"
    exit 1
fi

# Remover arquivos de configuração padrão que podem causar conflito
rm -f /etc/nginx/conf.d/default.conf

# Testar a configuração do nginx
echo "Testando configuração do nginx..."
nginx -t

if [ $? -ne 0 ]; then
    echo "ERRO: Configuração do nginx inválida!"
    exit 1
fi

echo "Configuração do nginx válida. Iniciando servidor..."

# Executar nginx
exec "$@"