import React, { useEffect, useState } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { authService } from '../services/authService';
import type { AuthContextType, User, LoginRequest, RegisterRequest } from '../types/auth';
import toast from 'react-hot-toast';
import { AuthContext } from './AuthContextDefinition';

interface AuthProviderProps {
  children: React.ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const queryClient = useQueryClient();
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('auth_token'));
  const [isLoading, setIsLoading] = useState(true);
  const [shouldFetchUser, setShouldFetchUser] = useState(false);

  const isAuthenticated = !!user && !!token;

  const clearUserData = () => {
    // Limpar dados específicos do usuário (cache de queries sensíveis)
    queryClient.removeQueries({ queryKey: ['budgets'] });
    queryClient.removeQueries({ queryKey: ['budget'] });
    queryClient.removeQueries({ queryKey: ['users'] });
    queryClient.removeQueries({ queryKey: ['profile'] });
    queryClient.removeQueries({ queryKey: ['dashboard'] });
  };

  // Load user data on mount if token exists or when explicitly requested
  useEffect(() => {
    async function loadUser() {
      if (token && (shouldFetchUser || !user)) {
        try {
          const userData = await authService.getCurrentUser();
          setUser(userData);
          setShouldFetchUser(false); // Reset flag after successful fetch
          
          // Show welcome message only when explicitly requested (after login)
          if (shouldFetchUser) {
            toast.success(`Bem-vindo(a), ${userData.full_name}!`);
          }
        } catch {
          // Token is invalid, remove it
          clearUserData();
          localStorage.removeItem('auth_token');
          setToken(null);
          setUser(null);
          setShouldFetchUser(false);
        }
      }
      setIsLoading(false);
    }

    loadUser();
  }, [token, shouldFetchUser]); // Removed clearUserData from dependencies

  const login = async (credentials: LoginRequest) => {
    setIsLoading(true);
    try {
      // Limpar dados do usuário anterior antes do login
      clearUserData();
      
      const response = await authService.login(credentials);
      const { access_token } = response;
      
      localStorage.setItem('auth_token', access_token);
      setToken(access_token);
      
      // Set flag to fetch user data instead of calling directly
      setShouldFetchUser(true);
      
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

export default AuthProvider;