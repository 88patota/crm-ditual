
## ARQUIVOS A SEREM MODIFICADOS

### 1. Backend - Schemas

**Arquivo**: `services/budget_service/app/schemas/budget.py`

**Alterações**:
- Remover `markup_percentage` dos campos editáveis em `BudgetInputBase`
- Adicionar `markup_percentage` apenas como campo de resposta calculado
- Criar novo schema `BudgetMarketAnalysis` para análise de preços de mercado

### 2. Backend - Calculadora

**Arquivo**: `services/budget_service/app/services/budget_calculator.py`

**Alterações**:
- Implementar função `calculate_automatic_markup()`
- Adicionar configurações de markup mínimo/máximo
- Implementar análise de preços de mercado
- Ajustar `calculate_item_from_input()` para não receber markup como parâmetro

### 3. Backend - Endpoints

**Arquivo**: `services/budget_service/app/api/v1/endpoints/budgets.py`

**Alterações**:
- Modificar endpoint `/simplified` para calcular markup automaticamente
- Adicionar endpoint `/analyze-market-prices` para análise de preços
- Remover parâmetro `markup_percentage` dos endpoints de cálculo

### 4. Frontend - Schemas de Serviço

**Arquivo**: `frontend/src/services/budgetService.ts`

**Alterações**:
- Remover `markup_percentage` de `BudgetInput`
- Adicionar `calculated_markup_percentage` em `BudgetPreviewCalculation`
- Adicionar serviços para análise de mercado

### 5. Frontend - Formulário Simplificado

**Arquivo**: `frontend/src/components/budgets/SimplifiedBudgetForm.tsx`

**Alterações**:
- Remover campo de entrada `markup_percentage`
- Adicionar exibição do markup calculado
- Implementar sugestões de preços de mercado

### 6. Frontend - Configurações do Sistema

**Novo arquivo**: `frontend/src/components/settings/MarkupSettings.tsx`

**Função**: Permitir configuração de parâmetros de markup pelo administrador

## IMPLEMENTAÇÃO DETALHADA

### 1. Novo Schema para Entrada Simplificada

```python
# services/budget_service/app/schemas/budget.py

class BudgetItemInput(BaseModel):
    """Schema simplificado - campos que o vendedor pode preencher"""
    description: str
    quantity: float = 1.0
    weight: Optional[float] = None
    purchase_value_with_icms: float
    purchase_icms_percentage: float = 17.0
    
    # REMOVER: markup_percentage (será calculado automaticamente)
    
    # NOVO: Análise de mercado (opcional)
    market_reference_price: Optional[float] = None
    competitor_price: Optional[float] = None

class BudgetInputCreate(BudgetInputBase):
    """Schema para criação sem markup manual"""
    items: List[BudgetItemInput] = []
    
    # REMOVER: markup_percentage (será calculado automaticamente)
    
    # NOVO: Configurações de negócio
    minimum_margin_percentage: Optional[float] = 20.0  # Margem mínima desejada
    target_market_position: Optional[str] = "competitive"  # competitive, premium, budget

class MarkupConfiguration(BaseModel):
    """Configurações do sistema para cálculo de markup"""
    minimum_markup_percentage: float = 20.0
    maximum_markup_percentage: float = 200.0
    default_market_position: str = "competitive"
    icms_sale_default: float = 17.0
    commission_default: float = 1.5
    other_expenses_default: float = 0.0
```

### 2. Nova Lógica de Cálculo de Markup

