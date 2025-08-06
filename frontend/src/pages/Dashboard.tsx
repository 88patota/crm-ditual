import { useAuth } from '../contexts/AuthContext';
import { useQuery } from '@tanstack/react-query';
import { authService } from '../services/authService';
import Card, { CardContent, CardHeader, CardTitle } from '../components/ui/Card';
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
            <Card key={stat.name} className="shadow-md rounded-xl border border-gray-100 bg-white">
              <CardContent className="flex items-center">
                <div className={`rounded-lg p-3 ${stat.bgColor}`}>
                  <Icon className={`h-6 w-6 ${stat.color}`} />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
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
        <Card>
          <CardHeader>
            <CardTitle>Meu Perfil</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div>
                <dt className="text-sm font-medium text-gray-500">Nome</dt>
                <dd className="text-sm text-gray-900">{user?.full_name}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Email</dt>
                <dd className="text-sm text-gray-900">{user?.email}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Username</dt>
                <dd className="text-sm text-gray-900">{user?.username}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Função</dt>
                <dd className="text-sm text-gray-900">
                  <StripeBadge variant={user?.role === 'admin' ? 'primary' : 'success'} size="sm">
                    {user?.role === 'admin' ? 'Administrador' : 'Vendas'}
                  </StripeBadge>
                </dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Status</dt>
                <dd className="text-sm text-gray-900">
                  <StripeBadge variant={user?.is_active ? 'success' : 'error'} size="sm">
                    {user?.is_active ? 'Ativo' : 'Inativo'}
                  </StripeBadge>
                </dd>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Recent Users (Admin only) */}
        {user?.role === 'admin' && (
          <Card>
            <CardHeader>
              <CardTitle>Usuários Recentes</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {recentUsers.map((recentUser) => (
                  <div key={recentUser.id} className="flex items-center justify-between">
                    <div className="flex items-center">
                      <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gray-100">
                        <span className="text-sm font-medium text-gray-700">
                          {recentUser.full_name.charAt(0).toUpperCase()}
                        </span>
                      </div>
                      <div className="ml-3">
                        <p className="text-sm font-medium text-gray-900">
                          {recentUser.full_name}
                        </p>
                        <p className="text-sm text-gray-500">{recentUser.email}</p>
                      </div>
                    </div>
                    <StripeBadge variant={recentUser.role === 'admin' ? 'primary' : 'success'} size="sm">
                      {recentUser.role === 'admin' ? 'Admin' : 'Vendas'}
                    </StripeBadge>
                  </div>
                ))}
                {recentUsers.length === 0 && (
                  <p className="text-sm text-gray-500">Nenhum usuário cadastrado ainda.</p>
                )}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}