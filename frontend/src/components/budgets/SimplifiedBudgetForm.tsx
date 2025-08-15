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
  Spin
} from 'antd';
import {
  PlusOutlined,
  DeleteOutlined,
  CalculatorOutlined,
  SaveOutlined,
  InfoCircleOutlined,
  ReloadOutlined
} from '@ant-design/icons';
import type { BudgetSimplified, BudgetItemSimplified, BudgetCalculation } from '../../services/budgetService';
import { budgetService } from '../../services/budgetService';
import dayjs from 'dayjs';
import { formatCurrency } from '../../lib/utils';

const { Title, Text } = Typography;
const { Option } = Select;

// Funções utilitárias para formatação de moeda brasileira
const formatBRLCurrency = (value: number | string | undefined): string => {
  if (!value && value !== 0) return '';
  const numValue = typeof value === 'string' ? parseFloat(value) : value;
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(numValue);
};

const parseBRLCurrency = (value: string | undefined): number => {
  if (!value) return 0;
  // Remove R$, espaços, pontos (separadores de milhares) e substitui vírgula por ponto
  const cleanValue = value
    .replace(/R\$\s?/g, '')
    .replace(/\./g, '')
    .replace(/,/g, '.');
  return parseFloat(cleanValue) || 0;
};

interface SimplifiedBudgetFormProps {
  onSubmit: (data: BudgetSimplified) => Promise<void>;
  onCancel: () => void;
  isLoading?: boolean;
}

const initialBudgetItem: BudgetItemSimplified = {
  description: '',
  quantity: 1,
  weight: 0,
  purchase_value_with_icms: 0,
  purchase_icms_percentage: 17,
  purchase_other_expenses: 0,
  sale_value_with_icms: 0,
  sale_icms_percentage: 17,
};

