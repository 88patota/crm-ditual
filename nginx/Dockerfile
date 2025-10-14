FROM nginx:alpine

# Instalar envsubst (já incluído no nginx:alpine)
# Copiar o template de configuração
COPY nginx.prod.conf /etc/nginx/nginx.conf.template

# Script para substituir variáveis e iniciar nginx
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

EXPOSE 80 443

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]