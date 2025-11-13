import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { message, Spin, Result } from 'antd';
import SimplifiedBudgetForm from '../components/budgets/SimplifiedBudgetForm';
import { budgetService } from '../services/budgetService';
import type { BudgetSimplified, Budget } from '../services/budgetService';

export default function BudgetEdit() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: budget, isLoading, error } = useQuery({
    queryKey: ['budget', id],
    queryFn: () => budgetService.getBudgetById(Number(id)),
    enabled: !!id,
  });

  const updateBudgetMutation = useMutation({
    mutationFn: (budgetData: BudgetSimplified) => {
      console.log('🔍 DEBUG - BudgetEdit mutationFn - Data passed to mutationFn:', budgetData);
      console.log('🔍 DEBUG - BudgetEdit mutationFn - payment_condition:', budgetData.payment_condition);
      console.log('🔍 DEBUG - BudgetEdit mutationFn - freight_type:', budgetData.freight_type);
      return budgetService.updateBudgetSimplified(Number(id), budgetData);
    },
    onSuccess: (data) => {
      console.log('🔍 DEBUG - BudgetEdit onSuccess - Updated budget data received from backend:', data);
      console.log('🔍 DEBUG - BudgetEdit onSuccess - payment_condition in response:', data.payment_condition);
      message.success('Orçamento atualizado com sucesso!');
      queryClient.invalidateQueries({ queryKey: ['budgets'] });
      queryClient.invalidateQueries({ queryKey: ['budget', id] });
      navigate(`/budgets/${data.id}`);
    },
    onError: (error: unknown) => {
      console.error('Erro ao atualizar orçamento:', error);
      const errorMessage = getErrorMessage(error);
      message.error(errorMessage);
    },
  });

  const getErrorMessage = (error: unknown): string => {
    if (typeof error === 'object' && error !== null && 'response' in error) {
      const axiosError = error as { response?: { data?: { detail?: string } } };
      if (axiosError.response?.data?.detail) {
        return axiosError.response.data.detail;
      }
    }
    return 'Ocorreu um erro ao atualizar o orçamento. Tente novamente.';
  };

  // Converter dados do orçamento para o formato simplificado
  const convertToSimplifiedBudget = (budget: Budget): BudgetSimplified => {
    console.log('🔍 DEBUG - BudgetEdit convertToSimplifiedBudget - Raw budget from backend:', budget);
    
    const result: BudgetSimplified = {
      order_number: budget.order_number,
      client_name: budget.client_name,
      status: budget.status,
      expires_at: budget.expires_at,
      notes: budget.notes,
      freight_type: budget.freight_type || 'FOB',
      payment_condition: budget.payment_condition,
      freight_value_total: budget.freight_value_total,
      prazo_medio: budget.prazo_medio || 30,
      outras_despesas_totais: budget.outras_despesas_totais || 0,
      items: budget.items?.map((item) => ({
        description: item.description,
        delivery_time: item.delivery_time || '0',
        peso_compra: item.weight || 0,
        valor_com_icms_compra: item.purchase_value_with_icms,
        percentual_icms_compra: item.purchase_icms_percentage,
        outras_despesas_item: item.purchase_other_expenses || 0,
        peso_venda: item.sale_weight || item.weight || 0,
        valor_com_icms_venda: item.sale_value_with_icms,
        percentual_icms_venda: item.sale_icms_percentage,
        percentual_ipi: item.ipi_percentage || 0.0,
        // Campos calculados (opcionais)
        valor_sem_icms_compra: item.purchase_value_without_taxes,
        valor_sem_icms_venda: item.sale_value_without_taxes,
        valor_ipi: item.ipi_value,
        valor_total_com_ipi: item.total_value_with_ipi,
        // Exibir rentabilidade total do item para refletir diferença de peso
        rentabilidade: item.total_profitability ?? item.profitability,
        comissao: item.commission_value,
        weight_difference_display: item.weight_difference_display,
      })) || [],
    };
    
    console.log('🔍 DEBUG - BudgetEdit convertToSimplifiedBudget - Converted result:', result);
    return result;
  };

  const handleSubmit = async (budgetData: BudgetSimplified) => {
    console.log('🔍 DEBUG - BudgetEdit handleSubmit - Budget data received from form:', budgetData);
    console.log('🔍 DEBUG - BudgetEdit handleSubmit - payment_condition:', budgetData.payment_condition);
    console.log('BudgetEdit handleSubmit - budgetData received:', budgetData);
    console.log('BudgetEdit handleSubmit - freight_type:', budgetData.freight_type);
    await updateBudgetMutation.mutateAsync(budgetData);
  };

  const handleCancel = () => {
    navigate(`/budgets/${id}`);
  };

  if (isLoading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        minHeight: '400px' 
      }}>
        <Spin size="large" />
      </div>
    );
  }

  if (error || !budget) {
    return (
      <Result
        status="404"
        title="Orçamento não encontrado"
        subTitle="O orçamento que você está procurando não existe ou foi removido."
        extra={
          <button
            onClick={() => navigate('/budgets')}
            style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              padding: '8px 16px',
              borderRadius: '6px',
              border: 'none',
              cursor: 'pointer'
            }}
          >
            Voltar para Orçamentos
          </button>
        }
      />
    );
  }

  const simplifiedBudget = budget ? convertToSimplifiedBudget(budget) : null;

  return (
    <SimplifiedBudgetForm
      initialData={simplifiedBudget}
      onSubmit={handleSubmit}
      onCancel={handleCancel}
      isLoading={updateBudgetMutation.isPending}
      isEdit={true}
    />
  );
}