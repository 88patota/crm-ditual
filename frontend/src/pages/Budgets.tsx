import { useState } from 'react';
import {
  Card,
  Row,
  Col,
  Typography,
  Space,
  Table,
  Tag,
  Button,
  Modal,
  message,
  Badge,
  Tooltip,
  Input,
  Select,
  Dropdown,
  DatePicker
} from 'antd';
import type { MenuProps, TableColumnsType } from 'antd';
import {
  FileTextOutlined,
  PlusOutlined,
  EyeOutlined,
  EditOutlined,
  DeleteOutlined,
  ClockCircleOutlined,
  FilterOutlined,
  MoreOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  ExclamationCircleOutlined,
  FilePdfOutlined,
  ReloadOutlined,
  CalendarOutlined,
  SearchOutlined
} from '@ant-design/icons';
import { 
  StatusCard 
} from '../components/ui/DashboardCard';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { budgetService } from '../services/budgetService';
import type { BudgetSummary } from '../services/budgetService';
import { Link, useNavigate } from 'react-router-dom';
import dayjs from 'dayjs';

const { Title, Text } = Typography;
const { Option } = Select;
const { RangePicker } = DatePicker;

export default function Budgets() {
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const [searchText, setSearchText] = useState('');
  const [statusFilter, setStatusFilter] = useState<string | undefined>();
  const [clientFilter, setClientFilter] = useState('');
  const [filterDays, setFilterDays] = useState<number>(30);
  const [customDateRange, setCustomDateRange] = useState<[string, string] | null>(null);
  const [showFilters, setShowFilters] = useState(false);

  const { data: budgets = [], isLoading, refetch, isRefetching } = useQuery({
    queryKey: ['budgets', searchText, statusFilter, clientFilter, filterDays, customDateRange],
    queryFn: () => budgetService.getBudgets({
      client_name: clientFilter || undefined,
      status: statusFilter,
      days: customDateRange ? undefined : (filterDays > 0 ? filterDays : undefined),
      custom_start: customDateRange ? customDateRange[0] : undefined,
      custom_end: customDateRange ? customDateRange[1] : undefined,
    }),
    refetchInterval: 2 * 60 * 1000, // Refetch a cada 2 minutos
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
    if (customDateRange && customDateRange[0] && customDateRange[1]) {
      return `Período personalizado: ${new Date(customDateRange[0]).toLocaleDateString('pt-BR')} até ${new Date(customDateRange[1]).toLocaleDateString('pt-BR')}`;
    }
    if (filterDays === 0) {
      return 'Selecione um período personalizado';
    }
    if (filterDays === 1) {
      return 'Hoje';
    }
    return `Últimos ${filterDays} dias`;
  };

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

  const handleExportPdf = async (budget: BudgetSummary) => {
    try {
      const loadingMessage = message.loading('Gerando PDF...', 0);
      
      await budgetService.exportAndDownloadPdf(
        budget.id, 
        `Proposta_${budget.order_number}.pdf`
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

  // Cards de estatísticas removidos conforme solicitado

  // Dados para os StatusCards
  const statusCounts = budgets.reduce((acc, budget) => {
    acc[budget.status] = (acc[budget.status] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const statusData = [
    {
      title: 'Rascunhos',
      value: statusCounts.draft || 0,
      icon: <FileTextOutlined />,
      color: '#8c8c8c'
    },
    {
      title: 'Pendentes',
      value: statusCounts.pending || 0,
      icon: <ClockCircleOutlined />,
      color: '#1890ff'
    },
    {
      title: 'Aprovados',
      value: statusCounts.approved || 0,
      icon: <CheckCircleOutlined />,
      color: '#52c41a'
    },
    {
      title: 'Rejeitados',
      value: statusCounts.rejected || 0,
      icon: <CloseCircleOutlined />,
      color: '#ff4d4f'
    },
    {
      title: 'Expirados',
      value: statusCounts.expired || 0,
      icon: <ExclamationCircleOutlined />,
      color: '#faad14'
    }
  ];

  // Configuração da tabela
  const columns: TableColumnsType<BudgetSummary> = [
    {
      title: 'Pedido',
      dataIndex: 'order_number',
      key: 'order_number',
      width: 120,
      fixed: 'left',
      render: (text: string, record: BudgetSummary) => (
        <Space direction="vertical" size={0}>
          <Text strong style={{ color: '#1890ff' }}>
            {text}
          </Text>
          <Text type="secondary" style={{ fontSize: '12px' }}>
            #{record.id}
          </Text>
        </Space>
      ),
    },
    {
      title: 'Cliente',
      dataIndex: 'client_name',
      key: 'client_name',
      ellipsis: true,
      render: (text: string) => (
        <Space>
          <Text strong>{text}</Text>
        </Space>
      ),
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      width: 120,
      filters: [
        { text: 'Rascunho', value: 'draft' },
        { text: 'Pendente', value: 'pending' },
        { text: 'Aprovado', value: 'approved' },
        { text: 'Rejeitado', value: 'rejected' },
        { text: 'Expirado', value: 'expired' },
      ],
      onFilter: (value: boolean | React.Key, record: BudgetSummary) => record.status === value,
      render: (status: string) => (
        <Tag 
          color={getStatusColor(status)}
          icon={getStatusIcon(status)}
        >
          {getStatusText(status)}
        </Tag>
      ),
    },
    {
      title: 'Itens',
      dataIndex: 'items_count',
      key: 'items_count',
      width: 80,
      align: 'center',
      render: (count: number) => (
        <Badge count={count} style={{ backgroundColor: '#1890ff' }} />
      ),
    },
    {
      title: 'Valor Total',
      dataIndex: 'total_sale_with_icms',
      key: 'total_sale_with_icms',
      width: 140,
      align: 'right',
      sorter: (a: BudgetSummary, b: BudgetSummary) => (a.total_sale_with_icms || 0) - (b.total_sale_with_icms || 0),
      render: (value: number) => (
        <Text strong style={{ color: '#52c41a', fontSize: '16px' }}>
          R$ {(value || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
        </Text>
      ),
    },
    {
      title: 'Comissão',
      dataIndex: 'total_commission',
      key: 'total_commission',
      width: 120,
      align: 'right',
      sorter: (a: BudgetSummary, b: BudgetSummary) => a.total_commission - b.total_commission,
      render: (value: number) => (
        <Text style={{ color: '#fa541c' }}>
          R$ {value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
        </Text>
      ),
    },
    {
      title: 'Markup',
      dataIndex: 'profitability_percentage',
      key: 'profitability_percentage',
      width: 120,
      align: 'center',
      sorter: (a: BudgetSummary, b: BudgetSummary) => a.profitability_percentage - b.profitability_percentage,
      render: (percentage: number) => (
        <Badge 
          count={`${percentage.toFixed(1)}%`}
          style={{ 
            backgroundColor: percentage > 20 ? '#52c41a' : 
                          percentage > 10 ? '#faad14' : '#ff4d4f'
          }}
        />
      ),
    },
    {
      title: 'Data',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 100,
      sorter: (a: BudgetSummary, b: BudgetSummary) => 
        new Date(a.created_at).getTime() - new Date(b.created_at).getTime(),
      render: (date: string) => (
        <Text type="secondary" style={{ fontSize: '12px' }}>
          {new Date(date).toLocaleDateString('pt-BR')}
        </Text>
      ),
    },
    {
      title: 'Ações',
      key: 'actions',
      width: 120,
      fixed: 'right',
      render: (_, record: BudgetSummary) => (
        <Space size="small">
          <Link to={`/budgets/${record.id}`}>
            <Tooltip title="Visualizar">
              <Button
                type="text"
                icon={<EyeOutlined />}
                size="small"
              />
            </Tooltip>
          </Link>
          <Link to={`/budgets/${record.id}/edit`}>
            <Tooltip title="Editar">
              <Button
                type="text"
                icon={<EditOutlined />}
                size="small"
              />
            </Tooltip>
          </Link>
          <Dropdown
            menu={{ items: getActionItems(record) }}
            trigger={['click']}
          >
            <Button type="text" icon={<MoreOutlined />} size="small" />
          </Dropdown>
        </Space>
      ),
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
      key: 'export-pdf',
      icon: <FilePdfOutlined />,
      label: 'Exportar PDF',
      onClick: () => handleExportPdf(budget),
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
    <div style={{ padding: '24px' }}>
      {/* Header com Filtros */}
      <div style={{ marginBottom: '32px' }}>
        <Row justify="space-between" align="middle">
          <Col>
            <Space direction="vertical" size={4}>
              <Title level={2} style={{ margin: 0, color: '#1890ff' }}>
                📋 Orçamentos
              </Title>
              <Text type="secondary" style={{ fontSize: '16px' }}>
                Gerencie seus orçamentos, rentabilidade e comissões • {getPeriodText()}
              </Text>
            </Space>
          </Col>
          <Col>
            <Space>
              <Button 
                icon={<FilterOutlined />}
                onClick={() => setShowFilters(!showFilters)}
                type={showFilters ? 'primary' : 'default'}
              >
                Filtros
              </Button>
              
              <Button 
                icon={<ReloadOutlined spin={isRefetching} />} 
                onClick={() => refetch()}
                loading={isRefetching}
              >
                Atualizar
              </Button>

              <Link to="/budgets/new">
                <Button 
                  type="primary" 
                  icon={<PlusOutlined />}
                  size="large"
                >
                  Novo Orçamento
                </Button>
              </Link>
            </Space>
          </Col>
        </Row>
      </div>


      {/* Status Cards */}
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

      {/* Filtros Avançados */}
      {showFilters && (
        <Card style={{ marginBottom: '24px' }}>
          <Row gutter={[16, 16]} align="middle">
            <Col xs={24} md={8}>
              <Input
                placeholder="🔍 Buscar por cliente ou pedido..."
                allowClear
                value={searchText}
                onChange={(e) => setSearchText(e.target.value)}
                prefix={<SearchOutlined />}
              />
            </Col>
            <Col xs={12} md={4}>
              <Select
                placeholder="Status"
                allowClear
                value={statusFilter}
                onChange={setStatusFilter}
                style={{ width: '100%' }}
              >
                <Option value="draft">🗂️ Rascunho</Option>
                <Option value="pending">⏳ Pendente</Option>
                <Option value="approved">✅ Aprovado</Option>
                <Option value="rejected">❌ Rejeitado</Option>
                <Option value="expired">⚠️ Expirado</Option>
              </Select>
            </Col>
            <Col xs={12} md={4}>
              <Input
                placeholder="Cliente"
                allowClear
                value={clientFilter}
                onChange={(e) => setClientFilter(e.target.value)}
              />
            </Col>
            <Col xs={24} md={6}>
              <Select
                placeholder="Período"
                allowClear
                value={filterDays === 0 ? 'custom' : filterDays.toString()}
                onChange={handlePeriodChange}
                style={{ width: '100%' }}
              >
                <Option value="1">📅 Hoje</Option>
                <Option value="3">📅 3 dias</Option>
                <Option value="7">📅 7 dias</Option>
                <Option value="15">📅 15 dias</Option>
                <Option value="30">📅 30 dias</Option>
                <Option value="90">📅 90 dias</Option>
                <Option value="custom">📅 Personalizado</Option>
              </Select>
            </Col>
            {filterDays === 0 && (
              <Col xs={24} md={6}>
                <RangePicker
                  placeholder={['Data inicial', 'Data final']}
                  onChange={handleCustomDateChange}
                  format="DD/MM/YYYY"
                  style={{ width: '100%' }}
                  value={customDateRange ? [
                    dayjs(customDateRange[0]),
                    dayjs(customDateRange[1])
                  ] : null}
                />
              </Col>
            )}
            <Col xs={24} md={2}>
              <Button
                icon={<CalendarOutlined />}
                onClick={() => {
                  setSearchText('');
                  setStatusFilter(undefined);
                  setClientFilter('');
                  setFilterDays(30);
                  setCustomDateRange(null);
                }}
                title="Limpar filtros"
              >
                Limpar
              </Button>
            </Col>
          </Row>
        </Card>
      )}

      {/* Tabela de Orçamentos */}
      <Card 
        title={
          <Space>
            <FileTextOutlined />
            <span>Lista de Orçamentos</span>
            <Badge count={filteredBudgets.length} style={{ backgroundColor: '#1890ff' }} />
          </Space>
        }
        loading={isLoading}
        extra={
          <Space>
            <Text type="secondary" style={{ fontSize: '12px' }}>
              Total: R$ {filteredBudgets.reduce((sum, budget) => sum + budget.total_sale_value, 0).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
            </Text>
          </Space>
        }
      >
        <Table<BudgetSummary>
          columns={columns}
          dataSource={filteredBudgets}
          rowKey="id"
          scroll={{ x: 1200 }}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total, range) =>
              `${range[0]}-${range[1]} de ${total} orçamentos`,
            pageSizeOptions: ['10', '20', '50', '100'],
          }}
          size="middle"
          bordered={false}
          rowClassName={(_, index) => 
            index % 2 === 0 ? 'table-row-light' : 'table-row-dark'
          }
          onRow={(record) => ({
            onClick: (event) => {
              // Verifica se o clique foi em um botão ou link de ação
              const target = event.target as HTMLElement;
              const isActionButton = target.closest('.ant-btn') || target.closest('a[href]');
              
              // Só navega se não foi clique em botão de ação
              if (!isActionButton) {
                navigate(`/budgets/${record.id}`);
              }
            },
            onDoubleClick: () => {
              window.open(`/budgets/${record.id}`, '_blank');
            },
            style: { cursor: 'pointer' }
          })}
        />
      </Card>
    </div>
  );
}