# 🔐 Guia de Autenticação JWT - CRM

Sistema completo de autenticação JWT com controle de acesso baseado em roles (Admin/Vendas).

## 🚀 Recursos Implementados

### ✅ **Autenticação JWT**
- Tokens seguros com expiração configurável
- Verificação automática em endpoints protegidos
- Sistema de refresh token (implementável)

### ✅ **Controle de Acesso por Roles**
- **Admin**: Acesso completo a todos os recursos
- **Vendas**: Acesso limitado e auto-gestão

### ✅ **Endpoints Protegidos**
- Sistema de dependências do FastAPI
- Middleware de segurança automático
- Validação de permissões granular

## 📚 Endpoints Disponíveis

### 🔓 **Endpoints Públicos** (Sem autenticação)

#### Login
```bash
POST /api/v1/users/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123456"
}

# Resposta:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

#### Registro Público
```bash
POST /api/v1/users/register
Content-Type: application/json

{
  "email": "novo@crm.com",
  "username": "novousuario", 
  "full_name": "Novo Usuário",
  "password": "senha123456"
}
# Nota: Role é automaticamente definido como "vendas"
```

### 🔒 **Endpoints Protegidos** (Requer JWT)

#### Ver Perfil Próprio
```bash
GET /api/v1/users/me
Authorization: Bearer {seu_token}

# Resposta:
{
  "id": 1,
  "email": "admin@crm.com",
  "username": "admin",
  "full_name": "Administrador", 
  "role": "admin",
  "is_active": true,
  "created_at": "2025-08-05T02:37:57.920043Z",
  "updated_at": "2025-08-05T02:37:57.920043Z"
}
```

#### Atualizar Perfil Próprio
```bash
PUT /api/v1/users/me
Authorization: Bearer {seu_token}
Content-Type: application/json

{
  "email": "novo_email@crm.com",
  "full_name": "Nome Atualizado"
}
```

#### Alterar Senha
```bash
PUT /api/v1/users/me/password
Authorization: Bearer {seu_token}
Content-Type: application/json

{
  "current_password": "senha_atual",
  "new_password": "nova_senha123"
}
```

### 👑 **Endpoints Apenas Admin**

#### Listar Todos Usuários
```bash
GET /api/v1/users/
Authorization: Bearer {admin_token}
```

#### Criar Usuário
```bash
POST /api/v1/users/
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "email": "usuario@crm.com",
  "username": "usuario",
  "full_name": "Nome Usuário",
  "password": "senha123456",
  "role": "vendas"  # ou "admin"
}
```

#### Ver Qualquer Usuário
```bash
GET /api/v1/users/{user_id}
Authorization: Bearer {admin_token}
```

#### Atualizar Qualquer Usuário
```bash
PUT /api/v1/users/{user_id}
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "email": "novo@crm.com",
  "role": "admin",
  "is_active": false
}
```

#### Deletar Usuário
```bash
DELETE /api/v1/users/{user_id}
Authorization: Bearer {admin_token}
```

## 🛡️ Matriz de Permissões

| Ação | Admin | Vendas | Público |
|------|-------|--------|---------|
| Login | ✅ | ✅ | ✅ |
| Registro | ✅ | ✅ | ✅ |
| Ver próprio perfil | ✅ | ✅ | ❌ |
| Editar próprio perfil | ✅ | ✅ | ❌ |
| Alterar própria senha | ✅ | ✅ | ❌ |
| Listar usuários | ✅ | ❌ | ❌ |
| Ver outro usuário | ✅ | ❌ | ❌ |
| Criar usuário | ✅ | ❌ | ❌ |
| Editar outro usuário | ✅ | ❌ | ❌ |
| Deletar usuário | ✅ | ❌ | ❌ |

## 💻 Exemplos Práticos

### 1. Fluxo Completo - Admin

```bash
# 1. Login
TOKEN=$(curl -s -X POST "http://localhost:8001/api/v1/users/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123456"}' | jq -r '.access_token')

# 2. Ver próprio perfil
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8001/api/v1/users/me" | jq .

# 3. Listar todos usuários
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8001/api/v1/users/" | jq .

# 4. Criar novo usuário
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email": "novo@crm.com", "username": "novo", "full_name": "Novo User", "password": "senha123", "role": "vendas"}' \
  "http://localhost:8001/api/v1/users/" | jq .
