# Configurações do Nginx - CRM Ditual

Este diretório contém as configurações do Nginx para diferentes ambientes.

## Arquivos de Configuração

### `nginx.dev.conf`
- **Uso**: Ambiente de desenvolvimento
- **Características**:
  - CORS permissivo (`*`)
  - Logs em modo debug
  - Nomes de serviços simples (`user_service`, `budget_service`)
  - Usado pelo `docker-compose.yml`

### `nginx.prod.conf`
- **Uso**: Ambiente de produção
- **Características**:
  - CORS restritivo baseado em origem
  - Rate limiting
  - Security headers
  - Compressão gzip
  - Nomes de serviços com prefixo (`crm_user_service`, `crm_budget_service`)
  - Suporte a SSL/HTTPS
  - Usado como template pelo `docker-compose.prod.yml`

### `docker-entrypoint.sh`
Script de inicialização que:
- Substitui variáveis de ambiente no template
- Valida a configuração
- Remove configurações conflitantes
- Inicia o Nginx

### `Dockerfile`
Constrói a imagem do Nginx para produção usando:
- Base: `nginx:alpine`
- Template: `nginx.prod.conf`
- Entrypoint: `docker-entrypoint.sh`

## Variáveis de Ambiente

### Produção
- `DOMAIN`: Domínio principal da aplicação (ex: `loen.digital`)

## Estrutura de Diretórios

```
nginx/
├── Dockerfile              # Build da imagem para produção
├── docker-entrypoint.sh    # Script de inicialização
├── nginx.dev.conf          # Configuração para desenvolvimento
├── nginx.prod.conf         # Template para produção
├── ssl/                    # Certificados SSL (produção)
└── README.md              # Esta documentação
```

## Como Usar

### Desenvolvimento
```bash
docker-compose up
```

### Produção
```bash
docker-compose -f docker-compose.prod.yml up
```

## Troubleshooting

### Nginx não inicia
1. Verifique se a variável `DOMAIN` está definida
2. Verifique os logs: `docker logs crm_nginx`
3. Teste a configuração: `docker exec crm_nginx nginx -t`

### Problemas de CORS
- **Desenvolvimento**: CORS está aberto para todos os domínios
- **Produção**: CORS está restrito ao domínio configurado