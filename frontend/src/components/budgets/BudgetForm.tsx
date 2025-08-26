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
  DatePicker
} from 'antd';
import {
  PlusOutlined,
  DeleteOutlined,
  CalculatorOutlined,
  SaveOutlined
} from '@ant-design/icons';
import type { Budget, BudgetItem } from '../../services/budgetService';
import { budgetService } from '../../services/budgetService';
import { formatCurrency } from '../../lib/utils';
import dayjs from 'dayjs';

const { Title } = Typography;
const { Option } = Select;

interface BudgetFormProps {
  initialData?: Budget;
  onSubmit: (data: Budget) => Promise<void>;
  onCancel: () => void;
  isLoading?: boolean;
  isEdit?: boolean;
}

const initialBudgetItem: BudgetItem = {
  description: '',
  weight: 0,
  purchase_icms_percentage: 0.17, // Decimal format (17%)
  purchase_other_expenses: 0,
  purchase_value_without_taxes: 0,
  sale_icms_percentage: 0.17, // Decimal format (17%)
  sale_value_without_taxes: 0,
  dunamis_cost: 0,
  purchase_value_with_icms: 0,
  sale_value_with_icms: 0
};

export default function BudgetForm({ 
  initialData, 
  onSubmit, 
  onCancel, 
  isLoading = false, 
  isEdit = false 
}: BudgetFormProps) {
  const [form] = Form.useForm();
  const [items, setItems] = useState<BudgetItem[]>([]);
  const [calculating, setCalculating] = useState(false);

  useEffect(() => {
    if (initialData) {
      form.setFieldsValue({
        ...initialData,
        expires_at: initialData.expires_at ? dayjs(initialData.expires_at) : undefined,
      });
      setItems(initialData.items || []);
    } else {
      setItems([{ ...initialBudgetItem }]);
    }
  }, [initialData, form]);

  const addItem = () => {
    setItems([...items, { ...initialBudgetItem }]);
  };

  const removeItem = (index: number) => {
    if (items.length > 1) {
      const newItems = items.filter((_, i) => i !== index);
      setItems(newItems);
    } else {
      message.warning('Deve haver pelo menos um item no orçamento');
    }
  };

  const updateItem = (index: number, field: keyof BudgetItem, value: unknown) => {
    const newItems = [...items];
    newItems[index] = { ...newItems[index], [field]: value };
    setItems(newItems);
    
    // Auto-recalculate when critical fields change (especially ICMS percentages)
    if (field === 'sale_icms_percentage' || field === 'purchase_icms_percentage' || 
        field === 'sale_value_with_icms' || field === 'purchase_value_with_icms' ||
        field === 'weight' || field === 'sale_weight') {
      // Debounce the auto-calculation to avoid too many API calls
      setTimeout(() => {
        autoCalculateBudget(newItems);
      }, 300);
    }
  };

  const calculateBudget = async () => {
    try {
      setCalculating(true);
      const formData = form.getFieldsValue();
      
      const budgetData: Budget = {
        ...formData,
        items: items,
        expires_at: formData.expires_at ? formData.expires_at.toISOString() : undefined,
      };
      
      const calculation = await budgetService.calculateBudget(budgetData);
      
      // Update form with calculated values
      form.setFieldsValue({
        total_purchase_value: calculation.total_purchase_value,
        total_sale_value: calculation.total_sale_value,
        total_commission: calculation.total_commission,
        profitability_percentage: calculation.profitability_percentage,
      });
      
      message.success('Orçamento calculado com sucesso!');
    } catch (error) {
      console.error('Erro ao calcular orçamento:', error);
      message.error('Erro ao calcular orçamento');
    } finally {
      setCalculating(false);
    }
  };

  // Auto-calculation function for real-time updates when ICMS changes
  const autoCalculateBudget = async (updatedItems: BudgetItem[]) => {
    try {
      const formData = form.getFieldsValue();
      
      // Only auto-calculate if we have basic required data
      if (!formData.client_name || updatedItems.length === 0) {
        return;
      }
      
      // Check if all items have minimum required fields for calculation
      const hasValidItems = updatedItems.every(item => 
        item.description && 
        (item.weight ?? 0) > 0 &&
        (item.purchase_value_with_icms ?? 0) > 0 &&
        (item.sale_value_with_icms ?? 0) > 0
      );
      
      if (!hasValidItems) {
        return; // Skip auto-calculation if items are incomplete
      }
      
      const budgetData: Budget = {
        ...formData,
        items: updatedItems,
        expires_at: formData.expires_at ? formData.expires_at.toISOString() : undefined,
      };
      
      const calculation = await budgetService.calculateBudget(budgetData);
      
      // Update form with calculated values (without showing success message)
      form.setFieldsValue({
        total_purchase_value: calculation.total_purchase_value,
        total_sale_value: calculation.total_sale_value,
        total_commission: calculation.total_commission,
        profitability_percentage: calculation.profitability_percentage,
      });
      
    } catch (error) {
      // Silently handle errors in auto-calculation to avoid spamming user
      console.warn('Auto-calculation failed:', error);
    }
  };

  // Função para mapear os itens para BudgetItemSimplified
  const mapToSimplifiedItems = () => {
    return items.map(item => ({
      description: item.description,
      peso_compra: item.weight ?? 0,
      valor_com_icms_compra: item.purchase_value_with_icms ?? 0,
      percentual_icms_compra: item.purchase_icms_percentage ?? 0,
      outras_despesas_item: item.purchase_other_expenses ?? 0,
      peso_venda: item.sale_weight ?? item.weight ?? 0,
      valor_com_icms_venda: item.sale_value_with_icms ?? 0,
      percentual_icms_venda: item.sale_icms_percentage ?? 0,
    }));
  };

  const handleSubmit = async () => {
    try {
      const formData = await form.validateFields();

      // Detecta se está usando endpoint simplificado (ajuste conforme sua lógica)
      const isSimplified = true;

      if (isSimplified) {
        const budgetDataSimplified = {
          ...formData,
          items: mapToSimplifiedItems(),
          expires_at: formData.expires_at ? formData.expires_at.toISOString() : undefined,
        };
        await onSubmit(budgetDataSimplified);
      } else {
        const budgetData: Budget = {
          ...formData,
          items: items,
          expires_at: formData.expires_at ? formData.expires_at.toISOString() : undefined,
        };
        await onSubmit(budgetData);
      }
    } catch (error) {
      console.error('Erro na validação do formulário:', error);
    }
  };

  const itemColumns = [
    {
      title: 'Descrição',
      dataIndex: 'description',
      key: 'description',
      width: 200,
      render: (value: string, _: BudgetItem, index: number) => (
        <Input
          value={value}
          onChange={(e) => updateItem(index, 'description', e.target.value)}
          placeholder="Descrição do item"
        />
      ),
    },
    {
      title: 'Peso (kg)',
      dataIndex: 'weight',
      key: 'weight',
      width: 100,
      render: (value: number, _: BudgetItem, index: number) => (
        <InputNumber
          value={value}
          onChange={(val) => updateItem(index, 'weight', val || 0)}
          min={0}
          step={0.001}
          precision={3}
          style={{ width: '100%' }}
        />
      ),
    },
    {
      title: 'Outras Despesas',
      dataIndex: 'purchase_other_expenses',
      key: 'purchase_other_expenses',
      width: 130,
      render: (value: number, _: BudgetItem, index: number) => (
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
      title: 'ICMS Venda (%)',
      dataIndex: 'sale_icms_percentage',
      key: 'sale_icms_percentage',
      width: 150,
      render: (value: number, _: BudgetItem, index: number) => (
        <InputNumber
          value={value * 100} // Convert from decimal to percentage for display
          onChange={(val) => updateItem(index, 'sale_icms_percentage', (val || 0) / 100)} // Convert back to decimal
          min={0}
          step={0.01}
          precision={2}
          style={{ width: '100%' }}
          placeholder="0,00"
        />
      ),
    },
    {
      title: '%ICMS (Venda)',
      dataIndex: 'sale_icms_percentage',
      key: 'sale_icms_percentage',
      width: 120,
      render: (value: number, _: BudgetItem, index: number) => (
        <InputNumber
          value={value * 100} // Convert from decimal to percentage for display
          onChange={(val) => updateItem(index, 'sale_icms_percentage', (val || 0) / 100)} // Convert back to decimal
          min={0}
          max={100}
          step={0.1}
          precision={1}
          addonAfter="%"
          style={{ width: '100%' }}
        />
      ),
    },
    {
      title: 'Comissão Calculada',
      dataIndex: 'commission_value',
      key: 'commission_value',
      width: 120,
      render: (value: number) => {
        return value ? `R$ ${value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}` : 'R$ 0,00';
      },
    },
    {
      title: 'Custo Dunamis',
      dataIndex: 'dunamis_cost',
      key: 'dunamis_cost',
      width: 130,
      render: (value: number, _: BudgetItem, index: number) => (
        <InputNumber
          value={value}
          onChange={(val) => updateItem(index, 'dunamis_cost', val || 0)}
          min={0}
          step={0.01}
          precision={2}
          style={{ width: '100%' }}
          placeholder="0,00"
        />
      ),
    },
    {
      title: 'Ações',
      key: 'actions',
      width: 80,
      fixed: 'right' as const,
      render: (_: unknown, __: BudgetItem, index: number) => (
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
            markup_percentage: 0,
          }}
        >
          <Row justify="space-between" align="middle" style={{ marginBottom: '24px' }}>
            <Col>
              <Title level={3} style={{ margin: 0 }}>
                {isEdit ? 'Editar Orçamento' : 'Novo Orçamento'} 💼
              </Title>
            </Col>
            <Col>
              <Space>
                <Button onClick={onCancel}>
                  Cancelar
                </Button>
                <Button
                  icon={<CalculatorOutlined />}
                  onClick={calculateBudget}
                  loading={calculating}
                >
                  Calcular
                </Button>
                <Button
                  type="primary"
                  icon={<SaveOutlined />}
                  htmlType="submit"
                  loading={isLoading}
                >
                  {isEdit ? 'Atualizar' : 'Salvar'}
                </Button>
              </Space>
            </Col>
          </Row>

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
            <Col xs={24} md={6}>
              <Form.Item
                label="% Markup"
                name="markup_percentage"
              >
                <InputNumber
                  min={0}
                  max={1000}
                  step={0.1}
                  precision={1}
                  addonAfter="%"
                  style={{ width: '100%' }}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={6}>
              <Form.Item
                label="Data de Expiração"
                name="expires_at"
              >
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item
                label="Observações"
                name="notes"
              >
                <Input.TextArea rows={2} placeholder="Observações adicionais..." />
              </Form.Item>
            </Col>
          </Row>

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
              scroll={{ x: 1600 }}
              size="small"
            />
          </div>

          <Divider>Totais Calculados</Divider>

          <Row gutter={[16, 16]}>
            <Col xs={24} md={6}>
              <Form.Item label="Total Compra" name="total_purchase_value">
                <InputNumber
                  readOnly
                  formatter={(value) => formatCurrency(Number(value || 0))}
                  style={{ width: '100%' }}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={6}>
              <Form.Item label="Total Venda" name="total_sale_value">
                <InputNumber
                  readOnly
                  formatter={(value) => formatCurrency(Number(value || 0))}
                  style={{ width: '100%' }}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={6}>
              <Form.Item label="Total Comissão" name="total_commission">
                <InputNumber
                  readOnly
                  formatter={(value) => formatCurrency(Number(value || 0))}
                  style={{ width: '100%' }}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={6}>
              <Form.Item label="% Rentabilidade" name="profitability_percentage">
                <InputNumber
                  readOnly
                  formatter={(value) => `${Number(value || 0).toFixed(1)}%`}
                  style={{ width: '100%' }}
                />
              </Form.Item>
            </Col>
          </Row>
        </Form>
      </Card>
    </div>
  );
}
