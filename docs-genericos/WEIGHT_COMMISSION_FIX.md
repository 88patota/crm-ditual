# CORREÇÃO: Cálculo de Comissão Baseado em Diferença de Peso

## 🐛 Problema Identificado

Quando o peso de venda era alterado de 1000kg para 1050kg, o sistema retornava:
- **Resultado atual**: 2.5% comissão → R$ 210,00
- **Resultado esperado**: 3% comissão → R$ 252,00

## 🔍 Análise da Causa

O problema estava na simplificação excessiva do cálculo de comissão. O sistema deveria usar duas abordagens diferentes:

### Cenário 1: Peso Igual (1000kg → 1000kg)
- **Usar rentabilidade unitária**: 43.1% 
- **Comissão**: 2.5% → R$ 200,00
- **Lógica**: Operação simples, sem diferença de quantidade

### Cenário 2: Peso Diferente (1000kg → 1050kg)  
- **Usar rentabilidade total**: 50.2%
- **Comissão**: 3.0% → R$ 252,00
- **Lógica**: Operação complexa, reflete venda de quantidade adicional

## ✅ Solução Implementada

### Arquivo: `/services/budget_service/app/services/business_rules_calculator.py`

**ANTES (Incorreto):**
```python
# Sempre usava rentabilidade unitária
percentual_comissao = CommissionService.calculate_commission_percentage(rentabilidade_item)
valor_comissao = total_venda_item_com_icms * percentual_comissao
```

**DEPOIS (Correto):**
```python
if peso_venda == peso_compra:
    # Mesma quantidade: usar rentabilidade unitária (SEM impostos)
    percentual_comissao = CommissionService.calculate_commission_percentage(rentabilidade_item)
else:
    # Quantidade diferente: usar rentabilidade total (SEM impostos) 
    if total_compra_sem_impostos == 0:
        rentabilidade_total = 0.0
    else:
        rentabilidade_total = (total_venda_sem_impostos / total_compra_sem_impostos) - 1
    percentual_comissao = CommissionService.calculate_commission_percentage(rentabilidade_total)

# Aplicar comissão sobre valor COM ICMS (faturamento real)
valor_comissao = total_venda_item_com_icms * percentual_comissao
```

## 🎯 Resultados dos Testes

### Teste 1: Peso Igual (1000kg)
```json
{
  "peso_compra": 1000,
  "peso_venda": 1000,
  "rentabilidade_unitaria": 43.1,
  "comissao_percentual": 2.5,
  "valor_comissao": 200.00,
  "status": "✅ CORRETO"
}
```

### Teste 2: Peso Diferente (1050kg)
```json
{
  "peso_compra": 1000,
  "peso_venda": 1050,
  "rentabilidade_total": 50.2,
  "comissao_percentual": 3.0,
  "valor_comissao": 252.00,
  "status": "✅ CORRETO"
}
```

## 📊 Faixas de Comissão Aplicadas

| Rentabilidade | Comissão | Aplicação |
|---------------|----------|-----------|
| < 20%         | 0%       | -         |
| 20% - 30%     | 1%       | -         |
| 30% - 40%     | 1.5%     | -         |
| 40% - 50%     | 2.5%     | ← Unitária (43.1%) |
| 50% - 60%     | 3%       | ← Total (50.2%) |
| 60% - 80%     | 4%       | -         |
| ≥ 80%         | 5%       | -         |

## 🔑 Regras de Negócio Implementadas

1. **Mesmo peso (peso_venda = peso_compra)**:
   - Usar rentabilidade unitária baseada em valores SEM impostos
   - Operação padrão, sem complexidade adicional

2. **Peso diferente (peso_venda ≠ peso_compra)**:
   - Usar rentabilidade total baseada em valores SEM impostos
   - Reflete o ganho real da operação completa
   - Incentiva vendas de maiores quantidades

3. **Aplicação da comissão**:
   - Sempre sobre o valor total de venda COM ICMS
   - Representa o faturamento real da empresa

## ✅ Validação

O sistema agora calcula corretamente:
- **1000kg → 1000kg**: 43.1% rentabilidade → 2.5% comissão → R$ 200,00
- **1000kg → 1050kg**: 50.2% rentabilidade → 3.0% comissão → R$ 252,00

---
**Status:** ✅ **RESOLVIDO**  
**Data:** 26/08/2025  
**Arquivo alterado:** `services/budget_service/app/services/business_rules_calculator.py`