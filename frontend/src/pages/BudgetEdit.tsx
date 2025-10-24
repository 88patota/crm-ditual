import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { message, Spin, Result } from 'antd';
import SimplifiedBudgetForm from '../components/budgets/SimplifiedBudgetForm';
import { budgetService } from '../services/budgetService';
import type { BudgetSimplified } from '../services/budgetService';

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

  return (
    <SimplifiedBudgetForm
      initialData={budget}
      onSubmit={handleSubmit}
      onCancel={handleCancel}
      isLoading={updateBudgetMutation.isPending}
      isEdit={true}
    />
  );
}