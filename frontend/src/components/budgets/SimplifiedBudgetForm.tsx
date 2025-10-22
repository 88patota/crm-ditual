import { useState, useEffect, useCallback } from 'react';
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
import { formatCurrency, convertNumericToBrazilian } from '../../lib/utils';
import CurrencyInput from '../common/CurrencyInput';
import dayjs from 'dayjs';

const { Title, Text } = Typography;
const { Option } = Select;


interface SimplifiedBudgetFormProps {
  initialData?: BudgetSimplified;
  onSubmit: (data: BudgetSimplified) => Promise<void>;
  onCancel: () => void;
  isLoading?: boolean;
  isEdit?: boolean;
}

// Interface para mapear dados do backend que podem ter campos em inglês
interface BackendBudgetItem {
  description?: string;
  delivery_time?: string;
  weight?: number;
  sale_weight?: number;
  purchase_value_with_icms?: number;
  purchase_icms_percentage?: number;
  purchase_other_expenses?: number;
  sale_value_with_icms?: number;
  sale_icms_percentage?: number;
  ipi_percentage?: number;
  // Campos em português (caso já estejam convertidos)
  peso_compra?: number;
  peso_venda?: number;
  valor_com_icms_compra?: number;
  percentual_icms_compra?: number;
  outras_despesas_item?: number;
  valor_com_icms_venda?: number;
  percentual_icms_venda?: number;
  percentual_ipi?: number;
}

// Interface estendida para incluir campos do backend que podem não estar na interface principal
interface BudgetItemWithBackendFields extends BudgetItemSimplified {
  ipi_percentage?: number;
  weight?: number;
  sale_weight?: number;
  purchase_value_with_icms?: number;
  purchase_icms_percentage?: number;
  purchase_other_expenses?: number;
  sale_value_with_icms?: number;
  sale_icms_percentage?: number;
}

const initialBudgetItem: BudgetItemSimplified = {
  description: '',
  delivery_time: '0', // Prazo padrão em dias (0 = imediato)
  peso_compra: 0,
  peso_venda: 0,
  valor_com_icms_compra: 0,
  percentual_icms_compra: 0.18, // 18% in decimal format
  outras_despesas_item: 0,
  valor_com_icms_venda: 0,
  percentual_icms_venda: 0.18, // 18% in decimal format
  percentual_ipi: 0.0, // 0% por padrão (formato decimal)
};

