import { useNavigate } from 'react-router-dom';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { message } from 'antd';
import BudgetForm from '../components/budgets/BudgetForm';
import { budgetService } from '../services/budgetService';
import type { Budget } from '../services/budgetService';

export default function BudgetCreate() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const createBudgetMutation = useMutation({
    mutationFn: budgetService.createBudget,
    onSuccess: (data) => {
      message.success('Orçamento criado com sucesso!');
      queryClient.invalidateQueries({ queryKey: ['budgets'] });
      navigate(`/budgets/${data.id}`);
    },
    onError: (error: unknown) => {
      console.error('Erro ao criar orçamento:', error);
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
    return 'Ocorreu um erro ao criar o orçamento. Tente novamente.';
  };

  const handleSubmit = async (budgetData: Budget) => {
    await createBudgetMutation.mutateAsync(budgetData);
  };

  const handleCancel = () => {
    navigate('/budgets');
  };

  return (
    <BudgetForm
      onSubmit={handleSubmit}
      onCancel={handleCancel}
      isLoading={createBudgetMutation.isPending}
      isEdit={false}
    />
  );
}