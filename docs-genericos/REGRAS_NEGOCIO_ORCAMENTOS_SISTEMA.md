# Regras de Negócio - Sistema de Orçamentos e Rentabilidade

**Versão:** 1.0  
**Data:** 19/08/2025  
**Baseado em:** Planilha "Calculo de rentabilidade e proposta rev5 (1).xlsx"

---

## 1. VISÃO GERAL DO SISTEMA

O sistema de orçamentos calcula a rentabilidade de pedidos de vendas e determina comissões baseadas em faixas de markup/rentabilidade. Cada pedido contém múltiplos itens com cálculos detalhados de compra, venda, impostos e comissões.

---

## 2. ESTRUTURA DE DADOS PRINCIPAL

### 2.1 Cabeçalho do Pedido
```
- pedido_id: string (ex: "32642")
- cliente: string (ex: "TIZIANI")
- markup_pedido: decimal (calculado automaticamente)
- comissao_total: decimal (soma de todas as comissões dos itens)
- prazo_medio: integer (dias)
```

### 2.2 Item do Pedido
```
- item_id: string/integer
- descricao: string (ex: "TB QDR. 20 X 20 X 1,25 ZINCADO")
- peso_compra: decimal
- peso_venda: decimal
- ... (campos detalhados nas seções seguintes)
```

---

## 3. BLOCO COMPRAS

### 3.1 Campos Obrigatórios
```
- peso: decimal (kg)
- valor_com_icms: decimal (R$)
- percentual_icms: decimal (padrão: 0.18)
- outras_despesas: decimal (R$)
- valor_sem_impostos: decimal (R$ - calculado)
```

### 3.2 Fórmulas de Compras

#### 3.2.1 Distribuição Proporcional de Outras Despesas
```
Formula Excel: IF(B7="",0,F27/SUM(B7:B26))
Formula Sistema: 
IF peso_item = 0 THEN 0 
ELSE outras_despesas_totais / soma_pesos_todos_itens_pedido
```

#### 3.2.2 Cálculo do Valor sem Impostos (Compra)
```
Formula Excel: C7*(1-D7)*(1-9.25%)+E7
Formula Sistema: 
valor_com_icms * (1 - percentual_icms) * (1 - 0.0925) + outras_despesas_distribuidas
```
**Onde:**
- 9.25% = PIS/COFINS (constante do sistema)
- Aplicar desconto de ICMS primeiro, depois PIS/COFINS
- Somar outras despesas já distribuídas proporcionalmente

#### 3.2.3 Valor Corrigido por Diferença de Peso
```
Formula Excel: IFERROR(F7*B7/H7,0)
Formula Sistema: 
IF peso_venda = 0 THEN 0 
ELSE valor_sem_impostos_compra * peso_compra / peso_venda
```

---

## 4. BLOCO VENDAS

### 4.1 Campos Obrigatórios
```
- peso: decimal (kg)
- valor_com_icms: decimal (R$)
- percentual_icms: decimal (padrão: 0.18)
- valor_sem_impostos: decimal (R$ - calculado)
- diferenca_peso: decimal (calculado)
```

### 4.2 Fórmulas de Vendas

#### 4.2.1 Cálculo do Valor sem Impostos (Venda)
```
Formula Excel: I7*(1-J7)*(1-9.25%)
Formula Sistema: 
valor_com_icms * (1 - percentual_icms) * (1 - 0.0925)
```

#### 4.2.2 Diferença de Peso
```
Formula Excel: IFERROR(H7/B7-1,0)
Formula Sistema: 
IF peso_compra = 0 THEN 0 
ELSE (peso_venda / peso_compra) - 1
```
**Resultado:** 
- Positivo = venda com peso maior que compra
- Negativo = venda com peso menor que compra
- Zero = pesos iguais

#### 4.2.3 Valor Unitário de Venda
```
Formula Sistema: 
IF peso_venda = 0 THEN 0 
ELSE valor_sem_impostos_venda / peso_venda
```

---

## 5. BLOCO RENTABILIDADE E MARKUP

### 5.1 Campos Calculados
```
- rentabilidade_item: decimal (percentual)
- markup_pedido: decimal (percentual)
- total_compra: decimal (R$)
- total_venda: decimal (R$)
```

### 5.2 Fórmulas de Rentabilidade

#### 5.2.1 Rentabilidade por Item
```
Formula Excel: IFERROR(K7/G7-1,0)
Formula Sistema: 
IF valor_sem_impostos_compra = 0 THEN 0 
ELSE (valor_sem_impostos_venda / valor_sem_impostos_compra) - 1
```

#### 5.2.2 Total Compra por Item
```
Formula Excel: B7*F7
Formula Sistema: peso_compra * valor_sem_impostos_compra
```

