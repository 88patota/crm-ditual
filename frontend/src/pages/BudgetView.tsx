import { useParams, useNavigate, Link } from 'react-router-dom';
import { useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { formatDeliveryTime } from '../lib/formatters';
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
  Spin,
  Result,
  Modal,
  message,
  Divider,
  Tooltip,
  Alert
} from 'antd';
import {
  EditOutlined,
  DeleteOutlined,
  ArrowLeftOutlined,
  CalculatorOutlined,
  FileTextOutlined,
  CalendarOutlined,
  UserOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  ExclamationCircleOutlined,
  ClockCircleOutlined,
  FilePdfOutlined
} from '@ant-design/icons';
import { budgetService, type Budget, type BudgetItem } from '../services/budgetService';
import dayjs from 'dayjs';
import '../styles/budget-table.css';

const { Title, Text } = Typography;

// Helper function to calculate financial data from backend values
const calculateBudgetFinancials = (budget: Budget) => {
  if (!budget.items || budget.items.length === 0) {
    return {
      totalSaleWithIcms: 0,
      totalNetRevenue: 0,
      totalTaxes: 0,
      taxPercentage: 0
    };
  }

  // Calcular total de venda COM ICMS (valor real que o cliente paga)
  let totalSaleWithIcms = 0;
  
  budget.items.forEach((item: BudgetItem) => {
    const saleWeight = item.sale_weight || item.weight || 0;
    const saleValueWithIcms = item.sale_value_with_icms || 0;
    totalSaleWithIcms += saleWeight * saleValueWithIcms;
  });

  // O total_sale_value do backend já é a receita líquida (SEM impostos)
  const totalNetRevenue = budget.total_sale_value || 0;
  
  // Impostos = Valor COM ICMS - Valor SEM impostos
  const totalTaxes = totalSaleWithIcms - totalNetRevenue;
  const taxPercentage = totalSaleWithIcms > 0 ? (totalTaxes / totalSaleWithIcms) * 100 : 0;

  return {
    totalSaleWithIcms,
    totalNetRevenue,
    totalTaxes,
    taxPercentage
  };
};

