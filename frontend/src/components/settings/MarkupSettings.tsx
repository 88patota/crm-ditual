import { useState, useEffect } from 'react';
import {
  Card,
  Form,
  Row,
  Col,
  InputNumber,
  Select,
  Button,
  Space,
  Typography,
  Divider,
  message,
  Alert,
  Descriptions,
  Statistic
} from 'antd';
import {
  SaveOutlined,
  ReloadOutlined,
  SettingOutlined,
  InfoCircleOutlined
} from '@ant-design/icons';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { budgetService } from '../../services/budgetService';
import type { MarkupConfiguration } from '../../services/budgetService';
import { formatCurrency } from '../../lib/utils';

const { Title, Text } = Typography;
const { Option } = Select;

// Funções utilitárias para formatação de moeda brasileira
const formatBRLCurrency = (value: number | string | undefined): string => {
  if (!value && value !== 0) return '';
  const numValue = typeof value === 'string' ? parseFloat(value) : value;
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(numValue);
};

const parseBRLCurrency = (value: string | undefined): number => {
  if (!value) return 0;
  // Remove R$, espaços, pontos (separadores de milhares) e substitui vírgula por ponto
  const cleanValue = value
    .replace(/R\$\s?/g, '')
    .replace(/\./g, '')
    .replace(/,/g, '.');
  return parseFloat(cleanValue) || 0;
};

