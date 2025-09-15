# 🖼️ Como Adicionar o Logo da Empresa no PDF

## 📋 Passo a Passo

### 1. Preparar o Logo
- **Formato**: PNG (recomendado) ou JPG
- **Nome do arquivo**: `logo.png`
- **Resolução**: Mínimo 300 DPI para impressão
- **Dimensões**: Aproximadamente 200x100 pixels
- **Fundo**: Transparente (PNG) para melhor integração

### 2. Colocar o Logo no Diretório
```bash
# Coloque o arquivo logo.png em:
services/budget_service/app/static/logo.png
```

### 3. Copiar para o Container (se necessário)
```bash
# Se o container já estiver rodando, copie manualmente:
docker exec crm_budget_service mkdir -p /app/static
docker cp services/budget_service/app/static/logo.png crm_budget_service:/app/static/logo.png
```

### 4. Reiniciar o Serviço
```bash
docker compose restart budget_service
```

## ✅ Verificação

1. **Acesse o sistema** em http://localhost:3000
2. **Faça login** como administrador
3. **Vá para Orçamentos** → Selecione qualquer orçamento
4. **Clique em "Exportar PDF"**
5. **Verifique o PDF** → O logo deve aparecer no cabeçalho vermelho

## 🔧 Solução de Problemas

### Logo não aparece no PDF
```bash
# Verificar se o logo existe no container
docker exec crm_budget_service ls -la /app/static/

# Se não existir, copiar novamente
docker cp services/budget_service/app/static/logo.png crm_budget_service:/app/static/logo.png

# Reiniciar o serviço
docker compose restart budget_service
```

### Verificar logs de erro
```bash
# Ver logs do serviço
docker logs crm_budget_service --tail 20
```

## 📁 Estrutura de Arquivos

```
services/budget_service/app/
├── static/
│   ├── logo.png              # ← Seu logo aqui
│   └── README_LOGO.md
├── services/
│   └── pdf_export_service.py # Código que carrega o logo
└── ...
```

## 🎨 Resultado

O logo aparecerá no **cabeçalho vermelho** do PDF, no canto superior esquerdo, conforme o template oficial da Ditual São Paulo Tubos e Aços.

## 📞 Suporte

Se o logo ainda não aparecer após seguir estes passos, verifique:
1. ✅ Arquivo está no local correto
2. ✅ Nome do arquivo é exatamente `logo.png`
3. ✅ Container foi reiniciado
4. ✅ Não há erros nos logs
