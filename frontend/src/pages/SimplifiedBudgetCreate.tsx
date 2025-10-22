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
      const axiosError = error as { 
        response?: { 
          data?: { 
            detail?: string | Array<{ msg: string; type: string; loc: string[] }>;
          } 
        } 
      };
      
      if (axiosError.response?.data?.detail) {
        const detail = axiosError.response.data.detail;
        
        // Se for um array de erros de validação
        if (Array.isArray(detail)) {
          const validationErrors = detail.map(err => {
            const field = err.loc.join('.');
            return `${field}: ${err.msg}`;
          }).join(', ');
          return `Erros de validação: ${validationErrors}`;
        }
        
        // Se for uma string simples
        if (typeof detail === 'string') {
          return detail;
        }
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
      isEdit={false}
    />
  );
}