```python
# services/budget_service/app/services/budget_calculator.py

class BudgetCalculatorService:
    
    # Configurações padrão do sistema
    DEFAULT_MINIMUM_MARKUP = 20.0  # 20% mínimo
    DEFAULT_MAXIMUM_MARKUP = 200.0  # 200% máximo
    DEFAULT_TARGET_MARGIN = 30.0   # 30% margem alvo
    
    @staticmethod
    def calculate_automatic_markup(item_input: BudgetItemInput, business_config: dict = None) -> float:
        """
        Calcula markup automaticamente baseado em:
        1. Custos totais do item
        2. Preços de referência de mercado (se disponível)
        3. Margem mínima configurada
        4. Posicionamento de mercado desejado
        """
        
        # 1. Calcular custo total
        purchase_value_without_taxes = item_input.purchase_value_with_icms * (1 - item_input.purchase_icms_percentage / 100)
        other_expenses = business_config.get('other_expenses_default', BudgetCalculatorService.DEFAULT_OTHER_EXPENSES)
        total_cost = purchase_value_without_taxes + other_expenses
        
        # 2. Determinar preço de venda baseado em referências de mercado
        if item_input.market_reference_price:
            # Se há preço de referência, usar como base
            target_sale_price = item_input.market_reference_price
        elif item_input.competitor_price:
            # Se há preço de concorrente, aplicar estratégia
            position = business_config.get('target_market_position', 'competitive')
            if position == 'premium':
                target_sale_price = item_input.competitor_price * 1.1  # 10% acima
            elif position == 'budget':
                target_sale_price = item_input.competitor_price * 0.95  # 5% abaixo
            else:  # competitive
                target_sale_price = item_input.competitor_price * 1.02  # 2% acima
        else:
            # Sem referência de mercado, usar margem mínima
            minimum_margin = business_config.get('minimum_margin_percentage', BudgetCalculatorService.DEFAULT_TARGET_MARGIN)
            target_sale_price = total_cost * (1 + minimum_margin / 100)
        
        # 3. Calcular markup resultante
        if total_cost > 0:
            calculated_markup = ((target_sale_price - total_cost) / total_cost) * 100
        else:
            calculated_markup = BudgetCalculatorService.DEFAULT_TARGET_MARGIN
        
        # 4. Aplicar limites mínimo e máximo
        min_markup = business_config.get('minimum_markup_percentage', BudgetCalculatorService.DEFAULT_MINIMUM_MARKUP)
        max_markup = business_config.get('maximum_markup_percentage', BudgetCalculatorService.DEFAULT_MAXIMUM_MARKUP)
        
        calculated_markup = max(min_markup, min(calculated_markup, max_markup))
        
        return round(calculated_markup, 2)
    
    @staticmethod
    def calculate_budget_from_inputs_auto_markup(items_input: List[BudgetItemInput], business_config: dict = None) -> Dict[str, Any]:
        """
        Calcula orçamento completo com markup automático para cada item
        """
        if business_config is None:
            business_config = {}
        
        calculated_items = []
        total_purchase_value = 0.0
        total_sale_value = 0.0
        total_commission = 0.0
        markups_calculated = []
        
        for item_input in items_input:
            # Calcular markup automático para este item
            item_markup = BudgetCalculatorService.calculate_automatic_markup(item_input, business_config)
            markups_calculated.append(item_markup)
            
            # Calcular valores do item com o markup calculado
            calculated_item = BudgetCalculatorService.calculate_item_from_input(item_input, item_markup)
            calculated_items.append(calculated_item)
            
            total_purchase_value += calculated_item['total_purchase']
            total_sale_value += calculated_item['total_sale']
            total_commission += calculated_item['commission_value']
        
        # Calcular markup médio ponderado do orçamento
        if total_purchase_value > 0:
            overall_markup = ((total_sale_value - total_purchase_value) / total_purchase_value) * 100
        else:
            overall_markup = 0.0
        
        # Calcular rentabilidade geral
        if total_purchase_value > 0:
            profitability_percentage = ((total_sale_value - total_purchase_value) / total_purchase_value) * 100
        else:
            profitability_percentage = 0.0
        
        return {
            'items': calculated_items,
            'totals': {
                'total_purchase_value': total_purchase_value,
                'total_sale_value': total_sale_value,
                'total_commission': total_commission,
                'profitability_percentage': profitability_percentage,
                'markup_percentage': overall_markup,  # Markup calculado automaticamente
                'individual_markups': markups_calculated  # Markup de cada item
            },
            'settings': {
                'commission_percentage_default': BudgetCalculatorService.DEFAULT_COMMISSION_PERCENTAGE,
                'sale_icms_percentage_default': BudgetCalculatorService.DEFAULT_SALE_ICMS_PERCENTAGE,
                'other_expenses_default': BudgetCalculatorService.DEFAULT_OTHER_EXPENSES,
                'minimum_markup_applied': business_config.get('minimum_markup_percentage', BudgetCalculatorService.DEFAULT_MINIMUM_MARKUP),
                'maximum_markup_applied': business_config.get('maximum_markup_percentage', BudgetCalculatorService.DEFAULT_MAXIMUM_MARKUP)
            }
        }
```