#### 5.2.3 Total Venda por Item
```
Formula Excel: H7*K7
Formula Sistema: peso_venda * valor_sem_impostos_venda
```

#### 5.2.4 Markup do Pedido
```
Formula Excel: IFERROR(O7/N7-1,0)
Formula Sistema: 
IF soma_total_compra_pedido = 0 THEN 0 
ELSE (soma_total_venda_pedido / soma_total_compra_pedido) - 1
```

---

## 6. BLOCO COMISSÕES

### 6.1 Campos de Comissão
```
- percentual_comissao: decimal (calculado por faixa)
- valor_comissao: decimal (R$ - calculado)
- comissao_total_pedido: decimal (R$ - soma de todos os itens)
```

### 6.2 Sistema de Faixas de Comissão

#### 6.2.1 Tabela de Faixas
```
Rentabilidade < 20%  → 0%
20% ≤ Rentabilidade < 30% → 1%
30% ≤ Rentabilidade < 40% → 1.5%
40% ≤ Rentabilidade < 50% → 2.5%
50% ≤ Rentabilidade < 60% → 3%
60% ≤ Rentabilidade < 80% → 4%
Rentabilidade ≥ 80% → 5%
```

#### 6.2.2 Fórmula de Percentual de Comissão
```
Formula Excel: IF(M7="","",IF(M7<20%,0,IF(M7<30%,1%,IF(M7<40%,1.5%,IF(M7<50%,2.5%,IF(M7<60%,3%,IF(M7<80%,4%,IF(M7<100%,5%,5%))))))))

Formula Sistema (Pseudocódigo):
function calcular_percentual_comissao(rentabilidade) {
    if (rentabilidade == null || rentabilidade == "") return 0;
    if (rentabilidade < 0.20) return 0.00;
    if (rentabilidade < 0.30) return 0.01;
    if (rentabilidade < 0.40) return 0.015;
    if (rentabilidade < 0.50) return 0.025;
    if (rentabilidade < 0.60) return 0.03;
    if (rentabilidade < 0.80) return 0.04;
    return 0.05; // Para rentabilidade >= 80%
}
```

#### 6.2.3 Valor da Comissão por Item
```
Formula Excel: R7*S7
Formula Sistema: 
valor_total_venda_item * percentual_comissao
```

#### 6.2.4 Soma Total de Comissões do Pedido
```
Formula Excel: SUM(T7:T26)
Formula Sistema: 
soma(valor_comissao_todos_itens_pedido)
```

---

## 7. BLOCO INTEGRAÇÃO DUNAMIS

### 7.1 Campos para Integração
```
- custo_dunamis: decimal (R$ - ajustado para lançamento)
```

### 7.2 Fórmulas para Dunamis

#### 7.2.1 Custo com Ajuste de Impostos (Versão 1)
```
Formula Excel: G7/(1-J7)/(1-9.25%)
Formula Sistema: 
valor_sem_impostos_compra / (1 - percentual_icms) / (1 - 0.0925)
```

#### 7.2.2 Custo com Ajuste de Impostos (Versão 2)
```
Formula Excel: G7/(1-J7)
Formula Sistema: 
valor_sem_impostos_compra / (1 - percentual_icms)
```

**Nota:** Verificar com a regra de negócio qual versão usar. A diferença está na aplicação ou não do desconto de PIS/COFINS.

---

## 8. VALIDAÇÕES E REGRAS DE NEGÓCIO

### 8.1 Validações Obrigatórias

#### 8.1.1 Campos Obrigatórios por Item
- Descrição não pode estar vazia
- Peso de compra deve ser > 0
- Valor com ICMS deve ser > 0
- Percentual de ICMS deve estar entre 0 e 1

#### 8.1.2 Validações de Consistência
- Peso de venda não pode ser 0 se houver valor de venda
- Percentual de ICMS padrão: 18%
- PIS/COFINS fixo: 9,25%

### 8.2 Regras de Cálculo

#### 8.2.1 Ordem de Execução dos Cálculos
1. Calcular distribuição proporcional de outras despesas
2. Calcular valores sem impostos (compra e venda)
3. Calcular rentabilidade por item
4. Calcular percentual de comissão baseado na rentabilidade
5. Calcular valor da comissão
6. Calcular totais do pedido (markup geral)
7. Calcular custos para Dunamis

#### 8.2.2 Tratamento de Erros
- Divisões por zero devem retornar 0
- Campos vazios devem ser tratados como 0
- Usar IFERROR/TryCatch para robustez

### 8.3 Constraints de Negócio

