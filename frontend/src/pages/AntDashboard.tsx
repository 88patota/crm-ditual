import React from 'react';
import '../styles/AntDashboard.css';
import type { User } from '../types/auth';
import { 
  Card, 
  Row, 
  Col, 
  Statistic, 
  Typography, 
  Space, 
  List, 
  Avatar, 
  Tag, 
  Button,
  Progress,
  Timeline,
  Badge
} from 'antd';
import { 
  UserOutlined, 
  TeamOutlined, 
  UserAddOutlined, 
  RiseOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined,
  EyeOutlined,
  MoreOutlined,
  ClockCircleOutlined
} from '@ant-design/icons';
import { useAuth } from '../contexts/AuthContext';
import { useQuery } from '@tanstack/react-query';
import { authService } from '../services/authService';
import AdminDashboard from './AdminDashboard';

const { Title, Text, Paragraph } = Typography;

const AntDashboard: React.FC = () => {
  const { user } = useAuth();

  const { data: users = [], isLoading } = useQuery<User[]>({
    queryKey: ['users'],
    queryFn: authService.getAllUsers,
    enabled: user?.role !== 'admin', // Só carregar se não for admin
  });

  // Se o usuário for admin, mostrar o dashboard administrativo
  if (user?.role === 'admin') {
    return <AdminDashboard />;
  }

  const stats = [
    {
      title: 'Total de Usuários',
      value: users.length,
      suffix: '',
      prefix: <UserOutlined className="stats-icon users" />,
      trend: { value: 12, isPositive: true },
      description: 'vs último mês'
    },
    {
      title: 'Usuários Ativos',
      value: users.filter(u => u.is_active).length,
      suffix: '',
      prefix: <TeamOutlined className="stats-icon active" />,
      trend: { value: 8, isPositive: true },
      description: 'vs último mês'
    },
    {
      title: 'Novos Usuários',
      value: users.filter(u => {
        const created = new Date(u.created_at);
        const lastMonth = new Date();
        lastMonth.setMonth(lastMonth.getMonth() - 1);
        return created > lastMonth;
      }).length,
      suffix: '',
      prefix: <UserAddOutlined className="stats-icon new" />,
      trend: { value: 23, isPositive: true },
      description: 'este mês'
    },
    {
      title: 'Taxa de Crescimento',
      value: (18.2).toFixed(2),
      suffix: '%',
      prefix: <RiseOutlined className="stats-icon growth" />,
      trend: { value: 2, isPositive: false },
      description: 'vs último trimestre'
    },
  ];

  const recentUsers = users
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 5);

  const timelineData = [
    {
      children: 'Novo usuário cadastrado - João Silva',
      color: 'green',
      time: '2 min atrás'
    },
    {
      children: 'Sistema de backup executado com sucesso',
      color: 'blue',
      time: '15 min atrás'
    },
    {
      children: 'Atualização de perfil - Maria Santos',
      color: 'orange',
      time: '1 hora atrás'
    },
    {
      children: 'Relatório mensal gerado',
      color: 'gray',
      time: '3 horas atrás'
    },
  ];

  const getRoleColor = (role: string) => {
    switch (role) {
      case 'admin':
        return 'red';
      case 'manager':
        return 'blue';
      default:
        return 'green';
    }
  };

  const getRoleText = (role: string) => {
    switch (role) {
      case 'admin':
        return 'Administrador';
      case 'manager':
        return 'Gerente';
      default:
        return 'Usuário';
    }
  };

  return (
    <Space direction="vertical" size="large" style={{ width: '100%' }}>
      {/* Welcome Header */}
      <div className="dashboard-header">
        <Row justify="space-between" align="middle">
          <Col>
            <Space direction="vertical" size={4}>
              <Title level={2} style={{ margin: 0 }}>
                Olá, {user?.full_name}! 👋
              </Title>
              <Paragraph style={{ margin: 0, fontSize: '16px', color: '#8c8c8c' }}>
                Aqui está um resumo do que está acontecendo no seu sistema hoje.
              </Paragraph>
            </Space>
          </Col>
          <Col>
            <Space>
              <Button icon={<ClockCircleOutlined />}>
                Últimos 30 dias
              </Button>
              <Button type="primary" icon={<EyeOutlined />}>
                Relatório Completo
              </Button>
            </Space>
          </Col>
        </Row>
      </div>

      {/* Stats Cards */}
      <Row gutter={[16, 16]}>
        {stats.map((stat, index) => (
          <Col xs={24} sm={12} lg={6} key={index}>
            <Card className="stats-card" hoverable>
              <Statistic
                title={stat.title}
                value={stat.value}
                suffix={stat.suffix}
                prefix={stat.prefix}
                valueStyle={{ 
                  fontSize: '20px', 
                  fontWeight: 'bold', 
                  lineHeight: '1.4', 
                  paddingBottom: '2px',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  whiteSpace: 'nowrap',
                  maxWidth: '100%',
                  display: 'block'
                }}
              />
              <div style={{ marginTop: 8, fontSize: '11px', color: '#8c8c8c', display: 'flex', alignItems: 'center', gap: 4 }}>
                {stat.trend.isPositive ? (
                  <ArrowUpOutlined style={{ color: '#52c41a', fontSize: '10px' }} />
                ) : (
                  <ArrowDownOutlined style={{ color: '#ff4d4f', fontSize: '10px' }} />
                )}
                <Text 
                  style={{ 
                    fontSize: '11px',
                    color: stat.trend.isPositive ? '#52c41a' : '#ff4d4f',
                    fontWeight: 500
                  }}
                >
                  {stat.trend.value}%
                </Text>
                <Text style={{ fontSize: '11px', color: '#8c8c8c' }}>
                  {stat.description}
                </Text>
              </div>
            </Card>
          </Col>
        ))}
      </Row>

      <Row gutter={[16, 16]}>
        {/* Account Overview */}
        <Col xs={24} lg={16}>
          <Card 
            title="Visão Geral da Conta"
            extra={<Button type="link" icon={<MoreOutlined />} />}
          >
            <Row gutter={[16, 16]}>
              <Col xs={24} md={8}>
                <Space direction="vertical" align="center" style={{ width: '100%' }}>
                  <Avatar 
                    size={80}
                    style={{ 
                      backgroundColor: '#1890ff',
                      fontSize: '32px',
                      fontWeight: 'bold'
                    }}
                  >
                    {user?.full_name?.charAt(0).toUpperCase()}
                  </Avatar>
                  <Space direction="vertical" size={0} align="center">
                    <Title level={4} style={{ margin: 0 }}>
                      {user?.full_name}
                    </Title>
                    <Tag color={getRoleColor(user?.role || '')}>
                      {getRoleText(user?.role || '')}
                    </Tag>
                    <Text type="secondary">{user?.email}</Text>
                  </Space>
                </Space>
              </Col>
              
              <Col xs={24} md={16}>
                <div className="card-info-grid">
                  <div className="card-info-item">
                    <div className="card-label">Função</div>
                    <div className="card-value" style={{ color: '#1890ff' }}>
                      {getRoleText(user?.role || '')}
                    </div>
                  </div>
                  <div className="card-info-item">
                    <div className="card-label">Status</div>
                    <div className="card-value" style={{ color: '#52c41a' }}>Online</div>
                  </div>
                  <div className="card-info-item">
                    <div className="card-label">Última Atividade</div>
                    <div className="card-value">Agora</div>
                  </div>
                  <div className="card-info-item">
                    <div className="card-label">ID</div>
                    <div className="card-value">{user?.id}</div>
                  </div>
                </div>
              </Col>
            </Row>
          </Card>
        </Col>

        {/* Recent Activity */}
        <Col xs={24} lg={8}>
          <Space direction="vertical" size="middle" style={{ width: '100%' }}>
            <Card 
              title="Usuários Recentes"
              extra={<Button type="link">Ver todos</Button>}
              loading={isLoading}
            >
              <List
                size="small"
                dataSource={recentUsers}
                renderItem={(recentUser) => (
                  <List.Item>
                    <List.Item.Meta
                      avatar={
                        <Avatar style={{ backgroundColor: '#1890ff' }}>
                          {recentUser.full_name.charAt(0).toUpperCase()}
                        </Avatar>
                      }
                      title={recentUser.full_name}
                      description={
                        <Space>
                          <Tag color={getRoleColor(recentUser.role)}>
                            {getRoleText(recentUser.role)}
                          </Tag>
                          <Badge 
                            status={recentUser.is_active ? "success" : "default"} 
                            text={recentUser.is_active ? "Ativo" : "Inativo"}
                          />
                        </Space>
                      }
                    />
                  </List.Item>
                )}
              />
            </Card>

            <Card title="Atividade Recente">
              <Timeline
                items={timelineData.map(item => ({
                  color: item.color,
                  children: (
                    <div>
                      <Text style={{ fontSize: '13px' }}>{item.children}</Text>
                      <br />
                      <Text type="secondary" style={{ fontSize: '11px' }}>
                        {item.time}
                      </Text>
                    </div>
                  )
                }))}
              />
            </Card>
          </Space>
        </Col>
      </Row>

      {/* Progress Cards */}
      <Row gutter={[16, 16]}>
        <Col xs={24} md={8}>
          <Card title="Meta Mensal de Usuários" className="progress-card">
            <Progress 
              percent={75} 
              status="active"
              strokeColor={{
                '0%': '#108ee9',
                '100%': '#87d068',
              }}
            />
            <div style={{ marginTop: 16 }}>
              <Text type="secondary">75 de 100 usuários</Text>
            </div>
          </Card>
        </Col>
        
        <Col xs={24} md={8}>
          <Card title="Satisfação dos Usuários" className="progress-card">
            <Progress 
              percent={92} 
              status="success"
              strokeColor="#52c41a"
            />
            <div style={{ marginTop: 16 }}>
              <Text type="secondary">Baseado em 45 avaliações</Text>
            </div>
          </Card>
        </Col>
        
        <Col xs={24} md={8}>
          <Card title="Uptime do Sistema" className="progress-card">
            <Progress 
              percent={99.9} 
              status="success"
              strokeColor="#1890ff"
            />
            <div style={{ marginTop: 16 }}>
              <Text type="secondary">99.9% este mês</Text>
            </div>
          </Card>
        </Col>
      </Row>
    </Space>
  );
};

export default AntDashboard;