export default function BudgetView() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: budget, isLoading, error } = useQuery<Budget>({
    queryKey: ['budget', id],
    queryFn: () => budgetService.getBudgetById(Number(id)),
    enabled: !!id,
  });

  // Debug log para monitorar mudanças nos dados do budget
  useEffect(() => {
    if (budget) {
      console.log('🔍 DEBUG - BudgetView useEffect - Budget data loaded from backend:', budget);
      console.log('🔍 DEBUG - BudgetView useQuery onSuccess - payment_condition:', budget.payment_condition);
    }
  }, [budget]);

  // Calculate net revenue and taxes dynamically
  const financialData = budget ? calculateBudgetFinancials(budget) : {
    totalSaleWithIcms: 0,
    totalNetRevenue: 0,
    totalTaxes: 0,
    taxPercentage: 0
  };

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

  // Função para exportar PDF
  const handleExportPdf = async () => {
    if (!budget) return;
    
    try {
      const loadingMessage = message.loading('Gerando PDF...', 0);
      
      await budgetService.exportAndDownloadPdf(
        budget.id!, 
        `Proposta_${budget.order_number}.pdf`
      );
      
      loadingMessage();
      message.success('PDF gerado e download iniciado!');
    } catch (error) {
      console.error('Erro ao exportar PDF:', error);
      message.error('Erro ao gerar PDF. Tente novamente.');
    }
  };

  const getErrorMessage = (error: unknown): string => {
    if (typeof error === 'object' && error !== null && 'response' in error) {
      const axiosError = error as { response?: { data?: { detail?: string } } };
      if (axiosError.response?.data?.detail) {
        return axiosError.response.data.detail;
      }
    }
    return 'Ocorreu um erro inesperado. Tente novamente.';
  };

  const getStatusColor = (status: string | undefined) => {
    switch (status) {
      case 'draft': return 'default';
      case 'pending': return 'processing';
      case 'approved': return 'success';
      case 'rejected': return 'error';
      case 'expired': return 'warning';
      default: return 'default';
    }
  };

  const getStatusText = (status: string | undefined) => {
    switch (status) {
      case 'draft': return 'Rascunho';
      case 'pending': return 'Pendente';
      case 'approved': return 'Aprovado';
      case 'rejected': return 'Rejeitado';
      case 'expired': return 'Expirado';
      default: return status || 'Desconhecido';
    }
  };

  const getStatusIcon = (status: string | undefined) => {
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
      width: 220,
      fixed: 'left' as const,
      render: (text: string) => (
        <div 
          style={{ 
            wordWrap: 'break-word', 
            wordBreak: 'break-word',
            color: '#333333',
            fontWeight: 500,
            lineHeight: '1.4'
          }}
        >
          {text}
        </div>
      ),
    },
    {
      title: 'Diferença de Peso',
      dataIndex: 'weight_difference_display',
      key: 'weight_difference_display',
      width: 150,
      align: 'center' as const,
      render: (weightDiffDisplay: BudgetItem['weight_difference_display']) => {
        // Só exibe se houver diferença de peso
        if (!weightDiffDisplay?.has_difference) {
          return null;
        }
        
        const isPositive = weightDiffDisplay.percentage_difference > 0;
        const color = isPositive ? '#52c41a' : '#ff4d4f'; // Verde para positivo, vermelho para negativo
        
        return (
          <Tooltip title={`Diferença absoluta: ${weightDiffDisplay.absolute_difference.toFixed(2)} kg`}>
            <div style={{
              color: color,
              fontWeight: 600,
              fontSize: '12px',
              padding: '4px 8px',
              borderRadius: '6px',
              backgroundColor: isPositive ? '#f6ffed' : '#fff2f0',
              border: `1px solid ${isPositive ? '#b7eb8f' : '#ffccc7'}`,
              textAlign: 'center',
              lineHeight: '1.2'
            }}>
              {weightDiffDisplay.formatted_display}
            </div>
          </Tooltip>
        );
      },
    },
    {
      title: 'Prazo',
      dataIndex: 'delivery_time',
      key: 'delivery_time',
      width: 80,
      align: 'center' as const,
      render: (value: string) => (
        <span style={{ 
          color: '#666666',
          fontSize: '13px',
          fontWeight: 500
        }}>
          {formatDeliveryTime(value)}
        </span>
      ),
    },
    {
      title: 'Peso (kg)',
      dataIndex: 'sale_weight',
      key: 'sale_weight',
      width: 90,
      align: 'right' as const,
      render: (value: number) => (
        <span style={{ 
          color: '#666666',
          fontSize: '13px',
          fontFamily: 'monospace'
        }}>
          {value ? value.toFixed(2) : '-'}
        </span>
      ),
    },
    {
      title: (
        <span style={{ 
          color: '#2C3E50', 
          fontWeight: 700,
          fontSize: '14px'
        }}>
          Compra
        </span>
      ),
      children: [
        {
          title: 'Valor c/ICMS',
          dataIndex: 'purchase_value_with_icms',
          key: 'purchase_value_with_icms',
          width: 110,
          align: 'right' as const,
          render: (value: number) => (
            <span style={{ 
              color: '#333333',
              fontWeight: 600,
              fontFamily: 'monospace',
              fontSize: '13px'
            }}>
              {value ? `R$ ${value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}` : 'R$ 0,00'}
            </span>
          ),
        },
        {
          title: 'ICMS %',
          dataIndex: 'purchase_icms_percentage',
          key: 'purchase_icms_percentage',
          width: 80,
          align: 'center' as const,
          render: (value: number) => (
            <span style={{ 
              color: '#666666',
              fontSize: '12px',
              padding: '2px 6px',
              borderRadius: '4px',
              fontWeight: 500
            }}>
              {value ? `${(value * 100).toFixed(1)}%` : '0%'}
            </span>
          ),
        },
      ],
    },
    {
      title: (
        <span style={{ 
          color: '#2C3E50', 
          fontWeight: 700,
          fontSize: '14px'
        }}>
          Venda
        </span>
      ),
      children: [
        {
          title: 'Valor c/ICMS',
          dataIndex: 'sale_value_with_icms',
          key: 'sale_value_with_icms',
          width: 110,
          align: 'right' as const,
          render: (value: number) => (
            <span style={{ 
              color: '#333333',
              fontWeight: 600,
              fontFamily: 'monospace',
              fontSize: '13px'
            }}>
              {value ? `R$ ${value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}` : 'R$ 0,00'}
            </span>
          ),
        },
        {
          title: 'ICMS %',
          dataIndex: 'sale_icms_percentage',
          key: 'sale_icms_percentage',
          width: 80,
          align: 'center' as const,
          render: (value: number) => (
            <span style={{ 
              color: '#666666',
              fontSize: '12px',
              padding: '2px 6px',
              borderRadius: '4px',
              fontWeight: 500
            }}>
              {value ? `${(value * 100).toFixed(1)}%` : '0%'}
            </span>
          ),
        },
      ],
    },
    {
      title: (
        <span style={{ 
          color: '#2C3E50', 
          fontWeight: 700,
          fontSize: '14px'
        }}>
          IPI
        </span>
      ),
      children: [
        {
          title: '%',
          dataIndex: 'ipi_percentage',
          key: 'ipi_percentage',
          width: 70,
          align: 'center' as const,
          render: (value: number) => {
            let displayValue = '0%';
            if (value && value !== 0) {
              if (value === 0.0325) displayValue = '3,25%';
              else if (value === 0.05) displayValue = '5%';
              else displayValue = `${(value * 100).toFixed(2)}%`;
            }
            return (
              <span style={{ 
                color: '#666666',
                fontSize: '12px',
                padding: '2px 6px',
                borderRadius: '4px',
                fontWeight: 500
              }}>
                {displayValue}
              </span>
            );
          },
        },
        {
          title: 'Valor',
          dataIndex: 'ipi_value',
          key: 'ipi_value',
          width: 90,
          align: 'right' as const,
          render: (value: number) => (
            <span style={{ 
              color: '#333333',
              fontWeight: 600,
              fontFamily: 'monospace',
              fontSize: '13px'
            }}>
              {value ? `R$ ${value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}` : '-'}
            </span>
          ),
        },
      ],
    },
    {
      title: (
        <span style={{ 
          color: '#2C3E50', 
          fontWeight: 700,
          fontSize: '14px'
        }}>
          Comissão
        </span>
      ),
      children: [
        {
          title: '%',
          dataIndex: 'commission_percentage_actual',
          key: 'commission_percentage_actual',
          width: 60,
          align: 'center' as const,
          render: (value: number) => (
            <span style={{ 
              color: '#666666',
              fontSize: '12px',
              padding: '2px 6px',
              borderRadius: '4px',
              fontWeight: 500
            }}>
              {value ? `${(value * 100).toFixed(1)}%` : '0%'}
            </span>
          ),
        },
        {
          title: 'Valor',
          dataIndex: 'commission_value',
          key: 'commission_value',
          width: 100,
          align: 'right' as const,
          render: (value: number) => (
            <span style={{ 
              color: '#333333',
              fontWeight: 600,
              fontFamily: 'monospace',
              fontSize: '13px'
            }}>
              {value ? `R$ ${value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}` : 'R$ 0,00'}
            </span>
          ),
        },
      ],
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
      {/* Header - Simplificado */}
      <Card style={{ marginBottom: '24px' }}>
        <Row justify="space-between" align="middle">
          <Col>
            <Space size="large">
              <Button 
                icon={<ArrowLeftOutlined />} 
                onClick={() => navigate('/budgets')}
              >
                Voltar
              </Button>
              <div>
                <Title level={2} style={{ margin: 0, color: '#1890ff' }}>
                  📋 Pedido {budget.order_number}
                </Title>
                <Space>
                  <Tag 
                    color={getStatusColor(budget.status)} 
                    icon={getStatusIcon(budget.status)}
                    style={{ fontSize: '13px', padding: '2px 8px', marginTop: '4px' }}
                  >
                    {getStatusText(budget.status)}
                  </Tag>
                  <Text type="secondary">
                    • {budget.client_name}
                  </Text>
                </Space>
              </div>
            </Space>
          </Col>
          <Col>
            <Space wrap>
              <Tooltip title="Recalcular valores">
                <Button
                  icon={<CalculatorOutlined />}
                  onClick={handleRecalculate}
                  loading={recalculateMutation.isPending}
                />
              </Tooltip>
              
              <Tooltip title="Exportar PDF">
                <Button
                  icon={<FilePdfOutlined />}
                  onClick={handleExportPdf}
                  style={{ color: '#dc2626' }}
                >
                  Exportar PDF
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
              />
            </Space>
          </Col>
        </Row>
      </Card>

      {/* Informações Gerais - Layout Otimizado */}
      <Card title="Informações do Orçamento" style={{ marginBottom: '24px' }}>
        <Row gutter={[24, 16]}>
          <Col xs={24} lg={16}>
            <Descriptions column={{ xs: 1, sm: 2 }} size="middle">
              <Descriptions.Item label="Cliente">
                <Space>
                  <UserOutlined />
                  <Text strong style={{ fontSize: '16px' }}>{budget.client_name}</Text>
                </Space>
              </Descriptions.Item>
              <Descriptions.Item label="Status">
                <Tag 
                  color={getStatusColor(budget.status)} 
                  icon={getStatusIcon(budget.status)}
                  style={{ fontSize: '14px', padding: '4px 12px' }}
                >
                  {getStatusText(budget.status)}
                </Tag>
              </Descriptions.Item>
              <Descriptions.Item label="Criado por">
                <Text>{budget.created_by}</Text>
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
              <Descriptions.Item label="Tipo de Frete">
                <Tag color={budget.freight_type === 'CIF' ? 'blue' : 'orange'}>
                  {budget.freight_type || 'FOB'}
                </Tag>
              </Descriptions.Item>
              <Descriptions.Item label="Condições de Pagamento">
                <Text>{budget.payment_condition || 'À vista'}</Text>
              </Descriptions.Item>
            </Descriptions>
            {budget.notes && (
              <>
                <Divider />
                <div>
                  <Text strong>Observações:</Text>
                  <p style={{ marginTop: '8px', marginBottom: 0, fontSize: '14px' }}>{budget.notes}</p>
                </div>
              </>
            )}
          </Col>
          
          {/* Totais do Pedido - Integrados */}
          <Col xs={24} lg={8}>
            <div style={{ 
              background: 'linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%)',
              padding: '20px',
              borderRadius: '8px',
              border: '1px solid #bae6fd'
            }}>
              <Title level={5} style={{ margin: '0 0 16px 0', color: '#0369a1' }}>
                💰 Totais do Pedido
              </Title>
              <Row gutter={[12, 12]}>
                <Col span={24}>
                  <div style={{ textAlign: 'center' }}>
                    <Text type="secondary" style={{ fontSize: '12px' }}>VALOR TOTAL</Text>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#52c41a' }}>
                      R$ {financialData.totalSaleWithIcms.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                    </div>
                    <Text type="secondary" style={{ fontSize: '11px' }}>
                      COM ICMS
                    </Text>
                  </div>
                </Col>
                <Col span={8}>
                  <div style={{ textAlign: 'center' }}>
                    <Text type="secondary" style={{ fontSize: '11px' }}>COMISSÃO</Text>
                    <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#722ed1' }}>
                      R$ {(budget.total_commission || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                    </div>
                  </div>
                </Col>
                <Col span={8}>
                  <div style={{ textAlign: 'center' }}>
                    <Text type="secondary" style={{ fontSize: '11px' }}>FRETE</Text>
                    <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#1890ff' }}>
                      R$ {(budget.freight_value_total || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                    </div>
                  </div>
                </Col>
                <Col span={8}>
                  <div style={{ textAlign: 'center' }}>
                    <Text type="secondary" style={{ fontSize: '11px' }}>IPI</Text>
                    <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#fa8c16' }}>
                      R$ {(budget.total_ipi_value || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                    </div>
                  </div>
                </Col>
              </Row>
              
              {/* Segunda linha de totais */}
              <Row gutter={[12, 12]} style={{ marginTop: '12px' }}>
                <Col span={12}>
                  <div style={{ textAlign: 'center' }}>
                    <Text type="secondary" style={{ fontSize: '11px' }}>MARKUP</Text>
                    <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#13c2c2' }}>
                      {budget.markup_percentage.toFixed(1)}%
                    </div>
                  </div>
                </Col>
                <Col span={12}>
                  <div style={{ textAlign: 'center' }}>
                    <Text type="secondary" style={{ fontSize: '11px' }}>DIFERENÇA PESO</Text>
                    <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#fa541c' }}>
                      {(budget.total_weight_difference_percentage || 0).toFixed(2)}%
                    </div>
                  </div>
                </Col>
              </Row>
              
              {/* Nota informativa quando há IPI */}
              {budget.total_ipi_value && budget.total_ipi_value > 0 && (
                <Alert 
                  message="IPI Aplicado" 
                  description={`Inclui R$ ${(budget.total_ipi_value || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2 })} de IPI`}
                  type="warning" 
                  showIcon 
                  style={{ marginTop: '12px', fontSize: '11px' }}
                />
              )}
            </div>
          </Col>
        </Row>
      </Card>

      {/* Items Table - Otimizada */}
      <Card 
        title={
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '12px',
            color: '#333333'
          }}>
            <div style={{
              width: '4px',
              height: '24px',
              backgroundColor: '#93CFF0',
              borderRadius: '2px'
            }} />
            <span style={{ 
              fontSize: '16px', 
              fontWeight: 600,
              color: '#333333'
            }}>
              Itens do Orçamento
            </span>
            <Tag 
              color="#E8F4FD" 
              style={{ 
                color: '#93CFF0', 
                fontWeight: 500,
                border: 'none',
                borderRadius: '6px'
              }}
            >
              {budget.items?.length || 0} {budget.items?.length === 1 ? 'item' : 'itens'}
            </Tag>
          </div>
        }
        style={{ 
          marginTop: 24,
          borderRadius: '12px',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)',
          border: '1px solid #F0F0F0'
        }}
      >
        <Table
          dataSource={budget.items}
          columns={itemColumns}
          pagination={false}
          rowKey="id"
          scroll={{ x: 1200 }}
          size="small"
          style={{
            backgroundColor: '#FFFFFF',
            borderRadius: '8px',
            overflow: 'hidden',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)'
          }}
          className="budget-items-table"
        />
      </Card>

    </div>
  );
}
