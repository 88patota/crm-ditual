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

// Arredondamento HALF_UP para evitar inconsistências de ponto flutuante
export function roundHalfUp(value: number, decimals = 2): number {
  if (!isFinite(value)) return 0;
  const factor = Math.pow(10, decimals);
  // Mitigar erros binários (ex.: 1.005)
  const scaled = parseFloat((value * factor).toFixed(12));
  const sign = scaled >= 0 ? 1 : -1;
  const abs = Math.abs(scaled);
  const floorAbs = Math.floor(abs);
  const frac = abs - floorAbs;
  const roundedAbs = frac > 0.5 ? floorAbs + 1 : frac < 0.5 ? floorAbs : floorAbs + 1; // tie -> up
  return (roundedAbs * sign) / factor;
}

export function formatCurrency(amount: number) {
  const rounded = roundHalfUp(amount, 2);
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(rounded);
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
  const rounded = roundHalfUp(numValue, 2);
  return rounded.toLocaleString('pt-BR', {
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
  const rounded = roundHalfUp(numValue, 2);
  return `R$ ${rounded.toLocaleString('pt-BR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })}`;
}

export function formatPercentageValue(value: number | string | undefined): string {
  if (value === undefined || value === null || value === '') return '';
  
  const numValue = typeof value === 'string' ? parseFloat(value) : value;
  
  if (isNaN(numValue)) return '';
  const rounded = roundHalfUp(numValue, 1);
  const formatted = new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
  }).format(rounded);
  return `${formatted}%`;
}

// Formata percentual sem arredondar (truncando), com casas configuráveis
export function formatPercentageValueNoRound(value: number | string | undefined, decimals: number = 2): string {
  if (value === undefined || value === null || value === '') return '';
  const numValue = typeof value === 'string' ? parseFloat(value) : value;
  if (isNaN(numValue)) return '';
  const factor = Math.pow(10, decimals);
  // Truncar em direção a zero para evitar arredondamento
  const scaled = numValue * factor;
  const truncatedScaled = scaled >= 0 ? Math.floor(scaled) : Math.ceil(scaled);
  const truncated = truncatedScaled / factor;
  const formatted = new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(truncated);
  return `${formatted}%`;
}

// Formata percentual a partir de fração (ex.: 0.175 → "17,5%"), com casas configuráveis
export function formatPercentFromFraction(value: number | string | undefined, decimals: number = 2): string {
  if (value === undefined || value === null || value === '') return '';
  const numValue = typeof value === 'string' ? parseFloat(value) : value;
  if (isNaN(numValue)) return '';
  const percent = numValue * 100;
  const rounded = roundHalfUp(percent, decimals);
  const formatted = new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(rounded);
  return `${formatted}%`;
}

export function parsePercentageValue(value: string | undefined): number {
  if (!value || value === '') return 0;
  
  // Remove o símbolo % e espaços
  const cleanValue = value.replace(/[%\s]/g, '').replace(',', '.');
  const parsed = parseFloat(cleanValue);
  
  return isNaN(parsed) ? 0 : parsed;
}

export const statusTheme = {
  draft: '#8c8c8c',
  pending: '#1890ff',
  approved: '#52c41a',
  lost: '#ff4d4f',
  sent: '#faad14',
};
