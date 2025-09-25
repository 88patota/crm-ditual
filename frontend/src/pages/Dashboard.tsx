import { useAuth } from '../contexts/AuthContext';
import { useQuery } from '@tanstack/react-query';
import { authService } from '../services/authService';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card';
import { Users, UserCheck, Shield, Activity } from 'lucide-react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import StripeBadge from '../components/ui/StripeBadge';

export default function Dashboard() {
  const { user } = useAuth();

  // Only fetch users if user is admin
  const { data: users = [] } = useQuery({
    queryKey: ['users'],
    queryFn: authService.getAllUsers,
    enabled: user?.role === 'admin',
  });

  const stats = [
    {
      name: 'Total de Usuários',
      value: users.length,
      icon: Users,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
      visible: user?.role === 'admin',
    },
    {
      name: 'Usuários Ativos',
      value: users.filter(u => u.is_active).length,
      icon: UserCheck,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
      visible: user?.role === 'admin',
    },
    {
      name: 'Administradores',
      value: users.filter(u => u.role === 'admin').length,
      icon: Shield,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
      visible: user?.role === 'admin',
    },
    {
      name: 'Meu Status',
      value: user?.is_active ? 'Ativo' : 'Inativo',
      icon: Activity,
      color: user?.is_active ? 'text-green-600' : 'text-red-600',
      bgColor: user?.is_active ? 'bg-green-100' : 'bg-red-100',
      visible: true,
    },
  ].filter(stat => stat.visible);

  const recentUsers = users
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 5);

  // Mock: vendedores por hora (exemplo)
  const vendedoresPorHora = [
    { hora: '08:00', quantidade: 2 },
    { hora: '09:00', quantidade: 3 },
    { hora: '10:00', quantidade: 4 },
    { hora: '11:00', quantidade: 5 },
    { hora: '12:00', quantidade: 6 },
    { hora: '13:00', quantidade: 7 },
    { hora: '14:00', quantidade: 8 },
    { hora: '15:00', quantidade: 6 },
    { hora: '16:00', quantidade: 5 },
    { hora: '17:00', quantidade: 4 },
  ];

  const chartData = {
    labels: vendedoresPorHora.map((v) => v.hora),
    datasets: [
      {
        label: 'Vendedores por Hora',
        data: vendedoresPorHora.map((v) => v.quantidade),
        borderColor: '#2563eb',
        backgroundColor: 'rgba(37, 99, 235, 0.1)',
        tension: 0.4,
        fill: true,
        pointRadius: 5,
        pointBackgroundColor: '#2563eb',
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
        },
      },
    },
  };

  ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-600">
          Bem-vindo(a), {user?.full_name}!
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <Card key={stat.name} className="shadow-md rounded-xl border border-gray-100 bg-white min-h-[140px] flex flex-col">
              <CardContent className="flex items-center p-6 flex-1">
                <div className={`rounded-lg p-3 ${stat.bgColor} flex-shrink-0`}>
                  <Icon className={`h-6 w-6 ${stat.color}`} />
                </div>
                <div className="ml-4 flex-1 overflow-hidden">
                  <p className="text-sm font-medium text-gray-600 truncate">{stat.name}</p>
                  <p className="text-2xl font-bold text-gray-900 mt-1 truncate" style={{ lineHeight: '1.4', paddingBottom: '1px', minHeight: '32px' }}>{stat.value}</p>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Gráfico de Vendedores por Hora */}
      <div className="bg-white rounded-xl shadow-md p-6 mt-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Vendedores por Hora</h2>
        <Line data={chartData} options={chartOptions} height={80} />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* User Profile Card */}
        <Card className="min-h-[300px]">
          <CardHeader>
            <CardTitle>Meu Perfil</CardTitle>
          </CardHeader>
          <CardContent className="flex-1">
            <div className="space-y-4 h-full">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="p-3 bg-gray-50 rounded-lg overflow-hidden">
                  <dt className="text-sm font-medium text-gray-500 mb-1 truncate">Nome</dt>
                  <dd className="text-sm text-gray-900 font-semibold truncate">{user?.full_name}</dd>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg overflow-hidden">
                  <dt className="text-sm font-medium text-gray-500 mb-1 truncate">Email</dt>
                  <dd className="text-sm text-gray-900 font-semibold truncate">{user?.email}</dd>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg overflow-hidden">
                  <dt className="text-sm font-medium text-gray-500 mb-1 truncate">Username</dt>
                  <dd className="text-sm text-gray-900 font-semibold truncate">{user?.username}</dd>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg overflow-hidden">
                  <dt className="text-sm font-medium text-gray-500 mb-1 truncate">Função</dt>
                  <dd className="text-sm text-gray-900">
                    <StripeBadge variant={user?.role === 'admin' ? 'primary' : 'success'} size="sm">
                      {user?.role === 'admin' ? 'Administrador' : 'Vendas'}
                    </StripeBadge>
                  </dd>
                </div>
              </div>
              <div className="pt-4">
                <div className="p-3 bg-gray-50 rounded-lg">
                  <dt className="text-sm font-medium text-gray-500 mb-1">Status</dt>
                  <dd className="text-sm text-gray-900">
                    <StripeBadge variant={user?.is_active ? 'success' : 'error'} size="sm">
                      {user?.is_active ? 'Ativo' : 'Inativo'}
                    </StripeBadge>
                  </dd>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Recent Users (Admin only) */}
        {user?.role === 'admin' && (
          <Card className="min-h-[300px]">
            <CardHeader>
              <CardTitle>Usuários Recentes</CardTitle>
            </CardHeader>
            <CardContent className="flex-1">
              <div className="space-y-3 h-full">
                {recentUsers.map((recentUser) => (
                  <div key={recentUser.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center">
                      <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gray-100 flex-shrink-0">
                        <span className="text-sm font-medium text-gray-700">
                          {recentUser.full_name.charAt(0).toUpperCase()}
                        </span>
                      </div>
                      <div className="ml-3 flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-900 truncate">
                          {recentUser.full_name}
                        </p>
                        <p className="text-sm text-gray-500 truncate">{recentUser.email}</p>
                      </div>
                    </div>
                    <StripeBadge variant={recentUser.role === 'admin' ? 'primary' : 'success'} size="sm">
                      {recentUser.role === 'admin' ? 'Admin' : 'Vendas'}
                    </StripeBadge>
                  </div>
                ))}
                {recentUsers.length === 0 && (
                  <div className="flex items-center justify-center h-32">
                    <p className="text-sm text-gray-500">Nenhum usuário cadastrado ainda.</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}