export default function SimplifiedBudgetForm({ 
  onSubmit, 
  onCancel, 
  isLoading = false 
}: SimplifiedBudgetFormProps) {
  const [form] = Form.useForm();
  const [items, setItems] = useState<BudgetItemSimplified[]>([{ ...initialBudgetItem }]);
  const [calculating, setCalculating] = useState(false);
  const [preview, setPreview] = useState<BudgetCalculation | null>(null);
  const [orderNumber, setOrderNumber] = useState<string>('');
  const [loadingOrderNumber, setLoadingOrderNumber] = useState(true);

  // Carregar número do pedido ao inicializar o componente
  useEffect(() => {
    loadNextOrderNumber();
  }, []);

  const loadNextOrderNumber = async () => {
    try {
      setLoadingOrderNumber(true);
      const nextNumber = await budgetService.getNextOrderNumber();
      setOrderNumber(nextNumber);
      form.setFieldValue('order_number', nextNumber);
    } catch (error) {
      console.error('Erro ao carregar número do pedido:', error);
      message.error('Erro ao gerar número do pedido');
    } finally {
      setLoadingOrderNumber(false);
    }
  };

  const addItem = () => {
    setItems([...items, { ...initialBudgetItem }]);
  };

  const removeItem = (index: number) => {
    if (items.length > 1) {
      const newItems = items.filter((_, i) => i !== index);
      setItems(newItems);
      setPreview(null);
    } else {
      message.warning('Deve haver pelo menos um item no orçamento');
    }
  };

  const updateItem = (index: number, field: keyof BudgetItemSimplified, value: any) => {
    const newItems = [...items];
    newItems[index] = { ...newItems[index], [field]: value };
    setItems(newItems);
    setPreview(null);
  };

  const calculatePreview = async () => {
    try {
      setCalculating(true);
      const formData = form.getFieldsValue();
      
      const budgetData: BudgetSimplified = {
        ...formData,
        order_number: orderNumber, // Usar o número gerado
        items: items,
        expires_at: formData.expires_at ? formData.expires_at.toISOString() : undefined,
      };
      
      const calculation = await budgetService.calculateBudgetSimplified(budgetData);
      setPreview(calculation);
      
      message.success(`Cálculos realizados! Markup: ${calculation.markup_percentage.toFixed(1)}%`);
    } catch (error) {
      console.error('Erro ao calcular orçamento:', error);
      message.error('Erro ao calcular orçamento. Verifique se todos os campos obrigatórios estão preenchidos.');
    } finally {
      setCalculating(false);
    }
  };

  const handleSubmit = async () => {
    try {
      const formData = await form.validateFields();
      const budgetData: BudgetSimplified = {
        ...formData,
        order_number: orderNumber, // Usar o número gerado automaticamente
        items: items,
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
      render: (value: string, _: BudgetItemSimplified, index: number) => (
        <Input
          value={value}
          onChange={(e) => updateItem(index, 'description', e.target.value)}
          placeholder="Descrição do produto"
        />
      ),
    },
    {
      title: 'Quantidade *',
      dataIndex: 'quantity',
      key: 'quantity',
      width: 120,
      render: (value: number, _: BudgetItemSimplified, index: number) => (
        <InputNumber
          value={value}
          onChange={(val) => updateItem(index, 'quantity', val || 1)}
          min={0.01}
          step={0.01}
          precision={2}
          style={{ width: '100%' }}
        />
      ),
    },
    {
      title: 'Peso (kg)',
      dataIndex: 'weight',
      key: 'weight',
      width: 120,
      render: (value: number, _: BudgetItemSimplified, index: number) => (
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
      render: (value: number, _: BudgetItemSimplified, index: number) => (
        <InputNumber
          value={value}
          onChange={(val) => updateItem(index, 'purchase_value_with_icms', val || 0)}
          min={0.01}
          step={0.01}
          precision={2}
          formatter={formatBRLCurrency}
          parser={parseBRLCurrency}
          style={{ width: '100%' }}
        />
      ),
    },
    {
      title: '% ICMS (Compra) *',
      dataIndex: 'purchase_icms_percentage',
      key: 'purchase_icms_percentage',
      width: 140,
      render: (value: number, _: BudgetItemSimplified, index: number) => (
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
        />
      ),
    },
    {
      title: 'Outras Despesas',
      dataIndex: 'purchase_other_expenses',
      key: 'purchase_other_expenses',
      width: 150,
      render: (value: number, _: BudgetItemSimplified, index: number) => (
        <InputNumber
          value={value}
          onChange={(val) => updateItem(index, 'purchase_other_expenses', val || 0)}
          min={0}
          step={0.01}
          precision={2}
          formatter={formatBRLCurrency}
          parser={parseBRLCurrency}
          style={{ width: '100%' }}
          placeholder="0,00"
        />
      ),
    },
    {
      title: 'Valor c/ICMS (Venda) *',
      dataIndex: 'sale_value_with_icms',
      key: 'sale_value_with_icms',
      width: 180,
      render: (value: number, _: BudgetItemSimplified, index: number) => (
        <InputNumber
          value={value}
          onChange={(val) => updateItem(index, 'sale_value_with_icms', val || 0)}
          min={0.01}
          step={0.01}
          precision={2}
          formatter={formatBRLCurrency}
          parser={parseBRLCurrency}
          style={{ width: '100%' }}
        />
      ),
    },
    {
      title: '% ICMS (Venda) *',
      dataIndex: 'sale_icms_percentage',
      key: 'sale_icms_percentage',
      width: 140,
      render: (value: number, _: BudgetItemSimplified, index: number) => (
        <InputNumber
          value={value}
          onChange={(val) => updateItem(index, 'sale_icms_percentage', val || 17)}
          min={0}
          max={100}
          step={0.1}
          precision={1}
          formatter={(value) => `${value}%`}
          parser={(value) => value!.replace('%', '')}
          style={{ width: '100%' }}
        />
      ),
    },
    {
      title: 'Ações',
      key: 'actions',
      width: 80,
      fixed: 'right' as const,
      render: (_: any, __: BudgetItemSimplified, index: number) => (
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
            status: 'draft',
          }}
        >
          <Row justify="space-between" align="middle" style={{ marginBottom: '24px' }}>
            <Col>
              <Space direction="vertical" size={4}>
                <Title level={3} style={{ margin: 0 }}>
                  Novo Orçamento Simplificado 💼
                </Title>
                <div style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '12px',
                  padding: '8px 12px',
                  backgroundColor: '#f0f9ff',
                  borderRadius: '6px',
                  border: '1px solid #bae6fd'
                }}>
                  {loadingOrderNumber ? (
                    <>
                      <Spin size="small" />
                      <Text type="secondary">Gerando número do pedido...</Text>
                    </>
                  ) : (
                    <>
                      <Text strong style={{ color: '#0369a1' }}>
                        Número do Pedido: {orderNumber}
                      </Text>
                      <Button 
                        type="link" 
                        size="small" 
                        icon={<ReloadOutlined />}
                        onClick={loadNextOrderNumber}
                        loading={loadingOrderNumber}
                        title="Gerar novo número"
                      >
                        Gerar novo
                      </Button>
                    </>
                  )}
                </div>
                <Text type="secondary">
                  Preencha os campos obrigatórios. O número será mantido durante a criação do orçamento.
                </Text>
              </Space>
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
                  Calcular
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
                extra="Número gerado automaticamente pelo sistema"
              >
                <Input
                  value={orderNumber}
                  readOnly
                  prefix={loadingOrderNumber ? <Spin size="small" /> : null}
                  suffix={
                    <Button 
                      type="text" 
                      size="small" 
                      icon={<ReloadOutlined />}
                      onClick={loadNextOrderNumber}
                      loading={loadingOrderNumber}
                      title="Gerar novo número"
                    />
                  }
                  placeholder={loadingOrderNumber ? "Gerando número..." : "PED-0001"}
                />
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
                label="Status"
                name="status"
              >
                <Select>
                  <Option value="draft">Rascunho</Option>
                  <Option value="pending">Pendente</Option>
                  <Option value="approved">Aprovado</Option>
                  <Option value="rejected">Rejeitado</Option>
                  <Option value="expired">Expirado</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={[16, 16]}>
            <Col xs={24} md={8}>
              <Form.Item
                label="Data de Expiração"
                name="expires_at"
              >
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col xs={24} md={16}>
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
            message="Campos Obrigatórios"
            description="Preencha: Cliente, Descrição, Quantidade, Valor c/ICMS (Compra), % ICMS (Compra), Valor c/ICMS (Venda) e % ICMS (Venda). Os demais campos serão calculados automaticamente."
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
              scroll={{ x: 1400 }}
              size="small"
            />
          </div>

          {/* Preview dos Cálculos */}
          {preview && (
            <>
              <Divider>Cálculos Realizados</Divider>
              
              <Alert
                message="Sucesso!"
                description={`Todos os cálculos foram realizados com base nas fórmulas. Markup calculado: ${preview.markup_percentage.toFixed(1)}%`}
                type="success"
                icon={<InfoCircleOutlined />}
                style={{ marginBottom: '16px' }}
                showIcon
              />

              <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
                <Col xs={12} md={6}>
                  <Card>
                    <Statistic
                      title="Total Compra"
                      value={preview.total_purchase_value}
                      formatter={(value) => formatCurrency(Number(value))}
                      valueStyle={{ color: '#ff4d4f' }}
                    />
                  </Card>
                </Col>
                <Col xs={12} md={6}>
                  <Card>
                    <Statistic
                      title="Total Venda"
                      value={preview.total_sale_value}
                      formatter={(value) => formatCurrency(Number(value))}
                      valueStyle={{ color: '#52c41a' }}
                    />
                  </Card>
                </Col>
                <Col xs={12} md={6}>
                  <Card>
                    <Statistic
                      title="Markup Calculado"
                      value={preview.markup_percentage}
                      formatter={(value) => `${Number(value).toFixed(1)}%`}
                      valueStyle={{ color: '#1890ff' }}
                      prefix={<CalculatorOutlined />}
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
            </>
          )}
        </Form>
      </Card>
    </div>
  );
}