### 3. Novo Endpoint para Configurações

```python
# services/budget_service/app/api/v1/endpoints/budgets.py

@router.get("/markup-settings", response_model=MarkupConfiguration)
async def get_markup_settings():
    """Obter configurações de markup do sistema"""
    return MarkupConfiguration(
        minimum_markup_percentage=20.0,
        maximum_markup_percentage=200.0,
        default_market_position="competitive",
        icms_sale_default=17.0,
        commission_default=1.5,
        other_expenses_default=0.0
    )

@router.post("/calculate-auto-markup", response_model=BudgetPreviewCalculation)
async def calculate_budget_auto_markup(
    budget_data: BudgetInputCreate
):
    """Calcular orçamento com markup automático"""
    try:
        # Validar dados
        budget_dict = budget_data.dict()
        errors = BudgetCalculatorService.validate_budget_input_data(budget_dict)
        if errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Dados inválidos: {'; '.join(errors)}"
            )
        
        # Preparar configurações de negócio
        business_config = {
            'minimum_margin_percentage': budget_data.minimum_margin_percentage,
            'target_market_position': budget_data.target_market_position,
            'minimum_markup_percentage': 20.0,  # Configurável
            'maximum_markup_percentage': 200.0,  # Configurável
            'other_expenses_default': 0.0,
            'commission_percentage_default': 1.5,
            'sale_icms_percentage_default': 17.0
        }
        
        # Calcular com markup automático
        calculation_result = BudgetCalculatorService.calculate_budget_from_inputs_auto_markup(
            budget_data.items, 
            business_config
        )
        
        # Preparar resposta
        items_preview = []
        for i, item in enumerate(calculation_result['items']):
            items_preview.append({
                'description': item['description'],
                'quantity': item['quantity'],
                'purchase_value_with_icms': item['purchase_value_with_icms'],
                'calculated_markup': calculation_result['totals']['individual_markups'][i],
                'sale_value_with_icms': item['sale_value_with_icms'],
                'total_purchase': item['total_purchase'],
                'total_sale': item['total_sale'],
                'profitability': item['profitability'],
                'commission_value': item['commission_value']
            })
        
        return BudgetPreviewCalculation(
            total_purchase_value=calculation_result['totals']['total_purchase_value'],
            total_sale_value=calculation_result['totals']['total_sale_value'],
            total_commission=calculation_result['totals']['total_commission'],
            profitability_percentage=calculation_result['totals']['profitability_percentage'],
            markup_percentage=calculation_result['totals']['markup_percentage'],  # CALCULADO AUTO
            items_preview=items_preview,
            commission_percentage_default=calculation_result['settings']['commission_percentage_default'],
            sale_icms_percentage_default=calculation_result['settings']['sale_icms_percentage_default'],
            other_expenses_default=calculation_result['settings']['other_expenses_default'],
            # NOVOS CAMPOS
            minimum_markup_applied=calculation_result['settings']['minimum_markup_applied'],
            maximum_markup_applied=calculation_result['settings']['maximum_markup_applied']
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
```

### 4. Frontend - Formulário Atualizado

