import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { AlertCircle, Eye, EyeOff, CheckCircle } from 'lucide-react';

interface LoginForm {
  username: string;
  password: string;
}

const ModernLogin: React.FC = () => {
  const { login } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const {
    register,
    handleSubmit,
    setError,
    formState: { errors },
  } = useForm<LoginForm>();

  const onSubmit = async (data: LoginForm) => {
    try {
      setIsLoading(true);
      await login({ username: data.username, password: data.password });
    } catch (error: any) {
      const errorDetail = error.response?.data?.detail;
      let errorMessage = 'Erro ao fazer login';
      
      if (typeof errorDetail === 'string') {
        errorMessage = errorDetail;
      } else if (Array.isArray(errorDetail)) {
        errorMessage = errorDetail.map((err: any) => err.msg).join(', ');
      }
      
      setError('root', { 
        message: errorMessage
      });
    } finally {
      setIsLoading(false);
    }
  };

  const demoCredentials = [
    {
      role: 'Administrador',
      description: 'Acesso completo ao sistema - Gerenciar usuários, orçamentos e configurações',
      username: 'admin',
      password: 'admin123',
      variant: 'default' as const,
    },
    {
      role: 'Vendedor',
      description: 'Perfil de vendas - Criar e gerenciar orçamentos, exportar propostas PDF',
      username: 'vendedor',
      password: 'vendedor123',
      variant: 'secondary' as const,
    },
  ];

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-4">
      <div className="w-full max-w-md space-y-6">
        {/* Header */}
        <div className="text-center space-y-4">
          <div className="flex justify-center">
            <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-600 to-purple-600 shadow-lg">
              <span className="text-2xl font-bold text-white">C</span>
            </div>
          </div>
          <div className="space-y-2">
            <h1 className="text-3xl font-bold tracking-tight">Bem-vindo de volta</h1>
            <p className="text-muted-foreground">
              Entre com suas credenciais para acessar o sistema
            </p>
          </div>
        </div>

        {/* Login Form */}
        <Card className="shadow-xl border-0">
          <CardHeader className="space-y-1">
            <CardTitle className="text-2xl text-center">Login</CardTitle>
            <CardDescription className="text-center">
              Digite seu usuário e senha para continuar
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {errors.root && (
              <div className="flex items-center gap-2 p-3 text-sm text-destructive bg-destructive/10 border border-destructive/20 rounded-lg">
                <AlertCircle className="h-4 w-4" />
                {errors.root.message}
              </div>
            )}

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <Input
                label="Usuário"
                placeholder="Digite seu usuário"
                error={errors.username?.message}
                {...register('username', {
                  required: 'Usuário é obrigatório',
                })}
              />

              <div className="relative">
                <Input
                  label="Senha"
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Digite sua senha"
                  error={errors.password?.message}
                  {...register('password', {
                    required: 'Senha é obrigatória',
                  })}
                />
                <Button
                  type="button"
                  variant="ghost"
                  size="icon"
                  className="absolute right-2 top-8 h-7 w-7"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? (
                    <EyeOff className="h-4 w-4" />
                  ) : (
                    <Eye className="h-4 w-4" />
                  )}
                </Button>
              </div>

              <Button type="submit" className="w-full" loading={isLoading}>
                Entrar
              </Button>
            </form>

            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-card px-2 text-muted-foreground">ou</span>
              </div>
            </div>

            <Button variant="outline" className="w-full" asChild>
              <Link to="/register">Criar nova conta</Link>
            </Button>
          </CardContent>
        </Card>

        {/* Demo Credentials */}
        <Card className="border-primary/20 bg-primary/5">
          <CardHeader>
            <div className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/10">
                <CheckCircle className="h-4 w-4 text-primary" />
              </div>
              <CardTitle className="text-lg">Credenciais de Demonstração</CardTitle>
            </div>
            <CardDescription>
              Use essas credenciais para testar o sistema
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {demoCredentials.map((credential, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-3 rounded-lg border bg-background"
              >
                <div className="flex flex-col">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-medium">{credential.role}</span>
                    <Badge variant={credential.variant} className="text-xs">
                      {credential.description}
                    </Badge>
                  </div>
                  <div className="flex gap-2 text-xs text-muted-foreground">
                    <code className="bg-muted px-2 py-1 rounded font-mono">
                      {credential.username}
                    </code>
                    <code className="bg-muted px-2 py-1 rounded font-mono">
                      {credential.password}
                    </code>
                  </div>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Status */}
        <div className="text-center space-y-2">
          <div className="flex items-center justify-center gap-2">
            <div className="h-2 w-2 rounded-full bg-success animate-pulse" />
            <span className="text-sm font-medium text-muted-foreground">
              Sistema online e funcionando
            </span>
          </div>
          <p className="text-xs text-muted-foreground">
            Versão 2.0 - Redesign completo
          </p>
        </div>
      </div>
    </div>
  );
};

export default ModernLogin;