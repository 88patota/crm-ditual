import api from '../lib/api';
import type {
  User,
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  UserSelfUpdateRequest,
  PasswordUpdateRequest,
} from '../types/auth';

export const authService = {
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await api.post<LoginResponse>('/users/login', credentials);
    return response.data;
  },

  async register(data: RegisterRequest): Promise<User> {
    const response = await api.post<User>('/users/register', data);
    return response.data;
  },

  async getCurrentUser(): Promise<User> {
    const response = await api.get<User>('/users/me');
    return response.data;
  },

  async updateProfile(data: UserSelfUpdateRequest): Promise<User> {
    const response = await api.put<User>('/users/me', data);
    return response.data;
  },

  async changePassword(data: PasswordUpdateRequest): Promise<{ message: string }> {
    const response = await api.put<{ message: string }>('/users/me/password', data);
    return response.data;
  },

  async getAllUsers(): Promise<User[]> {
    const response = await api.get<User[]>('/users/');
    return response.data;
  },

  async createUser(data: RegisterRequest): Promise<User> {
    const response = await api.post<User>('/users/', data);
    return response.data;
  },

  async getUserById(id: number): Promise<User> {
    const response = await api.get<User>(`/users/${id}`);
    return response.data;
  },

  async updateUser(id: number, data: Partial<User>): Promise<User> {
    const response = await api.put<User>(`/users/${id}`, data);
    return response.data;
  },

  async deleteUser(id: number): Promise<void> {
    await api.delete(`/users/${id}`);
  },
};