```typescript
// frontend/src/components/budgets/AutoMarkupBudgetForm.tsx

interface AutoMarkupBudgetFormProps {
  onSubmit: (data: BudgetInput) => Promise<void>;
  onCancel: () => void;
  isLoading?: boolean;
}

export default function AutoMarkupBudgetForm({ 
  onSubmit, 
  onCancel, 
  isLoading = false 
}: AutoMarkupBudgetFormProps) {
  const [form] = Form.useForm();
  const [items, setItems] = useState<BudgetItemInput[]>([{ ...initialBudgetItem }]);
  const [calculating, setCalculating] = useState(false);
  const [preview, setPreview] = useState<BudgetPreviewCalculation | null>(null);

  const calculatePreview = async () => {
    try {
      setCalculating(true);
      const formData = form.getFieldsValue();
      
      const budgetData: BudgetInput = {
        ...formData,
        items: items,
        // REMOVIDO: markup_percentage
        minimum_margin_percentage: formData.minimum_margin_percentage || 20,
        target_market_position: formData.target_market_position || 'competitive',
      };
      
      // NOVO ENDPOINT: calcular com markup automático
      const calculation = await budgetService.calculateBudgetAutoMarkup(budgetData);
      setPreview(calculation);
      
      message.success(`Markup calculado automaticamente: ${calculation.markup_percentage.toFixed(1)}%`);
    } catch (error) {
      console.error('Erro ao calcular orçamento:', error);
      message.error('Erro ao calcular orçamento');
    } finally {
      setCalculating(false);
    }
  };

  // Campos do formulário ATUALIZADOS
  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <Form form={form} layout="vertical" onFinish={handleSubmit}>
          {/* Informações básicas - SEM campo markup */}
          <Row gutter={[16, 16]}>
            <Col xs={24} md={8}>
              <Form.Item
                label="Margem Mínima Desejada (%)"
                name="minimum_margin_percentage"
                extra="Margem mínima de lucro desejada"
              >
                <InputNumber
                  min={5}
                  max={100}
                  step={0.1}
                  precision={1}
                  formatter={(value) => `${value}%`}
                  parser={(value) => value!.replace('%', '')}
                  style={{ width: '100%' }}
                  defaultValue={20}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={8}>
              <Form.Item
                label="Posicionamento de Mercado"
                name="target_market_position"
                extra="Estratégia de preços em relação aos concorrentes"
              >
                <Select defaultValue="competitive">
                  <Option value="budget">Econômico (5% abaixo da concorrência)</Option>
                  <Option value="competitive">Competitivo (2% acima da concorrência)</Option>
                  <Option value="premium">Premium (10% acima da concorrência)</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          {/* Tabela de itens ATUALIZADA */}
          <div style={{ overflowX: 'auto' }}>
            <Table
              dataSource={items}
              columns={[
                // ... colunas existentes ...
                {
                  title: 'Preço Referência Mercado',
                  dataIndex: 'market_reference_price',
                  key: 'market_reference_price',
                  width: 180,
                  render: (value: number, _: BudgetItemInput, index: number) => (
                    <InputNumber
                      value={value}
                      onChange={(val) => updateItem(index, 'market_reference_price', val || undefined)}
                      min={0}
                      step={0.01}
                      precision={2}
                      formatter={(value) => `R$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                      parser={(value) => value!.replace(/R\$\s?|(,*)/g, '')}
                      style={{ width: '100%' }}
                      placeholder="Opcional"
                    />
                  ),
                },
                // ... outras colunas ...
              ]}
            />
          </div>

          {/* Preview dos Cálculos ATUALIZADO */}
          {preview && (
            <>
              <Divider>Cálculos Automáticos</Divider>
              
              <Alert
                message="Markup Calculado Automaticamente"
                description={`
                  Markup aplicado: ${preview.markup_percentage.toFixed(1)}% 
                  (Baseado em análise de custos, margem mínima e posicionamento de mercado)
                `}
                type="success"
                icon={<InfoCircleOutlined />}
                style={{ marginBottom: '16px' }}
                showIcon
              />

              {/* Stats cards com markup calculado */}
              <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
                <Col xs={12} md={6}>
                  <Card>
                    <Statistic
                      title="Markup Calculado"
                      value={preview.markup_percentage}
                      formatter={(value) => `${Number(value).toFixed(1)}%`}
                      valueStyle={{ color: '#1890ff', fontSize: '24px' }}
                      prefix={<CalculatorOutlined />}
                    />
                  </Card>
                </Col>
                {/* ... outros cards de estatísticas ... */}
              </Row>

              <Card title="Configurações Aplicadas" size="small">
                <Text>
                  • Markup calculado automaticamente baseado em análise de mercado<br/>
                  • Margem mínima: {preview.minimum_markup_applied}%<br/>
                  • Margem máxima: {preview.maximum_markup_applied}%<br/>
                  • Comissão: {preview.commission_percentage_default}%<br/>
                  • ICMS venda: {preview.sale_icms_percentage_default}%
                </Text>
              </Card>
            </>
          )}
        </Form>
      </Card>
    </div>
  );
}
```

### 5. Atualização do Serviço Frontend

```typescript
// frontend/src/services/budgetService.ts

