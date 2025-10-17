import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: Date | string) {
  return new Intl.DateTimeFormat('pt-BR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(new Date(date));
}

export function formatDateTime(date: Date | string) {
  return new Intl.DateTimeFormat('pt-BR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(date));
}

export function formatCurrency(amount: number) {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(amount);
}

// Funções melhoradas para formatação de valores monetários sem interferir na digitação
export function formatCurrencyInputValue(value: number | string | undefined): string {
  if (value === undefined || value === null || value === '') return '';
  
  // Se for string, tentar converter para número
  const numValue = typeof value === 'string' ? parseFloat(value) : value;
  
  // Se não for um número válido ou for 0, retornar string vazia
  if (isNaN(numValue) || numValue === 0) return '';
  
  // Formatar apenas para exibição, sem símbolos que atrapalhem a digitação
  return numValue.toLocaleString('pt-BR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
}

export function parseCurrencyInputValue(value: string | undefined): number {
  if (!value || value === '') return 0;
  
  // Remove todos os caracteres que não são dígitos, vírgula ou ponto
  let cleanValue = value.replace(/[^\d.,]/g, '');
  
  // Se tiver vírgula e ponto, assumir que vírgula é decimal
  if (cleanValue.includes(',') && cleanValue.includes('.')) {
    // Remove pontos (separadores de milhares) e mantém vírgula como decimal
    cleanValue = cleanValue.replace(/\./g, '').replace(',', '.');
  } else if (cleanValue.includes(',')) {
    // Substitui vírgula por ponto
    cleanValue = cleanValue.replace(',', '.');
  }
  
  const parsed = parseFloat(cleanValue);
  return isNaN(parsed) ? 0 : parsed;
}

export function formatPercentageValue(value: number | string | undefined): string {
  if (value === undefined || value === null || value === '') return '';
  
  const numValue = typeof value === 'string' ? parseFloat(value) : value;
  
  if (isNaN(numValue)) return '';
  
  return `${numValue.toFixed(1)}%`;
}

export function parsePercentageValue(value: string | undefined): number {
  if (!value || value === '') return 0;
  
  // Remove o símbolo % e espaços
  const cleanValue = value.replace(/[%\s]/g, '').replace(',', '.');
  const parsed = parseFloat(cleanValue);
  
  return isNaN(parsed) ? 0 : parsed;
}
