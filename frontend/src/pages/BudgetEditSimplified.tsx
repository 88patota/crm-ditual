import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { message, Spin, Result } from 'antd';
import SimplifiedBudgetForm from '../components/budgets/SimplifiedBudgetForm';
import { budgetService } from '../services/budgetService';
import type { BudgetSimplified, Budget } from '../services/budgetService';

export default function BudgetEditSimplified() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: budget, isLoading, error } = useQuery({
    queryKey: ['budget', id],
    queryFn: () => budgetService.getBudgetById(Number(id)),
    enabled: !!id,
  });

  const updateBudgetMutation = useMutation({
    mutationFn: async (budgetData: BudgetSimplified) => {
      // Converter os dados simplificados para o formato completo para atualização
      const convertedBudget: Partial<Budget> = {
        order_number: budgetData.order_number || '',
        client_name: budgetData.client_name,
        status: budgetData.status as 'draft' | 'pending' | 'approved' | 'rejected' | 'expired',
        expires_at: budgetData.expires_at,
        notes: budgetData.notes,
        markup_percentage: 0, // Será calculado automaticamente
        items: budgetData.items.map(item => ({
          description: item.description,
          quantity: 1, // Valor padrão
          weight: item.peso_compra,
          sale_weight: item.peso_venda,
          purchase_value_with_icms: item.valor_com_icms_compra,
          purchase_icms_percentage: item.percentual_icms_compra, // Keep as decimal (0.18 for 18%)
          purchase_other_expenses: item.outras_despesas_item || 0,
          purchase_value_without_taxes: 0, // Será calculado
          sale_value_with_icms: item.valor_com_icms_venda,
          sale_icms_percentage: item.percentual_icms_venda, // Keep as decimal (0.18 for 18%)
          sale_value_without_taxes: 0, // Será calculado
          dunamis_cost: 0,
        })),
      };
      
      return budgetService.updateBudget(Number(id), convertedBudget);
    },
    onSuccess: (data: Budget) => {
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
    return {
      order_number: budget.order_number,
      client_name: budget.client_name,
      status: budget.status,
      expires_at: budget.expires_at,
      notes: budget.notes,
      prazo_medio: 30, // Valor padrão, pois não está no Budget original
      outras_despesas_totais: 0, // Valor padrão, pois não está no Budget original
      items: budget.items?.map((item) => ({
        description: item.description,
        peso_compra: item.weight || 0,
        peso_venda: item.sale_weight || item.weight || 0,
        valor_com_icms_compra: item.purchase_value_with_icms || 0,
        percentual_icms_compra: item.purchase_icms_percentage || 0.18, // Keep as decimal (0.18 for 18%)
        outras_despesas_item: item.purchase_other_expenses || 0,
        valor_com_icms_venda: item.sale_value_with_icms || 0,
        percentual_icms_venda: item.sale_icms_percentage || 0.18, // Keep as decimal (0.18 for 18%)
      })) || [],
    };
  };

  const handleSubmit = async (budgetData: BudgetSimplified) => {
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

  const simplifiedBudget = convertToSimplifiedBudget(budget);

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
