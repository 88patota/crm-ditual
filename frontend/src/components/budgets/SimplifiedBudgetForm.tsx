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
  Popconfirm,
  Select,
  DatePicker,
  Alert,
  Spin,
  App as AntdApp
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
import { formatCurrency, convertNumericToBrazilian, formatPercentageValue, formatPercentageValueNoRound, parsePercentageValue } from '../../lib/utils';
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
  const { message } = AntdApp.useApp();
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

  const updateItem = <K extends keyof BudgetItemSimplified>(
    index: number, 
    field: K, 
    value: BudgetItemSimplified[K] | string | number | null | undefined
  ) => {
    console.log('🔧 [EDIT DEBUG] Updating item', index, 'field:', field, 'value:', value);
    
    const newItems = [...items];
    const currentItem = { ...newItems[index] };
    
    // Log current item state before update
    console.log(`🔧 [EDIT DEBUG] Current item before update:`, currentItem);
    
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
      
      currentItem[field] = numericValue as BudgetItemSimplified[K];
      console.log('🔧 [EDIT DEBUG] Numeric field', field, 'converted to:', numericValue);
    } else {
      currentItem[field] = value as BudgetItemSimplified[K];
      console.log('🔧 [EDIT DEBUG] Non-numeric field', field, 'set to:', value);
    }
    
    newItems[index] = currentItem;
    
    // Log all items after update to ensure no data loss
    console.log(`🔧 [EDIT DEBUG] All items after update:`, newItems.map((item, idx) => ({
      index: idx,
      description: item.description,
      peso_compra: item.peso_compra,
      peso_venda: item.peso_venda,
      valor_com_icms_compra: item.valor_com_icms_compra,
      valor_com_icms_venda: item.valor_com_icms_venda,
      percentual_ipi: item.percentual_ipi,
      delivery_time: item.delivery_time
    })));
    
    setItems(newItems);
    setPreview(null);
    
    // Cálculos automáticos removidos - todos os cálculos são feitos no backend
  };

  // Função para recalcular quando o valor do frete total mudar
  const handleFreightValueChange = (value: number) => {
    console.log(`🔧 [EDIT DEBUG] Freight value changed to:`, value);
    
    // Update form field
    form.setFieldsValue({ freight_value_total: value });
    
    // Auto-calculate if we have enough data
    if (items.length > 0 && items.some(item => item.peso_compra > 0)) {
      console.log(`🔧 [EDIT DEBUG] Auto-cálculo removido - cálculos agora são feitos apenas no backend`);
    }
  };

  const calculatePreview = async () => {
    try {
      setCalculating(true);
      const formData = form.getFieldsValue();
      console.log('Calculate form data:', formData);
      console.log('Calculate freight_type:', formData.freight_type);
      
      // Normalizar itens antes da chamada ao backend (converter números e garantir defaults)
      const processedItems = items.map((item, index) => {
        const pesoCompra = parseFloat(item.peso_compra?.toString().replace(',', '.') || '0');
        const pesoVenda = parseFloat((item.peso_venda ?? item.peso_compra)?.toString().replace(',', '.') || '0');
        const valorCompra = parseFloat(item.valor_com_icms_compra?.toString().replace(',', '.') || '0');
        const valorVenda = parseFloat(item.valor_com_icms_venda?.toString().replace(',', '.') || '0');
        const outrasDespesas = parseFloat((item.outras_despesas_item ?? 0).toString().replace(',', '.') || '0');
        const percIpi = typeof item.percentual_ipi === 'number' ? item.percentual_ipi : 0.0;
        const percIcmsCompra = typeof item.percentual_icms_compra === 'number' ? item.percentual_icms_compra : 0.18;
        const percIcmsVenda = typeof item.percentual_icms_venda === 'number' ? item.percentual_icms_venda : 0.18;

        const normalized = {
          ...item,
          description: item.description || '',
          delivery_time: item.delivery_time || '0',
          peso_compra: pesoCompra,
          peso_venda: pesoVenda,
          valor_com_icms_compra: valorCompra,
          valor_com_icms_venda: valorVenda,
          outras_despesas_item: outrasDespesas,
          percentual_ipi: percIpi,
          percentual_icms_compra: percIcmsCompra,
          percentual_icms_venda: percIcmsVenda,
        };

        console.log('🔍 [CALC PREVIEW] Processed item', index, ':', normalized);
        return normalized;
      });
      
      // Validação básica antes da requisição
      const invalidIndex = processedItems.findIndex((it) => (
        !it.description ||
        (typeof it.peso_compra !== 'number' || it.peso_compra <= 0) ||
        (typeof it.valor_com_icms_compra !== 'number' || it.valor_com_icms_compra <= 0) ||
        (typeof it.valor_com_icms_venda !== 'number' || it.valor_com_icms_venda <= 0) ||
        (typeof it.percentual_icms_compra !== 'number' || it.percentual_icms_compra < 0 || it.percentual_icms_compra > 1) ||
        (typeof it.percentual_icms_venda !== 'number' || it.percentual_icms_venda < 0 || it.percentual_icms_venda > 1) ||
        (typeof it.percentual_ipi !== 'number' || ![0.0, 0.0325, 0.05].includes(it.percentual_ipi))
      ));
      if (invalidIndex !== -1) {
        message.error(`Preencha todos os campos obrigatórios do item ${invalidIndex + 1} e garanta percentuais válidos.`);
        return;
      }
      
      const budgetData: BudgetSimplified = {
        ...formData,
        order_number: orderNumber, // Usar o número gerado
        origem: formData.origem || undefined,
        outras_despesas_totais: formData.outras_despesas_totais || undefined,
        freight_type: formData.freight_type || 'FOB',
        payment_condition: formData.payment_condition || 'À vista',
        items: processedItems,
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
      
      // Atualizar os itens com os dados calculados, incluindo weight_difference_display
      if (calculation.items_calculations && calculation.items_calculations.length > 0) {
        const updatedItems = items.map((item, index) => {
          const calculatedItem = calculation.items_calculations[index];
          if (calculatedItem) {
            return {
              ...item,
              weight_difference_display: calculatedItem.weight_difference_display
            };
          }
          return item;
        });
        setItems(updatedItems);
      }
      
      // CORREÇÃO: Atualizar os campos do formulário com os valores calculados
      // Isso garante que os valores totais e de comissão sejam atualizados também no cálculo manual
      form.setFieldsValue({
        total_purchase_value: calculation.total_purchase_value,
        total_sale_value: calculation.total_sale_value,
        profitability_percentage: calculation.profitability_percentage,
        // Atualizar valores de IPI e finais se disponíveis
        total_ipi_value: calculation.total_ipi_value,
        total_final_value: calculation.total_final_value,
        // Atualizar impostos totais
        total_taxes: calculation.total_taxes,
        // Atualizar valor do frete por kg
        valor_frete_compra: calculation.valor_frete_compra,
        // Atualizar diferença total de peso
        total_weight_difference_percentage: calculation.total_weight_difference_percentage,
      });
      
      message.success(`Cálculos realizados! Rentabilidade calculada pelo backend: ${formatPercentageValueNoRound(calculation.profitability_percentage)}`);
    } catch (error) {
      console.error('Erro ao calcular orçamento:', error);
      const backendDetail =
        typeof error === 'object' && error !== null && 'response' in error
          ? (error as { response?: { data?: { detail?: string } } }).response?.data?.detail
          : undefined;
      if (backendDetail) {
        message.error(`Erro ao calcular orçamento: ${backendDetail}`);
      } else {
        message.error('Erro ao calcular orçamento. Verifique se todos os campos obrigatórios estão preenchidos.');
      }
    } finally {
      setCalculating(false);
    }
  };

  // Função de auto-cálculo removida - cálculos agora são feitos apenas no backend

  const handleSubmit = async () => {
    try {
      console.log('🚀 [SUBMIT DEBUG] Starting form submission...');
      
      const formData = await form.validateFields();
      console.log('🚀 [SUBMIT DEBUG] Form validation passed. Form data:', formData);
      console.log('🚀 [SUBMIT DEBUG] Current items state:', items);
      
      if (items.length === 0) {
        console.error('🚀 [SUBMIT DEBUG] No items found in budget');
        message.error('O orçamento deve conter pelo menos um item.');
        return;
      }

      // Validate required fields for each item
      const invalidItems = items.filter((item, index) => {
        const isInvalid = !item.description || 
                         item.peso_compra <= 0 || 
                         item.valor_com_icms_compra <= 0 || 
                         item.valor_com_icms_venda <= 0;
        
        if (isInvalid) {
          console.error(`🚀 [SUBMIT DEBUG] Item ${index} is invalid:`, {
            description: item.description,
            peso_compra: item.peso_compra,
            valor_com_icms_compra: item.valor_com_icms_compra,
            valor_com_icms_venda: item.valor_com_icms_venda
          });
        }
        
        return isInvalid;
      });

      if (invalidItems.length > 0) {
        console.error('🚀 [SUBMIT DEBUG] Found invalid items:', invalidItems);
        message.error('Todos os itens devem ter descrição, peso de compra, valor de compra e valor de venda preenchidos.');
        return;
      }

      // Prepare budget data with all required fields preserved
      const budgetData: BudgetSimplified = {
        ...formData,
        order_number: orderNumber, // Usar o número gerado automaticamente
        origem: formData.origem || undefined,
        outras_despesas_totais: formData.outras_despesas_totais || undefined,
        // Fix: Only include freight_type if it was explicitly set/changed
        ...(formData.freight_type !== undefined && { freight_type: formData.freight_type }),
        payment_condition: formData.payment_condition || 'À vista',
        items: items.map((item, index) => {
          console.log('🚀 [SUBMIT DEBUG] Processing item', index, ':', item);
          
          const processedItem = {
            ...item, // Preserve all existing fields
            description: item.description || '',
            delivery_time: item.delivery_time || '0',
            peso_compra: parseFloat(item.peso_compra.toString().replace(',', '.')),
            peso_venda: parseFloat((item.peso_venda || item.peso_compra).toString().replace(',', '.')),
            valor_com_icms_compra: parseFloat(item.valor_com_icms_compra.toString().replace(',', '.')),
            valor_com_icms_venda: parseFloat(item.valor_com_icms_venda.toString().replace(',', '.')),
            // CORREÇÃO: Garantir que o IPI seja incluído no salvamento
            percentual_ipi: typeof item.percentual_ipi === 'number' ? item.percentual_ipi : 0.0,
            // Preserve other fields that might exist
            percentual_icms_compra: item.percentual_icms_compra || 0.18,
            percentual_icms_venda: item.percentual_icms_venda || 0.18,
            outras_despesas_item: item.outras_despesas_item || 0
          };
          
          console.log('🚀 [SUBMIT DEBUG] Processed item', index, ':', processedItem);
          return processedItem;
        }),
        expires_at: formData.expires_at ? formData.expires_at.toISOString() : undefined,
      };
      
      console.log('🚀 [SUBMIT DEBUG] Final budget data being sent to backend:', JSON.stringify(budgetData, null, 2));
      console.log('🚀 [SUBMIT DEBUG] Items count:', budgetData.items.length);
      console.log('🚀 [SUBMIT DEBUG] All items have required fields:', budgetData.items.every(item => 
        item.description && item.peso_compra > 0 && item.valor_com_icms_compra > 0 && item.valor_com_icms_venda > 0
      ));
      
      await onSubmit(budgetData);
      
      console.log('🚀 [SUBMIT DEBUG] Form submission completed successfully');
    } catch (error) {
      console.error('🚀 [SUBMIT DEBUG] Form submission failed:', error);
      
      // Enhanced error handling
      if (error && typeof error === 'object' && 'response' in error) {
        const axiosError = error as { response?: { data?: { detail?: string; errors?: unknown } } };
        console.error('🚀 [SUBMIT DEBUG] Backend error details:', axiosError.response?.data);
        
        if (axiosError.response?.data?.detail) {
          message.error(`Erro de validação: ${axiosError.response.data.detail}`);
        } else {
          message.error('Erro ao validar dados no servidor. Verifique os campos obrigatórios.');
        }
      } else {
        console.error('🚀 [SUBMIT DEBUG] Validation error:', error);
        message.error('Erro ao validar o formulário. Verifique os campos obrigatórios.');
      }
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
      title: 'Quantidade Compra *',
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
      title: 'Quantidade Venda *',
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
      title: 'Diferença de Peso',
      dataIndex: 'weight_difference_display',
      key: 'weight_difference_display',
      width: 150,
      render: (value: { has_difference: boolean; absolute_difference: number; formatted_display: string } | undefined) => {
        if (!value || !value.has_difference) {
          return <Text type="secondary">-</Text>;
        }
        
        const isNegative = value.absolute_difference < 0;
        const color = isNegative ? '#ff4d4f' : '#52c41a';
        
        return (
          <Text style={{ color, fontWeight: 'bold' }}>
            {value.formatted_display}
          </Text>
        );
      },
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
          value={value * 100}
          onChange={(val) => updateItem(index, 'percentual_icms_compra', (val ?? 18) / 100)}
          min={0}
          max={100}
          step={0.1}
          precision={1}
          formatter={(v) => formatPercentageValue(Number(v || 0))}
          parser={(v) => parsePercentageValue(v || '')}
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
          value={value * 100}
          onChange={(val) => updateItem(index, 'percentual_icms_venda', (val ?? 18) / 100)}
          min={0}
          max={100}
          step={0.1}
          precision={1}
          formatter={(v) => formatPercentageValue(Number(v || 0))}
          parser={(v) => parsePercentageValue(v || '')}
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
                  placeholder={loadingOrderNumber ? "Gerando número..." : "PROP-00001"}
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
                  <Option value="approved">Aprovado</Option>
                  <Option value="lost">Perdido</Option>
                  <Option value="sent">Orçamento Enviado</Option>
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
                <DatePicker style={{ width: '100%' }} format="DD-MM-YYYY" />
              </Form.Item>
            </Col>
            <Col xs={24} md={6}>
              <Form.Item
                label="Origem"
                name="origem"
              >
                <Select style={{ width: '100%' }} placeholder="Selecione a origem">
                  <Option value="Orpen Whatsapp">Orpen Whatsapp</Option>
                  <Option value="Prospeccao">Prospecção</Option>
                  <Option value="Primeiro Google">Primeiro Contato Google</Option>
                  <Option value="Email Vendas">E-mail Vendas</Option>
                  <Option value="Cliente Ativo">Cliente Ativo</Option>
                  <Option value="Reativacao Cliente">Reativação Cliente</Option>
                  <Option value="Indicacao">Indicação</Option>
                </Select>
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
                  onChange={(value) => {
                    console.log('Select onChange - payment_condition:', value);
                    
                    // Auto-recalcular quando as condições de pagamento mudarem
                    const formData = form.getFieldsValue();
                    if (formData.client_name && items.length > 0) {
                      // Auto-cálculo removido - cálculos agora são feitos apenas no backend
                    }
                  }}
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
                    
                    // Auto-recalcular quando o tipo de frete mudar
                    const formData = form.getFieldsValue();
                    if (formData.client_name && items.length > 0) {
                      // Auto-cálculo removido - cálculos agora são feitos apenas no backend
                    }
                    
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
                label="Valor Total Frete"
                name="freight_value_total"
              >
                <CurrencyInput
                  value={form.getFieldValue('freight_value_total')}
                  onChange={handleFreightValueChange}
                  placeholder="R$ 0,00"
                  style={{ width: '100%' }}
                />
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
            description="Preencha: Cliente, Descrição, Quantidade Compra, Quantidade Venda, Valor c/ICMS (Compra), % ICMS (Compra), Valor c/ICMS (Venda) e % ICMS (Venda). O cálculo é baseado no peso dos produtos conforme a planilha de negócio."
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
            <Col xs={24} md={8}>
              <Form.Item label="Total Impostos" name="total_taxes">
                <InputNumber
                  style={{ width: '100%' }}
                  formatter={(value) => convertNumericToBrazilian(Number(value || 0))}
                  readOnly
                  precision={2}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={8}>
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
                background: '#FFFFFF',
                border: '1px solid #f0f0f0',
                marginBottom: '24px'
              }}>
                <Row gutter={[24, 16]}>
                  <Col xs={24} lg={16}>
                    <div style={{ padding: '8px 0' }}>
                      <Alert
                        message="🎯 Cálculo Realizado pelo Backend"
                description={`Orçamento calculado pelo backend com rentabilidade de ${formatPercentageValueNoRound(preview.profitability_percentage)}. Todos os valores estão prontos para revisão.`}
                        type="success"
                        showIcon
                        style={{ marginBottom: '16px' }}
                      />
                      
                      <Row gutter={[16, 8]}>
                        <Col span={8}>
                          <div style={{ textAlign: 'center', padding: '8px', background: 'rgba(255,255,255,0.7)', borderRadius: '6px' }}>
                            <Text type="secondary" style={{ fontSize: '11px' }}>COMISSÃO TOTAL</Text>
                            <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#722ed1' }}>
                              {formatCurrency(preview.total_commission)}
                            </div>
                          </div>
                        </Col>
                        <Col span={8}>
                          <div style={{ textAlign: 'center', padding: '8px', background: 'rgba(255,255,255,0.7)', borderRadius: '6px' }}>
                            <Text type="secondary" style={{ fontSize: '11px' }}>RENTABILIDADE</Text>
                            <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#13c2c2' }}>
                {formatPercentageValueNoRound(preview.profitability_percentage)}
                            </div>
                          </div>
                        </Col>
                        <Col span={8}>
                          <div style={{ textAlign: 'center', padding: '8px', background: 'rgba(255,255,255,0.7)', borderRadius: '6px' }}>
                            <Text type="secondary" style={{ fontSize: '11px' }}>DIFERENÇA PESO</Text>
                            <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#fa541c' }}>
                              {formatPercentageValue(preview.total_weight_difference_percentage || 0)}
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
