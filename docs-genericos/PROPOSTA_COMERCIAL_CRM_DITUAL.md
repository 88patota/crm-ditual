# 🚀 PROPOSTA COMERCIAL - CRM DITUAL
## Sistema Inteligente de Gestão Comercial

---

## 📋 RESUMO EXECUTIVO

O **CRM Ditual** é uma solução completa de gestão de relacionamento com clientes, desenvolvida com arquitetura de microserviços moderna e tecnologias de ponta. O sistema oferece funcionalidades avançadas de orçamentação, cálculos automáticos de rentabilidade, gestão de usuários e dashboards analíticos.

---

## 🎯 FUNCIONALIDADES DO SISTEMA

### 🔐 **Módulo de Autenticação e Usuários**
- **Login Seguro com JWT**: Autenticação baseada em tokens com expiração automática
- **Gestão de Perfis**: Sistema de roles (Admin/Vendas) com permissões granulares
- **Registro de Usuários**: Cadastro público para perfil de vendas
- **Gerenciamento Administrativo**: CRUD completo de usuários para administradores
- **Perfil Pessoal**: Edição de dados pessoais e alteração de senhas
- **Controle de Acesso**: Proteção de rotas baseada em roles e permissões

### 💰 **Módulo de Orçamentos**
- **Criação de Orçamentos**: Interface simplificada para criação rápida
- **Cálculos Automáticos**: 
  - Rentabilidade por item e total
  - Comissões automáticas (1,5% padrão)
  - ICMS de compra e venda
  - IPI com cálculos detalhados
  - Markup inteligente (20% a 200%)
- **Gestão de Status**: Draft, Pendente, Aprovado, Rejeitado, Expirado
- **Numeração Automática**: Sistema de numeração sequencial de pedidos
- **Tipos de Frete**: CIF/FOB com cálculos específicos
- **Condições de Pagamento**: Gestão flexível de prazos e condições
- **Exportação PDF**: Geração automática de propostas em PDF
- **Filtros Avançados**: Por cliente, status, período, vendedor

### 📊 **Dashboard Analítico**
- **Métricas em Tempo Real**: 
  - Total de orçamentos por período
  - Valor total negociado
  - Taxa de conversão
  - Orçamentos aprovados vs rejeitados
- **Gráficos Interativos**: Visualização de dados com Chart.js
- **Filtros Temporais**: Análise por períodos customizados
- **Estatísticas de Performance**: Acompanhamento de resultados

### 🧮 **Calculadora de Rentabilidade**
- **Cálculos Complexos**: 
  - Margem de lucro por item
  - Impacto de impostos (ICMS, IPI, PIS/COFINS)
  - Comissões por peso e valor
  - Outras despesas operacionais
- **Markup Automático**: Aplicação inteligente baseada em regras de negócio
- **Preview de Cálculos**: Visualização antes da confirmação
- **Validações**: Controle de margens mínimas e máximas

---

## 🛠️ STACK TECNOLÓGICO

### **Frontend**
- **React 18** - Framework principal
- **TypeScript** - Type safety e melhor experiência de desenvolvimento
- **Vite** - Build tool moderno e rápido
- **Tailwind CSS** - Framework CSS utility-first
- **Ant Design** - Biblioteca de componentes UI profissionais
- **TanStack Query** - Gerenciamento de estado do servidor
- **React Router v6** - Roteamento SPA
- **React Hook Form** - Formulários performáticos
- **Chart.js** - Gráficos e visualizações
- **Axios** - Cliente HTTP com interceptors

### **Backend**
- **FastAPI** - Framework Python moderno e rápido
- **Python 3.11+** - Linguagem principal
- **SQLAlchemy** - ORM assíncrono
- **Alembic** - Migrações de banco de dados
- **Pydantic** - Validação de dados e serialização
- **JWT (Jose)** - Autenticação baseada em tokens
- **Bcrypt** - Hash seguro de senhas
- **AsyncPG** - Driver PostgreSQL assíncrono
- **Redis** - Cache e messaging
- **Uvicorn** - Servidor ASGI de alta performance