export default function SimplifiedBudgetForm({ 
  initialData,
  onSubmit, 
  onCancel, 
  isLoading = false,
  isEdit = false
}: SimplifiedBudgetFormProps) {
  const [form] = Form.useForm();
  const [items, setItems] = useState<BudgetItemSimplified[]>([{ ...initialBudgetItem }]);
  const [calculating, setCalculating] = useState(false);
  const [preview, setPreview] = useState<BudgetCalculation | null>(null);
  const [orderNumber, setOrderNumber] = useState<string>('');
  const [loadingOrderNumber, setLoadingOrderNumber] = useState(!isEdit);

  const loadNextOrderNumber = useCallback(async () => {
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
  }, [form]);

  // Inicializar com dados existentes ou carregar novo número do pedido
  useEffect(() => {
    if (isEdit && initialData) {
      console.log('=== DEBUG IPI - SimplifiedBudgetForm ===');
      console.log('Initial data items:', initialData.items?.map(item => ({ 
        desc: item.description, 
        ipi_original: item.percentual_ipi 
      })));
      console.log('Initial data freight_type:', initialData.freight_type);
      
      // Modo edição - usar dados iniciais
      const formData = {
        ...initialData,
        expires_at: initialData.expires_at ? dayjs(initialData.expires_at) : undefined,
        // Fix: Only set freight_type if it exists in initialData
        ...(initialData.freight_type !== undefined && { freight_type: initialData.freight_type }),
      };
      
      console.log('Setting form fields with data:', formData);
      form.setFieldsValue(formData);
      
      // Also set the field value directly if freight_type exists
      if (initialData.freight_type !== undefined) {
        form.setFieldValue('freight_type', initialData.freight_type);
      }
      
      // Also set the field value directly if payment_condition exists
      if (initialData.payment_condition !== undefined) {
        form.setFieldValue('payment_condition', initialData.payment_condition);
      }
      
      // Log the field value after setting it
      setTimeout(() => {
        const fieldValue = form.getFieldValue('freight_type');
        console.log('Field value after setFieldsValue:', fieldValue);
      }, 0);
      
      // CORREÇÃO FINAL: Mapear corretamente os dados do backend
      const itemsWithPreservedIPI = (initialData.items || [{ ...initialBudgetItem }]).map(item => {
        // Usar a interface BackendBudgetItem para acessar propriedades que podem vir do backend
        const backendItem = item as BudgetItemSimplified & BackendBudgetItem & { [key: string]: unknown };
          
        console.log('🔍 Raw backend item:', backendItem);
        console.log('🔍 Available keys:', Object.keys(backendItem));
        console.log('🔍 IPI related fields:', Object.keys(backendItem).filter(k => k.toLowerCase().includes('ipi')));
          
        const preservedItem: BudgetItemSimplified = {
          description: item.description || '',
          // CORREÇÃO CRÍTICA: Mapear delivery_time do backend
          delivery_time: item.delivery_time || '0',
          // Mapear campos de peso corretamente
          peso_compra: typeof backendItem.weight === 'number' ? backendItem.weight : 
                        typeof item.peso_compra === 'number' ? item.peso_compra : 0,
          peso_venda: typeof backendItem.sale_weight === 'number' ? backendItem.sale_weight : 
                       typeof item.peso_venda === 'number' ? item.peso_venda : 
                       typeof backendItem.weight === 'number' ? backendItem.weight :
                       typeof item.peso_compra === 'number' ? item.peso_compra : 0,
            
          // Mapear campos de valor de compra
          valor_com_icms_compra: typeof backendItem.purchase_value_with_icms === 'number' ? backendItem.purchase_value_with_icms :
                                  typeof item.valor_com_icms_compra === 'number' ? item.valor_com_icms_compra : 0,
          percentual_icms_compra: typeof backendItem.purchase_icms_percentage === 'number' ? backendItem.purchase_icms_percentage :
                                   typeof item.percentual_icms_compra === 'number' ? item.percentual_icms_compra : 0.18,
          outras_despesas_item: typeof backendItem.purchase_other_expenses === 'number' ? backendItem.purchase_other_expenses :
                                 typeof item.outras_despesas_item === 'number' ? item.outras_despesas_item : 0,
            
            // Mapear campos de valor de venda
            valor_com_icms_venda: typeof backendItem.sale_value_with_icms === 'number' ? backendItem.sale_value_with_icms :
                                 typeof item.valor_com_icms_venda === 'number' ? item.valor_com_icms_venda : 0,
            percentual_icms_venda: typeof backendItem.sale_icms_percentage === 'number' ? backendItem.sale_icms_percentage :
                                  typeof item.percentual_icms_venda === 'number' ? item.percentual_icms_venda : 0.18,
            
            // CORREÇÃO CRÍTICA: Mapear IPI corretamente do backend para o frontend
            // O backend retorna "ipi_percentage": 0.0325, precisa mapear para "percentual_ipi"
            percentual_ipi: (() => {
              // PRIMEIRO: Verificar se o item já tem o campo correto mapeado
              if (typeof item.percentual_ipi === 'number' && !isNaN(item.percentual_ipi) && item.percentual_ipi > 0) {
                console.log(`🎯 Found IPI already mapped: ${item.percentual_ipi}`);
                return item.percentual_ipi;
              }
              
              // SEGUNDO: O backend retorna "ipi_percentage", mapear diretamente
              const itemWithBackend = item as BudgetItemWithBackendFields;
              if (typeof itemWithBackend.ipi_percentage === 'number' && !isNaN(itemWithBackend.ipi_percentage)) {
                console.log(`🎯 Mapping IPI from backend 'ipi_percentage': ${itemWithBackend.ipi_percentage}`);
                return itemWithBackend.ipi_percentage;
              }
              
              // TERCEIRO: Verificar através do backendItem (cast genérico)
              if (typeof backendItem.ipi_percentage === 'number' && !isNaN(backendItem.ipi_percentage)) {
                console.log(`🎯 Found IPI via backendItem: ${backendItem.ipi_percentage}`);
                return backendItem.ipi_percentage;
              }
              
              // QUARTO: Buscar em outros possíveis nomes de campo
              const ipiFieldNames = ['percentual_ipi', 'ipi_value', 'ipi_percent'];
              for (const fieldName of ipiFieldNames) {
                const value = backendItem[fieldName];
                if (typeof value === 'number' && !isNaN(value) && value > 0) {
                  console.log(`🎯 Found IPI in fallback field '${fieldName}': ${value}`);
                  return value;
                }
              }
              
              // Se não encontrou nenhum campo válido, retornar 0
              console.log('⚠️ No valid IPI field found, defaulting to 0');
              console.log('Available item keys:', Object.keys(item));
              console.log('Available backendItem keys:', Object.keys(backendItem));
              return 0.0;
            })()
          };
          return preservedItem;
        });
      
      console.log('Items after processing:', itemsWithPreservedIPI.map(item => ({ 
        desc: item.description, 
        ipi_processed: item.percentual_ipi 
      })));
      console.log('==========================================');
      
      setItems(itemsWithPreservedIPI);
      setOrderNumber(initialData.order_number || '');
      setLoadingOrderNumber(false);
    } else {
      // Modo criação - carregar novo número
      loadNextOrderNumber();
      // Set default payment_condition for new budgets
      form.setFieldValue('payment_condition', 'À vista');
    }
  }, [initialData, isEdit, form, loadNextOrderNumber]);

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

  const updateItem = (index: number, field: keyof BudgetItemSimplified, value: unknown) => {
    const newItems = [...items];
    
    // Garantir conversão correta de números, especialmente com vírgulas
    if (field === 'peso_compra' || field === 'peso_venda' || 
        field === 'valor_com_icms_compra' || field === 'valor_com_icms_venda' ||
        field === 'outras_despesas_item' || field === 'percentual_ipi') {
      let numericValue = 0;
      
      if (typeof value === 'number') {
        numericValue = value;
      } else if (typeof value === 'string') {
        // Converter vírgulas em pontos para garantir parsing correto
        const normalizedValue = value.replace(',', '.');
        numericValue = parseFloat(normalizedValue) || 0;
      } else if (value === null || value === undefined) {
        numericValue = 0;
      }
      
      newItems[index] = { ...newItems[index], [field]: numericValue };
    } else {
      newItems[index] = { ...newItems[index], [field]: value };
    }
    
    setItems(newItems);
    setPreview(null);
    
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
      console.log('Calculate form data:', formData);
      console.log('Calculate freight_type:', formData.freight_type);
      
      const budgetData: BudgetSimplified = {
        ...formData,
        order_number: orderNumber, // Usar o número gerado
        // CORREÇÃO: Incluir campos prazo_medio e outras_despesas_totais
        prazo_medio: formData.prazo_medio || undefined,
        outras_despesas_totais: formData.outras_despesas_totais || undefined,
        freight_type: formData.freight_type || 'FOB',
        payment_condition: formData.payment_condition || 'À vista',
        items: items,
        expires_at: formData.expires_at ? formData.expires_at.toISOString() : undefined,
      };
      
      console.log('Calculate budget data:', budgetData);
      console.log('Calculate budget freight_type:', budgetData.freight_type);
      
      // Log temporário para debug - capturar valores enviados
      console.log('=== DEBUG: Dados enviados para o backend ===');
      console.log('budgetData completo:', JSON.stringify(budgetData, null, 2));
      console.log('Items com outras_despesas_item:', budgetData.items.map(item => ({
        description: item.description,
        outras_despesas_item: item.outras_despesas_item,
        tipo: typeof item.outras_despesas_item
      })));
      
      const calculation = await budgetService.calculateBudgetSimplified(budgetData);
      setPreview(calculation);
      
      // CORREÇÃO: Atualizar os campos do formulário com os valores calculados
      // Isso garante que os valores totais e de comissão sejam atualizados também no cálculo manual
      form.setFieldsValue({
        total_purchase_value: calculation.total_purchase_value,
        total_sale_value: calculation.total_sale_value,
        total_commission: calculation.total_commission,
        profitability_percentage: calculation.profitability_percentage,
        markup_percentage: calculation.markup_percentage,
        // Atualizar valores de IPI e finais se disponíveis
        total_ipi_value: calculation.total_ipi_value,
        total_final_value: calculation.total_final_value,
        // Atualizar impostos totais
        total_taxes: calculation.total_taxes,
      });
      
      message.success(`Cálculos realizados! Markup: ${calculation.markup_percentage.toFixed(1)}%`);
    } catch (error) {
      console.error('Erro ao calcular orçamento:', error);
      message.error('Erro ao calcular orçamento. Verifique se todos os campos obrigatórios estão preenchidos.');
    } finally {
      setCalculating(false);
    }
  };

  // Auto-calculation function for real-time updates
  const autoCalculatePreview = async (updatedItems: BudgetItemSimplified[]) => {
    try {
      const formData = form.getFieldsValue();
      console.log('Auto-calculate form data:', formData);
      console.log('Auto-calculate freight_type:', formData.freight_type);
      
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
        order_number: orderNumber,
        // CORREÇÃO: Incluir campos prazo_medio, outras_despesas_totais e freight_type
        prazo_medio: formData.prazo_medio || undefined,
        outras_despesas_totais: formData.outras_despesas_totais || undefined,
        freight_type: formData.freight_type || 'FOB',
        payment_condition: formData.payment_condition || 'À vista',
        items: updatedItems,
        expires_at: formData.expires_at ? formData.expires_at.toISOString() : undefined,
      };
      
      console.log('Auto-calculate budget data:', budgetData);
      console.log('Auto-calculate budget freight_type:', budgetData.freight_type);
      
      const calculation = await budgetService.calculateBudgetSimplified(budgetData);
      setPreview(calculation);
      
      // CORREÇÃO CRÍTICA: Atualizar os campos do formulário com os valores calculados
      // Isso garante que os valores totais e de comissão sejam atualizados em tempo real
      form.setFieldsValue({
        total_purchase_value: calculation.total_purchase_value,
        total_sale_value: calculation.total_sale_value,
        total_commission: calculation.total_commission,
        profitability_percentage: calculation.profitability_percentage,
        markup_percentage: calculation.markup_percentage,
        // Atualizar valores de IPI e finais se disponíveis
        total_ipi_value: calculation.total_ipi_value,
        total_final_value: calculation.total_final_value,
        // Atualizar impostos totais
        total_taxes: calculation.total_taxes,
      });
      
    } catch (error) {
      // Silently handle errors in auto-calculation to avoid spamming user
      console.warn('Auto-calculation failed:', error);
      setPreview(null);
    }
  };

  const handleSubmit = async () => {
    try {
      const formData = await form.validateFields();
      console.log('Form data being submitted:', formData);
      console.log('Freight type in form data:', formData.freight_type);
      if (items.length === 0) {
        message.error('O orçamento deve conter pelo menos um item.');
        return;
      }
      const budgetData: BudgetSimplified = {
        ...formData,
        order_number: orderNumber, // Usar o número gerado automaticamente
        // CORREÇÃO: Incluir o campo prazo_medio na requisição
        prazo_medio: formData.prazo_medio || undefined,
        outras_despesas_totais: formData.outras_despesas_totais || undefined,
        // Fix: Only include freight_type if it was explicitly set/changed
        ...(formData.freight_type !== undefined && { freight_type: formData.freight_type }),
        payment_condition: formData.payment_condition || 'À vista',
        items: items.map(item => ({
          ...item,
          peso_compra: parseFloat(item.peso_compra.toString().replace(',', '.')),
          peso_venda: parseFloat(item.peso_venda.toString().replace(',', '.')),
          valor_com_icms_compra: parseFloat(item.valor_com_icms_compra.toString().replace(',', '.')),
          valor_com_icms_venda: parseFloat(item.valor_com_icms_venda.toString().replace(',', '.')),
          // CORREÇÃO: Garantir que o IPI seja incluído no salvamento
          percentual_ipi: typeof item.percentual_ipi === 'number' ? item.percentual_ipi : 0.0,
          // CORREÇÃO: Garantir que o delivery_time seja incluído no salvamento
          delivery_time: item.delivery_time || '0'
        })),
        expires_at: formData.expires_at ? formData.expires_at.toISOString() : undefined,
      };
      
      console.log('Budget data being sent to backend:', budgetData);
      console.log('Freight type in budget data:', budgetData.freight_type);
      await onSubmit(budgetData);
    } catch (error) {
      console.error('Erro na validação do formulário:', error);
      message.error('Erro ao validar o formulário. Verifique os campos obrigatórios.');
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
      title: 'Prazo (dias)',
      dataIndex: 'delivery_time',
      key: 'delivery_time',
      width: 120,
      render: (value: string, _: BudgetItemSimplified, index: number) => (
        <InputNumber
          value={value ? parseInt(value) : 0}
          onChange={(val) => updateItem(index, 'delivery_time', val?.toString() || '0')}
          min={0}
          max={365}
          step={1}
          style={{ width: '100%' }}
          placeholder="Dias"
        />
      ),
    },
    {
      title: 'Peso Compra (kg) *',
      dataIndex: 'peso_compra',
      key: 'peso_compra',
      width: 140,
      render: (value: number, _: BudgetItemSimplified, index: number) => (
        <InputNumber
          value={value}
          onChange={(val) => updateItem(index, 'peso_compra', val || 0)}
          min={0}
          step={0.001}
          precision={3}
          style={{ width: '100%' }}
          placeholder="0,000"
          decimalSeparator=","
          formatter={(value) => value ? value.toString().replace('.', ',') : ''}
          parser={(value) => value ? parseFloat(value.replace(',', '.')) : 0}
        />
      ),
    },
    {
      title: 'Peso Venda (kg) *',
      dataIndex: 'peso_venda',
      key: 'peso_venda',
      width: 140,
      render: (value: number, _: BudgetItemSimplified, index: number) => (
        <InputNumber
          value={value}
          onChange={(val) => updateItem(index, 'peso_venda', val || 0)}
          min={0}
          step={0.001}
          precision={3}
          style={{ width: '100%' }}
          placeholder="0,000"
          decimalSeparator=","
          formatter={(value) => value ? value.toString().replace('.', ',') : ''}
          parser={(value) => value ? parseFloat(value.replace(',', '.')) : 0}
        />
      ),
    },
    {
      title: 'Valor c/ICMS (Compra) *',
      dataIndex: 'valor_com_icms_compra',
      key: 'valor_com_icms_compra',
      width: 180,
      render: (value: number, _: BudgetItemSimplified, index: number) => (
        <CurrencyInput
          value={value}
          onChange={(val) => updateItem(index, 'valor_com_icms_compra', val || 0)}
          placeholder="0,00"
          style={{ width: '100%' }}
        />
      ),
    },
    {
      title: '% ICMS (Compra) *',
      dataIndex: 'percentual_icms_compra',
      key: 'percentual_icms_compra',
      width: 140,
      render: (value: number, _: BudgetItemSimplified, index: number) => (
        <InputNumber
          value={value * 100} // Convert from decimal to percentage for display
          onChange={(val) => updateItem(index, 'percentual_icms_compra', (val || 18) / 100)} // Convert back to decimal
          min={0}
          max={100}
          step={0.1}
          precision={1}
          formatter={(value) => `${value}%`}
          parser={(value) => parseFloat(value!.replace('%', '')) || 0}
          style={{ width: '100%' }}
        />
      ),
    },
    {
      title: 'Outras Despesas',
      dataIndex: 'outras_despesas_item',
      key: 'outras_despesas_item',
      width: 150,
      render: (value: number, _: BudgetItemSimplified, index: number) => (
        <CurrencyInput
          value={value}
          onChange={(val) => updateItem(index, 'outras_despesas_item', val || 0)}
          placeholder="0,00"
          style={{ width: '100%' }}
        />
      ),
    },
    {
      title: 'Valor c/ICMS (Venda) *',
      dataIndex: 'valor_com_icms_venda',
      key: 'valor_com_icms_venda',
      width: 180,
      render: (value: number, _: BudgetItemSimplified, index: number) => (
        <CurrencyInput
          value={value}
          onChange={(val) => updateItem(index, 'valor_com_icms_venda', val || 0)}
          placeholder="0,00"
          style={{ width: '100%' }}
        />
      ),
    },
    {
      title: '% ICMS (Venda) *',
      dataIndex: 'percentual_icms_venda',
      key: 'percentual_icms_venda',
      width: 140,
      render: (value: number, _: BudgetItemSimplified, index: number) => (
        <InputNumber
          value={value * 100} // Convert from decimal to percentage for display
          onChange={(val) => updateItem(index, 'percentual_icms_venda', (val || 18) / 100)} // Convert back to decimal
          min={0}
          max={100}
          step={0.1}
          precision={1}
          formatter={(value) => `${value}%`}
          parser={(value) => parseFloat(value!.replace('%', '')) || 0}
          style={{ width: '100%' }}
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
          initialValues={{
            status: 'draft',
            // Fix: Only set freight_type default for new budgets, not for editing
            ...(!isEdit && { freight_type: 'FOB' }),
            // Fix: Set payment_condition default for new budgets, similar to freight_type
            ...(!isEdit && { payment_condition: 'À vista' }),
          }}
        >
          <Row justify="space-between" align="middle" style={{ marginBottom: '24px' }}>
            <Col>
              <Space direction="vertical" size={4}>
                <Title level={3} style={{ margin: 0 }}>
                  {isEdit ? 'Editar Orçamento' : 'Novo Orçamento Simplificado'} 💼
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
            <Col xs={24} md={6}>
              <Form.Item
                label="Data de Expiração"
                name="expires_at"
              >
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col xs={24} md={6}>
              <Form.Item
                label="Prazo Médio (dias)"
                name="prazo_medio"
              >
                <InputNumber 
                  min={1}
                  step={1}
                  precision={0}
                  style={{ width: '100%' }}
                  placeholder="Ex: 30"
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={6}>
              <Form.Item
                label="Condições de Pagamento"
                name="payment_condition"
                rules={[{ required: true, message: 'Condições de pagamento são obrigatórias' }]}
              >
                <Select 
                  placeholder="Selecione as condições de pagamento"
                  style={{ width: '100%' }}
                  allowClear={false}
                  onChange={(value) => console.log('Select onChange - payment_condition:', value)}
                >
                  <Option value="À vista">À vista</Option>
                  <Option value="7">7</Option>
                  <Option value="21">21</Option>
                  <Option value="28">28</Option>
                  <Option value="28/35">28/35</Option>
                  <Option value="28/35/42">28/35/42</Option>
                  <Option value="28/35/42/49">28/35/42/49</Option>
                  <Option value="30">30</Option>
                  <Option value="30/45">30/45</Option>
                  <Option value="30/45/60">30/45/60</Option>
                  <Option value="30/45/60/75">30/45/60/75</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col xs={24} md={6}>
              <Form.Item
                label="Frete"
                name="freight_type"
              >
                <Select 
                  placeholder="Selecione o tipo de frete"
                  onChange={(value) => {
                    console.log('Frete type changed to:', value);
                    console.log('Current form values before update:', form.getFieldsValue());
                    form.setFieldsValue({ freight_type: value });
                    setTimeout(() => {
                      const updatedValue = form.getFieldValue('freight_type');
                      console.log('Field value after update:', updatedValue);
                    }, 0);
                  }}
                >
                  <Option value="CIF">CIF</Option>
                  <Option value="FOB">FOB</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col xs={24} md={6}>
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
            description="Preencha: Cliente, Descrição, Peso Compra (kg), Peso Venda (kg), Valor c/ICMS (Compra), % ICMS (Compra), Valor c/ICMS (Venda) e % ICMS (Venda). O cálculo é baseado no peso dos produtos conforme a planilha de negócio."
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
              scroll={{ x: 1400 }}
              size="small"
            />
          </div>

          {/* Campos de Totais */}
          <Divider>Totais do Orçamento</Divider>
          
          <Row gutter={[16, 16]}>
            <Col xs={24} md={8}>
              <Form.Item label="Total Compra" name="total_purchase_value">
                <InputNumber
                  style={{ width: '100%' }}
                  formatter={(value) => convertNumericToBrazilian(Number(value || 0))}
                  readOnly
                  precision={2}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={8}>
              <Form.Item label="Total Venda" name="total_sale_value">
                <InputNumber
                  style={{ width: '100%' }}
                  formatter={(value) => convertNumericToBrazilian(Number(value || 0))}
                  readOnly
                  precision={2}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={8}>
              <Form.Item label="Total Comissão" name="total_commission">
                <InputNumber
                  style={{ width: '100%' }}
                  formatter={(value) => convertNumericToBrazilian(Number(value || 0))}
                  readOnly
                  precision={2}
                />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={[16, 16]}>
            <Col xs={24} md={8}>
              <Form.Item label="% Rentabilidade" name="profitability_percentage">
                <InputNumber
                  style={{ width: '100%' }}
                  formatter={(value) => `${value}%`}
                  parser={(value) => value!.replace('%', '')}
                  readOnly
                  precision={2}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={8}>
              <Form.Item label="% Markup" name="markup_percentage">
                <InputNumber
                  style={{ width: '100%' }}
                  formatter={(value) => `${value}%`}
                  parser={(value) => value!.replace('%', '')}
                  readOnly
                  precision={2}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={8}>
              <Form.Item label="Total IPI" name="total_ipi_value">
                <InputNumber
                  style={{ width: '100%' }}
                  formatter={(value) => convertNumericToBrazilian(Number(value || 0))}
                  readOnly
                  precision={2}
                />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={[16, 16]}>
            <Col xs={24} md={12}>
              <Form.Item label="Total Impostos" name="total_taxes">
                <InputNumber
                  style={{ width: '100%' }}
                  formatter={(value) => convertNumericToBrazilian(Number(value || 0))}
                  readOnly
                  precision={2}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item label="Valor Final" name="total_final_value">
                <InputNumber
                  style={{ width: '100%' }}
                  formatter={(value) => convertNumericToBrazilian(Number(value || 0))}
                  readOnly
                  precision={2}
                />
              </Form.Item>
            </Col>
          </Row>

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
                        message="🎯 Cálculo Concluído"
                        description={`Orçamento calculado com markup de ${preview.markup_percentage.toFixed(1)}%. Todos os valores estão prontos para revisão.`}
                        type="success"
                        showIcon
                        style={{ marginBottom: '16px' }}
                      />
                      
                      <Row gutter={[16, 8]}>
                        <Col span={12}>
                          <div style={{ textAlign: 'center', padding: '8px', background: 'rgba(255,255,255,0.7)', borderRadius: '6px' }}>
                            <Text type="secondary" style={{ fontSize: '11px' }}>COMISSÃO TOTAL</Text>
                            <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#722ed1' }}>
                              {formatCurrency(preview.total_commission)}
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
                          style={{ marginTop: '12px' }}
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
