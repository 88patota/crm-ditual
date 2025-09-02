import React, { useState } from 'react';
import { 
  Row,
  Col, 
  Typography, 
  Space, 
  Button,
  Select,
  DatePicker,
  Spin,
  Card
} from 'antd';
import { 
  UserOutlined, 
  FileTextOutlined,
  DollarOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  CloseCircleOutlined,
  ExclamationCircleOutlined,
  WarningOutlined,
  CalendarOutlined,
  ReloadOutlined
} from '@ant-design/icons';
import { useAuth } from '../contexts/AuthContext';
import { useQuery } from '@tanstack/react-query';
import { budgetService, type DashboardStats } from '../services/budgetService';
import { StatsCard, StatusCard, ProgressCard, InfoCard } from '../components/ui/DashboardCard';
import '../styles/DashboardCard.css';
import dayjs from 'dayjs';
import 'dayjs/locale/pt-br';

dayjs.locale('pt-br');

const { Title, Text } = Typography;
const { RangePicker } = DatePicker;
const { Option } = Select;

const AdminDashboardRefactored: React.FC = () => {
  const { user } = useAuth();
  const [filterDays, setFilterDays] = useState<number>(30);
  const [customDateRange, setCustomDateRange] = useState<[string, string] | null>(null);
  
  const { 
    data: dashboardStats, 
    isLoading, 
    refetch,
    isRefetching 
  } = useQuery<DashboardStats>({
    queryKey: ['dashboard-stats', filterDays, customDateRange],
    queryFn: () => {
      if (customDateRange) {
        return budgetService.getDashboardStats(undefined, customDateRange[0], customDateRange[1]);
      }
      return budgetService.getDashboardStats(filterDays);
    },
    enabled: user?.role === 'admin',
    refetchInterval: 5 * 60 * 1000, // Refetch a cada 5 minutos
  });

  const handlePeriodChange = (value: string) => {
    if (value === 'custom') {
      setCustomDateRange(null);
      setFilterDays(30);
    } else {
      const days = parseInt(value);
      setFilterDays(days);
      setCustomDateRange(null);
    }
  };

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const handleCustomDateChange = (dates: any) => {
    if (dates && dates[0] && dates[1]) {
      setCustomDateRange([
        dates[0].format('YYYY-MM-DD'),
        dates[1].format('YYYY-MM-DD')
      ]);
    } else {
      setCustomDateRange(null);
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  const getStatusConfig = (status: string) => {
    switch (status) {
      case 'draft':
        return { title: 'Rascunhos', icon: <FileTextOutlined />, color: '#8c8c8c' };
      case 'pending':
        return { title: 'Pendentes', icon: <ClockCircleOutlined />, color: '#faad14' };
      case 'approved':
        return { title: 'Aprovados', icon: <CheckCircleOutlined />, color: '#52c41a' };
      case 'rejected':
        return { title: 'Rejeitados', icon: <CloseCircleOutlined />, color: '#ff4d4f' };
      case 'expired':
        return { title: 'Expirados', icon: <WarningOutlined />, color: '#fa8c16' };
      default:
        return { title: status, icon: <ExclamationCircleOutlined />, color: '#8c8c8c' };
    }
  };

  const getPeriodText = () => {
    if (customDateRange) {
      return `${dayjs(customDateRange[0]).format('DD/MM/YYYY')} - ${dayjs(customDateRange[1]).format('DD/MM/YYYY')}`;
    }
    
    switch (filterDays) {
      case 1:
        return 'Hoje';
      case 3:
        return 'Últimos 3 dias';
      case 7:
        return 'Últimos 7 dias';
      case 15:
        return 'Últimos 15 dias';
      case 30:
        return 'Últimos 30 dias';
      default:
        return `Últimos ${filterDays} dias`;
    }
  };

  if (user?.role !== 'admin') {
    return (
      <div style={{ padding: '24px', textAlign: 'center' }}>
        <Title level={3}>Acesso Negado</Title>
        <Text>Apenas administradores podem acessar o dashboard administrativo.</Text>
      </div>
    );
  }

  // Dados para os cards principais usando os novos componentes
  const mainStatsData = [
    {
      title: 'Total de Orçamentos',
      value: dashboardStats?.total_budgets || 0,
      prefix: <FileTextOutlined />,
      color: '#1890ff',
      trend: { value: 12, isPositive: true },
      description: 'neste período'
    },
    {
      title: 'Valor Total',
      value: formatCurrency(dashboardStats?.total_value || 0),
      prefix: <DollarOutlined />,
      color: '#52c41a',
      trend: { value: 8, isPositive: true },
      description: 'em orçamentos'
    },
    {
      title: 'Aprovados',
      value: dashboardStats?.approved_budgets || 0,
      prefix: <CheckCircleOutlined />,
      color: '#52c41a',
      trend: { value: 15, isPositive: true },
      description: 'aprovações'
    },
    {
      title: 'Taxa de Conversão',
      value: (dashboardStats?.conversion_rate || 0).toFixed(2),
      suffix: '%',
      prefix: <UserOutlined />,
      color: '#fa8c16',
      trend: { value: 3, isPositive: false },
      description: 'de aprovação'
    }
  ];

  // Dados para progress cards
  const progressData = [
    {
      title: 'Meta de Orçamentos',
      progress: ((dashboardStats?.total_budgets || 0) / 100) * 100, // Assumindo meta de 100
      status: 'active' as const,
      description: `${dashboardStats?.total_budgets || 0} de 100 orçamentos`
    },
    {
      title: 'Taxa de Aprovação',
      progress: dashboardStats?.conversion_rate || 0,
      status: (dashboardStats?.conversion_rate || 0) > 70 ? 'success' as const : 'active' as const,
      description: 'Baseado nos orçamentos enviados'
    },
    {
      title: 'Performance do Sistema',
      progress: 98.5,
      status: 'success' as const,
      description: '98.5% de uptime este mês'
    }
  ];

  // Dados para info card do usuário
  const userInfo = {
    title: 'Informações do Admin',
    items: [
      {
        label: 'Nome',
        value: user?.full_name || 'Administrador',
        color: '#1890ff'
      },
      {
        label: 'Email',
        value: user?.email || 'admin@exemplo.com',
        color: '#8c8c8c'
      },
      {
        label: 'Role',
        value: 'Administrador',
        color: '#722ed1'
      },
      {
        label: 'Status',
        value: 'Online',
        color: '#52c41a'
      }
    ]
  };

  return (
    <div style={{ padding: '24px' }}>
      {/* Header */}
      <div style={{ marginBottom: '32px' }}>
        <Row justify="space-between" align="middle">
          <Col>
            <Space direction="vertical" size={4}>
              <Title level={2} style={{ margin: 0 }}>
                Dashboard Administrativo
              </Title>
              <Text style={{ fontSize: '16px', color: '#8c8c8c' }}>
                Período: {getPeriodText()}
              </Text>
            </Space>
          </Col>
          <Col>
            <Space>
              <Select
                value={customDateRange ? 'custom' : filterDays.toString()}
                onChange={handlePeriodChange}
                style={{ width: 150 }}
              >
                <Option value="1">Hoje</Option>
                <Option value="3">3 dias</Option>
                <Option value="7">7 dias</Option>
                <Option value="15">15 dias</Option>
                <Option value="30">30 dias</Option>
                <Option value="custom">Personalizado</Option>
              </Select>
              
              {filterDays > 0 && !customDateRange && (
                <RangePicker
                  onChange={handleCustomDateChange}
                  format="DD/MM/YYYY"
                  placeholder={['Data inicial', 'Data final']}
                />
              )}
              
              <Button 
                icon={<CalendarOutlined />}
                onClick={() => setCustomDateRange(null)}
                disabled={!customDateRange}
              >
                Limpar
              </Button>
              
              <Button 
                type="primary"
                icon={<ReloadOutlined spin={isRefetching} />}
                onClick={() => refetch()}
                loading={isRefetching}
              >
                Atualizar
              </Button>
            </Space>
          </Col>
        </Row>
      </div>

      {isLoading ? (
        <div style={{ textAlign: 'center', padding: '100px' }}>
          <Spin size="large" />
          <div style={{ marginTop: '16px' }}>
            <Text>Carregando estatísticas...</Text>
          </div>
        </div>
      ) : (
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          {/* Cards principais com novo componente */}
          <Row gutter={[24, 24]}>
            {mainStatsData.map((stat, index) => (
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

          {/* Cards de status por orçamento */}
          <Card title="Orçamentos por Status">
            <Row gutter={[16, 16]}>
              {dashboardStats?.budgets_by_status && Object.entries(dashboardStats.budgets_by_status).map(([status, count]) => {
                const config = getStatusConfig(status);
                return (
                  <Col xs={24} sm={12} md={8} lg={4.8} key={status}>
                    <StatusCard
                      title={config.title}
                      value={count}
                      icon={config.icon}
                      color={config.color}
                    />
                  </Col>
                );
              })}
            </Row>
          </Card>

          {/* Cards de progresso */}
          <Card title="Performance e Metas">
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
          </Card>

          {/* Informações do usuário */}
          <Row gutter={[24, 24]}>
            <Col xs={24} lg={12}>
              <InfoCard
                title={userInfo.title}
                items={userInfo.items}
              />
            </Col>
          </Row>
        </Space>
      )}
    </div>
  );
};

export default AdminDashboardRefactored;