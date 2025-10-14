# Configuração de Variáveis de Ambiente na AWS - CRM Ditual

## Problema Identificado

O arquivo `nginx.prod.conf` utiliza a variável `${DOMAIN}` que não estava sendo encontrada durante o deploy na AWS. Isso acontece porque o Nginx precisa que as variáveis de ambiente sejam passadas explicitamente para o container.

## Solução Implementada

### 1. Variável DOMAIN Adicionada ao .env.prod

```bash
# Domain Configuration
DOMAIN=loen.digital
```

### 2. Configuração do Docker Compose

O serviço nginx no `docker-compose.prod.yml` agora inclui:

```yaml
nginx:
  image: nginx:alpine
  container_name: crm_nginx
  environment:
    - DOMAIN=${DOMAIN}  # ← Variável passada para o container
  volumes:
    - ./nginx/nginx.prod.conf:/etc/nginx/nginx.conf
```

## Configuração na AWS

### Opção 1: EC2 com Docker Compose

1. **Configurar variáveis no servidor EC2:**
```bash
# Editar o arquivo .env.prod no servidor
sudo nano /caminho/para/projeto/.env.prod

# Adicionar/modificar:
DOMAIN=seu-dominio.com
```

2. **Deploy com as variáveis:**
```bash
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

### Opção 2: ECS (Elastic Container Service)

1. **Definir variáveis no Task Definition:**
```json
{
  "containerDefinitions": [
    {
      "name": "nginx",
      "environment": [
        {
          "name": "DOMAIN",
          "value": "seu-dominio.com"
        }
      ]
    }
  ]
}
```

2. **Ou usar AWS Systems Manager Parameter Store:**
```json
{
  "secrets": [
    {
      "name": "DOMAIN",
      "valueFrom": "/crm-ditual/domain"
    }
  ]
}
```

### Opção 3: EKS (Kubernetes)

1. **Criar ConfigMap:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: crm-config
data:
  DOMAIN: "seu-dominio.com"
```

2. **Usar no Deployment:**
```yaml
spec:
  containers:
  - name: nginx
    envFrom:
    - configMapRef:
        name: crm-config
```

## Verificação

Para verificar se as variáveis estão sendo carregadas corretamente:

```bash
# Verificar variáveis no container nginx
docker exec crm_nginx env | grep DOMAIN

# Verificar configuração do nginx
docker exec crm_nginx nginx -T | grep server_name
```

## Variáveis Necessárias

### Obrigatórias para o Nginx:
- `DOMAIN` - Domínio principal do sistema

### Outras variáveis importantes:
- `POSTGRES_PASSWORD` - Senha do banco de dados
- `REDIS_PASSWORD` - Senha do Redis
- `SECRET_KEY` - Chave secreta JWT
- `ALLOWED_ORIGINS` - Domínios permitidos para CORS

## Segurança na AWS

### AWS Secrets Manager (Recomendado para produção)

1. **Criar secret:**
```bash
aws secretsmanager create-secret \
  --name "crm-ditual/env" \
  --description "CRM Ditual environment variables" \
  --secret-string file://secrets.json
```

2. **Usar no ECS:**
```json
{
  "secrets": [
    {
      "name": "DOMAIN",
      "valueFrom": "arn:aws:secretsmanager:region:account:secret:crm-ditual/env:DOMAIN::"
    }
  ]
}
```

## Troubleshooting

### Problema: Nginx não encontra a variável DOMAIN

**Sintomas:**
- Erro 502 Bad Gateway
- Logs do nginx mostram erro de configuração

**Solução:**
1. Verificar se a variável está no .env.prod
2. Confirmar que está sendo passada no docker-compose.prod.yml
3. Reiniciar o container nginx

### Problema: Certificado SSL não funciona

**Sintomas:**
- Erro de certificado no navegador
- Conexão não segura

**Solução:**
1. Verificar se o domínio está correto
2. Confirmar que os certificados SSL estão no diretório correto
3. Usar Let's Encrypt para certificados gratuitos

## Comandos Úteis

```bash
# Verificar logs do nginx
docker logs crm_nginx

# Recarregar configuração do nginx
docker exec crm_nginx nginx -s reload

# Testar configuração do nginx
docker exec crm_nginx nginx -t

# Verificar todas as variáveis de ambiente
docker exec crm_nginx env
```