import React from 'react';
import '../styles/AntDashboard.css';
import { 
  Card, 
  Row, 
  Col, 
  Typography, 
  Space, 
  Button,
  Select,
  DatePicker
} from 'antd';
import { 
  FileTextOutlined,
  DollarCircleOutlined,
  TrophyOutlined,
  PlusOutlined,
  EyeOutlined,
  ReloadOutlined
} from '@ant-design/icons';
import { useAuth } from '../hooks/useAuth';
import { useQuery } from '@tanstack/react-query';
import { budgetService } from '../services/budgetService';
import { Link } from 'react-router-dom';
import { authService } from '../services/authService';
import { 
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title as ChartTitle,
  Tooltip,
  Legend
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import { useState } from 'react';
import dayjs, { Dayjs } from 'dayjs';
import { formatCurrency } from '../lib/utils';
import type { BudgetSummary } from '../services/budgetService';
import type { User } from '../types/auth';

const { Title, Text } = Typography;
const { RangePicker } = DatePicker;
const { Option } = Select;

// Registrar componentes do Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ChartTitle,
  Tooltip,
  Legend
);

const AntDashboard: React.FC = () => {
  const { user } = useAuth();
  const [filterDays, setFilterDays] = useState<number>(30);
  const [customDateRange, setCustomDateRange] = useState<[string, string] | null>(null);
  const [selectedSeller, setSelectedSeller] = useState<string | undefined>(undefined);

  

  const { data: users = [] } = useQuery<User[]>({
    queryKey: ['users'],
    queryFn: authService.getAllUsers,
    enabled: user?.role === 'admin'
  });

  const { data: adminBudgets = [], isLoading: adminLoading, refetch: adminRefetch, isRefetching: adminRefetching } = useQuery<BudgetSummary[]>({
    queryKey: ['admin-budgets', selectedSeller, filterDays, customDateRange],
    queryFn: () => {
      const params: Record<string, string | number | undefined> = {};
      if (selectedSeller) params.created_by = selectedSeller;
      if (customDateRange) {
        params.custom_start = customDateRange[0];
        params.custom_end = customDateRange[1];
      } else {
        params.days = filterDays;
      }
      return budgetService.getBudgets(params);
    },
    enabled: user?.role === 'admin'
  });

  const isLoading = user?.role === 'admin' ? adminLoading : false;

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

  const handleCustomDateChange = (dates: [Dayjs, Dayjs] | null) => {
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

  // Formatação centralizada via utilitário

  




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


  const adminStatusCountsData = {
    labels: ['Rascunhos', 'Pendentes', 'Aprovados', 'Perdidos', 'Enviados'],
    datasets: [
      {
        label: 'Quantidade',
        data: [
          adminBudgets.filter((b) => b.status === 'draft').length,
          adminBudgets.filter((b) => b.status === 'pending').length,
          adminBudgets.filter((b) => b.status === 'approved').length,
          adminBudgets.filter((b) => b.status === 'lost').length,
          adminBudgets.filter((b) => b.status === 'sent').length,
        ],
        backgroundColor: 'rgba(24, 144, 255, 0.8)',
        borderColor: '#1890ff',
        borderWidth: 2,
        borderRadius: 4,
        borderSkipped: false,
      },
    ],
  };

  const adminStatusValuesData = {
    labels: ['Rascunhos', 'Pendentes', 'Aprovados', 'Perdidos', 'Enviados'],
    datasets: [
      {
        label: 'Valor Total (R$)',
        data: [
          adminBudgets.filter((b) => b.status === 'draft').reduce((s, x) => s + (x.total_sale_value || 0), 0),
          adminBudgets.filter((b) => b.status === 'pending').reduce((s, x) => s + (x.total_sale_value || 0), 0),
          adminBudgets.filter((b) => b.status === 'approved').reduce((s, x) => s + (x.total_sale_value || 0), 0),
          adminBudgets.filter((b) => b.status === 'lost').reduce((s, x) => s + (x.total_sale_value || 0), 0),
          adminBudgets.filter((b) => b.status === 'sent').reduce((s, x) => s + (x.total_sale_value || 0), 0),
        ],
        backgroundColor: 'rgba(250, 140, 22, 0.8)',
        borderColor: '#fa8c16',
        borderWidth: 2,
        borderRadius: 4,
        borderSkipped: false,
      },
    ],
  };

  const currencyBarOptions = {
    ...chartOptions,
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: function(value: number | string) {
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
          label: function(tooltipItem: { dataset: { label?: string }; parsed: { y: number } }) {
            return `${tooltipItem.dataset.label || 'Dados'}: ${formatCurrency(tooltipItem.parsed.y)}`;
          }
        }
      }
    }
  };

  const origins = Array.from(
    new Set(adminBudgets.map((b) => b.origem || 'Não informada'))
  );
  const adminOriginsCountsData = {
    labels: origins,
    datasets: [
      {
        label: 'Quantidade',
        data: origins.map((o) => adminBudgets.filter((b) => (b.origem || 'Não informada') === o).length),
        backgroundColor: 'rgba(114, 46, 209, 0.8)',
        borderColor: '#722ed1',
        borderWidth: 2,
        borderRadius: 4,
        borderSkipped: false,
      },
    ],
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
                Análise visual das suas propostas • {getPeriodText()}
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
                icon={<ReloadOutlined spin={adminRefetching} />} 
                onClick={() => adminRefetch()}
                loading={adminRefetching}
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
                  Nova Proposta
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
          
          {user?.role === 'admin' && (
            <>
              <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
                <Col span={24}>
                  <Title level={4} style={{ margin: '0 0 16px 0' }}>
                    Administração
                  </Title>
                </Col>
                <Col xs={24} lg={8}>
                  <Card 
                    title={
                      <Space>
                        <FileTextOutlined />
                        <span>Propostas por Status</span>
                      </Space>
                    }
                    extra={
                      <Select
                        placeholder="Selecionar vendedor"
                        allowClear
                        style={{ width: 220 }}
                        value={selectedSeller}
                        onChange={(val) => setSelectedSeller(val)}
                      >
                        {users.map((u) => (
                          <Option key={u.id} value={u.username}>{u.full_name}</Option>
                        ))}
                      </Select>
                    }
                    style={{ height: '400px' }}
                  >
                    <div style={{ height: '300px', position: 'relative' }}>
                      <Bar data={adminStatusCountsData} options={chartOptions} />
                    </div>
                  </Card>
                </Col>
                <Col xs={24} lg={8}>
                  <Card 
                    title={
                      <Space>
                        <DollarCircleOutlined />
                        <span>Valor Total por Status (R$)</span>
                      </Space>
                    }
                    style={{ height: '400px' }}
                  >
                    <div style={{ height: '300px', position: 'relative' }}>
                      <Bar data={adminStatusValuesData} options={currencyBarOptions} />
                    </div>
                  </Card>
                </Col>
                <Col xs={24} lg={8}>
                  <Card 
                    title={
                      <Space>
                        <TrophyOutlined />
                        <span>Propostas por Origem</span>
                      </Space>
                    }
                    style={{ height: '400px' }}
                  >
                    <div style={{ height: '300px', position: 'relative' }}>
                      <Bar data={adminOriginsCountsData} options={chartOptions} />
                    </div>
                  </Card>
                </Col>
              </Row>
            </>
          )}

      

      
        </>
      )}
    </div>
  );
};

export default AntDashboard;