```

### 2. Fluxo Completo - Vendas

```bash
# 1. Login como vendedor
VENDEDOR_TOKEN=$(curl -s -X POST "http://localhost:8001/api/v1/users/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "vendedor1", "password": "venda123456"}' | jq -r '.access_token')

# 2. Ver próprio perfil (✅ Permitido)
curl -H "Authorization: Bearer $VENDEDOR_TOKEN" \
  "http://localhost:8001/api/v1/users/me" | jq .

# 3. Tentar listar usuários (❌ Negado)
curl -H "Authorization: Bearer $VENDEDOR_TOKEN" \
  "http://localhost:8001/api/v1/users/" | jq .
# Resultado: {"detail": "Operação não permitida para este tipo de usuário"}

# 4. Atualizar próprio perfil (✅ Permitido)
curl -X PUT -H "Authorization: Bearer $VENDEDOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"full_name": "João Vendedor Atualizado"}' \
  "http://localhost:8001/api/v1/users/me" | jq .
```

### 3. Testando Segurança

```bash
# Tentar acessar sem token (❌ Negado)
curl "http://localhost:8001/api/v1/users/" | jq .
# Resultado: {"detail": "Not authenticated"}

# Tentar usar token inválido (❌ Negado)
curl -H "Authorization: Bearer token_invalido" \
  "http://localhost:8001/api/v1/users/me" | jq .
# Resultado: {"detail": "Não foi possível validar as credenciais"}
```

## 🔧 Configuração de Segurança

### JWT Settings
```python
# services/user_service/app/core/config.py
secret_key: str = "your-secret-key-change-in-production"
algorithm: str = "HS256"
access_token_expire_minutes: int = 30
```

### Headers de Autenticação
```bash
# Formato padrão
Authorization: Bearer {seu_token_jwt}

# Exemplo
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 🚨 Códigos de Erro

| Código | Descrição | Quando Ocorre |
|--------|-----------|---------------|
| `401` | Not authenticated | Token ausente/inválido |
| `403` | Forbidden | Sem permissão para ação |
| `404` | Not found | Usuário não existe |
| `400` | Bad request | Dados inválidos |

## 🎯 Respostas de Erro

```json
// Token inválido/ausente
{
  "detail": "Not authenticated"
}

// Sem permissão
{
  "detail": "Operação não permitida para este tipo de usuário"
}

// Credenciais inválidas no login
{
  "detail": "Credenciais inválidas"
}

// Token malformado
{
  "detail": "Não foi possível validar as credenciais"
}
```

## 📱 Integração Frontend

### JavaScript/Fetch
```javascript
// Login e obter token
const login = async (username, password) => {
  const response = await fetch('http://localhost:8001/api/v1/users/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password })
  });
  
  const data = await response.json();
  localStorage.setItem('token', data.access_token);
  return data;
};

// Fazer requisições autenticadas
const fetchWithAuth = async (url, options = {}) => {
  const token = localStorage.getItem('token');
  
  return fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${token}`
    }
  });
};

// Exemplo: Ver perfil
const getProfile = async () => {
  const response = await fetchWithAuth('http://localhost:8001/api/v1/users/me');
  return response.json();
};
```

### Python/Requests
```python
import requests

# Login
login_data = {
    "username": "admin",
    "password": "admin123456"
}

response = requests.post(
    "http://localhost:8001/api/v1/users/login",
    json=login_data
)

token = response.json()["access_token"]

# Requisições autenticadas
headers = {"Authorization": f"Bearer {token}"}

# Ver perfil
profile = requests.get(
    "http://localhost:8001/api/v1/users/me",
    headers=headers
).json()
```

## 🔄 Renovação de Token

O token JWT tem expiração configurável (padrão: 30 minutos). Para implementar renovação:

1. Detectar erro 401 no frontend
2. Redirecionar para login
3. Ou implementar refresh token (futuro)

## 🏗️ Arquitetura de Segurança

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────┐
│   Client App    │───▶│  JWT Token   │───▶│   FastAPI   │
└─────────────────┘    └──────────────┘    └─────────────┘
                               │                    │
                               ▼                    ▼
                    ┌──────────────┐    ┌─────────────┐
                    │ Token Valid? │    │ Check Role  │
                    └──────────────┘    └─────────────┘
                               │                    │
                               ▼                    ▼
                    ┌──────────────┐    ┌─────────────┐
                    │ Get User     │    │ Allow/Deny  │
                    └──────────────┘    └─────────────┘
```

## ✨ Próximas Melhorias

- [ ] Refresh tokens
- [ ] Rate limiting por usuário
- [ ] Audit log de ações
- [ ] Two-factor authentication (2FA)
- [ ] OAuth2 integração
- [ ] Session management
- [ ] Password policy enforcement

---

**🎉 Sistema JWT totalmente funcional e seguro!** 

Acesse a documentação interativa em: http://localhost:8001/docs