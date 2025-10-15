import React, { createContext, useContext, useEffect, useState } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { authService } from '../services/authService';
import type { AuthContextType, User, LoginRequest, RegisterRequest } from '../types/auth';
import toast from 'react-hot-toast';

const AuthContext = createContext<AuthContextType | null>(null);

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

interface AuthProviderProps {
  children: React.ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const queryClient = useQueryClient();
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('auth_token'));
  const [isLoading, setIsLoading] = useState(true);

  const isAuthenticated = !!user && !!token;

  const clearUserData = () => {
    // Limpar dados específicos do usuário (cache de queries sensíveis)
    queryClient.removeQueries({ queryKey: ['budgets'] });
    queryClient.removeQueries({ queryKey: ['budget'] });
    queryClient.removeQueries({ queryKey: ['users'] });
    queryClient.removeQueries({ queryKey: ['profile'] });
    queryClient.removeQueries({ queryKey: ['dashboard'] });
  };

  // Load user data on mount if token exists
  useEffect(() => {
    async function loadUser() {
      if (token) {
        try {
          const userData = await authService.getCurrentUser();
          setUser(userData);
        } catch {
          // Token is invalid, remove it
          clearUserData(); // Limpar dados do usuário quando token é inválido
          localStorage.removeItem('auth_token');
          setToken(null);
        }
      }
      setIsLoading(false);
    }

    loadUser();
  }, [token, clearUserData]);

  const login = async (credentials: LoginRequest) => {
    setIsLoading(true);
    try {
      // Limpar dados do usuário anterior antes do login
      clearUserData();
      
      const response = await authService.login(credentials);
      const { access_token } = response;
      
      localStorage.setItem('auth_token', access_token);
      setToken(access_token);
      
      // Get user data
      const userData = await authService.getCurrentUser();
      setUser(userData);
      
      toast.success(`Bem-vindo(a), ${userData.full_name}!`);
      setIsLoading(false);
    } catch (error) {
      setIsLoading(false);
      throw error;
    }
  };

  const register = async (data: RegisterRequest) => {
    setIsLoading(true);
    try {
      await authService.register(data);
      toast.success('Conta criada com sucesso! Faça login para continuar.');
      setIsLoading(false);
    } catch (error) {
      setIsLoading(false);
      throw error;
    }
  };

  const logout = () => {
    // Limpar dados específicos do usuário durante logout
    clearUserData();
    
    localStorage.removeItem('auth_token');
    setToken(null);
    setUser(null);
    toast.success('Logout realizado com sucesso!');
  };

  const value: AuthContextType = {
    user,
    token,
    login,
    register,
    logout,
    isLoading,
    isAuthenticated,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export default AuthContext;