import { useState } from 'react';
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
  DatePicker,
  Alert,
  Statistic
} from 'antd';
import {
  PlusOutlined,
  DeleteOutlined,
  CalculatorOutlined,
  SaveOutlined,
  InfoCircleOutlined
} from '@ant-design/icons';
import type { BudgetSimplified, BudgetItemSimplified, BudgetCalculation } from '../../services/budgetService';
import { budgetService } from '../../services/budgetService';
import { ErrorHandler } from '../../utils/errorHandler';
import { formatCurrency } from '../../lib/utils';

const { Title, Text } = Typography;

interface AutoMarkupBudgetFormProps {
  onSubmit: (data: BudgetSimplified) => Promise<void>;
  onCancel: () => void;
  isLoading?: boolean;
}

const initialBudgetItem: BudgetItemSimplified = {
  description: '',
  quantity: 1,
  weight: 0,
  purchase_value_with_icms: 0,
  purchase_icms_percentage: 17, // ICMS padrão Brasil
  purchase_other_expenses: 0,
  sale_value_with_icms: 0,
  sale_icms_percentage: 18
};

export default function AutoMarkupBudgetForm({ 
  onSubmit, 
  onCancel, 
  isLoading = false 
}: AutoMarkupBudgetFormProps) {
  const [form] = Form.useForm();
  const [items, setItems] = useState<BudgetItemSimplified[]>([{ ...initialBudgetItem }]);
  const [calculating, setCalculating] = useState(false);
  const [preview, setPreview] = useState<BudgetCalculation | null>(null);

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

  const updateItem = (index: number, field: keyof BudgetItemSimplified, value: string | number | undefined) => {
    const newItems = [...items];
    newItems[index] = { ...newItems[index], [field]: value };
    setItems(newItems);
    setPreview(null); // Limpar preview quando alterar item
  };

  const calculatePreview = async () => {
    try {
      setCalculating(true);
      const formData = form.getFieldsValue();
      
      const budgetData: BudgetSimplified = {
        ...formData,
        items: items,
        expires_at: formData.expires_at ? formData.expires_at.toISOString() : undefined,
      };
      
      const calculation = await budgetService.calculateBudgetSimplified(budgetData);
      setPreview(calculation);
      
      message.success('Orçamento calculado com sucesso!');
    } catch (error) {
      const errorMessage = ErrorHandler.handle(error, 'Calculate Budget');
      message.error(errorMessage);
    } finally {
      setCalculating(false);
    }
  };

  const handleSubmit = async () => {
    try {
      const formData = await form.validateFields();
      const budgetData: BudgetSimplified = {
        ...formData,
        items: items,
        expires_at: formData.expires_at ? formData.expires_at.toISOString() : undefined,
      };
      
      await onSubmit(budgetData);
    } catch (error) {
      ErrorHandler.handle(error, 'Form Validation');
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
          required
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
          required
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
          style={{ width: '100%' }}
          required
          placeholder="0,00"
        />
      ),
    },
    {
      title: '% ICMS Compra *',
      dataIndex: 'purchase_icms_percentage',
      key: 'purchase_icms_percentage',
      width: 120,
      render: (value: number, _: BudgetItemSimplified, index: number) => (
        <InputNumber
          value={value}
          onChange={(val) => updateItem(index, 'purchase_icms_percentage', val || 17)}
          min={0}
          max={100}
          step={0.1}
          precision={1}
          formatter={(value) => `${value}%`}
          parser={(value) => Number(value!.replace('%', ''))}
          style={{ width: '100%' }}
          required
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
          min={0}
          step={0.01}
          precision={2}
          style={{ width: '100%' }}
          placeholder="0,00"
        />
      ),
    },
    {
      title: '% ICMS Venda *',
      dataIndex: 'sale_icms_percentage',
      key: 'sale_icms_percentage',
      width: 120,
      render: (value: number, _: BudgetItemSimplified, index: number) => (
        <InputNumber
          value={value}
          onChange={(val) => updateItem(index, 'sale_icms_percentage', val || 18)}
          min={0}
          max={100}
          step={0.1}
          precision={1}
          formatter={(value) => `${value}%`}
          parser={(value) => Number(value!.replace('%', ''))}
          style={{ width: '100%' }}
          required
        />
      ),
    },
    {
      title: 'Ações',
      key: 'actions',
      width: 80,
      fixed: 'right' as const,
      render: (_: unknown, __: BudgetItemSimplified, index: number) => (
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
        >
          <Row justify="space-between" align="middle" style={{ marginBottom: '24px' }}>
            <Col>
              <Title level={3} style={{ margin: 0 }}>
                Novo Orçamento Simplificado 💼
              </Title>
              <Text type="secondary">
                Formulário simplificado para criação rápida de orçamentos. Informe os valores de compra e venda para cada item.
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
                label="Observações"
                name="notes"
              >
                <Input.TextArea rows={3} placeholder="Observações adicionais..." />
              </Form.Item>
            </Col>
          </Row>

          {/* Alerta explicativo */}
          <Alert
            message="Formulário Simplificado"
            description="Este formulário permite criação rápida de orçamentos. Preencha os valores de compra e venda para cada item."
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

          {/* Preview dos Cálculos */}
          {preview && (
            <>
              <Divider>Resumo Financeiro</Divider>
              
              <Alert
                message="Cálculo Realizado"
                description={`
                  Markup aplicado: ${preview.markup_percentage.toFixed(1)}% 
                  (Baseado nos valores de compra e venda informados)
                `}
                type="success"
                icon={<InfoCircleOutlined />}
                style={{ marginBottom: '16px' }}
                showIcon
              />

              {/* Stats cards */}
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
