import { useState, useEffect } from 'react';
import {
  Form,
  Card,
  Row,
  Col,
  Input,
  InputNumber,
  Button,
  Space,
  Typography,
  Divider,
  Table,
  message,
  Popconfirm,
  Select,
  DatePicker,
  Alert,
  Statistic,
  Tooltip
} from 'antd';
import {
  PlusOutlined,
  DeleteOutlined,
  CalculatorOutlined,
  SaveOutlined,
  InfoCircleOutlined
} from '@ant-design/icons';
import type { BudgetInput, BudgetItemInput, BudgetPreviewCalculation } from '../../services/budgetService';
import { budgetService } from '../../services/budgetService';
import dayjs from 'dayjs';

const { Title, Text } = Typography;
const { Option } = Select;

interface AutoMarkupBudgetFormProps {
  onSubmit: (data: BudgetInput) => Promise<void>;
  onCancel: () => void;
  isLoading?: boolean;
}

const initialBudgetItem: BudgetItemInput = {
  description: '',
  quantity: 1,
  weight: 0,
  purchase_value_with_icms: 0,
  purchase_icms_percentage: 17, // ICMS padrão Brasil
  market_reference_price: undefined,
  competitor_price: undefined,
};

export default function AutoMarkupBudgetForm({ 
  onSubmit, 
  onCancel, 
  isLoading = false 
}: AutoMarkupBudgetFormProps) {
  const [form] = Form.useForm();
  const [items, setItems] = useState<BudgetItemInput[]>([{ ...initialBudgetItem }]);
  const [calculating, setCalculating] = useState(false);
  const [preview, setPreview] = useState<BudgetPreviewCalculation | null>(null);

  const addItem = () => {
    setItems([...items, { ...initialBudgetItem }]);
  };

  const removeItem = (index: number) => {
    if (items.length > 1) {
      const newItems = items.filter((_, i) => i !== index);
      setItems(newItems);
      setPreview(null); // Limpar preview quando remover item
    } else {
      message.warning('Deve haver pelo menos um item no orçamento');
    }
  };

  const updateItem = (index: number, field: keyof BudgetItemInput, value: any) => {
    const newItems = [...items];
    newItems[index] = { ...newItems[index], [field]: value };
    setItems(newItems);
    setPreview(null); // Limpar preview quando alterar item
  };

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
        expires_at: formData.expires_at ? formData.expires_at.toISOString() : undefined,
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

  const handleSubmit = async () => {
    try {
      const formData = await form.validateFields();
      const budgetData: BudgetInput = {
        ...formData,
        items: items,
        minimum_margin_percentage: formData.minimum_margin_percentage || 20,
        target_market_position: formData.target_market_position || 'competitive',
        expires_at: formData.expires_at ? formData.expires_at.toISOString() : undefined,
      };
      
      await onSubmit(budgetData);
    } catch (error) {
      console.error('Erro na validação do formulário:', error);
    }
  };

  const itemColumns = [
    {
      title: 'Descrição *',
      dataIndex: 'description',
      key: 'description',
      width: 200,
      render: (value: string, _: BudgetItemInput, index: number) => (
        <Input
          value={value}
          onChange={(e) => updateItem(index, 'description', e.target.value)}
          placeholder="Descrição do produto"
          required
        />
      ),
    },
    {
      title: 'Quantidade *',
      dataIndex: 'quantity',
      key: 'quantity',
      width: 120,
      render: (value: number, _: BudgetItemInput, index: number) => (
        <InputNumber
          value={value}
          onChange={(val) => updateItem(index, 'quantity', val || 1)}
          min={0.01}
          step={0.01}
          precision={2}
          style={{ width: '100%' }}
          required
        />
      ),
    },
    {
      title: 'Peso (kg)',
      dataIndex: 'weight',
      key: 'weight',
      width: 120,
      render: (value: number, _: BudgetItemInput, index: number) => (
        <InputNumber
          value={value}
          onChange={(val) => updateItem(index, 'weight', val || 0)}
          min={0}
          step={0.001}
          precision={3}
          style={{ width: '100%' }}
          placeholder="0,000"
        />
      ),
    },
    {
      title: 'Valor c/ICMS (Compra) *',
      dataIndex: 'purchase_value_with_icms',
      key: 'purchase_value_with_icms',
      width: 180,
      render: (value: number, _: BudgetItemInput, index: number) => (
        <InputNumber
          value={value}
          onChange={(val) => updateItem(index, 'purchase_value_with_icms', val || 0)}
          min={0.01}
          step={0.01}
          precision={2}
          formatter={(value) => `R$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
          parser={(value) => value!.replace(/R\$\s?|(,*)/g, '')}
          style={{ width: '100%' }}
          required
        />
      ),
    },
    {
      title: '% ICMS *',
      dataIndex: 'purchase_icms_percentage',
      key: 'purchase_icms_percentage',
      width: 120,
      render: (value: number, _: BudgetItemInput, index: number) => (
        <InputNumber
          value={value}
          onChange={(val) => updateItem(index, 'purchase_icms_percentage', val || 17)}
          min={0}
          max={100}
          step={0.1}
          precision={1}
          formatter={(value) => `${value}%`}
          parser={(value) => value!.replace('%', '')}
          style={{ width: '100%' }}
          required
        />
      ),
    },
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
    {
      title: 'Preço Concorrente',
      dataIndex: 'competitor_price',
      key: 'competitor_price',
      width: 160,
      render: (value: number, _: BudgetItemInput, index: number) => (
        <InputNumber
          value={value}
          onChange={(val) => updateItem(index, 'competitor_price', val || undefined)}
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
    {
      title: 'Ações',
      key: 'actions',
      width: 80,
      fixed: 'right' as const,
      render: (_: any, __: BudgetItemInput, index: number) => (
        <Popconfirm
          title="Remover item"
          description="Tem certeza que deseja remover este item?"
          onConfirm={() => removeItem(index)}
          okText="Sim"
          cancelText="Não"
          disabled={items.length <= 1}
        >
          <Button
            type="text"
            danger
            icon={<DeleteOutlined />}
            disabled={items.length <= 1}
          />
        </Popconfirm>
      ),
    },
  ];

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          initialValues={{
            minimum_margin_percentage: 20,
            target_market_position: 'competitive',
          }}
        >
          <Row justify="space-between" align="middle" style={{ marginBottom: '24px' }}>
            <Col>
              <Title level={3} style={{ margin: 0 }}>
                Novo Orçamento com Markup Automático 💼
              </Title>
              <Text type="secondary">
                Preencha apenas os campos essenciais. O markup será calculado automaticamente baseado em análise de mercado.
              </Text>
            </Col>
            <Col>
              <Space>
                <Button onClick={onCancel}>
                  Cancelar
                </Button>
                <Button
                  icon={<CalculatorOutlined />}
                  onClick={calculatePreview}
                  loading={calculating}
                  type="default"
                >
                  Calcular Preview
                </Button>
                <Button
                  type="primary"
                  icon={<SaveOutlined />}
                  htmlType="submit"
                  loading={isLoading}
                >
                  Salvar Orçamento
                </Button>
              </Space>
            </Col>
          </Row>

          {/* Informações Básicas */}
          <Row gutter={[16, 16]}>
            <Col xs={24} md={8}>
              <Form.Item
                label="Número do Pedido"
                name="order_number"
                rules={[{ required: true, message: 'Número do pedido é obrigatório' }]}
              >
                <Input placeholder="Ex: PED-2024-001" />
              </Form.Item>
            </Col>
            <Col xs={24} md={8}>
              <Form.Item
                label="Cliente"
                name="client_name"
                rules={[{ required: true, message: 'Nome do cliente é obrigatório' }]}
              >
                <Input placeholder="Nome do cliente" />
              </Form.Item>
            </Col>
            <Col xs={24} md={8}>
              <Form.Item
                label="Data de Expiração"
                name="expires_at"
              >
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>

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
            <Col xs={24} md={8}>
              <Form.Item
                label="Observações"
                name="notes"
              >
                <Input.TextArea rows={2} placeholder="Observações adicionais..." />
              </Form.Item>
            </Col>
          </Row>

          {/* Alerta explicativo */}
          <Alert
            message="Markup Calculado Automaticamente"
            description="O markup será calculado automaticamente baseado nos custos, margem mínima configurada, posicionamento de mercado e preços de referência informados."
            type="info"
            icon={<InfoCircleOutlined />}
            style={{ marginBottom: '24px' }}
            showIcon
          />

          <Divider>Itens do Orçamento</Divider>

          <div style={{ marginBottom: '16px' }}>
            <Button
              type="dashed"
              icon={<PlusOutlined />}
              onClick={addItem}
              style={{ width: '100%' }}
            >
              Adicionar Item
            </Button>
          </div>

          <div style={{ overflowX: 'auto' }}>
            <Table
              dataSource={items}
              columns={itemColumns}
              pagination={false}
              rowKey={(_, index) => index!}
              scroll={{ x: 1200 }}
              size="small"
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
                <Col xs={12} md={6}>
                  <Card>
                    <Statistic
                      title="Total Compra"
                      value={preview.total_purchase_value}
                      formatter={(value) => `R$ ${Number(value).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`}
                      valueStyle={{ color: '#ff4d4f' }}
                    />
                  </Card>
                </Col>
                <Col xs={12} md={6}>
                  <Card>
                    <Statistic
                      title="Total Venda"
                      value={preview.total_sale_value}
                      formatter={(value) => `R$ ${Number(value).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`}
                      valueStyle={{ color: '#52c41a' }}
                    />
                  </Card>
                </Col>
                <Col xs={12} md={6}>
                  <Card>
                    <Statistic
                      title="Rentabilidade"
                      value={preview.profitability_percentage}
                      formatter={(value) => `${Number(value).toFixed(1)}%`}
                      valueStyle={{ 
                        color: Number(preview.profitability_percentage) > 20 ? '#52c41a' : 
                               Number(preview.profitability_percentage) > 10 ? '#faad14' : '#ff4d4f'
                      }}
                    />
                  </Card>
                </Col>
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
