# Perfis de Usuários Demo - CRM Ditual

## 📋 Resumo

Foram criados perfis de usuários demo para facilitar o teste e demonstração do sistema CRM Ditual. Os perfis incluem diferentes níveis de acesso e permissões.

## 👥 Usuários Disponíveis

### 👑 Administrador
- **Usuário:** `admin`
- **Senha:** `admin123`
- **Nome:** Administrador Sistema
- **Email:** admin@crmditual.com
- **Permissões:**
  - ✅ Acesso completo ao sistema
  - ✅ Gerenciar usuários
  - ✅ Gerenciar orçamentos
  - ✅ Acessar todas as configurações
  - ✅ Visualizar relatórios completos
  - ✅ Exportar propostas PDF

### 👨‍💼 Vendedor 1 (João Silva)
- **Usuário:** `vendedor`
- **Senha:** `vendedor123`
- **Nome:** João Silva
- **Email:** vendedor@crmditual.com
- **Permissões:**
  - ✅ Criar e gerenciar orçamentos
  - ✅ Exportar propostas em PDF
  - ✅ Visualizar seus próprios orçamentos
  - ✅ Acessar calculadora de markup
  - ❌ Gerenciar outros usuários
  - ❌ Acessar configurações avançadas

### 👩‍💼 Vendedor 2 (Maria Santos)
- **Usuário:** `vendedor2`
- **Senha:** `vendedor123`
- **Nome:** Maria Santos
- **Email:** vendedor2@crmditual.com
- **Permissões:**
  - ✅ Criar e gerenciar orçamentos
  - ✅ Exportar propostas em PDF
  - ✅ Visualizar seus próprios orçamentos
  - ✅ Acessar calculadora de markup
  - ❌ Gerenciar outros usuários
  - ❌ Acessar configurações avançadas

## 🔐 Sistema de Autenticação

### Estrutura de Roles
- **admin:** Acesso total ao sistema
- **vendas:** Acesso limitado para funções de vendas

### Funcionalidades por Perfil

#### Administrador
- Gerenciamento completo de usuários
- Acesso a todos os orçamentos do sistema
- Configurações globais do sistema
- Relatórios e estatísticas completas
- Backup e manutenção

#### Vendedores
- Criação e edição de orçamentos
- Calculadora automática de markup
- Exportação de propostas em PDF (completa e simplificada)
- Visualização de histórico próprio
- Perfil pessoal

## 🖥️ Interface de Login

### Credenciais Demo na Tela de Login
A página de login (`AntLogin`) inclui botões de credenciais demo que preenchem automaticamente os campos:

1. **Administrador** (azul)
   - Descrição: "Acesso completo ao sistema - Gerenciar usuários, orçamentos e configurações"

2. **Vendedor (João)** (verde)
   - Descrição: "Perfil de vendas - Criar e gerenciar orçamentos, exportar propostas PDF"

3. **Vendedor (Maria)** (laranja)
   - Descrição: "Perfil de vendas - Criar e gerenciar orçamentos, exportar propostas PDF"

### Como Usar
1. Acesse a página de login
2. Clique em qualquer botão de credencial demo
3. Os campos serão preenchidos automaticamente
4. Clique em "Entrar" para acessar o sistema

## 📊 Funcionalidades Disponíveis por Perfil

### Todos os Usuários
- Login/Logout seguro
- Dashboard personalizado
- Perfil pessoal
- Notificações

### Vendedores
- **Orçamentos:**
  - Criar novos orçamentos
  - Formulário simplificado com cálculo automático
  - Editar orçamentos existentes
  - Visualizar histórico de orçamentos
  
- **Exportação PDF:**
  - Proposta completa (tabela detalhada)
  - Proposta simplificada (resumo para cliente)
  - Download automático
  - Nomenclatura padronizada

- **Calculadora de Markup:**
  - Cálculo automático baseado em custos
  - Sugestão de preços de venda
  - Análise de rentabilidade

### Administradores (Funcionalidades Extras)
- **Gestão de Usuários:**
  - Criar novos usuários
  - Editar perfis existentes
  - Ativar/desativar usuários
  - Gerenciar permissões

- **Configurações:**
  - Parâmetros de markup
  - Configurações de sistema
  - Backup e restauração

## 🔧 Configuração Técnica

### Backend (User Service)
- Autenticação JWT
- Hash de senhas com bcrypt
- Validação de roles
- Endpoints de login/registro

### Frontend
- Context de autenticação
- Proteção de rotas
- Redirecionamento baseado em role
- Interface de login responsiva

## 🚀 Próximos Passos

1. **Testes:** Validar todas as funcionalidades com cada perfil
2. **Produção:** Alterar senhas padrão antes do deploy
3. **Personalização:** Ajustar permissões conforme necessário
4. **Logs:** Implementar auditoria de ações dos usuários

## 📞 Suporte

Para dúvidas sobre os perfis de usuário ou funcionalidades:
- Consulte a documentação técnica
- Teste com as credenciais demo fornecidas
- Verifique logs de sistema para troubleshooting