export default function MarkupSettings() {
  const [form] = Form.useForm();
  const queryClient = useQueryClient();

  // Buscar configurações atuais
  const { data: settings, isLoading, refetch } = useQuery({
    queryKey: ['markup-settings'],
    queryFn: budgetService.getMarkupSettings,
  });

  // Mutation para salvar configurações (simulada - implementar endpoint no backend)
  const saveSettingsMutation = useMutation({
    mutationFn: async (newSettings: MarkupConfiguration) => {
      // TODO: Implementar endpoint de salvamento no backend
      // Por enquanto, apenas simula o salvamento
      await new Promise(resolve => setTimeout(resolve, 1000));
      return newSettings;
    },
    onSuccess: () => {
      message.success('Configurações salvas com sucesso!');
      queryClient.invalidateQueries({ queryKey: ['markup-settings'] });
    },
    onError: () => {
      message.error('Erro ao salvar configurações');
    },
  });

  useEffect(() => {
    if (settings) {
      form.setFieldsValue(settings);
    }
  }, [settings, form]);

  const handleSave = async () => {
    try {
      const formData = await form.validateFields();
      await saveSettingsMutation.mutateAsync(formData);
    } catch (error) {
      console.error('Erro na validação:', error);
    }
  };

  const handleReset = () => {
    if (settings) {
      form.setFieldsValue(settings);
      message.info('Configurações restauradas aos valores atuais');
    }
  };

  const handleDefaults = () => {
    const defaultSettings: MarkupConfiguration = {
      minimum_markup_percentage: 20.0,
      maximum_markup_percentage: 200.0,
      default_market_position: 'competitive',
      icms_sale_default: 17.0,
      commission_default: 1.5,
      other_expenses_default: 0.0,
    };
    
    form.setFieldsValue(defaultSettings);
    message.info('Configurações padrão aplicadas');
  };

  if (isLoading) {
    return (
      <Card loading={true}>
        <div style={{ height: 400 }} />
      </Card>
    );
  }

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <Row justify="space-between" align="middle" style={{ marginBottom: '24px' }}>
          <Col>
            <Space direction="vertical" size={4}>
              <Title level={3} style={{ margin: 0 }}>
                <SettingOutlined /> Configurações de Markup
              </Title>
              <Text type="secondary">
                Configure os parâmetros para cálculo automático de markup nos orçamentos.
              </Text>
            </Space>
          </Col>
          <Col>
            <Space>
              <Button
                icon={<ReloadOutlined />}
                onClick={() => refetch()}
                loading={isLoading}
              >
                Atualizar
              </Button>
              <Button onClick={handleDefaults}>
                Padrões
              </Button>
              <Button onClick={handleReset}>
                Restaurar
              </Button>
              <Button
                type="primary"
                icon={<SaveOutlined />}
                onClick={handleSave}
                loading={saveSettingsMutation.isPending}
              >
                Salvar
              </Button>
            </Space>
          </Col>
        </Row>

        <Alert
          message="Configurações Globais"
          description="Estas configurações afetam o cálculo automático de markup em todos os novos orçamentos criados no sistema."
          type="info"
          icon={<InfoCircleOutlined />}
          style={{ marginBottom: '24px' }}
          showIcon
        />

        <Form
          form={form}
          layout="vertical"
          initialValues={settings}
        >
          <Row gutter={[24, 24]}>
            {/* Configurações de Markup */}
            <Col xs={24} lg={12}>
              <Card title="Limites de Markup" size="small">
                <Row gutter={[16, 16]}>
                  <Col span={12}>
                    <Form.Item
                      label="Markup Mínimo (%)"
                      name="minimum_markup_percentage"
                      rules={[
                        { required: true, message: 'Campo obrigatório' },
                        { type: 'number', min: 0, max: 100, message: 'Deve estar entre 0 e 100%' }
                      ]}
                      extra="Markup mínimo aplicado automaticamente"
                    >
                      <InputNumber
                        min={0}
                        max={100}
                        step={0.1}
                        precision={1}
                        formatter={(value) => `${value}%`}
                        parser={(value) => value!.replace('%', '')}
                        style={{ width: '100%' }}
                      />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item
                      label="Markup Máximo (%)"
                      name="maximum_markup_percentage"
                      rules={[
                        { required: true, message: 'Campo obrigatório' },
                        { type: 'number', min: 0, max: 1000, message: 'Deve estar entre 0 e 1000%' }
                      ]}
                      extra="Markup máximo permitido no sistema"
                    >
                      <InputNumber
                        min={0}
                        max={1000}
                        step={0.1}
                        precision={1}
                        formatter={(value) => `${value}%`}
                        parser={(value) => value!.replace('%', '')}
                        style={{ width: '100%' }}
                      />
                    </Form.Item>
                  </Col>
                </Row>

                <Form.Item
                  label="Posicionamento Padrão de Mercado"
                  name="default_market_position"
                  extra="Estratégia padrão quando não há preços de referência"
                >
                  <Select>
                    <Option value="budget">Econômico (5% abaixo da concorrência)</Option>
                    <Option value="competitive">Competitivo (2% acima da concorrência)</Option>
                    <Option value="premium">Premium (10% acima da concorrência)</Option>
                  </Select>
                </Form.Item>
              </Card>
            </Col>

            {/* Configurações Fiscais */}
            <Col xs={24} lg={12}>
              <Card title="Configurações Fiscais" size="small">
                <Row gutter={[16, 16]}>
                  <Col span={12}>
                    <Form.Item
                      label="ICMS Venda Padrão (%)"
                      name="icms_sale_default"
                      rules={[
                        { required: true, message: 'Campo obrigatório' },
                        { type: 'number', min: 0, max: 100, message: 'Deve estar entre 0 e 100%' }
                      ]}
                      extra="ICMS aplicado nas vendas"
                    >
                      <InputNumber
                        min={0}
                        max={100}
                        step={0.1}
                        precision={1}
                        formatter={(value) => `${value}%`}
                        parser={(value) => value!.replace('%', '')}
                        style={{ width: '100%' }}
                      />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item
                      label="Comissão Padrão (%)"
                      name="commission_default"
                      rules={[
                        { required: true, message: 'Campo obrigatório' },
                        { type: 'number', min: 0, max: 100, message: 'Deve estar entre 0 e 100%' }
                      ]}
                      extra="Comissão padrão dos vendedores"
                    >
                      <InputNumber
                        min={0}
                        max={100}
                        step={0.1}
                        precision={1}
                        formatter={(value) => `${value}%`}
                        parser={(value) => value!.replace('%', '')}
                        style={{ width: '100%' }}
                      />
                    </Form.Item>
                  </Col>
                </Row>

                <Form.Item
                  label="Outras Despesas Padrão (R$)"
                  name="other_expenses_default"
                  rules={[
                    { required: true, message: 'Campo obrigatório' },
                    { type: 'number', min: 0, message: 'Deve ser positivo' }
                  ]}
                  extra="Valor padrão para outras despesas"
                >
                  <InputNumber
                    min={0}
                    step={0.01}
                    precision={2}
                    formatter={formatBRLCurrency}
                    parser={parseBRLCurrency}
                    style={{ width: '100%' }}
                  />
                </Form.Item>
              </Card>
            </Col>
          </Row>

          {/* Preview das Configurações */}
          {settings && (
            <>
              <Divider>Configurações Atuais</Divider>
              
              <Row gutter={[16, 16]}>
                <Col xs={12} md={6}>
                  <Card>
                    <Statistic
                      title="Markup Mínimo"
                      value={settings.minimum_markup_percentage}
                      formatter={(value) => `${Number(value).toFixed(1)}%`}
                      valueStyle={{ color: '#ff4d4f' }}
                    />
                  </Card>
                </Col>
                <Col xs={12} md={6}>
                  <Card>
                    <Statistic
                      title="Markup Máximo"
                      value={settings.maximum_markup_percentage}
                      formatter={(value) => `${Number(value).toFixed(1)}%`}
                      valueStyle={{ color: '#52c41a' }}
                    />
                  </Card>
                </Col>
                <Col xs={12} md={6}>
                  <Card>
                    <Statistic
                      title="ICMS Venda"
                      value={settings.icms_sale_default}
                      formatter={(value) => `${Number(value).toFixed(1)}%`}
                      valueStyle={{ color: '#1890ff' }}
                    />
                  </Card>
                </Col>
                <Col xs={12} md={6}>
                  <Card>
                    <Statistic
                      title="Comissão"
                      value={settings.commission_default}
                      formatter={(value) => `${Number(value).toFixed(1)}%`}
                      valueStyle={{ color: '#fa541c' }}
                    />
                  </Card>
                </Col>
              </Row>

              <Card title="Resumo das Configurações" style={{ marginTop: '16px' }} size="small">
                <Descriptions column={2} size="small">
                  <Descriptions.Item label="Posicionamento Padrão">
                    {settings.default_market_position === 'budget' ? 'Econômico' :
                     settings.default_market_position === 'premium' ? 'Premium' : 'Competitivo'}
                  </Descriptions.Item>
                  <Descriptions.Item label="Outras Despesas">
                    R$ {settings.other_expenses_default.toFixed(2)}
                  </Descriptions.Item>
                </Descriptions>
              </Card>
            </>
          )}
        </Form>
      </Card>
    </div>
  );
}
