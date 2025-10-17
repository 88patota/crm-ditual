export interface User {
  id: number;
  email: string;
  username: string;
  full_name: string;
  role: 'admin' | 'vendas';
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  full_name: string;
  password: string;
  role?: 'admin' | 'vendas';
}

export interface UserUpdateRequest {
  email?: string;
  username?: string;
  full_name?: string;
  role?: 'admin' | 'vendas';
  is_active?: boolean;
}

export interface UserSelfUpdateRequest {
  email?: string;
  username?: string;
  full_name?: string;
}

export interface PasswordUpdateRequest {
  current_password: string;
  new_password: string;
}

export interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (credentials: LoginRequest) => Promise<void>;
  register: (data: RegisterRequest) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
  isAuthenticated: boolean;
}

export interface ApiError {
  detail: string | Array<{
    type: string;
    loc: string[];
    msg: string;
    input: unknown;
  }>;
}