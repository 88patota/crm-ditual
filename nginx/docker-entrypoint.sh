#!/bin/sh

# Substituir variáveis de ambiente no template
envsubst '${DOMAIN}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

# Remover arquivos de configuração padrão que podem causar conflito
rm -f /etc/nginx/conf.d/default.conf

# Executar nginx
exec "$@"