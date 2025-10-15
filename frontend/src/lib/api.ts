import axios, { AxiosError, AxiosHeaders } from 'axios';
import type { InternalAxiosRequestConfig } from 'axios';
import type { QueryClient } from '@tanstack/react-query';
import type { ApiError } from '../types/auth';

// Variável para armazenar a referência do queryClient
// Será definida pelo App.tsx
let queryClientRef: QueryClient | null = null;

export const setQueryClient = (queryClient: QueryClient) => {
  queryClientRef = queryClient;
};

// Use relative URLs para aproveitar o proxy Nginx em produção
// CORREÇÃO: Sempre usar a variável de ambiente quando disponível
const ENV_BASE = import.meta.env.VITE_API_BASE_URL as string | undefined;
const DEFAULT_BASE = '/api/v1';

// Se temos uma variável de ambiente definida, usar ela
// Caso contrário, usar o padrão relativo
const resolvedBaseURL = ENV_BASE || DEFAULT_BASE;

export const api = axios.create({
  // Use '/api/v1' como padrão para alinhar com o gateway Nginx em produção
  // e evitar chamadas para '/api' sem versão.
  baseURL: resolvedBaseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      const authValue = `Bearer ${token}`;
      // Garantir que headers seja uma instância de AxiosHeaders para compatibilidade com os tipos
      if (!config.headers || typeof (config.headers as AxiosHeaders).set !== 'function') {
        config.headers = new AxiosHeaders(config.headers || {});
      }
      (config.headers as AxiosHeaders).set('Authorization', authValue);
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ApiError>) => {
    // Redirect to login on 401 errors
    if (error.response?.status === 401) {
      // Limpar dados específicos do usuário se disponível
      if (queryClientRef) {
        queryClientRef.removeQueries({ queryKey: ['budgets'] });
        queryClientRef.removeQueries({ queryKey: ['budget'] });
        queryClientRef.removeQueries({ queryKey: ['users'] });
        queryClientRef.removeQueries({ queryKey: ['profile'] });
        queryClientRef.removeQueries({ queryKey: ['dashboard'] });
      }
      
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    
    return Promise.reject(error);
  }
);

export function getErrorMessage(error: AxiosError<ApiError>): string {
  if (error.response?.data?.detail) {
    const detail = error.response.data.detail;
    
    if (typeof detail === 'string') {
      return detail;
    }
    
    if (Array.isArray(detail)) {
      return detail.map(err => err.msg).join(', ');
    }
  }
  
  return error.message || 'Algo deu errado. Tente novamente.';
}

export default api;