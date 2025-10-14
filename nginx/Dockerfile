FROM nginx:alpine

# Instalar dependências necessárias
RUN apk add --no-cache openssl bash netcat-openbsd

# Copiar arquivos de configuração
COPY nginx.prod.conf /etc/nginx/nginx.prod.conf
COPY nginx.dev.conf /etc/nginx/nginx.dev.conf

# Copiar e configurar o script de entrada
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Criar diretórios necessários
RUN mkdir -p /etc/nginx/ssl /var/log/nginx

EXPOSE 80 443

ENTRYPOINT ["/docker-entrypoint.sh"]