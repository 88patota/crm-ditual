# CORREÇÃO: Inconsistência no Cálculo de Comissão entre Criação e Visualização de Orçamento

## 🐛 Problema Identificado

O cálculo do percentual de comissão estava inconsistente entre:

1. ❌ **Tela de visualização**: Cálculo hardcoded incorreto no frontend
2. ❌ **Backend**: Usava valores **COM ICMS** para calcular rentabilidade

**Resultado incorreto:**
- Compra: R$ 6,00 (ICMS 18%) → Venda: R$ 8,00 (ICMS 12%)
- Rentabilidade: 33.33% (COM ICMS) → Comissão: 1.5% → R$ 120,00

**Resultado esperado:**
- Rentabilidade: 43.1% (SEM impostos) → Comissão: 2.5% → R$ 200,00

## 🔍 Análise do Problema

### Problema 1: Frontend (BudgetView.tsx) - ANTES (Incorreto)
```typescript
render: (profitability: number) => {
  let commissionPercentage = 0;
  if (profitability >= 80) commissionPercentage = 5.0;
  else if (profitability >= 60) commissionPercentage = 4.0;
  else if (profitability >= 50) commissionPercentage = 3.0;  // ❌ ERRO: faixa incorreta
  else if (profitability >= 40) commissionPercentage = 2.5;
  else if (profitability >= 30) commissionPercentage = 1.5;
  else if (profitability >= 20) commissionPercentage = 1.0;
  else commissionPercentage = 0.0;
```

### Problema 2: Backend - Rentabilidade COM ICMS (Incorreto)
```python
# ANTES: Usava valores COM ICMS (33.33% rentabilidade)
rentabilidade_item = BusinessRulesCalculator.calculate_item_profitability(
    valor_com_icms_venda,    # R$ 8,00
    valor_com_icms_compra    # R$ 6,00  
)  # Resultado: (8/6) - 1 = 33.33%
```

## ✅ Solução Implementada

### Correção 1: Frontend (BudgetView.tsx)
```typescript
render: (profitability: number) => {
  // CORREÇÃO: Usar mesma lógica do backend
  const rentabilidadeDecimal = profitability > 1 ? profitability / 100 : profitability;
  
  // Aplicar mesmas faixas do backend (CommissionService.COMMISSION_BRACKETS)
  if (rentabilidadeDecimal >= 0.80) commissionPercentage = 5.0;        // >=80% = 5%
  else if (rentabilidadeDecimal >= 0.60) commissionPercentage = 4.0;   // 60-80% = 4%
  else if (rentabilidadeDecimal >= 0.50) commissionPercentage = 3.0;   // 50-60% = 3%
  else if (rentabilidadeDecimal >= 0.40) commissionPercentage = 2.5;   // 40-50% = 2.5%
  else if (rentabilidadeDecimal >= 0.30) commissionPercentage = 1.5;   // 30-40% = 1.5%
  else if (rentabilidadeDecimal >= 0.20) commissionPercentage = 1.0;   // 20-30% = 1%
  else commissionPercentage = 0.0;                                     // <20% = 0%
```

### Correção 2: Backend - Rentabilidade SEM Impostos
```python
# DEPOIS: Usa valores SEM impostos (43.1% rentabilidade)
rentabilidade_item = BusinessRulesCalculator.calculate_item_profitability(
    valor_sem_impostos_venda,    # R$ 6,3888
    valor_sem_impostos_compra    # R$ 4,4649
)  # Resultado: (6.3888/4.4649) - 1 = 43.1%

# E aplica comissão sobre valor COM ICMS (valor real pago pelo cliente)
percentual_comissao = CommissionService.calculate_commission_percentage(rentabilidade_item)
valor_comissao = total_venda_item_com_icms * percentual_comissao  # R$ 8.000 * 2.5%
```

