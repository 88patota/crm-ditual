/**
 * Utilitários de formatação para a aplicação
 */

/**
 * Formata o prazo de entrega para exibição
 * @param deliveryTime - Prazo em dias (string)
 * @returns String formatada para exibição
 */
export function formatDeliveryTime(deliveryTime?: string | null): string {
  if (!deliveryTime) return 'Imediato';
  
  try {
    const days = parseInt(deliveryTime);
    if (days <= 0) return 'Imediato';
    if (days === 1) return '1 dia';
    return `${days} dias`;
  } catch {
    return deliveryTime || 'Imediato';
  }
}

/**
 * Formata valores monetários
 * @param value - Valor numérico
 * @returns String formatada em Real brasileiro
 */
export function formatCurrency(value: number): string {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value);
}
