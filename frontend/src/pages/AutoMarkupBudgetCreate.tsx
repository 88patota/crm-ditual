import { useNavigate } from 'react-router-dom';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { message } from 'antd';
import SimplifiedBudgetForm from '../components/budgets/SimplifiedBudgetForm';
import { budgetService } from '../services/budgetService';
import type { BudgetSimplified } from '../services/budgetService';

export default function SimplifiedBudgetCreate() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const createBudgetMutation = useMutation({
    mutationFn: budgetService.createBudgetSimplified,
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

  const handleSubmit = async (budgetData: BudgetSimplified) => {
    await createBudgetMutation.mutateAsync(budgetData);
  };

  const handleCancel = () => {
    navigate('/budgets');
  };

  return (
    <SimplifiedBudgetForm
      onSubmit={handleSubmit}
      onCancel={handleCancel}
      isLoading={createBudgetMutation.isPending}
    />
  );
}
