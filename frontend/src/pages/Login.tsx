import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { useAuth } from '../hooks/useAuth';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Card } from '../components/ui/Card';
import type { LoginRequest } from '../types/auth';
import { LogIn, UserPlus } from 'lucide-react';

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
    setError,
  } = useForm<LoginRequest>();

  const onSubmit = async (data: LoginRequest) => {
    setIsLoading(true);
    try {
      await login(data);
      navigate('/dashboard');
    } catch (error: unknown) {
      const axiosError = error as { response?: { status?: number } };
      if (axiosError.response?.status === 401) {
        setError('root', { message: 'Credenciais inválidas' });
      } else {
        setError('root', { message: 'Erro ao fazer login. Tente novamente.' });
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <div className="text-center">
          <div className="flex justify-center mb-6">
            <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-600 to-purple-600 shadow-lg">
              <span className="text-2xl font-bold text-white">C</span>
            </div>
          </div>
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Bem-vindo de volta
          </h2>
          <p className="text-muted-foreground mb-2">
            Acesse o sistema com suas credencias
          </p>
          <p className="text-sm text-muted-foreground">
            Ou{' '}
            <Link
              to="/register"
              className="font-semibold text-blue-600 hover:text-blue-700"
            >
              crie uma nova conta
            </Link>
          </p>
        </div>

        {/* Login Form */}
        <Card className="shadow-xl border-0">
          <form className="space-y-6 p-6" onSubmit={handleSubmit(onSubmit)}>
            <Input
              label="Usuário"
              type="text"
              autoComplete="username"
              placeholder="Digite seu username"
              error={errors.username?.message}
              {...register('username', {
                required: 'Username é obrigatório',
                minLength: {
                  value: 3,
                  message: 'Username deve ter pelo menos 3 caracteres',
                },
              })}
            />

            <Input
              label="Senha"
              type="password"
              autoComplete="current-password"
              placeholder="Digite sua senha"
              error={errors.password?.message}
              {...register('password', {
                required: 'Senha é obrigatória',
                minLength: {
                  value: 8,
                  message: 'Senha deve ter pelo menos 8 caracteres',
                },
              })}
            />

            {errors.root && (
              <div className="rounded-md bg-red-50 p-4">
                <div className="text-sm text-red-700">{errors.root.message}</div>
              </div>
            )}

            <div className="flex flex-col space-y-3">
              <Button
                type="submit"
                loading={isLoading}
                className="w-full"
              >
                <LogIn className="mr-2 h-4 w-4" />
                Entrar
              </Button>

              <Link to="/register">
                <Button
                  type="button"
                  variant="outline"
                  className="w-full"
                >
                  <UserPlus className="mr-2 h-4 w-4" />
                  Criar conta
                </Button>
              </Link>
            </div>
          </form>
        </Card>

        {/* Footer */}
        <div className="text-center space-y-3">
          <div className="flex items-center justify-center gap-2">
            <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse"></div>
            <span className="text-sm font-medium text-muted-foreground">
              Sistema online e funcionando
            </span>
          </div>
          <p className="text-xs text-muted-foreground">
            Sistema CRM - Acesso seguro com autenticação JWT
          </p>
        </div>
      </div>
    </div>
  );
}