// Tipos atualizados
export interface BudgetItemInput {
  description: string;
  quantity: number;
  weight?: number;
  purchase_value_with_icms: number;
  purchase_icms_percentage: number;
  // NOVOS CAMPOS
  market_reference_price?: number;
  competitor_price?: number;
}

export interface BudgetInput {
  order_number: string;
  client_name: string;
  // REMOVIDO: markup_percentage
  notes?: string;
  expires_at?: string;
  items: BudgetItemInput[];
  // NOVOS CAMPOS
  minimum_margin_percentage?: number;
  target_market_position?: 'budget' | 'competitive' | 'premium';
}

export interface BudgetPreviewCalculation {
  total_purchase_value: number;
  total_sale_value: number;
  total_commission: number;
  profitability_percentage: number;
  markup_percentage: number; // CALCULADO AUTOMATICAMENTE
  items_preview: Array<{
    description: string;
    quantity: number;
    purchase_value_with_icms: number;
    calculated_markup: number; // NOVO: markup individual calculado
    sale_value_with_icms: number;
    total_purchase: number;
    total_sale: number;
    profitability: number;
    commission_value: number;
  }>;
  commission_percentage_default: number;
  sale_icms_percentage_default: number;
  other_expenses_default: number;
  // NOVOS CAMPOS
  minimum_markup_applied: number;
  maximum_markup_applied: number;
}

// Serviços atualizados
export const budgetService = {
  // NOVO MÉTODO
  async calculateBudgetAutoMarkup(budget: BudgetInput): Promise<BudgetPreviewCalculation> {
    const response = await api.post<BudgetPreviewCalculation>('/budgets/calculate-auto-markup', budget);
    return response.data;
  },

  // NOVO MÉTODO
  async getMarkupSettings(): Promise<MarkupConfiguration> {
    const response = await api.get<MarkupConfiguration>('/budgets/markup-settings');
    return response.data;
  },

  // Método atualizado
  async createBudgetSimplified(budget: BudgetInput): Promise<Budget> {
    // Agora usa cálculo automático de markup
    const response = await api.post<Budget>('/budgets/simplified-auto', budget);
    return response.data;
  },

  // ... outros métodos existentes ...
};
```

## TESTES E VALIDAÇÃO

### 1. Testes Unitários
- Testar função `calculate_automatic_markup()` com diferentes cenários
- Validar limites mínimos e máximos
- Testar com e sem preços de referência

### 2. Testes de Integração
- Testar endpoint `/calculate-auto-markup`
- Validar criação de orçamentos com markup automático
- Testar configurações personalizadas

### 3. Testes de UI
- Verificar que campo markup não é mais editável
- Validar exibição de markup calculado
- Testar formulário com diferentes posicionamentos de mercado

## CRONOGRAMA DE IMPLEMENTAÇÃO

### Fase 1 (2-3 dias): Backend Core
1. Atualizar schemas para remover markup editável
2. Implementar função de cálculo automático de markup
3. Criar novos endpoints

### Fase 2 (2 dias): Frontend
1. Atualizar formulários para remover campo markup
2. Implementar exibição de markup calculado
3. Adicionar campos de análise de mercado

### Fase 3 (1 dia): Testes e Ajustes
1. Testes unitários e integração
2. Validação com dados reais
3. Ajustes finos na fórmula

### Fase 4 (1 dia): Configurações Admin
1. Interface para configurar parâmetros de markup
2. Documentação das regras de negócio
3. Treinamento para usuários

## CONFIGURAÇÕES RECOMENDADAS

### Parâmetros Padrão do Sistema
```python
DEFAULT_MARKUP_SETTINGS = {
    'minimum_markup_percentage': 20.0,  # 20% mínimo
    'maximum_markup_percentage': 200.0,  # 200% máximo
    'target_margin_default': 30.0,     # 30% margem padrão
    'icms_sale_default': 17.0,         # 17% ICMS venda
    'commission_default': 1.5,         # 1,5% comissão
    'other_expenses_default': 0.0,     # R$ 0,00 outras despesas
    'market_position_default': 'competitive'
}
```

Este arquivo fornece uma visão completa de como implementar o markup automático no sistema, mantendo a simplicidade para o vendedor enquanto aplica regras de negócio sofisticadas nos bastidores.