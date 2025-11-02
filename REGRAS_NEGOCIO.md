# Regras de Negócio - CRM Ditual

## 📋 Índice

1. [Regras de Cálculo de Orçamentos](#1-regras-de-cálculo-de-orçamentos)
2. [Regras de Comissão](#2-regras-de-comissão)
3. [Regras de Controle de Acesso](#3-regras-de-controle-de-acesso)
4. [Regras de Validação](#4-regras-de-validação)
5. [Regras de IPI](#5-regras-de-ipi)
6. [Regras de Frete](#6-regras-de-frete)
7. [Regras de Status e Workflow](#7-regras-de-status-e-workflow)

---

## 1. Regras de Cálculo de Orçamentos

### 1.1 Cálculo de Valores sem Impostos

#### 1.1.1 Valor s/Impostos (Compra)
- **Fórmula**: `Valor s/Impostos (Compra) = [Valor c/ICMS (Compra) * (1 - % ICMS (Compra))] * (1 - Taxa PIS/COFINS) - [Outras Despesas / Peso (Compra)]`
- **Descrição**: Calcula o valor líquido de compra sem impostos, deduzindo sequencialmente ICMS e PIS/COFINS
- **Taxa PIS/COFINS**: Fixa em 9,25% (0.0925)
- **Outras Despesas**: Distribuídas proporcionalmente ao peso do item

#### 1.1.2 Valor s/Impostos (Venda)
- **Fórmula**: `Valor s/Impostos (Venda) = [Valor c/ICMS (Venda) * (1 - % ICMS (Venda))] * (1 - Taxa PIS/COFINS)`
- **Descrição**: Calcula o valor líquido de venda sem impostos
- **ICMS Padrão**: 18% (0.18) para vendas

### 1.2 Correção por Diferença de Peso

#### 1.2.1 Valor Corrigido por Peso (Compra)
- **Fórmula**: `Valor Corrigido = valor_sem_impostos_compra * (peso_compra / peso_venda)`
- **Descrição**: Ajusta o custo unitário para compensar diferenças entre peso comprado e vendido
- **Aplicação**: Perdas/ganhos por umidade, tolerância de produção

#### 1.2.2 Diferença de Peso
- **Fórmula**: `Diferença de Peso = (Peso (Venda) - Peso (Compra)) / Peso (Compra)`
- **Descrição**: Quantifica a variação percentual de peso entre compra e venda
- **Valores**: Zero = equilíbrio; positivo = ganho; negativo = perda

### 1.3 Cálculo de Rentabilidade

#### 1.3.1 Rentabilidade por Item
- **Fórmula**: `Rentabilidade = [Valor s/Impostos (Venda) / Valor c/Difer. Peso (Compra)] - 1`
- **Descrição**: Representa o markup ou margem de lucro unitário sobre o custo ajustado
- **Formato**: Decimal (ex: 0.3077 = 30,77%)

#### 1.3.2 Markup do Pedido
- **Fórmula**: `Markup = (soma_total_venda_pedido / soma_total_compra_pedido) - 1`
- **Descrição**: Markup agregado de todo o pedido
- **Validação**: Se soma_total_compra_pedido = 0, então markup = 0

### 1.4 Totalizações

#### 1.4.1 Total Compra
- **Fórmula**: `Total Compra = Peso (Compra) * Valor s/Impostos (Compra)`
- **Descrição**: Custo líquido total do lote sem impostos

#### 1.4.2 Total Venda
- **Fórmula**: `Total Venda = Peso (Venda) * Valor s/Impostos (Venda)`
- **Descrição**: Receita líquida total sem impostos

#### 1.4.3 Valor Total (com ICMS)
- **Fórmula**: `Valor Total = Peso (Venda) * Valor c/ICMS (Venda)`
- **Descrição**: Valor bruto total da venda incluindo ICMS

---

## 2. Regras de Comissão

### 2.1 Faixas de Comissão por Rentabilidade

| Rentabilidade | Comissão |
|---------------|----------|
| < 20% | 0% |
| 20% - 29,99% | 1% |
| 30% - 39,99% | 1,5% |
| 40% - 49,99% | 2,5% |
| 50% - 59,99% | 3% |
| 60% - 79,99% | 4% |
| ≥ 80% | 5% |

### 2.2 Cálculo de Comissão

#### 2.2.1 Percentual de Comissão
- **Fórmula**: Baseado na tabela de faixas acima
- **Entrada**: Rentabilidade do item em decimal
- **Saída**: Percentual de comissão em decimal

#### 2.2.2 Valor da Comissão
- **Fórmula**: `Valor Comissão = Valor Total * % Comissão`
- **Base de Cálculo**: Valor total COM ICMS
- **Ajuste por Quantidade**: Considera diferenças entre peso de compra e venda

#### 2.2.3 Comissão com Ajuste de Quantidade
- **Regra**: Para diferenças de peso, usa rentabilidade baseada nos totais reais COM ICMS
- **Aplicação**: Quando peso_venda ≠ peso_compra
- **Cálculo**: `rentabilidade_total = (total_venda_com_icms / total_compra_com_icms) - 1`

---

## 3. Regras de Controle de Acesso

### 3.1 Perfis de Usuário

#### 3.1.1 Administrador (ADMIN)
- **Acesso**: Total a todos os orçamentos e funcionalidades
- **Permissões**:
  - Criar, visualizar, editar e excluir qualquer orçamento
  - Gerenciar usuários
  - Acessar relatórios completos
  - Configurar sistema

#### 3.1.2 Vendedor (VENDAS)
- **Acesso**: Apenas aos próprios orçamentos
- **Permissões**:
  - Criar orçamentos (associados automaticamente ao usuário)
  - Visualizar apenas orçamentos próprios
  - Editar apenas orçamentos próprios
  - Exportar PDFs dos próprios orçamentos

### 3.2 Autenticação e Autorização

#### 3.2.1 JWT Token
- **Payload**: `{"sub": username, "role": user_role, "exp": timestamp}`
- **Expiração**: Configurável via settings
- **Validação**: Obrigatória em todos os endpoints protegidos

#### 3.2.2 Filtros Automáticos
- **Admin**: Sem filtros (vê todos os orçamentos)
- **Vendas**: Filtro automático por `created_by = current_user.username`

### 3.3 Validações de Permissão

#### 3.3.1 Modificação de Usuários
- **Admin**: Pode modificar qualquer usuário
- **Usuário**: Pode modificar apenas próprio perfil

#### 3.3.2 Visualização de Dados
- **Admin**: Acesso total
- **Vendas**: Acesso apenas aos próprios dados

---

## 4. Regras de Validação

### 4.1 Validação de Orçamentos

#### 4.1.1 Número do Pedido
- **Regra**: Deve ser único no sistema
- **Validação**: Verificação antes de criar/atualizar
- **Tamanho**: Mínimo 3 caracteres

#### 4.1.2 Cliente
- **Nome**: Mínimo 2 caracteres
- **ID**: Opcional, mas se fornecido deve ser válido

#### 4.1.3 Itens do Orçamento
- **Peso**: Deve ser maior que zero
- **Valores**: Não podem ser negativos
- **ICMS**: Percentual válido (0-1)
- **IPI**: Apenas valores permitidos (0%, 3.25%, 5%)

### 4.2 Validação de Usuários

#### 4.2.1 Credenciais
- **Username**: Mínimo 3 caracteres, único
- **Email**: Formato válido, único
- **Senha**: Mínimo 8 caracteres

#### 4.2.2 Perfil
- **Role**: Deve ser ADMIN ou VENDAS
- **Status**: is_active (boolean)

---

## 5. Regras de IPI

### 5.1 Percentuais Válidos
- **0%**: Produtos não tributados
- **3,25%**: Produtos com tributação reduzida
- **5%**: Produtos com tributação normal

### 5.2 Cálculos de IPI

#### 5.2.1 Valor IPI Unitário
- **Fórmula**: `Valor IPI = valor_com_icms_venda * percentual_ipi`
- **Base**: Valor COM ICMS de venda

#### 5.2.2 Valor IPI Total do Item
- **Fórmula**: `Total IPI = peso_venda * valor_com_icms_venda * percentual_ipi`
- **Aplicação**: Por item do orçamento

#### 5.2.3 Valor Final com IPI
- **Fórmula**: `Valor Final = valor_com_icms_venda * (1 + percentual_ipi)`
- **Descrição**: Valor unitário incluindo IPI

---

## 6. Regras de Frete

### 6.1 Tipos de Frete
- **FOB**: Free On Board (padrão)
- **CIF**: Cost, Insurance and Freight

### 6.2 Cálculo de Frete

#### 6.2.1 Valor Frete por Kg
- **Fórmula**: `Valor Frete/Kg = Valor Frete Total / Peso Total (kg)`
- **Validação**: Peso total deve ser > 0
- **Distribuição**: Proporcional ao peso de cada item

#### 6.2.2 Inclusão no Custo
- **Aplicação**: Frete é incluído no cálculo do valor sem impostos de compra
- **Fórmula**: `outras_despesas_por_kg + frete_distribuido_por_kg`

---

## 7. Regras de Status e Workflow

### 7.1 Status de Orçamento
- **DRAFT**: Rascunho (padrão)
- **SENT**: Enviado ao cliente
- **APPROVED**: Aprovado pelo cliente
- **REJECTED**: Rejeitado pelo cliente
- **EXPIRED**: Expirado

### 7.2 Transições de Status
- **DRAFT → SENT**: Orçamento enviado
- **SENT → APPROVED/REJECTED**: Resposta do cliente
- **Qualquer → EXPIRED**: Data de expiração atingida

### 7.3 Regras de Expiração
- **Data**: Campo `expires_at` opcional
- **Validação**: Se definida, deve ser futura
- **Comportamento**: Status muda automaticamente para EXPIRED

---

## 8. Regras de Integração

### 8.1 Eventos de Sistema
- **Criação de Usuário**: Publicação via Redis
- **Atualização de Usuário**: Publicação via Redis
- **Login de Usuário**: Publicação via Redis
- **Exclusão de Usuário**: Publicação via Redis

---

## 9. Constantes do Sistema

### 9.1 Impostos
- **PIS/COFINS**: 9,25% (0.0925) - fixo
- **ICMS Padrão**: 18% (0.18)
- **IPI Válidos**: 0%, 3.25%, 5%

### 9.2 Comissão
- **Padrão**: 1,5%
- **Mínima**: 0%
- **Máxima**: 5%

### 9.3 Markup
- **Mínimo**: 20%
- **Máximo**: 200%
- **Alvo**: 30%

### 9.4 Validações
- **Precisão Decimal**: 6 casas para cálculos internos
- **Exibição**: 2 casas para valores monetários
- **Arredondamento**: ROUND_HALF_UP

---

## 10. Observações Importantes

### 10.1 Cálculos Fiscais
- **Método**: Cálculo "por dentro" para impostos brasileiros
- **Sequência**: ICMS primeiro, depois PIS/COFINS
- **Base**: Impostos incidem sobre bases que incluem outros tributos

### 10.2 Precisão
- **Decimal**: Uso obrigatório para cálculos financeiros
- **Float**: Apenas para exibição final
- **Arredondamento**: Consistente em todo o sistema

### 10.3 Auditoria
- **Logs**: Todos os cálculos são logados
- **Validação**: Métodos de validação para auditoria
- **Rastreabilidade**: Histórico de alterações mantido

---

*Documento gerado automaticamente a partir da análise do código fonte do CRM Ditual*
*Última atualização: $(date)*