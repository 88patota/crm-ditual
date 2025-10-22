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
  Select
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
const { Option } = Select;

interface AutoMarkupBudgetFormProps {
  onSubmit: (data: BudgetSimplified) => Promise<void>;
  onCancel: () => void;
  isLoading?: boolean;
}

const initialBudgetItem: BudgetItemSimplified = {
  description: '',
  peso_compra: 1,
  peso_venda: 1,
  valor_com_icms_compra: 0,
  percentual_icms_compra: 0.17, // Decimal format (17%)
  outras_despesas_item: 0,
  valor_com_icms_venda: 0,
  percentual_icms_venda: 0.18, // Decimal format (18%)
  percentual_ipi: 0.0 // 0% por padrão (formato decimal)
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
    
    // Auto-recalculate when critical fields change (especially ICMS percentages, IPI and outras despesas)
    if (field === 'percentual_icms_venda' || field === 'percentual_icms_compra' || 
        field === 'valor_com_icms_venda' || field === 'valor_com_icms_compra' ||
        field === 'peso_venda' || field === 'peso_compra' || field === 'percentual_ipi' ||
        field === 'outras_despesas_item') {
      // Debounce the auto-calculation to avoid too many API calls
      setTimeout(() => {
        autoCalculatePreview(newItems);
      }, 300);
    }
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

  // Auto-calculation function for real-time updates when ICMS changes
  const autoCalculatePreview = async (updatedItems: BudgetItemSimplified[]) => {
    try {
      const formData = form.getFieldsValue();
      
      // Only auto-calculate if we have basic required data
      if (!formData.client_name || updatedItems.length === 0) {
        return;
      }
      
      // Check if all items have minimum required fields for calculation
      const hasValidItems = updatedItems.every(item => 
        item.description && 
        item.peso_compra > 0 && 
        item.peso_venda > 0 &&
        item.valor_com_icms_compra > 0 &&
        item.valor_com_icms_venda > 0
      );
      
      if (!hasValidItems) {
        return; // Skip auto-calculation if items are incomplete
      }
      
      const budgetData: BudgetSimplified = {
        ...formData,
        items: updatedItems,
        expires_at: formData.expires_at ? formData.expires_at.toISOString() : undefined,
      };
      
      const calculation = await budgetService.calculateBudgetSimplified(budgetData);
      setPreview(calculation);
      
    } catch (error) {
      // Silently handle errors in auto-calculation to avoid spamming user
      console.warn('Auto-calculation failed:', error);
      setPreview(null);
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
      title: 'Peso Compra (kg) *',
      dataIndex: 'peso_compra',
      key: 'peso_compra',
      width: 120,
      render: (value: number, _: BudgetItemSimplified, index: number) => (
        <InputNumber
          value={value}
          onChange={(val) => updateItem(index, 'peso_compra', val || 1)}
          min={0.01}
          step={0.001}
          precision={3}
          style={{ width: '100%' }}
          placeholder="0,000"
          required
        />
      ),
    },
    {
      title: 'Peso Venda (kg) *',
      dataIndex: 'peso_venda',
      key: 'peso_venda',
      width: 120,
      render: (value: number, _: BudgetItemSimplified, index: number) => (
        <InputNumber
          value={value}
          onChange={(val) => updateItem(index, 'peso_venda', val || 1)}
          min={0.01}
          step={0.001}
          precision={3}
          style={{ width: '100%' }}
          placeholder="0,000"
          required
        />
      ),
    },
    {
      title: 'Valor c/ICMS (Compra) *',
      dataIndex: 'valor_com_icms_compra',
      key: 'valor_com_icms_compra',
      width: 180,
      render: (value: number, _: BudgetItemSimplified, index: number) => (
        <InputNumber
          value={value}
          onChange={(val) => updateItem(index, 'valor_com_icms_compra', val || 0)}
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
      dataIndex: 'percentual_icms_compra',
      key: 'percentual_icms_compra',
      width: 120,
      render: (value: number, _: BudgetItemSimplified, index: number) => (
        <InputNumber
          value={value * 100} // Convert from decimal to percentage for display
          onChange={(val) => updateItem(index, 'percentual_icms_compra', (val || 17) / 100)} // Convert back to decimal
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
      dataIndex: 'outras_despesas_item',
      key: 'outras_despesas_item',
      width: 150,
      render: (value: number, _: BudgetItemSimplified, index: number) => (
        <InputNumber
          value={value}
          onChange={(val) => updateItem(index, 'outras_despesas_item', val || 0)}
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
      dataIndex: 'valor_com_icms_venda',
      key: 'valor_com_icms_venda',
      width: 180,
      render: (value: number, _: BudgetItemSimplified, index: number) => (
        <InputNumber
          value={value}
          onChange={(val) => updateItem(index, 'valor_com_icms_venda', val || 0)}
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
      dataIndex: 'percentual_icms_venda',
      key: 'percentual_icms_venda',
      width: 120,
      render: (value: number, _: BudgetItemSimplified, index: number) => (
        <InputNumber
          value={value * 100} // Convert from decimal to percentage for display
          onChange={(val) => updateItem(index, 'percentual_icms_venda', (val || 18) / 100)} // Convert back to decimal
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
      title: '% IPI *',
      dataIndex: 'percentual_ipi',
      key: 'percentual_ipi',
      width: 120,
      render: (value: number, _: BudgetItemSimplified, index: number) => (
        <Select
          value={value}
          onChange={(val) => updateItem(index, 'percentual_ipi', val)}
          style={{ width: '100%' }}
          placeholder="Selecione"
        >
          <Option value={0.0}>0% (Isento)</Option>
          <Option value={0.0325}>3,25%</Option>
          <Option value={0.05}>5%</Option>
        </Select>
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
              rowKey={(record) => items.indexOf(record)}
              scroll={{ x: 1200 }}
              size="small"
            />
          </div>

          {/* Preview dos Cálculos - Layout Otimizado */}
          {preview && (
            <>
              <Divider>✅ Orçamento Calculado</Divider>
              
              {/* Totais do Pedido - Design Integrado */}
              <Card style={{ 
                background: 'linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%)',
                border: '1px solid #bae6fd',
                marginBottom: '24px'
              }}>
                <Row gutter={[24, 16]}>
                  <Col xs={24} lg={16}>
                    <div style={{ padding: '8px 0' }}>
                      <Alert
                        message="🎯 Markup Automático Aplicado"
                        description={`Markup calculado: ${preview.markup_percentage.toFixed(1)}% baseado nos valores de compra e venda informados.`}
                        type="success"
                        showIcon
                        style={{ marginBottom: '16px' }}
                      />
                      
                      <Row gutter={[16, 8]}>
                        <Col span={12}>
                          <div style={{ textAlign: 'center', padding: '8px', background: 'rgba(255,255,255,0.7)', borderRadius: '6px' }}>
                            <Text type="secondary" style={{ fontSize: '11px' }}>COMISSÃO TOTAL</Text>
                            <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#722ed1' }}>
                              {formatCurrency(preview.total_commission || 0)}
                            </div>
                          </div>
                        </Col>
                        <Col span={12}>
                          <div style={{ textAlign: 'center', padding: '8px', background: 'rgba(255,255,255,0.7)', borderRadius: '6px' }}>
                            <Text type="secondary" style={{ fontSize: '11px' }}>MARKUP</Text>
                            <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#13c2c2' }}>
                              {preview.markup_percentage.toFixed(1)}%
                            </div>
                          </div>
                        </Col>
                      </Row>
                    </div>
                  </Col>
                  
                  {/* Valor Total Destacado */}
                  <Col xs={24} lg={8}>
                    <div style={{ 
                      background: 'rgba(255,255,255,0.9)',
                      padding: '20px',
                      borderRadius: '8px',
                      textAlign: 'center',
                      border: '2px solid #52c41a'
                    }}>
                      <Text type="secondary" style={{ fontSize: '12px' }}>VALOR TOTAL</Text>
                      <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#52c41a' }}>
                        {formatCurrency(preview.total_sale_value + preview.total_taxes)}
                      </div>
                      <Text type="secondary" style={{ fontSize: '11px' }}>
                        COM ICMS
                      </Text>
                      
                      {/* Nota informativa quando há IPI */}
                      {preview.total_ipi_value && preview.total_ipi_value > 0 && (
                        <Alert 
                          message="IPI Aplicado" 
                          description={`Inclui ${formatCurrency(preview.total_ipi_value)} de IPI`}
                          type="warning" 
                          showIcon 
                          style={{ marginTop: '12px', fontSize: '11px' }}
                        />
                      )}
                    </div>
                  </Col>
                </Row>
              </Card>
            </>
          )}
        </Form>
      </Card>
    </div>
  );
}