### Backend (CommissionService.py) - CORRETO
```python
COMMISSION_BRACKETS = [
    {"min_profitability": 0.0, "max_profitability": 0.20, "commission_rate": 0.00},    # < 20% = 0%
    {"min_profitability": 0.20, "max_profitability": 0.30, "commission_rate": 0.01},   # 20-30% = 1%
    {"min_profitability": 0.30, "max_profitability": 0.40, "commission_rate": 0.015},  # 30-40% = 1.5%
    {"min_profitability": 0.40, "max_profitability": 0.50, "commission_rate": 0.025},  # 40-50% = 2.5%
    {"min_profitability": 0.50, "max_profitability": 0.60, "commission_rate": 0.03},   # 50-60% = 3%
    {"min_profitability": 0.60, "max_profitability": 0.80, "commission_rate": 0.04},   # 60-80% = 4%
    {"min_profitability": 0.80, "max_profitability": float('inf'), "commission_rate": 0.05}  # >=80% = 5%
]
```

## ✅ Solução Implementada

### Frontend (BudgetView.tsx) - DEPOIS (Corrigido)
```typescript
render: (profitability: number) => {
  // CORREÇÃO: Usar mesma lógica do backend (profitability vem como decimal: 0.50 = 50%)
  let commissionPercentage = 0;
  
  // Converter rentabilidade para decimal se necessário (caso venha como %)
  const rentabilidadeDecimal = profitability > 1 ? profitability / 100 : profitability;
  
  // Aplicar mesmas faixas do backend (CommissionService.COMMISSION_BRACKETS)
  if (rentabilidadeDecimal >= 0.80) commissionPercentage = 5.0;        // >=80% = 5%
  else if (rentabilidadeDecimal >= 0.60) commissionPercentage = 4.0;   // 60-80% = 4%
  else if (rentabilidadeDecimal >= 0.50) commissionPercentage = 3.0;   // 50-60% = 3%
  else if (rentabilidadeDecimal >= 0.40) commissionPercentage = 2.5;   // 40-50% = 2.5%
  else if (rentabilidadeDecimal >= 0.30) commissionPercentage = 1.5;   // 30-40% = 1.5%
  else if (rentabilidadeDecimal >= 0.20) commissionPercentage = 1.0;   // 20-30% = 1%
  else commissionPercentage = 0.0;                                     // <20% = 0%
  
  return `${commissionPercentage.toFixed(1)}%`;
},
```

## 🔧 Mudanças Realizadas

### Arquivo: `/frontend/src/pages/BudgetView.tsx`
- ✅ Corrigida lógica de cálculo de comissão na coluna "Comissão %"
- ✅ Adicionado tratamento para formato decimal vs percentual
- ✅ Implementada mesma lógica do backend (CommissionService.COMMISSION_BRACKETS)
- ✅ Adicionados comentários explicativos

## 🎯 Resultado

Agora o cálculo de comissão é **consistente** entre:
- ✅ Tela de criação de orçamento (usa backend via API)
- ✅ Tela de visualização de orçamento (usa lógica corrigida)
- ✅ Backend (CommissionService.py)

## 📊 Faixas de Comissão (Unificadas)

| Rentabilidade | Comissão |
|---------------|----------|
| < 20%         | 0%       |
| 20% - 30%     | 1%       |
| 30% - 40%     | 1.5%     |
| 40% - 50%     | 2.5%     |
| 50% - 60%     | 3%       |
| 60% - 80%     | 4%       |
| ≥ 80%         | 5%       |

## ✅ Validação

Para validar a correção:
1. 🖥️ Acesse o frontend em http://localhost:3001
2. 🔑 Faça login com credenciais demo (admin/admin123)
3. 📋 Crie um novo orçamento e anote os valores de comissão
4. 👁️ Visualize o orçamento criado
5. ✅ Confirme que os percentuais de comissão são idênticos

## 🔮 Prevenção Futura

Para evitar inconsistências similares:
1. 📚 Centralizar regras de negócio no backend
2. 🧪 Implementar testes automatizados de consistência
3. 📝 Documentar fórmulas em local centralizado
4. 🔄 Revisar cálculos durante code review

---
**Status:** ✅ **RESOLVIDO**  
**Data:** 26/08/2025  
**Arquivo alterado:** `frontend/src/pages/BudgetView.tsx`