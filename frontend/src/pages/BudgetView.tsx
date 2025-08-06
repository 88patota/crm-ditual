import { useParams, useNavigate, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  Card,
  Row,
  Col,
  Descriptions,
  Table,
  Tag,
  Space,
  Button,
  Typography,
  Statistic,
  Spin,
  Result,
  Modal,
  message,
  Divider,
  Tooltip
} from 'antd';
import {
  EditOutlined,
  DeleteOutlined,
  ArrowLeftOutlined,
  CalculatorOutlined,
  FileTextOutlined,
  CalendarOutlined,
  UserOutlined,
  DollarCircleOutlined,
  TrophyOutlined,
  PercentageOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  ExclamationCircleOutlined,
  ClockCircleOutlined
} from '@ant-design/icons';
import { budgetService } from '../services/budgetService';
import type { Budget, BudgetItem } from '../services/budgetService';
import dayjs from 'dayjs';

const { Title, Text } = Typography;

export default function BudgetView() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: budget, isLoading, error } = useQuery({
    queryKey: ['budget', id],
    queryFn: () => budgetService.getBudgetById(Number(id)),
    enabled: !!id,
  });

  const deleteBudgetMutation = useMutation({
    mutationFn: budgetService.deleteBudget,
    onSuccess: () => {
      message.success('Orçamento deletado com sucesso!');
      queryClient.invalidateQueries({ queryKey: ['budgets'] });
      navigate('/budgets');
    },
    onError: (error: unknown) => {
      console.error('Erro ao deletar orçamento:', error);
      const errorMessage = getErrorMessage(error);
      message.error(errorMessage);
    },
  });

  const recalculateMutation = useMutation({
    mutationFn: () => budgetService.recalculateBudget(Number(id)),
    onSuccess: () => {
      message.success('Orçamento recalculado com sucesso!');
      queryClient.invalidateQueries({ queryKey: ['budget', id] });
      queryClient.invalidateQueries({ queryKey: ['budgets'] });
    },
    onError: (error: unknown) => {
      console.error('Erro ao recalcular orçamento:', error);
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
      case 'draft': return 'default';
      case 'pending': return 'processing';
      case 'approved': return 'success';
      case 'rejected': return 'error';
      case 'expired': return 'warning';
      default: return 'default';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'draft': return 'Rascunho';
      case 'pending': return 'Pendente';
      case 'approved': return 'Aprovado';
      case 'rejected': return 'Rejeitado';
      case 'expired': return 'Expirado';
      default: return status;
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'approved': return <CheckCircleOutlined />;
      case 'rejected': return <CloseCircleOutlined />;
      case 'expired': return <ExclamationCircleOutlined />;
      case 'pending': return <ClockCircleOutlined />;
      default: return <FileTextOutlined />;
    }
  };

  const handleDelete = () => {
    Modal.confirm({
      title: 'Confirmar exclusão',
      content: 'Tem certeza que deseja deletar este orçamento? Esta ação não pode ser desfeita.',
      okText: 'Sim, deletar',
      okType: 'danger',
      cancelText: 'Cancelar',
      onOk: () => deleteBudgetMutation.mutate(Number(id)),
    });
  };

  const handleRecalculate = () => {
    Modal.confirm({
      title: 'Recalcular orçamento',
      content: 'Isso irá recalcular todos os valores do orçamento. Deseja continuar?',
      okText: 'Sim, recalcular',
      cancelText: 'Cancelar',
      onOk: () => recalculateMutation.mutate(),
    });
  };

  const itemColumns = [
    {
      title: 'Descrição',
      dataIndex: 'description',
      key: 'description',
      width: 200,
    },
    {
      title: 'Qtd',
      dataIndex: 'quantity',
      key: 'quantity',
      width: 80,
      render: (value: number) => value.toFixed(2),
    },
    {
      title: 'Peso (kg)',
      dataIndex: 'weight',
      key: 'weight',
      width: 100,
      render: (value: number) => value?.toFixed(3) || '-',
    },
    {
      title: 'Compra c/ICMS',
      dataIndex: 'purchase_value_with_icms',
      key: 'purchase_value_with_icms',
      width: 130,
      render: (value: number) => `R$ ${value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`,
    },
    {
      title: 'ICMS Compra',
      dataIndex: 'purchase_icms_percentage',
      key: 'purchase_icms_percentage',
      width: 100,
      render: (value: number) => `${value.toFixed(1)}%`,
    },
    {
      title: 'Outras Despesas',
      dataIndex: 'purchase_other_expenses',
      key: 'purchase_other_expenses',
      width: 130,
      render: (value: number) => `R$ ${value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`,
    },
    {
      title: 'Venda c/ICMS',
      dataIndex: 'sale_value_with_icms',
      key: 'sale_value_with_icms',
      width: 130,
      render: (value: number) => `R$ ${value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`,
    },
    {
      title: 'ICMS Venda',
      dataIndex: 'sale_icms_percentage',
      key: 'sale_icms_percentage',
      width: 100,
      render: (value: number) => `${value.toFixed(1)}%`,
    },
    {
      title: 'Comissão',
      dataIndex: 'commission_percentage',
      key: 'commission_percentage',
      width: 100,
      render: (value: number) => `${value.toFixed(1)}%`,
    },
    {
      title: 'Custo Dunamis',
      dataIndex: 'dunamis_cost',
      key: 'dunamis_cost',
      width: 130,
      render: (value: number) => value ? `R$ ${value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}` : '-',
    },
  ];

  if (isLoading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        minHeight: '400px' 
      }}>
        <Spin size="large" />
      </div>
    );
  }

  if (error || !budget) {
    return (
      <Result
        status="404"
        title="Orçamento não encontrado"
        subTitle="O orçamento que você está procurando não existe ou foi removido."
        extra={
          <Link to="/budgets">
            <Button type="primary">Voltar para Orçamentos</Button>
          </Link>
        }
      />
    );
  }

  return (
    <div style={{ padding: '24px' }}>
      {/* Header */}
      <Card style={{ marginBottom: '24px' }}>
        <Row justify="space-between" align="middle">
          <Col>
            <Space>
              <Button 
                icon={<ArrowLeftOutlined />} 
                onClick={() => navigate('/budgets')}
              >
                Voltar
              </Button>
              <div>
                <Title level={3} style={{ margin: 0 }}>
                  Pedido {budget.order_number} 📋
                </Title>
                <Text type="secondary">
                  Criado em {dayjs(budget.created_at).format('DD/MM/YYYY HH:mm')}
                </Text>
              </div>
            </Space>
          </Col>
          <Col>
            <Space>
              <Tooltip title="Recalcular valores">
                <Button
                  icon={<CalculatorOutlined />}
                  onClick={handleRecalculate}
                  loading={recalculateMutation.isPending}
                >
                  Recalcular
                </Button>
              </Tooltip>
              <Link to={`/budgets/${id}/edit`}>
                <Button type="primary" icon={<EditOutlined />}>
                  Editar
                </Button>
              </Link>
              <Button 
                danger 
                icon={<DeleteOutlined />}
                onClick={handleDelete}
                loading={deleteBudgetMutation.isPending}
              >
                Deletar
              </Button>
            </Space>
          </Col>
        </Row>
      </Card>

      {/* Status and Basic Info */}
      <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
        <Col xs={24} lg={16}>
          <Card title="Informações Gerais">
            <Descriptions column={2}>
              <Descriptions.Item label="Número do Pedido">
                <Text strong>{budget.order_number}</Text>
              </Descriptions.Item>
              <Descriptions.Item label="Cliente">
                <Space>
                  <UserOutlined />
                  <Text strong>{budget.client_name}</Text>
                </Space>
              </Descriptions.Item>
              <Descriptions.Item label="Status">
                <Tag 
                  color={getStatusColor(budget.status)} 
                  icon={getStatusIcon(budget.status)}
                >
                  {getStatusText(budget.status)}
                </Tag>
              </Descriptions.Item>
              <Descriptions.Item label="Criado por">
                <Text>{budget.created_by}</Text>
              </Descriptions.Item>
              <Descriptions.Item label="Data de Criação">
                <Space>
                  <CalendarOutlined />
                  <Text>{dayjs(budget.created_at).format('DD/MM/YYYY HH:mm')}</Text>
                </Space>
              </Descriptions.Item>
              <Descriptions.Item label="Última Atualização">
                <Text>{dayjs(budget.updated_at).format('DD/MM/YYYY HH:mm')}</Text>
              </Descriptions.Item>
              {budget.expires_at && (
                <Descriptions.Item label="Data de Expiração">
                  <Space>
                    <CalendarOutlined />
                    <Text>{dayjs(budget.expires_at).format('DD/MM/YYYY')}</Text>
                  </Space>
                </Descriptions.Item>
              )}
              <Descriptions.Item label="% Markup">
                <Text>{budget.markup_percentage?.toFixed(1)}%</Text>
              </Descriptions.Item>
            </Descriptions>
            {budget.notes && (
              <>
                <Divider />
                <div>
                  <Text strong>Observações:</Text>
                  <p style={{ marginTop: '8px', marginBottom: 0 }}>{budget.notes}</p>
                </div>
              </>
            )}
          </Card>
        </Col>
        
        <Col xs={24} lg={8}>
          <Row gutter={[16, 16]}>
            <Col span={24}>
              <Card>
                <Statistic
                  title="Total de Venda"
                  value={budget.total_sale_value}
                  prefix={<DollarCircleOutlined style={{ color: '#52c41a' }} />}
                  formatter={(value) => `R$ ${Number(value).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`}
                  valueStyle={{ color: '#52c41a', fontSize: '24px' }}
                />
              </Card>
            </Col>
            <Col span={24}>
              <Card>
                <Statistic
                  title="Total de Comissão"
                  value={budget.total_commission}
                  prefix={<TrophyOutlined style={{ color: '#fa541c' }} />}
                  formatter={(value) => `R$ ${Number(value).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`}
                  valueStyle={{ color: '#fa541c', fontSize: '24px' }}
                />
              </Card>
            </Col>
            <Col span={24}>
              <Card>
                <Statistic
                  title="Rentabilidade"
                  value={budget.profitability_percentage}
                  prefix={<PercentageOutlined style={{ color: '#722ed1' }} />}
                  formatter={(value) => `${Number(value).toFixed(1)}%`}
                  valueStyle={{ 
                    color: Number(budget.profitability_percentage) > 20 ? '#52c41a' : 
                           Number(budget.profitability_percentage) > 10 ? '#faad14' : '#ff4d4f',
                    fontSize: '24px'
                  }}
                />
              </Card>
            </Col>
          </Row>
        </Col>
      </Row>

      {/* Items Table */}
      <Card title={`Itens do Orçamento (${budget.items?.length || 0})`}>
        <Table
          dataSource={budget.items}
          columns={itemColumns}
          pagination={false}
          rowKey="id"
          scroll={{ x: 1200 }}
          size="small"
        />
      </Card>

      {/* Summary */}
      <Card title="Resumo Financeiro" style={{ marginTop: '24px' }}>
        <Row gutter={[16, 16]}>
          <Col xs={12} md={6}>
            <Statistic
              title="Total Compra"
              value={budget.total_purchase_value}
              formatter={(value) => `R$ ${Number(value).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`}
            />
          </Col>
          <Col xs={12} md={6}>
            <Statistic
              title="Total Venda"
              value={budget.total_sale_value}
              formatter={(value) => `R$ ${Number(value).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`}
            />
          </Col>
          <Col xs={12} md={6}>
            <Statistic
              title="Total Comissão"
              value={budget.total_commission}
              formatter={(value) => `R$ ${Number(value).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`}
            />
          </Col>
          <Col xs={12} md={6}>
            <Statistic
              title="Rentabilidade"
              value={budget.profitability_percentage}
              formatter={(value) => `${Number(value).toFixed(1)}%`}
            />
          </Col>
        </Row>
      </Card>
    </div>
  );
}