#### 8.3.1 Limites Operacionais
- Rentabilidade mínima: sem limite inferior (pode ser negativa)
- Rentabilidade máxima: sem limite superior
- Comissão máxima: 5% (para rentabilidades ≥ 80%)

#### 8.3.2 Regras de Arredondamento
- Valores monetários: 2 casas decimais
- Percentuais: 4 casas decimais para cálculos, 2 para exibição
- Pesos: 3 casas decimais

---

## 9. CASOS DE TESTE

### 9.1 Caso Teste 1: Item Básico
```
Entrada:
- peso_compra: 100 kg
- valor_com_icms_compra: 6.50
- percentual_icms: 0.18
- outras_despesas: 0
- peso_venda: 100 kg  
- valor_com_icms_venda: 8.50
- percentual_icms_venda: 0.18

Resultado Esperado:
- valor_sem_impostos_compra: 4.8369 (6.50 * (1-0.18) * (1-0.0925))
- valor_sem_impostos_venda: 6.3253 (8.50 * (1-0.18) * (1-0.0925))
- rentabilidade: 0.3077 (30.77%)
- percentual_comissao: 0.015 (1.5%)
- valor_comissao: 9.49 (6.3253 * 100 * 0.015)
```

### 9.2 Caso Teste 2: Com Outras Despesas
```
Entrada:
- Mesmo do Caso 1, mas outras_despesas_totais: 50
- Assumindo que este item representa 50% do peso total do pedido

Resultado Esperado:
- outras_despesas_distribuidas: 25 (50 * 0.5)
- valor_sem_impostos_compra: 29.8369 (4.8369 + 25)
- Rentabilidade menor devido ao custo adicional
```

---

## 10. IMPLEMENTAÇÃO TÉCNICA

### 10.1 Estrutura de Banco de Dados Sugerida

```sql
-- Tabela principal do pedido
CREATE TABLE pedidos (
    id VARCHAR PRIMARY KEY,
    cliente VARCHAR NOT NULL,
    data_pedido TIMESTAMP,
    markup_pedido DECIMAL(10,6),
    comissao_total DECIMAL(10,2),
    prazo_medio INTEGER
);

-- Tabela de itens do pedido
CREATE TABLE itens_pedido (
    id SERIAL PRIMARY KEY,
    pedido_id VARCHAR REFERENCES pedidos(id),
    descricao VARCHAR NOT NULL,
    
    -- Campos de compra
    peso_compra DECIMAL(10,3) NOT NULL,
    valor_com_icms_compra DECIMAL(10,2) NOT NULL,
    percentual_icms_compra DECIMAL(5,4) DEFAULT 0.18,
    outras_despesas DECIMAL(10,2) DEFAULT 0,
    valor_sem_impostos_compra DECIMAL(10,2),
    
    -- Campos de venda  
    peso_venda DECIMAL(10,3),
    valor_com_icms_venda DECIMAL(10,2),
    percentual_icms_venda DECIMAL(5,4) DEFAULT 0.18,
    valor_sem_impostos_venda DECIMAL(10,2),
    
    -- Campos calculados
    rentabilidade DECIMAL(10,6),
    percentual_comissao DECIMAL(5,4),
    valor_comissao DECIMAL(10,2),
    custo_dunamis DECIMAL(10,2),
    
    -- Auditoria
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 10.2 Triggers e Procedures Sugeridas

```sql
-- Trigger para recalcular automaticamente após inserção/atualização
CREATE OR REPLACE FUNCTION recalcular_item_pedido()
RETURNS TRIGGER AS $$
BEGIN
    -- Implementar todas as fórmulas aqui
    -- Atualizar campos calculados do item
    -- Recalcular totais do pedido
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_recalcular_item
    AFTER INSERT OR UPDATE ON itens_pedido
    FOR EACH ROW EXECUTE FUNCTION recalcular_item_pedido();
```

---

## 11. OBSERVAÇÕES IMPORTANTES

### 11.1 Pontos de Atenção
1. **Precisão Decimal**: Usar DECIMAL em vez de FLOAT para cálculos financeiros
2. **Ordem de Cálculo**: Respeitar a sequência das operações matemáticas
3. **Tratamento de Nulos**: Campos vazios devem ser tratados como zero
4. **Performance**: Considerar índices nas colunas de pesquisa frequente

### 11.2 Integrações Externas
- **Sistema Dunamis**: Valores calculados serão exportados
- **Sistema de Propostas**: Dados serão utilizados para geração de propostas

### 11.3 Auditoria e Log
- Manter histórico de alterações nos cálculos
- Log de todas as operações de recálculo
- Rastreabilidade de mudanças nas fórmulas

---

**Documento elaborado baseado na análise da planilha Excel fornecida.**  
**Revisão necessária com equipe de negócios antes da implementação.**
