import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useQuery } from '@tanstack/react-query';
import { authService } from '../services/authService';
import type { User } from '../types/auth';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import {
  Users,
  UserPlus,
  TrendingUp,
  Activity,
  DollarSign,
  Calendar,
  Clock,
  Shield,
  MoreHorizontal,
  ArrowUpRight,
  ArrowDownRight,
} from 'lucide-react';
import { formatDateTime } from '../lib/utils';

const ModernDashboard: React.FC = () => {
  const { user } = useAuth();

  const { data: users = [], isLoading } = useQuery<User[]>({
    queryKey: ['users'],
    queryFn: authService.getAllUsers,
  });

  const stats = [
    {
      title: 'Total de Usuários',
      value: users.length.toString(),
      change: '+12%',
      changeType: 'positive' as const,
      icon: Users,
      description: 'vs último mês',
    },
    {
      title: 'Usuários Ativos',
      value: users.filter(u => u.is_active).length.toString(),
      change: '+8%',
      changeType: 'positive' as const,
      icon: Activity,
      description: 'vs último mês',
    },
    {
      title: 'Novos Usuários',
      value: users.filter(u => {
        const created = new Date(u.created_at);
        const lastMonth = new Date();
        lastMonth.setMonth(lastMonth.getMonth() - 1);
        return created > lastMonth;
      }).length.toString(),
      change: '+23%',
      changeType: 'positive' as const,
      icon: UserPlus,
      description: 'este mês',
    },
    {
      title: 'Taxa de Crescimento',
      value: '18.20%',
      change: '-2%',
      changeType: 'negative' as const,
      icon: TrendingUp,
      description: 'vs último trimestre',
    },
  ];

  const recentUsers = users
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 5);

  const getRoleVariant = (role: string) => {
    switch (role) {
      case 'admin':
        return 'default';
      case 'manager':
        return 'secondary';
      default:
        return 'outline';
    }
  };

  return (
    <div className="space-y-6">
      {/* Welcome Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div className="space-y-1">
          <h1 className="text-3xl font-bold tracking-tight">
            Olá, {user?.full_name}! 👋
          </h1>
          <p className="text-muted-foreground">
            Aqui está um resumo do que está acontecendo no seu sistema hoje.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm">
            <Calendar className="mr-2 h-4 w-4" />
            Últimos 30 dias
          </Button>
          <Button size="sm">
            <ArrowUpRight className="mr-2 h-4 w-4" />
            Relatório Completo
          </Button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <Card key={stat.title} className="hover:shadow-md transition-shadow min-h-[130px] flex flex-col overflow-hidden">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 flex-shrink-0">
                <CardTitle className="text-xs font-medium text-muted-foreground truncate">
                  {stat.title}
                </CardTitle>
                <Icon className="h-4 w-4 text-muted-foreground flex-shrink-0" />
              </CardHeader>
              <CardContent className="flex-1 flex flex-col justify-center pt-0 overflow-hidden">
                <div className="text-xl font-bold mb-1 truncate overflow-hidden text-ellipsis whitespace-nowrap" style={{ lineHeight: '1.4', paddingBottom: '1px', minHeight: '24px' }}>{stat.value}</div>
                <div className="flex items-center text-xs text-muted-foreground overflow-hidden">
                  {stat.changeType === 'positive' ? (
                    <ArrowUpRight className="mr-1 h-3 w-3 text-green-600 flex-shrink-0" />
                  ) : (
                    <ArrowDownRight className="mr-1 h-3 w-3 text-red-600 flex-shrink-0" />
                  )}
                  <span 
                    className={stat.changeType === 'positive' ? 'text-green-600' : 'text-red-600'}
                  >
                    {stat.change}
                  </span>
                  <span className="ml-1 truncate overflow-hidden text-ellipsis">{stat.description}</span>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Account Overview */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Visão Geral da Conta</CardTitle>
                  <CardDescription>
                    Informações sobre seu perfil e permissões
                  </CardDescription>
                </div>
                <Button variant="ghost" size="icon">
                  <MoreHorizontal className="h-4 w-4" />
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-start gap-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary text-primary-foreground font-semibold">
                  {user?.full_name?.charAt(0).toUpperCase()}
                </div>
                <div className="flex-1 space-y-1">
                  <div className="flex items-center gap-2">
                    <h3 className="font-semibold">{user?.full_name}</h3>
                    <Badge variant={getRoleVariant(user?.role || '')}>
                      {user?.role}
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground">{user?.email}</p>
                  <div className="flex items-center gap-4 text-xs text-muted-foreground">
                    <span>ID: {user?.id}</span>
                    <span>•</span>
                    <span>Membro desde {formatDateTime(new Date())}</span>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="rounded-lg border p-3 min-h-[70px] flex flex-col justify-center overflow-hidden">
                  <div className="flex items-center gap-2 mb-1">
                    <Shield className="h-3 w-3 text-muted-foreground flex-shrink-0" />
                    <span className="text-xs font-medium">Função</span>
                  </div>
                  <p className="text-xs font-semibold capitalize truncate">{user?.role}</p>
                </div>
                <div className="rounded-lg border p-3 min-h-[70px] flex flex-col justify-center overflow-hidden">
                  <div className="flex items-center gap-2 mb-1">
                    <Clock className="h-3 w-3 text-muted-foreground flex-shrink-0" />
                    <span className="text-xs font-medium">Última Atividade</span>
                  </div>
                  <p className="text-xs font-semibold truncate">Agora mesmo</p>
                </div>
                <div className="rounded-lg border p-3 min-h-[70px] flex flex-col justify-center overflow-hidden">
                  <div className="flex items-center gap-2 mb-1">
                    <Activity className="h-3 w-3 text-muted-foreground flex-shrink-0" />
                    <span className="text-xs font-medium">Status</span>
                  </div>
                  <Badge variant="default" className="text-xs">Online</Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Recent Activity */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Atividade Recente</CardTitle>
                <Button variant="ghost" size="sm">
                  Ver tudo
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              {isLoading ? (
                <div className="space-y-2">
                  {[...Array(3)].map((_, i) => (
                    <div key={i} className="flex items-center gap-3">
                      <div className="h-8 w-8 rounded-full bg-muted animate-pulse" />
                      <div className="flex-1 space-y-1">
                        <div className="h-4 w-full bg-muted rounded animate-pulse" />
                        <div className="h-3 w-1/2 bg-muted rounded animate-pulse" />
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="space-y-4">
                  {recentUsers.map((recentUser) => (
                    <div key={recentUser.id} className="flex items-center gap-3">
                      <div className="flex h-8 w-8 items-center justify-center rounded-full bg-muted text-sm font-medium">
                        {recentUser.full_name.charAt(0).toUpperCase()}
                      </div>
                      <div className="flex-1 space-y-1">
                        <p className="text-sm font-medium leading-none">
                          {recentUser.full_name}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          Novo usuário criado
                        </p>
                      </div>
                      <div className="text-xs text-muted-foreground">
                        {formatDateTime(recentUser.created_at)}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card>
            <CardHeader>
              <CardTitle>Ações Rápidas</CardTitle>
              <CardDescription>
                Acesso rápido às funções mais usadas
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-2">
              <Button variant="outline" className="w-full justify-start min-h-[48px]">
                <UserPlus className="mr-2 h-4 w-4" />
                Adicionar Usuário
              </Button>
              <Button variant="outline" className="w-full justify-start min-h-[48px]">
                <TrendingUp className="mr-2 h-4 w-4" />
                Ver Relatórios
              </Button>
              <Button variant="outline" className="w-full justify-start min-h-[48px]">
                <DollarSign className="mr-2 h-4 w-4" />
                Gerenciar Vendas
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default ModernDashboard;