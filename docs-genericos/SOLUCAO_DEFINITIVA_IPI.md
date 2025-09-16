# SOLUÇÃO DEFINITIVA - PADRONIZAR CAMPOS IPI

## 🎯 PROBLEMA IDENTIFICADO

O sistema tem uma **confusão de idiomas** entre frontend e backend:
- **Backend**: usa `ipi_percentage` (inglês)
- **Frontend**: usa `percentual_ipi` (português) 
- **Resultado**: Mapeamento falha constantemente

## 💡 SOLUÇÃO PROPOSTA

**PADRONIZAR TUDO PARA INGLÊS** no frontend, seguindo o padrão do backend.

### Vantagens:
✅ **Consistência total** entre frontend e backend  
✅ **Sem conversão** de nomes de campos  
✅ **Menos propenso a erros** de mapeamento  
✅ **Mais simples** de manter  

## 🔧 MUDANÇAS NECESSÁRIAS

### 1. Interface BudgetItemSimplified

**DE:**
```typescript
interface BudgetItemSimplified {
  percentual_ipi: number;  // português
}
```

**PARA:**
```typescript
interface BudgetItemSimplified {
  ipi_percentage: number;  // inglês (igual ao backend)
}
```

### 2. SimplifiedBudgetForm.tsx

**DE:**
```typescript
// Mapeamento complexo tentando converter nomes
percentual_ipi: (() => {
  // múltiplas tentativas...
})()
```

**PARA:**
```typescript
// Simples: usar o mesmo nome do backend
ipi_percentage: item.ipi_percentage || 0.0
```

### 3. Campos da tabela

**DE:**
```typescript
dataIndex: 'percentual_ipi',
key: 'percentual_ipi',
```

**PARA:**
```typescript
dataIndex: 'ipi_percentage',
key: 'ipi_percentage',
```

## 🚀 IMPLEMENTAÇÃO

Vou implementar essas mudanças agora para resolver definitivamente o problema.

## 📋 RESULTADO ESPERADO

- ✅ Frontend usa `ipi_percentage` (igual ao backend)
- ✅ Sem conversão de nomes de campos
- ✅ Mapeamento direto e simples
- ✅ Bug resolvido definitivamente

Esta abordagem elimina a fonte do problema ao invés de tentar contorná-lo.
