import api from '../lib/api';

// Tipos simplificados - APENAS campos obrigatórios (atualizados conforme novas regras de negócio)
export interface BudgetItemSimplified {
  description: string;
  
  // Bloco Compras - Purchase data
  peso_compra: number;
  valor_com_icms_compra: number;
  percentual_icms_compra: number;
  outras_despesas_item?: number;
  
  // Bloco Vendas - Sale data  
  peso_venda: number;
  valor_com_icms_venda: number;
  percentual_icms_venda: number;
  
  // IPI (Imposto sobre Produtos Industrializados)
  percentual_ipi?: number; // 0%, 3.25% ou 5% (formato decimal: 0.0, 0.0325, 0.05)
}

export interface BudgetSimplified {
  order_number?: string; // Será gerado automaticamente se não fornecido
  client_name: string;
  status?: string;
  expires_at?: string;
  notes?: string;
  
  // Novos campos conforme regras de negócio
  prazo_medio?: number; // Prazo médio em dias
  outras_despesas_totais?: number; // Outras despesas do pedido
  
  items: BudgetItemSimplified[];
}

export interface BudgetPreviewCalculation {
  total_purchase_value: number;
  total_sale_value: number;
  total_commission: number;
  profitability_percentage: number;
  markup_percentage: number; // CALCULADO AUTOMATICAMENTE
  items_preview: Array<{
    description: string;
    quantity: number;
    purchase_value_with_icms: number;
    calculated_markup: number; // NOVO: markup individual calculado
    sale_value_with_icms: number;
    total_purchase: number;
    total_sale: number;
    profitability: number;
    commission_value: number;
  }>;
  commission_percentage_default: number;
  sale_icms_percentage_default: number;
  other_expenses_default: number;
  // NOVOS CAMPOS
  minimum_markup_applied: number;
  maximum_markup_applied: number;
  
  // IPI preview calculations
  total_ipi_value?: number; // Total do IPI de todos os itens
  total_final_value?: number; // Valor final incluindo IPI
}

export interface MarkupConfiguration {
  minimum_markup_percentage: number;
  maximum_markup_percentage: number;
  default_market_position: string;
  icms_sale_default: number;
  commission_default: number;
  other_expenses_default: number;
}

// Interface para estatísticas do dashboard
export interface DashboardStats {
  period: {
    start_date: string;
    end_date: string;
    days?: number;
  };
  budgets_by_status: {
    draft: number;
    pending: number;
    approved: number;
    rejected: number;
    expired: number;
  };
  total_budgets: number;
  total_value: number;
  approved_budgets: number;
  approved_value: number;
  conversion_rate: number;
}

export interface BudgetItem {
  id?: number;
  description: string;
  quantity?: number;
  weight?: number;
  
  // Purchase data
  purchase_value_with_icms: number;
  purchase_icms_percentage: number;
  purchase_other_expenses: number;
  purchase_value_without_taxes: number;
  purchase_value_with_weight_diff?: number;
  
  // Sale data
  sale_weight?: number;
  sale_value_with_icms: number;
  sale_icms_percentage: number;
  sale_value_without_taxes: number;
  weight_difference?: number;
  
  // Calculated fields
  profitability?: number;
  total_purchase?: number;
  total_sale?: number;
  unit_value?: number;
  total_value?: number;
  
  // Commission
  commission_percentage?: number;  // Now calculated dynamically based on profitability
  commission_percentage_actual?: number;  // Actual percentage used by backend
  commission_value?: number;
  dunamis_cost?: number;
  
  // IPI (Imposto sobre Produtos Industrializados)
  ipi_percentage?: number; // Percentual de IPI (formato decimal: 0.0, 0.0325, 0.05)
  ipi_value?: number; // Valor do IPI calculado
  total_value_with_ipi?: number; // Valor total incluindo IPI
}

export interface Budget {
  id?: number;
  order_number: string;
  client_name: string;
  client_id?: number;
  markup_percentage: number;
  notes?: string;
  expires_at?: string;
  
  // Financial totals
  total_purchase_value?: number;
  total_sale_value?: number;
  total_commission?: number;
  profitability_percentage?: number;
  
  // IPI totals
  total_ipi_value?: number; // Total do IPI de todos os itens
  total_final_value?: number; // Valor final incluindo IPI (valor que o cliente paga)
  
  status?: 'draft' | 'pending' | 'approved' | 'rejected' | 'expired';
  created_by?: string;
  created_at?: string;
  updated_at?: string;
  
  items: BudgetItem[];
}

export interface BudgetSummary {
  id: number;
  order_number: string;
  client_name: string;
  status: string;
  total_sale_value: number;
  total_commission: number;
  profitability_percentage: number;
  items_count: number;
  created_at: string;
}

export interface BudgetCalculation {
  total_purchase_value: number;
  total_sale_value: number;  // SEM impostos - valor que muda quando ICMS muda
  total_net_revenue: number;  // SEM impostos - receita líquida que muda com ICMS (mesmo que total_sale_value)
  total_taxes: number;  // Impostos totais
  total_commission: number;
  profitability_percentage: number;
  markup_percentage: number;
  items_calculations: Array<{
    description: string;
    quantity: number;
    total_purchase: number;
    total_sale: number;
    profitability: number;
    commission_value: number;
  }>;
  
  // IPI calculations
  total_ipi_value?: number; // Total do IPI de todos os itens
  total_final_value?: number; // Valor final incluindo IPI
}

