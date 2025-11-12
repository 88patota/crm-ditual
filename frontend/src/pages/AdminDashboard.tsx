import React, { useState } from 'react';
import { formatCurrency, formatPercentageValue } from '../lib/utils';
import { 
  Card, 
  Row, 
  Col, 
  Typography, 
  Space, 
  Button,
  Select,
  DatePicker,
  Spin,
  Tag
} from 'antd';
import { 
  UserOutlined, 
  FileTextOutlined,
  DollarOutlined,
  TrophyOutlined,
  ClockCircleOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  ExclamationCircleOutlined,
  WarningOutlined,
  CalendarOutlined,
  ReloadOutlined
} from '@ant-design/icons';
import { useAuth } from '../hooks/useAuth';
import { useQuery } from '@tanstack/react-query';
import { budgetService, type DashboardStats } from '../services/budgetService';
import dayjs from 'dayjs';
import 'dayjs/locale/pt-br';

dayjs.locale('pt-br');

const { Title, Text } = Typography;
const { RangePicker } = DatePicker;
const { Option } = Select;

interface StatusCardProps {
  title: string;
  value: number;
  icon: React.ReactNode;
  color: string;
  description?: string;
}

const StatusCard: React.FC<StatusCardProps> = ({ title, value, icon, color, description }) => (
  <Card className="status-card" hoverable>
    <div style={{ display: 'flex', alignItems: 'center', gap: 12, height: '100%' }}>
      <div 
        style={{ 
          backgroundColor: `${color}15`, 
          color: color, 
          borderRadius: '8px',
          padding: '8px',
          fontSize: '18px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          minWidth: '36px',
          minHeight: '36px',
          flexShrink: 0
        }}
      >
        {icon}
      </div>
      <div style={{ flex: 1, minWidth: 0, overflow: 'hidden' }}>
        <Text type="secondary" style={{ fontSize: '11px', marginBottom: '2px', display: 'block', lineHeight: 1.2 }}>
          {title}
        </Text>
        <Title level={5} style={{ 
          margin: 0, 
          color: color, 
          fontSize: '16px', 
          lineHeight: 1.4, 
          whiteSpace: 'nowrap', 
          overflow: 'hidden', 
          textOverflow: 'ellipsis',
          paddingBottom: '1px',
          minHeight: '20px',
          display: 'flex',
          alignItems: 'center'
        }}>
          {value}
        </Title>
        {description && (
          <Text type="secondary" style={{ fontSize: '10px', lineHeight: 1.2 }}>
            {description}
          </Text>
        )}
      </div>
    </div>
  </Card>
);

