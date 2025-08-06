# 🚀 Guia de Inicialização do Frontend React

## 💡 **Problema Identificado e Soluções**

### **🔍 Problema: Incompatibilidade Node.js + Vite**
- **Node.js v21.6.0** (sua versão atual)
- **Vite 7.0.6** (requer Node.js ^20.19.0 || >=22.12.0)
- **Erro**: `TypeError: crypto.hash is not a function`

### **✅ Solução Aplicada**
Fizemos downgrade do Vite para versão compatível:
```bash
npm install vite@5.4.10 --save-dev
```

## 🚀 **Como Inicializar o Frontend**

### **Método 1: Comando Direto (Recomendado)**
```bash
# 1. Navegue para o diretório frontend
cd /Users/erikpatekoski/dev/crm-ditual/frontend

# 2. Inicie o servidor de desenvolvimento
npm run dev

# 3. Acesse no navegador
# http://localhost:3000
```

### **Método 2: Com Mais Memória (Se der erro)**
```bash
cd /Users/erikpatekoski/dev/crm-ditual/frontend
NODE_OPTIONS="--max-old-space-size=4096" npm run dev
```

### **Método 3: Força limpeza (Se persistir problema)**
```bash
cd /Users/erikpatekoski/dev/crm-ditual/frontend

# Limpar cache e node_modules
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## 🔧 **Verificações de Status**

### **✅ Verificar se está rodando:**
```bash
# Verificar processos
ps aux | grep vite

# Verificar porta 3000
lsof -i :3000

# Testar acesso
curl -I http://localhost:3000
```

### **✅ Verificar versões:**
```bash
cd frontend
node --version        # v21.6.0
npm list vite         # 5.4.10
npm run build         # Testar build
```

## 🌐 **URLs de Acesso**

### **📱 Frontend (React)**
- **Desenvolvimento**: http://localhost:3000
- **Build preview**: `npm run preview` → http://localhost:4173

### **🚀 Backend (FastAPI)**
- **API**: http://localhost:8001
- **Docs**: http://localhost:8001/docs
- **Health**: http://localhost:8001/health

## 🎯 **Credenciais de Teste**

### **👑 Administrador**
```
Username: admin
Password: admin123456
Acesso: Dashboard + Usuários + Perfil
```

### **👤 Vendedor**
```
Username: vendedor1
Password: venda123456
Acesso: Dashboard + Perfil (próprio)
```

## 🛠️ **Comandos Úteis do Frontend**

```bash
cd frontend

# Desenvolvimento
npm run dev           # Servidor desenvolvimento (port 3000)
npm run build         # Build produção
npm run preview       # Preview do build
npm run lint          # Verificar código

# Instalação/limpeza
npm install           # Instalar dependências
npm audit fix         # Corrigir vulnerabilidades
rm -rf node_modules   # Limpeza total
```

## 🚨 **Solução de Problemas**

### **Problema 1: Erro crypto.hash**
```bash
# Solução: Downgrade Vite
cd frontend
npm install vite@5.4.10 --save-dev
npm run dev
```

### **Problema 2: Porta 3000 ocupada**
```bash
# Verificar processo na porta
lsof -i :3000

# Matar processo se necessário
kill -9 <PID>

# Ou usar porta diferente
npm run dev -- --port 3001
```

### **Problema 3: Module not found**
```bash
# Reinstalar dependências
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### **Problema 4: Build falha**
```bash
# Verificar TypeScript
npm run build

# Se houver erros TS, corrigir ou
npm run dev  # (desenvolvimento ignora alguns erros)
```

## 📊 **Status Atual do Sistema**

### **✅ Backend Funcionando**
```bash
# Verificar containers
docker compose ps

# Testar API
curl http://localhost:8001/health
```

### **✅ Frontend Configurado**
- ✅ Projeto React + TypeScript criado
- ✅ Dependências instaladas
- ✅ Vite downgrade para compatibilidade
- ✅ Componentes e páginas implementadas
- ✅ Integração com API configurada

## 🎯 **Fluxo de Teste Completo**

### **1. Verificar Backend**
```bash
curl http://localhost:8001/health
# Deve retornar: {"status":"healthy","service":"user_service"}
```

### **2. Iniciar Frontend**
```bash
cd frontend
npm run dev
# Aguardar mensagem: "Local: http://localhost:3000"
```

### **3. Testar no Navegador**
1. Acesse: http://localhost:3000
2. Faça login com: `admin` / `admin123456`
3. Explore Dashboard e funcionalidades

## 🚀 **Comando Final (Copy & Paste)**

```bash
# Execute este comando para iniciar tudo:
cd /Users/erikpatekoski/dev/crm-ditual/frontend && npm run dev
```

## 🎉 **Resultado Esperado**

Quando funcionar, você verá algo como:
```
VITE v5.4.10  ready in 1234 ms

➜  Local:   http://localhost:3000/
➜  Network: use --host to expose
➜  press h + enter to show help
```

---

## **✨ Status: Frontend Pronto para Inicializar!**

Siga os passos acima e o sistema estará **100% funcional** - Backend + Frontend integrados! 🚀