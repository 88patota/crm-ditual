import React from 'react';
import '../styles/AntDashboard.css';
import { 
  Card, 
  Row, 
  Col, 
  Typography, 
  Space, 
  Button,
  Alert,
  Select,
  DatePicker
} from 'antd';
import { 
  FileTextOutlined,
  DollarCircleOutlined,
  CheckCircleOutlined,
  TrophyOutlined,
  PlusOutlined,
  EyeOutlined,
  CalculatorOutlined,
  ClockCircleOutlined,
  CloseCircleOutlined,
  WarningOutlined,
  ReloadOutlined
} from '@ant-design/icons';
import { useAuth } from '../hooks/useAuth';
import { useQuery } from '@tanstack/react-query';
import { budgetService, type DashboardStats } from '../services/budgetService';
import { Link } from 'react-router-dom';
import { 
  StatusCard
} from '../components/ui/DashboardCard';
import { 
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title as ChartTitle,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Bar, Doughnut, Line } from 'react-chartjs-2';
import { useState } from 'react';
import dayjs from 'dayjs';

const { Title, Text } = Typography;
const { RangePicker } = DatePicker;
const { Option } = Select;

// Registrar componentes do Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  ChartTitle,
  Tooltip,
  Legend,
  Filler
);

const AntDashboard: React.FC = () => {
  const { user } = useAuth();
  const [filterDays, setFilterDays] = useState<number>(30);
  const [customDateRange, setCustomDateRange] = useState<[string, string] | null>(null);

  // Buscar estatísticas dos orçamentos com filtros dinâmicos
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
    enabled: !!user,
    refetchInterval: 5 * 60 * 1000, // Refetch a cada 5 minutos
  });

  const handlePeriodChange = (value: string) => {
    if (value === 'custom') {
      setFilterDays(0); // 0 indica modo personalizado
      // Não limpar customDateRange aqui, deixar o usuário selecionar
    } else {
      const days = parseInt(value);
      setFilterDays(days);
      setCustomDateRange(null); // Limpar range personalizado
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

  const getPeriodText = () => {
    if (customDateRange) {
      return `Período personalizado: ${customDateRange[0]} até ${customDateRange[1]}`;
    }
    return `Últimos ${filterDays} dias`;
  };

  // Formatar valores monetários
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  // Cards de estatísticas removidos conforme solicitado

  // Dados para os StatusCards padronizados
  const statusData = dashboardStats ? [
    {
      title: 'Rascunhos',
      value: dashboardStats.budgets_by_status.draft,
      icon: <FileTextOutlined />,
      color: '#8c8c8c'
    },
    {
      title: 'Pendentes',
      value: dashboardStats.budgets_by_status.pending,
      icon: <ClockCircleOutlined />,
      color: '#1890ff'
    },
    {
      title: 'Aprovados',
      value: dashboardStats.budgets_by_status.approved,
      icon: <CheckCircleOutlined />,
      color: '#52c41a'
    },
    {
      title: 'Rejeitados',
      value: dashboardStats.budgets_by_status.rejected,
      icon: <CloseCircleOutlined />,
      color: '#ff4d4f'
    },
    {
      title: 'Expirados',
      value: dashboardStats.budgets_by_status.expired,
      icon: <WarningOutlined />,
      color: '#faad14'
    }
  ] : [];



  // Dados para gráfico de pizza - Status dos Orçamentos
  const statusChartData = {
    labels: ['Rascunhos', 'Pendentes', 'Aprovados', 'Rejeitados', 'Expirados'],
    datasets: [
      {
        data: [
          dashboardStats?.budgets_by_status.draft || 0,
          dashboardStats?.budgets_by_status.pending || 0,
          dashboardStats?.budgets_by_status.approved || 0,
          dashboardStats?.budgets_by_status.rejected || 0,
          dashboardStats?.budgets_by_status.expired || 0
        ],
        backgroundColor: [
          '#8c8c8c',
          '#1890ff',
          '#52c41a',
          '#ff4d4f',
          '#faad14'
        ],
        borderWidth: 2,
        borderColor: '#ffffff',
        hoverOffset: 4
      }
    ]
  };

  // Dados para gráfico de linha - Evolução de Orçamentos (mock data baseado em dados reais)
  const evolutionChartData = {
    labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
    datasets: [
      {
        label: 'Orçamentos Criados',
        data: [
          Math.round((dashboardStats?.total_budgets || 0) * 0.6),
          Math.round((dashboardStats?.total_budgets || 0) * 0.7),
          Math.round((dashboardStats?.total_budgets || 0) * 0.8),
          Math.round((dashboardStats?.total_budgets || 0) * 0.9),
          Math.round((dashboardStats?.total_budgets || 0) * 0.95),
          dashboardStats?.total_budgets || 0
        ],
        borderColor: '#1890ff',
        backgroundColor: 'rgba(24, 144, 255, 0.1)',
        tension: 0.4,
        fill: true,
        pointRadius: 4,
        pointBackgroundColor: '#1890ff',
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2
      },
      {
        label: 'Orçamentos Aprovados',
        data: [
          Math.round((dashboardStats?.budgets_by_status.approved || 0) * 0.5),
          Math.round((dashboardStats?.budgets_by_status.approved || 0) * 0.6),
          Math.round((dashboardStats?.budgets_by_status.approved || 0) * 0.7),
          Math.round((dashboardStats?.budgets_by_status.approved || 0) * 0.8),
          Math.round((dashboardStats?.budgets_by_status.approved || 0) * 0.9),
          dashboardStats?.budgets_by_status.approved || 0
        ],
        borderColor: '#52c41a',
        backgroundColor: 'rgba(82, 196, 26, 0.1)',
        tension: 0.4,
        fill: true,
        pointRadius: 4,
        pointBackgroundColor: '#52c41a',
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2
      }
    ]
  };

  // Dados para gráfico de barras - Performance Financeira
  const performanceChartData = {
    labels: ['Total Orçado', 'Total Aprovado', 'Comissões', 'Meta Mensal'],
    datasets: [
      {
        label: 'Valores (R$)',
        data: [
          dashboardStats?.total_value || 0,
          dashboardStats?.approved_value || 0,
          (dashboardStats?.approved_value || 0) * 0.1, // 10% de comissão estimada
          (dashboardStats?.total_value || 0) * 1.2 // Meta 20% acima do atual
        ],
        backgroundColor: [
          'rgba(24, 144, 255, 0.8)',
          'rgba(82, 196, 26, 0.8)',
          'rgba(250, 140, 22, 0.8)',
          'rgba(114, 46, 209, 0.8)'
        ],
        borderColor: [
          '#1890ff',
          '#52c41a',
          '#fa8c16',
          '#722ed1'
        ],
        borderWidth: 2,
        borderRadius: 4,
        borderSkipped: false
      }
    ]
  };

  // Configurações comuns para os gráficos
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    backgroundColor: '#FFFFFF',
    plugins: {
      legend: {
        position: 'bottom' as const,
        labels: {
          padding: 20,
          usePointStyle: true,
          font: {
            size: 12
          }
        }
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#ffffff',
        bodyColor: '#ffffff',
        cornerRadius: 6,
        displayColors: true
      }
    },
    layout: {
      padding: 0
    }
  };

  const statusChartOptions = {
    ...chartOptions,
    plugins: {
      ...chartOptions.plugins,
      tooltip: {
        ...chartOptions.plugins.tooltip,
        callbacks: {
          label: function(context: { dataset: { data: number[] }, parsed: number, label: string }) {
            const total = context.dataset.data.reduce((a: number, b: number) => a + b, 0);
            const percentage = total > 0 ? ((context.parsed * 100) / total).toFixed(1) : '0.0';
            return `${context.label}: ${context.parsed} (${percentage}%)`;
          }
        }
      }
    }
  };

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const performanceChartOptions: any = {
    ...chartOptions,
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          callback: function(value: any) {
            return formatCurrency(Number(value));
          }
        }
      }
    },
    plugins: {
      ...chartOptions.plugins,
      tooltip: {
        ...chartOptions.plugins.tooltip,
        callbacks: {
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          label: function(tooltipItem: any) {
            return `${tooltipItem.dataset.label || 'Dados'}: ${formatCurrency(tooltipItem.parsed.y)}`;
          }
        }
      }
    }
  };

  return (
    <div style={{ padding: '24px' }}>
      {/* Header com Filtros */}
      <div style={{ marginBottom: '32px' }}>
        <Row justify="space-between" align="middle">
          <Col>
            <Space direction="vertical" size={4}>
              <Title level={2} style={{ margin: 0, color: '#1890ff' }}>
                📊 Dashboard - Olá, {user?.full_name}!
              </Title>
              <Text type="secondary" style={{ fontSize: '16px' }}>
                Análise visual dos seus orçamentos • {getPeriodText()}
              </Text>
            </Space>
          </Col>
          <Col>
            <Space>
              <Select
                value={customDateRange ? 'custom' : filterDays.toString()}
                onChange={handlePeriodChange}
                style={{ width: 160 }}
              >
                <Option value="1">Hoje</Option>
                <Option value="3">3 dias</Option>
                <Option value="7">7 dias</Option>
                <Option value="15">15 dias</Option>
                <Option value="30">30 dias</Option>
                <Option value="90">90 dias</Option>
                <Option value="custom">Personalizado</Option>
              </Select>
              
              {filterDays === 0 && (
                <RangePicker
                  placeholder={['Data inicial', 'Data final']}
                  onChange={handleCustomDateChange}
                  format="DD/MM/YYYY"
                  style={{ width: 250 }}
                  value={customDateRange ? [
                    dayjs(customDateRange[0]),
                    dayjs(customDateRange[1])
                  ] : null}
                />
              )}
              
              <Button 
                icon={<ReloadOutlined spin={isRefetching} />} 
                onClick={() => refetch()}
                loading={isRefetching}
              >
                Atualizar
              </Button>

              <Link to="/budgets">
                <Button icon={<EyeOutlined />}>
                  Ver Todos
                </Button>
              </Link>
              
              <Link to="/budgets/new">
                <Button type="primary" icon={<PlusOutlined />}>
                  Novo Orçamento
                </Button>
              </Link>
            </Space>
          </Col>
        </Row>
      </div>

      {isLoading ? (
        <div style={{ textAlign: 'center', padding: '100px' }}>
          <div style={{ 
            fontSize: '48px', 
            color: '#1890ff', 
            marginBottom: '16px' 
          }}>
            📊
          </div>
          <Title level={3} style={{ color: '#8c8c8c' }}>
            Carregando dados do dashboard...
          </Title>
          <Text type="secondary">
            Por favor, aguarde enquanto coletamos as informações dos seus orçamentos.
          </Text>
        </div>
      ) : (
        <>
          {/* Status dos Orçamentos com StatusCards */}
      <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
        <Col span={24}>
          <Title level={4} style={{ margin: '0 0 16px 0' }}>
            <FileTextOutlined style={{ marginRight: '8px' }} />
            Status dos Orçamentos
          </Title>
        </Col>
        {statusData.map((status, index) => (
          <Col xs={12} sm={8} lg={5} key={index}>
            <StatusCard
              title={status.title}
              value={status.value}
              icon={status.icon}
              color={status.color}
            />
          </Col>
        ))}
      </Row>

      {/* Gráficos Analíticos */}
      <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
        {/* Gráfico de Pizza - Status dos Orçamentos */}
        <Col xs={24} lg={8}>
          <Card 
            title={
              <Space>
                <FileTextOutlined />
                <span>Distribuição por Status</span>
              </Space>
            }
            loading={isLoading}
            style={{ height: '400px' }}
          >
            <div style={{ height: '300px', position: 'relative' }}>
              <Doughnut data={statusChartData} options={statusChartOptions} />
                </div>
          </Card>
        </Col>

        {/* Gráfico de Linha - Evolução Temporal */}
        <Col xs={24} lg={8}>
            <Card 
            title={
                        <Space>
                <TrophyOutlined />
                <span>Evolução dos Orçamentos</span>
                        </Space>
                      }
            loading={isLoading}
            style={{ height: '400px' }}
          >
            <div style={{ height: '300px', position: 'relative' }}>
              <Line data={evolutionChartData} options={chartOptions} />
            </div>
          </Card>
        </Col>
        
        {/* Gráfico de Barras - Performance Financeira */}
        <Col xs={24} lg={8}>
          <Card 
            title={
              <Space>
                <DollarCircleOutlined />
                <span>Performance Financeira</span>
              </Space>
            }
            loading={isLoading}
            style={{ height: '400px' }}
          >
            <div style={{ height: '300px', position: 'relative' }}>
              <Bar data={performanceChartData} options={performanceChartOptions} />
            </div>
          </Card>
        </Col>
      </Row>

      {/* Ações Rápidas - Mantida em layout horizontal */}
      <Row gutter={[16, 16]}>
        <Col span={24}>
          <Card 
            title={
              <Space>
                <CalculatorOutlined />
                <span>⚡ Ações Rápidas</span>
              </Space>
            }
          >
            <Row gutter={[16, 16]} align="middle">
              <Col xs={24} sm={12} lg={6}>
                <Link to="/budgets/new" style={{ width: '100%' }}>
                  <Button 
                    type="primary" 
                    size="large" 
                    icon={<PlusOutlined />}
                    block
                    style={{ height: '50px', fontSize: '16px' }}
                  >
                    Criar Novo Orçamento
                  </Button>
                </Link>
              </Col>
              
              <Col xs={24} sm={12} lg={6}>
                <Link to="/budgets" style={{ width: '100%' }}>
                  <Button 
                    size="large" 
                    icon={<FileTextOutlined />}
                    block
                    style={{ height: '50px', fontSize: '16px' }}
                  >
                    Ver Todos os Orçamentos
                  </Button>
                </Link>
        </Col>
        
              <Col xs={24} lg={12}>
                <Alert
                  message="💡 Dica Rápida"
                  description="Use o formulário simplificado para criar orçamentos mais rapidamente com markup automático."
                  type="info"
                  showIcon
                  style={{ fontSize: '12px', margin: 0 }}
                />
              </Col>
            </Row>
          </Card>
        </Col>
      </Row>

      {/* Resumo de Performance */}
      {dashboardStats && (
        <Card 
          title="📈 Resumo de Performance"
          style={{ marginTop: '24px' }}
        >
          <Row gutter={[24, 16]}>
            <Col xs={24} md={12}>
              <div style={{ 
                background: '#FFFFFF',
                padding: '20px',
                borderRadius: '8px',
                border: '1px solid #f0f0f0'
              }}>
                <Title level={5} style={{ margin: '0 0 16px 0', color: '#0369a1' }}>
                  💰 Performance Financeira
                </Title>
                <Row gutter={[16, 8]}>
                  <Col span={12}>
                    <div style={{ textAlign: 'center' }}>
                      <Text type="secondary" style={{ fontSize: '11px' }}>TOTAL ORÇADO</Text>
                      <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#52c41a' }}>
                        {formatCurrency(dashboardStats.total_value)}
                      </div>
                    </div>
                  </Col>
                  <Col span={12}>
                    <div style={{ textAlign: 'center' }}>
                      <Text type="secondary" style={{ fontSize: '11px' }}>TOTAL APROVADO</Text>
                      <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#722ed1' }}>
                        {formatCurrency(dashboardStats.approved_value)}
                      </div>
                    </div>
                  </Col>
                </Row>
              </div>
            </Col>
            
            <Col xs={24} md={12}>
              <div style={{ 
                background: '#FFFFFF',
                padding: '20px',
                borderRadius: '8px',
                border: '1px solid #f0f0f0'
              }}>
                <Title level={5} style={{ margin: '0 0 16px 0', color: '#c2410c' }}>
                  📊 Taxa de Conversão
                </Title>
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#ea580c' }}>
                    {dashboardStats.conversion_rate.toFixed(1)}%
                  </div>
                  <Text type="secondary" style={{ fontSize: '12px' }}>
                    {dashboardStats.approved_budgets} de {dashboardStats.total_budgets} orçamentos aprovados
                  </Text>
                </div>
              </div>
            </Col>
          </Row>
        </Card>
      )}
        </>
      )}
    </div>
  );
};

export default AntDashboard;