# CRM - Sistema de Microserviços

Sistema de CRM desenvolvido com arquitetura de microserviços usando Python, FastAPI, PostgreSQL e Redis.

## 🏗️ Arquitetura

O projeto segue a arquitetura de microserviços com os seguintes componentes:

### Serviços
- **User Service**: Gerenciamento de usuários e autenticação
- **Shared**: Bibliotecas compartilhadas entre serviços

### Infraestrutura
- **PostgreSQL**: Banco de dados principal
- **Redis**: Cache e sistema de mensageria
- **Docker**: Containerização dos serviços

## 🚀 Setup Rápido

### Pré-requisitos
- Python 3.11+
- Docker & Docker Compose
- Make (opcional)

### Configuração Inicial

```bash
# Usando Make (recomendado)
make setup

# Ou manualmente
./scripts/setup_dev.sh
```

### Iniciar Ambiente de Desenvolvimento

```bash
# Usando Make
make dev

# Ou manualmente
./scripts/run_dev.sh
```

## 📚 Serviços Disponíveis

### User Service (Porto 8001)
Responsável pelo gerenciamento de usuários e autenticação.

**Funcionalidades:**
- ✅ Criação de usuários
- ✅ Autenticação com JWT
- ✅ Perfis de usuário (Admin, Vendas)
- ✅ CRUD completo de usuários
- ✅ Sistema de eventos via Redis

**Endpoints principais:**
- `POST /api/v1/users/` - Criar usuário
- `POST /api/v1/users/login` - Login
- `GET /api/v1/users/` - Listar usuários
- `GET /api/v1/users/{id}` - Obter usuário
- `PUT /api/v1/users/{id}` - Atualizar usuário
- `DELETE /api/v1/users/{id}` - Deletar usuário

## 🔗 URLs de Acesso

- **User Service**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## 🛠️ Comandos Úteis

```bash
# Parar serviços
make stop

# Ver logs
make logs

# Status dos serviços
make status

# Limpar ambiente
make clean

# Executar migrações
make migrate

# Criar nova migração
make migration

# Testes
make test

# Linting
make lint
```

## 📊 Estrutura do Projeto

```
crm-ditual/
├── services/
│   └── user_service/          # Serviço de usuários
│       ├── app/
│       │   ├── api/          # Rotas da API
│       │   ├── core/         # Configurações
│       │   ├── models/       # Modelos SQLAlchemy
│       │   ├── schemas/      # Schemas Pydantic
│       │   └── services/     # Lógica de negócio
│       ├── alembic/          # Migrações
│       ├── Dockerfile
│       └── requirements.txt
├── shared/                    # Código compartilhado
│   ├── database/             # Utilidades de banco
│   ├── messaging/            # Sistema de eventos
│   └── utils/                # Utilitários gerais
├── scripts/                  # Scripts de setup
├── docker-compose.yml
└── Makefile
```

## 🔐 Perfis de Usuário

O sistema suporta dois tipos de perfil:

- **Admin**: Acesso completo ao sistema
- **Vendas**: Acesso limitado a funcionalidades de vendas

## 🌐 Sistema de Eventos

O sistema utiliza Redis para comunicação entre microserviços através de eventos:

- `user.created` - Usuário criado
- `user.updated` - Usuário atualizado
- `user.deleted` - Usuário deletado
- `user.login` - Login realizado

## 🔄 Próximos Passos

### Serviços Planejados
- [ ] **Product Service**: Gerenciamento de produtos
- [ ] **Sales Service**: Gestão de vendas
- [ ] **Notification Service**: Envio de notificações
- [ ] **Analytics Service**: Relatórios e métricas

### Melhorias Técnicas
- [ ] Autenticação avançada (OAuth2, refresh tokens)
- [ ] Rate limiting
- [ ] Monitoramento (Prometheus, Grafana)
- [ ] Logs centralizados (ELK Stack)
- [ ] Testes automatizados
- [ ] CI/CD Pipeline

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Add nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.