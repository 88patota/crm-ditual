# Regras de Negócio - Fórmulas de Cálculo de Orçamento

## Análise Baseada no Código Existente

Com base na análise do código do sistema CRM Ditual, especificamente os arquivos:
- `services/budget_service/app/services/budget_calculator.py`
- `frontend/src/components/budgets/AutoMarkupBudgetForm.tsx`
- `frontend/src/services/budgetService.ts`

## 1. Fórmulas Principais Identificadas

### 1.1 Cálculo de Valor sem Impostos

#### Valor de Compra sem ICMS
```
Valor Compra s/ICMS = Valor Compra c/ICMS × (1 - % ICMS Compra / 100)
```

#### Valor de Venda sem ICMS
```
Valor Venda s/ICMS = Valor Venda c/ICMS × (1 - % ICMS Venda / 100)
```

### 1.2 Cálculo de Markup (Rentabilidade)

#### Fórmula Principal do Markup
```
Markup (%) = ((Valor Venda s/ICMS - Valor Compra s/ICMS) / Valor Compra s/ICMS) × 100
```

**Observação:** A fórmula considera outras despesas no custo base:
```
Custo Total = Valor Compra s/ICMS + Outras Despesas
Markup (%) = ((Valor Venda s/ICMS - Custo Total) / Custo Total) × 100
```

### 1.3 Cálculo de Totais por Item

#### Total de Compra
```
Total Compra = (Valor Compra s/ICMS + Outras Despesas) × Quantidade
```

#### Total de Venda
```
Total Venda = Valor Venda c/ICMS × Quantidade
```

**IMPORTANTE:** O total de venda deve usar o valor COM ICMS porque:
- É o valor real que o cliente paga
- A comissão é calculada sobre o valor real de venda
- Os relatórios e totais devem mostrar os valores reais de faturamento

### 1.4 Cálculo de Comissão

#### Valor da Comissão
```
Valor Comissão = Total Venda × (% Comissão / 100)
```

**Padrão do Sistema:** 1,5% de comissão

### 1.5 Cálculo de Rentabilidade Geral do Orçamento

#### Rentabilidade do Orçamento
```
Rentabilidade (%) = ((Total Venda Geral - Total Compra Geral) / Total Compra Geral) × 100
```

Onde:
- `Total Compra Geral = Σ(Total Compra de cada item)`
- `Total Venda Geral = Σ(Total Venda de cada item)`

## 2. Configurações Padrão do Sistema

### 2.1 Percentuais ICMS
- **ICMS Compra:** 17% (padrão)
- **ICMS Venda:** 18% (padrão)

### 2.2 Markup
- **Mínimo:** 20%
- **Máximo:** 200%
- **Margem Alvo:** 30%

### 2.3 Comissão
- **Padrão:** 1,5%

## 3. Regras de Negócio

### 3.1 Validações Obrigatórias

#### Para cada Item do Orçamento:
1. **Descrição:** Obrigatória, não pode estar vazia
2. **Quantidade:** Obrigatória, deve ser > 0
3. **Valor de Compra c/ICMS:** Obrigatório, deve ser > 0
4. **Valor de Venda c/ICMS:** Obrigatório, deve ser > 0
5. **% ICMS Compra:** Obrigatório, entre 0% e 100%
6. **% ICMS Venda:** Obrigatório, entre 0% e 100%

#### Validação de Lógica de Negócio:
- **Valor de venda deve ser maior que valor de compra**
- **Orçamento deve ter pelo menos um item**

### 3.2 Cálculo Automático de Markup

#### Quando aplicar markup desejado:
1. Calcular total de compra de todos os itens
2. Calcular valor total de venda necessário: `Total Compra × (1 + Markup Desejado / 100)`
3. Ajustar preços de venda proporcionalmente para atingir markup

#### Fórmula para Preço de Venda com Markup:
```
Valor Venda s/ICMS Necessário = Custo Total × (1 + Markup Desejado / 100)
Valor Venda c/ICMS = Valor Venda s/ICMS Necessário / (1 - % ICMS Venda / 100)
```