### **Banco de Dados**
- **PostgreSQL 15** - Banco principal relacional
- **Redis 7** - Cache e sessões
- **Backup Automático** - Rotinas de backup configuradas

### **Infraestrutura**
- **Docker & Docker Compose** - Containerização
- **Nginx** - Proxy reverso e load balancer
- **Arquitetura de Microserviços**:
  - User Service
  - Budget Service
  - API Gateway
- **Health Checks** - Monitoramento automático de serviços

---

## 🔒 SEGURANÇA

### **Autenticação e Autorização**
- **JWT Tokens** - Autenticação stateless segura
- **Bcrypt Hashing** - Hash de senhas com salt
- **Role-Based Access Control** - Controle granular de permissões
- **Token Expiration** - Expiração automática de sessões
- **Protected Routes** - Proteção de endpoints sensíveis

### **Segurança de Dados**
- **Validação de Input** - Pydantic para validação rigorosa
- **SQL Injection Protection** - ORM com prepared statements
- **CORS Configurado** - Controle de origens permitidas
- **Environment Variables** - Secrets em variáveis de ambiente
- **HTTPS Ready** - Configuração para SSL/TLS

### **Monitoramento**
- **Health Checks** - Verificação contínua de serviços
- **Logging Estruturado** - Logs detalhados para auditoria
- **Error Handling** - Tratamento robusto de erros
- **Rate Limiting** - Proteção contra ataques DDoS

---

## 🏗️ OPÇÕES DE HOSPEDAGEM

### **🌩️ AWS (Amazon Web Services) - RECOMENDADO**

#### **Configuração Básica**
- **EC2 t3.medium** (2 vCPU, 4GB RAM)
- **RDS PostgreSQL db.t3.micro**
- **ElastiCache Redis t3.micro**
- **Application Load Balancer** 
- **S3 + CloudFront** 
- **Route 53** 

---

## 💼 MODELO COMERCIAL

### **📦 PACOTE COMPLETO - CRM DITUAL**

**Valor: R$ 300/mês**
- Todas as funcionalidades
- Suporte por chamado
- Backup diário
- Hospedagem incluída
- Implementação: R$ 2.500 (única vez)

### **🔧 SERVIÇOS ADICIONAIS**

#### **Desenvolvimento e Customização**
- **Hora de Desenvolvimento**: R$ 150/hora
- **Pacote 20h**: R$ 2.800 (desconto de 7%)
- **Pacote 40h**: R$ 5.200 (desconto de 13%)
- **Pacote 80h**: R$ 9.600 (desconto de 20%)

#### **Integrações**
- **API Simples**: R$ 2.500
- **ERP Integration**: R$ 8.000
- **Integração Customizada**: R$ 150/hora

#### **Treinamento e Suporte**
- **Treinamento Básico**
- **Suporte Técnico Dedicado**
- **Consultoria Especializada**: R$ 200/hora

### **💳 CONDIÇÕES COMERCIAIS**

#### **Formas de Pagamento**
- **À Vista**: 10% de desconto
- **Parcelado**: Até 12x com juros
- **Anual**: 2 meses de desconto
- **Bienal**: 4 meses de desconto

#### **Garantias**
- **30 dias** - Satisfação garantida ou dinheiro de volta
- **SLA 99.5%** - Uptime garantido
- **Suporte Vitalício** - Suporte técnico contínuo

#### **Benefícios Inclusos**
- ✅ Implementação completa
- ✅ Treinamento da equipe
- ✅ Suporte técnico
- ✅ Backup e segurança
- ✅ Monitoramento 24/7

---

## 📈 ROI ESPERADO

### **Benefícios Quantificáveis**
- **Aumento na produtividade da equipe de vendas**
- **Redução no tempo de criação de orçamentos**

---

## 🤝 CONTATO COMERCIAL

**Erik Patekoski**  
📧 erikpatekoski@gmail.com
📱 (11) 96409-2302  

---

*Esta proposta é válida por 30 dias a partir da data de emissão. Valores sujeitos a alteração sem aviso prévio.*