const AdminDashboard: React.FC = () => {
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

  // Formatação centralizada via utilitário

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

  return (
    <div style={{ padding: '24px' }}>
      {/* Header */}
      <div style={{ marginBottom: '32px' }}>
        <Row justify="space-between" align="middle">
          <Col>
            <Space direction="vertical" size={4}>
              <Title level={2} style={{ margin: 0 }}>
                Dashboard Administrativo 📊
              </Title>
              <Text type="secondary" style={{ fontSize: '16px' }}>
                Indicadores e métricas do sistema • {getPeriodText()}
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
                icon={<ReloadOutlined />} 
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
          {/* Cards principais */}
          <Row gutter={[24, 24]}>
            <Col xs={24} sm={12} lg={6}>
              <Card className="stats-card" hoverable>
                <div style={{ textAlign: 'center', height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', padding: '8px 0' }}>
                  <div style={{ marginBottom: '8px' }}>
                    <FileTextOutlined style={{ color: '#1890ff', fontSize: '24px' }} />
                  </div>
                  <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                    <div style={{ fontSize: '11px', color: '#8c8c8c', marginBottom: '6px', lineHeight: '1.2' }}>Total de Orçamentos</div>
                    <div style={{ color: '#1890ff', fontSize: '22px', fontWeight: 'bold', lineHeight: '1.4', paddingBottom: '2px' }}>
                      {dashboardStats?.total_budgets || 0}
                    </div>
                  </div>
                  <div style={{ marginTop: '4px' }}>
                    <Text type="secondary" style={{ fontSize: '10px', lineHeight: '1.2' }}>
                      no período
                    </Text>
                  </div>
                </div>
              </Card>
            </Col>
            
            <Col xs={24} sm={12} lg={6}>
              <Card className="stats-card" hoverable>
                <div style={{ textAlign: 'center', height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', padding: '8px 0' }}>
                  <div style={{ marginBottom: '8px' }}>
                    <DollarOutlined style={{ color: '#52c41a', fontSize: '24px' }} />
                  </div>
                  <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                    <div style={{ fontSize: '11px', color: '#8c8c8c', marginBottom: '6px', lineHeight: '1.2' }}>Valor Total</div>
                    <div style={{ color: '#52c41a', fontSize: '16px', fontWeight: 'bold', lineHeight: '1.4', paddingBottom: '2px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', maxWidth: '100%', minHeight: '18px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                      {formatCurrency(dashboardStats?.total_value || 0)}
                    </div>
                  </div>
                  <div style={{ marginTop: '4px' }}>
                    <Text type="secondary" style={{ fontSize: '10px', lineHeight: '1.2' }}>
                      em orçamentos
                    </Text>
                  </div>
                </div>
              </Card>
            </Col>
            
            <Col xs={24} sm={12} lg={6}>
              <Card className="stats-card" hoverable>
                <div style={{ textAlign: 'center', height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', padding: '8px 0' }}>
                  <div style={{ marginBottom: '8px' }}>
                    <CheckCircleOutlined style={{ color: '#52c41a', fontSize: '24px' }} />
                  </div>
                  <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                    <div style={{ fontSize: '11px', color: '#8c8c8c', marginBottom: '6px', lineHeight: '1.2' }}>Aprovados</div>
                    <div style={{ color: '#52c41a', fontSize: '22px', fontWeight: 'bold', lineHeight: '1.4', paddingBottom: '2px' }}>
                      {dashboardStats?.approved_budgets || 0}
                    </div>
                  </div>
                  <div style={{ marginTop: '4px' }}>
                    <Text type="secondary" style={{ fontSize: '10px', lineHeight: '1.2' }}>
                      fechados
                    </Text>
                  </div>
                </div>
              </Card>
            </Col>
            
            <Col xs={24} sm={12} lg={6}>
              <Card className="stats-card" hoverable>
                <div style={{ textAlign: 'center', height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', padding: '8px 0' }}>
                  <div style={{ marginBottom: '8px' }}>
                    <TrophyOutlined style={{ color: '#fa8c16', fontSize: '24px' }} />
                  </div>
                  <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                    <div style={{ fontSize: '11px', color: '#8c8c8c', marginBottom: '6px', lineHeight: '1.2' }}>Taxa Conversão</div>
                    <div style={{ color: '#fa8c16', fontSize: '22px', fontWeight: 'bold', lineHeight: '1.4', paddingBottom: '2px' }}>
                      {formatPercentageValue(dashboardStats?.conversion_rate || 0)}
                    </div>
                  </div>
                  <div style={{ marginTop: '4px' }}>
                    <Text type="secondary" style={{ fontSize: '10px', lineHeight: '1.2' }}>
                      aprovação
                    </Text>
                  </div>
                </div>
              </Card>
            </Col>
          </Row>

          {/* Cards por status */}
          <Card title="Orçamentos por Status" style={{ marginTop: '24px' }}>
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

          {/* Resumo do período */}
          {dashboardStats?.period && (
            <Card title="Informações do Período">
              <Row gutter={[16, 16]}>
                <Col xs={24} sm={8}>
                  <div style={{ textAlign: 'center', padding: '16px' }}>
                    <CalendarOutlined style={{ fontSize: '24px', color: '#1890ff', marginBottom: '8px' }} />
                    <div>
                      <Text strong>Período Analisado</Text>
                      <br />
                      <Text type="secondary">
                        {dayjs(dashboardStats.period.start_date).format('DD/MM/YYYY')} até{' '}
                        {dayjs(dashboardStats.period.end_date).format('DD/MM/YYYY')}
                      </Text>
                    </div>
                  </div>
                </Col>
                
                <Col xs={24} sm={8}>
                  <div style={{ textAlign: 'center', padding: '16px' }}>
                    <UserOutlined style={{ fontSize: '24px', color: '#52c41a', marginBottom: '8px' }} />
                    <div>
                      <Text strong>Usuário Logado</Text>
                      <br />
                      <Tag color="blue">{user?.full_name}</Tag>
                    </div>
                  </div>
                </Col>
                
                <Col xs={24} sm={8}>
                  <div style={{ textAlign: 'center', padding: '16px' }}>
                    <ClockCircleOutlined style={{ fontSize: '24px', color: '#fa8c16', marginBottom: '8px' }} />
                    <div>
                      <Text strong>Última Atualização</Text>
                      <br />
                      <Text type="secondary">
                        {dayjs().format('DD/MM/YYYY HH:mm')}
                      </Text>
                    </div>
                  </div>
                </Col>
              </Row>
            </Card>
          )}
        </Space>
      )}
    </div>
  );
};

export default AdminDashboard;