### 3.3 Cálculo de Diferença de Peso

#### Diferença de Peso (quando aplicável)
```
Diferença Peso = Peso Venda - Peso Compra
```

### 3.4 Custo Dunamis

#### Fórmula do Custo Dunamis
```
Custo Dunamis = Valor Compra s/ICMS × Quantidade
```

## 4. Campos Calculados Automaticamente

### 4.1 Por Item:
- Valor de compra sem impostos
- Valor de venda sem impostos
- Total de compra
- Total de venda
- Rentabilidade (markup individual)
- Valor da comissão
- Diferença de peso
- Custo Dunamis

### 4.2 Por Orçamento:
- Total geral de compra
- Total geral de venda
- Total de comissão
- Rentabilidade geral
- Markup médio do orçamento

## 5. Fluxo de Cálculo

### 5.1 Entrada de Dados (Campos Obrigatórios):
1. Descrição do produto
2. Quantidade
3. Valor de compra com ICMS
4. % ICMS da compra
5. Valor de venda com ICMS
6. % ICMS da venda

### 5.2 Entrada de Dados (Campos Opcionais):
1. Peso do produto (kg)
2. Outras despesas
3. % de comissão (usa padrão 1,5% se não informado)

### 5.3 Processo de Cálculo:
1. **Validar dados de entrada**
2. **Calcular valores sem impostos** para compra e venda
3. **Calcular totais** multiplicando pela quantidade
4. **Calcular markup/rentabilidade** usando a fórmula principal
5. **Calcular comissão** baseada no total de venda
6. **Somar todos os itens** para obter totais do orçamento
7. **Calcular rentabilidade geral** do orçamento

## 6. Casos Especiais

### 6.1 Markup Automático por Faixa de Valores
- O sistema tem capacidade para aplicar markup automático
- Baseado em configurações mínimas e máximas
- Considera posição de mercado desejada

### 6.2 Ajuste Proporcional de Preços
- Quando um markup específico é aplicado ao orçamento
- Todos os preços de venda são ajustados proporcionalmente
- Mantém a relação entre os itens

### 6.3 Prevenção de Markup Negativo
- Sistema impede criação de orçamentos com markup negativo
- Validação automática garante que valor de venda > valor de compra

## 7. Implementação Técnica

### 7.1 Frontend (React/TypeScript):
- Formatação em moeda brasileira (R$)
- Validação em tempo real
- Cálculo de preview antes da submissão
- Interface para entrada de dados simplificada

### 7.2 Backend (Python/FastAPI):
- Cálculos precisos com ponto flutuante
- Validação de dados robusta
- API RESTful para cálculos
- Geração de PDF com fórmulas aplicadas

## 8. Pontos de Atenção

### 8.1 Precisão de Cálculos:
- Valores monetários: 2 casas decimais
- Percentuais: 1 casa decimal para ICMS, 2 casas para markup
- Peso: 3 casas decimais

### 8.2 Tratamento de Zeros:
- Sistema trata divisão por zero retornando 0%
- Valores mínimos aplicados onde necessário

### 8.3 Formatação Brasileira:
- Moeda em Real (R$)
- Separador decimal: vírgula
- Separador de milhares: ponto

## 9. Próximos Passos Recomendados

Para analisar a **linha 7 específica** da planilha mencionada, seria necessário:

1. **Acesso direto à planilha** ou
2. **Screenshot da linha 7** ou  
3. **Cópia dos valores e fórmulas** da linha 7

Com essas informações, posso:
- Comparar com as fórmulas implementadas
- Identificar discrepâncias
- Sugerir ajustes no código
- Criar testes específicos para a linha 7

## 10. Solicitação

**Para uma análise mais precisa da linha 7, você poderia fornecer:**
- Os valores exatos da linha 7
- As fórmulas das células calculadas
- Screenshot da linha ou dados em texto

Assim poderei criar regras de negócio específicas e validar se a implementação atual está correta.