export const budgetService = {
  // Create budget
  async createBudget(budget: Budget): Promise<Budget> {
    const response = await api.post<Budget>('/budgets/', budget);
    return response.data;
  },

  // Get all budgets
  async getBudgets(params?: {
    skip?: number;
    limit?: number;
    status?: string;
    client_name?: string;
    created_by?: string;
  }): Promise<BudgetSummary[]> {
    const response = await api.get<BudgetSummary[]>('/budgets/', { params });
    return response.data;
  },

  // Get budget by ID
  async getBudgetById(id: number): Promise<Budget> {
    const response = await api.get<Budget>(`/budgets/${id}`);
    return response.data;
  },

  // Get budget by order number
  async getBudgetByOrderNumber(orderNumber: string): Promise<Budget> {
    const response = await api.get<Budget>(`/budgets/order/${orderNumber}`);
    return response.data;
  },

  // Update budget
  async updateBudget(id: number, budget: Partial<Budget>): Promise<Budget> {
    const response = await api.put<Budget>(`/budgets/${id}`, budget);
    return response.data;
  },

  // Delete budget
  async deleteBudget(id: number): Promise<void> {
    await api.delete(`/budgets/${id}`);
  },

  // Recalculate budget
  async recalculateBudget(id: number): Promise<Budget> {
    const response = await api.post<Budget>(`/budgets/${id}/recalculate`);
    return response.data;
  },

  // Apply markup
  async applyMarkup(id: number, markupPercentage: number): Promise<Budget> {
    const response = await api.post<Budget>(
      `/budgets/${id}/apply-markup?markup_percentage=${markupPercentage}`
    );
    return response.data;
  },

  // Calculate budget (preview)
  async calculateBudget(budget: Budget): Promise<BudgetCalculation> {
    const response = await api.post<BudgetCalculation>('/budgets/calculate', budget);
    return response.data;
  },

  // Calculate with markup (preview)
  async calculateWithMarkup(budget: Budget, markupPercentage: number): Promise<BudgetCalculation> {
    const response = await api.post<BudgetCalculation>(
      `/budgets/calculate-with-markup?markup_percentage=${markupPercentage}`,
      budget
    );
    return response.data;
  },

  // MÉTODOS SIMPLIFICADOS

  // Método para calcular orçamento simplificado
  async calculateBudgetSimplified(budget: BudgetSimplified): Promise<BudgetCalculation> {
    const response = await api.post<BudgetCalculation>('/budgets/calculate-simplified', budget);
    return response.data;
  },

  // Método para obter configurações de markup
  async getMarkupSettings(): Promise<MarkupConfiguration> {
    const response = await api.get<MarkupConfiguration>('/budgets/markup-settings');
    return response.data;
  },

  // Método para obter próximo número de pedido
  async getNextOrderNumber(): Promise<string> {
    const response = await api.get<{order_number: string}>('/budgets/next-order-number');
    return response.data.order_number;
  },

  // Método para criar orçamento simplificado
  async createBudgetSimplified(budget: BudgetSimplified): Promise<Budget> {
    const response = await api.post<Budget>('/budgets/simplified', budget);
    return response.data;
  },

  // MÉTODOS PARA EXPORTAÇÃO PDF

  // Exportar orçamento como PDF por ID
  async exportBudgetAsPdf(id: number, simplified: boolean = false): Promise<Blob> {
    const response = await api.get(`/budgets/${id}/export-pdf?simplified=${simplified}`, {
      responseType: 'blob',
    });
    return response.data;
  },

  // Exportar orçamento como PDF por número do pedido
  async exportBudgetByOrderAsPdf(orderNumber: string, simplified: boolean = false): Promise<Blob> {
    const response = await api.get(`/budgets/order/${orderNumber}/export-pdf?simplified=${simplified}`, {
      responseType: 'blob',
    });
    return response.data;
  },

  // Função auxiliar para fazer download do PDF
  downloadPdf(pdfBlob: Blob, filename: string): void {
    const url = window.URL.createObjectURL(pdfBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  },

  // Método completo para exportar e fazer download
  async exportAndDownloadPdf(
    id: number, 
    simplified: boolean = false, 
    customFilename?: string
  ): Promise<void> {
    try {
      const pdfBlob = await this.exportBudgetAsPdf(id, simplified);
      
      // Gerar nome do arquivo se não fornecido
      const filename = customFilename || 
        `Proposta_${simplified ? 'Simplificada' : 'Completa'}_${Date.now()}.pdf`;
      
      this.downloadPdf(pdfBlob, filename);
    } catch (error) {
      // Log error for debugging but don't expose to user
      if (import.meta.env.DEV) {
        console.error('Erro ao exportar PDF:', error);
      }
      throw error;
    }
  },

  // Método completo para exportar por número do pedido e fazer download
  async exportAndDownloadPdfByOrder(
    orderNumber: string, 
    simplified: boolean = false, 
    customFilename?: string
  ): Promise<void> {
    try {
      const pdfBlob = await this.exportBudgetByOrderAsPdf(orderNumber, simplified);
      
      // Gerar nome do arquivo se não fornecido
      const filename = customFilename || 
        `Proposta_${simplified ? 'Simplificada' : 'Completa'}_${orderNumber}.pdf`;
      
      this.downloadPdf(pdfBlob, filename);
    } catch (error) {
      // Log error for debugging but don't expose to user
      if (import.meta.env.DEV) {
        console.error('Erro ao exportar PDF:', error);
      }
      throw error;
    }
  },

  // Estatísticas do dashboard
  async getDashboardStats(days?: number, customStart?: string, customEnd?: string): Promise<DashboardStats> {
    const params = new URLSearchParams();
    
    if (days !== undefined) {
      params.append('days', days.toString());
    }
    
    if (customStart && customEnd) {
      params.append('custom_start', customStart);
      params.append('custom_end', customEnd);
    }
    
    const response = await api.get(`/dashboard/stats?${params.toString()}`);
    return response.data;
  },
};
