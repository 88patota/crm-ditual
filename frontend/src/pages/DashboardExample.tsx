import React from 'react';
import { Row, Col, Typography, Space } from 'antd';
import {
  UserOutlined,
  FileTextOutlined,
  DollarOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  WarningOutlined
} from '@ant-design/icons';
import { useAuth } from '../contexts/AuthContext';
import { useQuery } from '@tanstack/react-query';
import { budgetService } from '../services/budgetService';
import { 
  StatsCard, 
  StatusCard, 
  ProgressCard, 
  InfoCard 
} from '../components/ui/DashboardCard';
import '../styles/DashboardCard.css';

const { Title, Text } = Typography;

const DashboardExample: React.FC = () => {
  const { user } = useAuth();
  
  const { data: dashboardStats, isLoading } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: () => budgetService.getDashboardStats(30),
    enabled: !!user
  });

  // Dados de exemplo para demonstração
  const statsData = [
    {
      title: 'Total de Orçamentos',
      value: dashboardStats?.total_budgets || 0,
      prefix: <FileTextOutlined />,
      color: '#1890ff',
      trend: { value: 12, isPositive: true },
      description: 'vs mês anterior'
    },
    {
      title: 'Valor Total',
      value: `R$ ${(dashboardStats?.total_value || 0).toLocaleString('pt-BR')}`,
      prefix: <DollarOutlined />,
      color: '#52c41a',
      trend: { value: 8, isPositive: true },
      description: 'em orçamentos'
    },
    {
      title: 'Taxa de Aprovação',
      value: (dashboardStats?.conversion_rate || 0).toFixed(2),
      suffix: '%',
      prefix: <CheckCircleOutlined />,
      color: '#fa8c16',
      trend: { value: 3, isPositive: false },
      description: 'de conversão'
    },
    {
      title: 'Usuários Ativos',
      value: 24,
      prefix: <UserOutlined />,
      color: '#722ed1',
      trend: { value: 15, isPositive: true },
      description: 'neste mês'
    }
  ];

  const statusData = [
    {
      title: 'Pendentes',
      value: dashboardStats?.budgets_by_status?.pending || 0,
      icon: <ClockCircleOutlined />,
      color: '#faad14'
    },
    {
      title: 'Aprovados',
      value: dashboardStats?.budgets_by_status?.approved || 0,
      icon: <CheckCircleOutlined />,
      color: '#52c41a'
    },
    {
      title: 'Rascunhos',
      value: dashboardStats?.budgets_by_status?.draft || 0,
      icon: <FileTextOutlined />,
      color: '#8c8c8c'
    },
    {
      title: 'Expirados',
      value: dashboardStats?.budgets_by_status?.expired || 0,
      icon: <WarningOutlined />,
      color: '#ff4d4f'
    }
  ];

  const progressData = [
    {
      title: 'Meta Mensal de Vendas',
      progress: 75.5,
      status: 'active' as const,
      description: 'R$ 75.000 de R$ 100.000'
    },
    {
      title: 'Satisfação dos Clientes',
      progress: 92.3,
      status: 'success' as const,
      description: 'Baseado em 45 avaliações'
    },
    {
      title: 'Uptime do Sistema',
      progress: 99.9,
      status: 'success' as const,
      description: '99.9% este mês'
    }
  ];

  const userInfo = {
    title: 'Informações do Perfil',
    items: [
      {
        label: 'Função',
        value: user?.role === 'admin' ? 'Administrador' : user?.role === 'vendas' ? 'Vendas' : 'Usuário',
        color: '#1890ff'
      },
      {
        label: 'Status',
        value: 'Online',
        color: '#52c41a'
      },
      {
        label: 'Última Atividade',
        value: 'Agora',
        color: '#8c8c8c'
      },
      {
        label: 'ID do Usuário',
        value: `#${user?.id || 'N/A'}`,
        color: '#8c8c8c'
      }
    ]
  };

  if (isLoading) {
    return (
      <div style={{ padding: '24px', textAlign: 'center' }}>
        <Text>Carregando dashboard...</Text>
      </div>
    );
  }

  return (
    <div style={{ padding: '24px' }}>
      {/* Header */}
      <div style={{ marginBottom: '32px' }}>
        <Title level={2} style={{ margin: 0 }}>
          Dashboard - Componentes Padronizados
        </Title>
        <Text type="secondary" style={{ fontSize: '16px' }}>
          Demonstração dos componentes de card seguindo o padrão do projeto
        </Text>
      </div>

      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        {/* Cards de Estatísticas */}
        <div>
          <Title level={4}>Cards de Estatísticas</Title>
          <Row gutter={[16, 16]}>
            {statsData.map((stat, index) => (
              <Col xs={24} sm={12} lg={6} key={index}>
                <StatsCard
                  title={stat.title}
                  value={stat.value}
                  prefix={stat.prefix}
                  suffix={stat.suffix}
                  color={stat.color}
                  trend={stat.trend}
                  description={stat.description}
                />
              </Col>
            ))}
          </Row>
        </div>

        {/* Cards de Status */}
        <div>
          <Title level={4}>Cards de Status</Title>
          <Row gutter={[16, 16]}>
            {statusData.map((status, index) => (
              <Col xs={24} sm={12} lg={6} key={index}>
                <StatusCard
                  title={status.title}
                  value={status.value}
                  icon={status.icon}
                  color={status.color}
                />
              </Col>
            ))}
          </Row>
        </div>

        {/* Cards de Progresso */}
        <div>
          <Title level={4}>Cards de Progresso</Title>
          <Row gutter={[16, 16]}>
            {progressData.map((progress, index) => (
              <Col xs={24} md={8} key={index}>
                <ProgressCard
                  title={progress.title}
                  progress={progress.progress}
                  status={progress.status}
                  description={progress.description}
                />
              </Col>
            ))}
          </Row>
        </div>

        {/* Card de Informações */}
        <div>
          <Title level={4}>Card de Informações</Title>
          <Row gutter={[16, 16]}>
            <Col xs={24} md={12}>
              <InfoCard
                title={userInfo.title}
                items={userInfo.items}
              />
            </Col>
          </Row>
        </div>

        {/* Documentação */}
        <div style={{ marginTop: '32px', padding: '24px', backgroundColor: '#f9f9f9', borderRadius: '8px' }}>
          <Title level={4}>Como Usar os Componentes</Title>
          <div style={{ fontSize: '14px', color: '#666' }}>
            <p><strong>StatsCard:</strong> Para métricas principais com valores numéricos, tendências e ícones</p>
            <p><strong>StatusCard:</strong> Para indicadores de status com ícones e cores diferenciadas</p>
            <p><strong>ProgressCard:</strong> Para mostrar progresso percentual com barras visuais</p>
            <p><strong>InfoCard:</strong> Para exibir informações organizadas em grade</p>
            <p><strong>Padrões seguidos:</strong></p>
            <ul>
              <li>Alturas consistentes: Stats (140px), Status (120px), Progress (180px)</li>
              <li>Espaçamento uniforme e responsivo</li>
              <li>Tratamento de overflow de texto</li>
              <li>Line-height mínimo de 1.4 e padding-bottom para evitar corte</li>
              <li>Valores percentuais com 2 casas decimais</li>
              <li>Efeitos hover consistentes</li>
            </ul>
          </div>
        </div>
      </Space>
    </div>
  );
};

export default DashboardExample;