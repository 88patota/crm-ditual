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

// Funções aprimoradas para formatação brasileira de valores monetários
export function formatCurrencyInputValue(value: number | string | undefined): string {
  if (value === undefined || value === null || value === '') return '';
  
  // Se for string, tentar converter para número
  const numValue = typeof value === 'string' ? parseFloat(value) : value;
  
  // Se não for um número válido, retornar string vazia
  if (isNaN(numValue)) return '';
  
  // Se for 0, retornar "0,00"
  if (numValue === 0) return '0,00';
  
  // Formatar no padrão brasileiro: 1.000,00
  return numValue.toLocaleString('pt-BR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
}

// Função para formatação durante a digitação (máscara automática)
export function formatCurrencyAsYouType(value: string): string {
  if (!value) return '';
  
  // Remove tudo que não é dígito
  const digits = value.replace(/\D/g, '');
  
  if (!digits) return '';
  
  // Converte para número (centavos)
  const cents = parseInt(digits, 10);
  
  // Converte centavos para reais
  const reais = cents / 100;
  
  // Formatar no padrão brasileiro com símbolo R$
  return 'R$ ' + reais.toLocaleString('pt-BR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
}

export function parseCurrencyInputValue(value: string | undefined): number {
  if (!value || value === '') return 0;
  
  // Remove todos os caracteres que não são dígitos, vírgula ou ponto
  let cleanValue = value.replace(/[^\d.,]/g, '');
  
  // Se tiver vírgula e ponto, assumir que vírgula é decimal (padrão brasileiro)
  if (cleanValue.includes(',') && cleanValue.includes('.')) {
    // Remove pontos (separadores de milhares) e mantém vírgula como decimal
    cleanValue = cleanValue.replace(/\./g, '').replace(',', '.');
  } else if (cleanValue.includes(',')) {
    // Substitui vírgula por ponto para parseFloat
    cleanValue = cleanValue.replace(',', '.');
  }
  
  const parsed = parseFloat(cleanValue);
  return isNaN(parsed) ? 0 : parsed;
}

// Função para converter valor brasileiro para formato numérico da API
export function convertBrazilianToNumeric(value: string | number): number {
  if (typeof value === 'number') return value;
  if (!value || value === '') return 0;
  
  // Remove "R$", espaços e outros caracteres não numéricos exceto vírgula e ponto
  let cleanValue = value.toString().replace(/[R$\s]/g, '').replace(/[^\d.,]/g, '');
  
  // Tratar formato brasileiro: 1.000,00 → 1000.00
  if (cleanValue.includes(',') && cleanValue.includes('.')) {
    // Formato: 1.000,00 - remove pontos e substitui vírgula por ponto
    cleanValue = cleanValue.replace(/\./g, '').replace(',', '.');
  } else if (cleanValue.includes(',')) {
    // Formato: 1000,00 - substitui vírgula por ponto
    cleanValue = cleanValue.replace(',', '.');
  }
  
  const parsed = parseFloat(cleanValue);
  return isNaN(parsed) ? 0 : parsed;
}

// Função para converter valor numérico para formato brasileiro de exibição
export function convertNumericToBrazilian(value: number | string): string {
  if (value === undefined || value === null || value === '') return 'R$ 0,00';
  
  const numValue = typeof value === 'string' ? parseFloat(value) : value;
  
  if (isNaN(numValue)) return 'R$ 0,00';
  
  return `R$ ${numValue.toLocaleString('pt-BR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })}`;
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
