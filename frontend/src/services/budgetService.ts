import api from '../lib/api';

export interface BudgetItem {
  id?: number;
  description: string;
  quantity: number;
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
  commission_percentage: number;
  commission_value?: number;
  dunamis_cost?: number;
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
  total_sale_value: number;
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
}

const BUDGET_API_URL = 'http://localhost:8002/api/v1/budgets';

export const budgetService = {
  // Create budget
  async createBudget(budget: Budget): Promise<Budget> {
    const response = await api.post<Budget>(`${BUDGET_API_URL}/`, budget);
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
    const response = await api.get<BudgetSummary[]>(BUDGET_API_URL, { params });
    return response.data;
  },

  // Get budget by ID
  async getBudgetById(id: number): Promise<Budget> {
    const response = await api.get<Budget>(`${BUDGET_API_URL}/${id}`);
    return response.data;
  },

  // Get budget by order number
  async getBudgetByOrderNumber(orderNumber: string): Promise<Budget> {
    const response = await api.get<Budget>(`${BUDGET_API_URL}/order/${orderNumber}`);
    return response.data;
  },

  // Update budget
  async updateBudget(id: number, budget: Partial<Budget>): Promise<Budget> {
    const response = await api.put<Budget>(`${BUDGET_API_URL}/${id}`, budget);
    return response.data;
  },

  // Delete budget
  async deleteBudget(id: number): Promise<void> {
    await api.delete(`${BUDGET_API_URL}/${id}`);
  },

  // Recalculate budget
  async recalculateBudget(id: number): Promise<Budget> {
    const response = await api.post<Budget>(`${BUDGET_API_URL}/${id}/recalculate`);
    return response.data;
  },

  // Apply markup
  async applyMarkup(id: number, markupPercentage: number): Promise<Budget> {
    const response = await api.post<Budget>(
      `${BUDGET_API_URL}/${id}/apply-markup?markup_percentage=${markupPercentage}`
    );
    return response.data;
  },

  // Calculate budget (preview)
  async calculateBudget(budget: Budget): Promise<BudgetCalculation> {
    const response = await api.post<BudgetCalculation>(`${BUDGET_API_URL}/calculate`, budget);
    return response.data;
  },

  // Calculate with markup (preview)
  async calculateWithMarkup(budget: Budget, markupPercentage: number): Promise<BudgetCalculation> {
    const response = await api.post<BudgetCalculation>(
      `${BUDGET_API_URL}/calculate-with-markup?markup_percentage=${markupPercentage}`,
      budget
    );
    return response.data;
  },
};