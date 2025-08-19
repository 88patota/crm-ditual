import { useState } from 'react';
import {
  Card,
  Row,
  Col,
  Statistic,
  Typography,
  Space,
  List,
  Tag,
  Button,
  Modal,
  message,
  Badge,
  Tooltip,
  Input,
  Select,
  Dropdown
} from 'antd';
import type { MenuProps } from 'antd';
import {
  FileTextOutlined,
  PlusOutlined,
  EyeOutlined,
  EditOutlined,
  DeleteOutlined,
  CalculatorOutlined,
  DollarCircleOutlined,
  TrophyOutlined,
  ClockCircleOutlined,
  FilterOutlined,
  MoreOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  ExclamationCircleOutlined,
  FilePdfOutlined,
  DownloadOutlined
} from '@ant-design/icons';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { budgetService } from '../services/budgetService';
import type { BudgetSummary } from '../services/budgetService';
import { Link } from 'react-router-dom';

const { Title, Text } = Typography;
const { Option } = Select;

export default function Budgets() {
  const queryClient = useQueryClient();
  const [searchText, setSearchText] = useState('');
  const [statusFilter, setStatusFilter] = useState<string | undefined>();
  const [clientFilter, setClientFilter] = useState('');

  const { data: budgets = [], isLoading } = useQuery({
    queryKey: ['budgets', searchText, statusFilter, clientFilter],
    queryFn: () => budgetService.getBudgets({
      client_name: clientFilter || undefined,
      status: statusFilter
    }),
  });

  const deleteBudgetMutation = useMutation({
    mutationFn: budgetService.deleteBudget,
    onSuccess: () => {
      message.success('Orçamento deletado com sucesso!');
      queryClient.invalidateQueries({ queryKey: ['budgets'] });
    },
    onError: (error: unknown) => {
      const errorMessage = getErrorMessage(error);
      message.error(errorMessage);
    },
  });

  const getErrorMessage = (error: unknown): string => {
    if (typeof error === 'object' && error !== null && 'response' in error) {
      const axiosError = error as { response?: { data?: { detail?: string } } };
      if (axiosError.response?.data?.detail) {
        return axiosError.response.data.detail;
      }
    }
    return 'Ocorreu um erro inesperado. Tente novamente.';
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'draft':
        return 'default';
      case 'pending':
        return 'processing';
      case 'approved':
        return 'success';
      case 'rejected':
        return 'error';
      case 'expired':
        return 'warning';
      default:
        return 'default';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'draft':
        return 'Rascunho';
      case 'pending':
        return 'Pendente';
      case 'approved':
        return 'Aprovado';
      case 'rejected':
        return 'Rejeitado';
      case 'expired':
        return 'Expirado';
      default:
        return status;
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'approved':
        return <CheckCircleOutlined />;
      case 'rejected':
        return <CloseCircleOutlined />;
      case 'expired':
        return <ExclamationCircleOutlined />;
      case 'pending':
        return <ClockCircleOutlined />;
      default:
        return <FileTextOutlined />;
    }
  };

  const handleDeleteBudget = (budgetId: number) => {
    Modal.confirm({
      title: 'Confirmar exclusão',
      content: 'Tem certeza que deseja deletar este orçamento? Esta ação não pode ser desfeita.',
      okText: 'Sim, deletar',
      okType: 'danger',
      cancelText: 'Cancelar',
      onOk: () => deleteBudgetMutation.mutate(budgetId),
    });
  };

  const handleExportPdf = async (budget: BudgetSummary, simplified: boolean = false) => {
    try {
      const loadingMessage = message.loading('Gerando PDF...', 0);
      
      await budgetService.exportAndDownloadPdf(
        budget.id, 
        simplified,
        `Proposta_${simplified ? 'Simplificada' : 'Completa'}_${budget.order_number}.pdf`
      );
      
      loadingMessage();
      message.success('PDF gerado e download iniciado!');
    } catch (error) {
      console.error('Erro ao exportar PDF:', error);
      message.error('Erro ao gerar PDF. Tente novamente.');
    }
  };

  const filteredBudgets = budgets.filter(budget =>
    budget.client_name.toLowerCase().includes(searchText.toLowerCase()) ||
    budget.order_number.toLowerCase().includes(searchText.toLowerCase())
  );

  const stats = [
    {
      title: 'Total de Orçamentos',
      value: budgets.length,
      prefix: <FileTextOutlined className="stats-icon budgets" />,
      color: '#1890ff',
      bgColor: '#e6f7ff',
    },
    {
      title: 'Valor Total',
      value: budgets.reduce((sum, budget) => sum + budget.total_sale_value, 0),
      prefix: <DollarCircleOutlined className="stats-icon total-value" />,
      color: '#52c41a',
      bgColor: '#f6ffed',
      formatter: (value: string | number) => `R$ ${Number(value).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`,
    },
    {
      title: 'Comissões Totais',
      value: budgets.reduce((sum, budget) => sum + budget.total_commission, 0),
      prefix: <TrophyOutlined className="stats-icon commissions" />,
      color: '#fa541c',
      bgColor: '#fff2e8',
      formatter: (value: string | number) => `R$ ${Number(value).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`,
    },
    {
      title: 'Rentabilidade Média',
      value: budgets.length > 0 
        ? budgets.reduce((sum, budget) => sum + budget.profitability_percentage, 0) / budgets.length 
        : 0,
      prefix: <CalculatorOutlined className="stats-icon profitability" />,
      color: '#722ed1',
      bgColor: '#f9f0ff',
      formatter: (value: string | number) => `${Number(value).toFixed(1)}%`,
    },
  ];

  const getActionItems = (budget: BudgetSummary): MenuProps['items'] => [
    {
      key: 'view',
      icon: <EyeOutlined />,
      label: <Link to={`/budgets/${budget.id}`}>Visualizar</Link>,
    },
    {
      key: 'edit',
      icon: <EditOutlined />,
      label: <Link to={`/budgets/${budget.id}/edit`}>Editar</Link>,
    },
    {
      type: 'divider',
    },
    {
      key: 'export-submenu',
      icon: <FilePdfOutlined />,
      label: 'Exportar PDF',
      children: [
        {
          key: 'export-complete',
          icon: <FilePdfOutlined style={{ color: '#dc2626' }} />,
          label: 'Proposta Completa',
          onClick: () => handleExportPdf(budget, false),
        },
        {
          key: 'export-simple',
          icon: <DownloadOutlined style={{ color: '#059669' }} />,
          label: 'Proposta Simplificada',
          onClick: () => handleExportPdf(budget, true),
        },
      ],
    },
    {
      type: 'divider',
    },
    {
      key: 'delete',
      icon: <DeleteOutlined />,
      label: 'Deletar',
      danger: true,
      onClick: () => handleDeleteBudget(budget.id),
    },
  ];

  return (
    <Space direction="vertical" size="large" style={{ width: '100%' }}>
      {/* Header */}
      <div className="budgets-header">
        <Row justify="space-between" align="middle">
          <Col>
            <Space direction="vertical" size={4}>
              <Title level={2} style={{ margin: 0 }}>
                Orçamentos 📋
              </Title>
              <Text style={{ fontSize: '16px', color: '#8c8c8c' }}>
                Gerencie orçamentos, cálculos de rentabilidade e comissões.
              </Text>
            </Space>
          </Col>
          <Col>
            <Space>
              <Button icon={<FilterOutlined />}>
                Filtros
              </Button>
              <Link to="/budgets/new">
                <Button 
                  type="primary" 
                  icon={<PlusOutlined />}
                >
                  Novo Orçamento
                </Button>
              </Link>
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
                prefix={
                  <div 
                    style={{ 
                      backgroundColor: stat.bgColor,
                      color: stat.color,
                      borderRadius: '8px',
                      padding: '8px',
                      display: 'inline-block',
                      marginRight: '12px'
                    }}
                  >
                    {stat.prefix}
                  </div>
                }
                formatter={stat.formatter}
                valueStyle={{ fontSize: '24px', fontWeight: 'bold', color: stat.color }}
              />
            </Card>
          </Col>
        ))}
      </Row>

      {/* Filters and Search */}
      <Card>
        <Row gutter={16} align="middle">
          <Col flex="auto">
            <Input.Search
              placeholder="Buscar por cliente ou número do pedido..."
              allowClear
              onSearch={setSearchText}
              onChange={(e) => setSearchText(e.target.value)}
              style={{ width: '100%' }}
            />
          </Col>
          <Col>
            <Select
              placeholder="Status"
              allowClear
              value={statusFilter}
              onChange={setStatusFilter}
              style={{ width: 150 }}
            >
              <Option value="draft">Rascunho</Option>
              <Option value="pending">Pendente</Option>
              <Option value="approved">Aprovado</Option>
              <Option value="rejected">Rejeitado</Option>
              <Option value="expired">Expirado</Option>
            </Select>
          </Col>
          <Col>
            <Input
              placeholder="Cliente"
              allowClear
              value={clientFilter}
              onChange={(e) => setClientFilter(e.target.value)}
              style={{ width: 200 }}
            />
          </Col>
        </Row>
      </Card>

      {/* Budgets List */}
      <Card 
        title={
          <Space>
            <FileTextOutlined />
            <span>Orçamentos ({filteredBudgets.length})</span>
          </Space>
        }
        loading={isLoading}
      >
        <List
          itemLayout="horizontal"
          dataSource={filteredBudgets}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total, range) =>
              `${range[0]}-${range[1]} de ${total} orçamentos`,
          }}
          renderItem={(budget) => (
            <List.Item
              actions={[
                <Tooltip title="Visualizar">
                  <Link to={`/budgets/${budget.id}`}>
                    <Button
                      type="text"
                      icon={<EyeOutlined />}
                    />
                  </Link>
                </Tooltip>,
                <Tooltip title="Editar">
                  <Link to={`/budgets/${budget.id}/edit`}>
                    <Button
                      type="text"
                      icon={<EditOutlined />}
                    />
                  </Link>
                </Tooltip>,
                <Dropdown
                  menu={{ items: getActionItems(budget) }}
                  trigger={['click']}
                >
                  <Button type="text" icon={<MoreOutlined />} />
                </Dropdown>,
              ]}
            >
              <List.Item.Meta
                avatar={
                  <div style={{
                    width: 48,
                    height: 48,
                    borderRadius: '8px',
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    fontSize: '16px',
                    fontWeight: 'bold'
                  }}>
                    {getStatusIcon(budget.status)}
                  </div>
                }
                title={
                  <Space>
                    <Text strong style={{ fontSize: '16px' }}>
                      Pedido {budget.order_number}
                    </Text>
                    <Tag 
                      color={getStatusColor(budget.status)}
                      icon={getStatusIcon(budget.status)}
                    >
                      {getStatusText(budget.status)}
                    </Tag>
                  </Space>
                }
                description={
                  <Space direction="vertical" size={4}>
                    <Text type="secondary">
                      🏢 {budget.client_name}
                    </Text>
                    <Space>
                      <Text type="secondary">
                        💰 R$ {budget.total_sale_value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                      </Text>
                      <Text type="secondary">
                        📊 {budget.profitability_percentage.toFixed(1)}% rentabilidade
                      </Text>
                      <Text type="secondary">
                        📦 {budget.items_count} itens
                      </Text>
                    </Space>
                    <Text type="secondary" style={{ fontSize: '12px' }}>
                      📅 Criado em {new Date(budget.created_at).toLocaleDateString('pt-BR')}
                    </Text>
                  </Space>
                }
              />
              <div style={{ textAlign: 'right', marginLeft: 16 }}>
                <Space direction="vertical" size={4} style={{ alignItems: 'flex-end' }}>
                  <Text strong style={{ fontSize: '18px', color: '#52c41a' }}>
                    R$ {budget.total_commission.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                  </Text>
                  <Text type="secondary" style={{ fontSize: '12px' }}>
                    Comissão
                  </Text>
                  <Badge 
                    count={`${budget.profitability_percentage.toFixed(1)}%`}
                    style={{ 
                      backgroundColor: budget.profitability_percentage > 20 ? '#52c41a' : 
                                      budget.profitability_percentage > 10 ? '#faad14' : '#ff4d4f'
                    }}
                  />
                </Space>
              </div>
            </List.Item>
          )}
        />
      </Card>
    </Space>
  );
}