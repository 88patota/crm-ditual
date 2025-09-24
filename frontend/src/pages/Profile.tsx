
import { useState } from 'react';
import {
  Card,
  Row,
  Col,
  Typography,
  Form,
  Input,
  Button,
  Avatar,
  Tag,
  Divider,
  Space,
  Upload,
  Tooltip,
  message
} from 'antd';
import {
  UserOutlined,
  LockOutlined,
  MailOutlined,
  CalendarOutlined,
  SaveOutlined,
  EditOutlined,
  CameraOutlined,
  ReloadOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined
} from '@ant-design/icons';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from '../contexts/AuthContext';
import { authService } from '../services/authService';
import type { UserSelfUpdateRequest, PasswordUpdateRequest } from '../types/auth';

const { Title, Text } = Typography;

export default function Profile() {
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const [profileForm] = Form.useForm();
  const [passwordForm] = Form.useForm();

  // Mutations
  const updateProfileMutation = useMutation({
    mutationFn: authService.updateProfile,
    onSuccess: () => {
      message.success('Perfil atualizado com sucesso!');
      queryClient.invalidateQueries({ queryKey: ['user'] });
    },
    onError: (error: any) => {
      message.error(error.response?.data?.detail || 'Falha ao atualizar perfil');
    },
  });

  const updatePasswordMutation = useMutation({
    mutationFn: authService.changePassword,
    onSuccess: () => {
      message.success('Senha atualizada com sucesso!');
      passwordForm.resetFields();
    },
    onError: (error: any) => {
      message.error(error.response?.data?.detail || 'Falha ao atualizar senha');
    },
  });

  const onProfileSubmit = (values: UserSelfUpdateRequest) => {
    updateProfileMutation.mutate(values);
  };

  const onPasswordSubmit = (values: PasswordUpdateRequest) => {
    updatePasswordMutation.mutate(values);
  };

  const getRoleTag = (role: string) => {
    if (role === 'admin') {
      return <Tag color="red" icon={<UserOutlined />}>Administrador</Tag>;
    }
    return <Tag color="blue" icon={<UserOutlined />}>Representante de Vendas</Tag>;
  };

  const getStatusTag = (isActive: boolean) => {
    if (isActive) {
      return <Tag color="success" icon={<CheckCircleOutlined />}>Ativo</Tag>;
    }
    return <Tag color="error" icon={<CloseCircleOutlined />}>Inativo</Tag>;
  };

  return (
    <div style={{ padding: '24px' }}>
      {/* Header */}
      <div style={{ marginBottom: '24px' }}>
        <Title level={2} style={{ margin: 0 }}>
          Configurações do Perfil
        </Title>
        <Text type="secondary">
          Gerencie suas informações pessoais e configurações da conta.
        </Text>
      </div>

      <Row gutter={[24, 24]}>
        {/* Profile Overview Card */}
        <Col span={24}>
          <Card>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '24px' }}>
              <Avatar 
                size={80} 
                icon={<UserOutlined />}
                style={{ 
                  backgroundColor: '#1890ff',
                  marginRight: '24px'
                }}
              />
              <div style={{ flex: 1 }}>
                <Title level={4} style={{ margin: 0 }}>
                  {user?.full_name || 'Usuário'}
                </Title>
                <Text type="secondary" style={{ display: 'block', marginBottom: '8px' }}>
                  @{user?.username}
                </Text>
                <Space>
                  {getRoleTag(user?.role || 'user')}
                  {getStatusTag(user?.is_active || false)}
                </Space>
              </div>
              <Tooltip title="Alterar foto do perfil">
                <Button 
                  type="dashed" 
                  icon={<CameraOutlined />}
                  style={{ marginLeft: 'auto' }}
                >
                  Alterar Foto
                </Button>
              </Tooltip>
            </div>
            
            <Divider />
            
            <Row gutter={[16, 16]}>
              <Col xs={24} sm={12}>
                <Space direction="vertical" size="small">
                  <Text strong>E-mail</Text>
                  <Text copyable>{user?.email}</Text>
                </Space>
              </Col>
              <Col xs={24} sm={12}>
                <Space direction="vertical" size="small">
                  <Text strong>Membro desde</Text>
                  <Space>
                    <CalendarOutlined />
                    <Text>
                      {user?.created_at 
                        ? new Date(user.created_at).toLocaleDateString('pt-BR', {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric'
                          }) 
                        : 'N/A'
                      }
                    </Text>
                  </Space>
                </Space>
              </Col>
            </Row>
          </Card>
        </Col>

        {/* Profile Information */}
        <Col xs={24} lg={12}>
          <Card 
            title={
              <Space>
                <EditOutlined />
                Informações Pessoais
              </Space>
            }
          >
            <Form
              form={profileForm}
              layout="vertical"
              initialValues={{
                full_name: user?.full_name || '',
                email: user?.email || '',
                username: user?.username || '',
              }}
              onFinish={onProfileSubmit}
            >
              <Form.Item
                name="full_name"
                label="Nome Completo"
                rules={[
                  { required: true, message: 'Nome completo é obrigatório' }
                ]}
              >
                <Input 
                  prefix={<UserOutlined />}
                  placeholder="Digite seu nome completo"
                />
              </Form.Item>

              <Form.Item
                name="email"
                label="E-mail"
                rules={[
                  { required: true, message: 'E-mail é obrigatório' },
                  { type: 'email', message: 'E-mail inválido' }
                ]}
              >
                <Input 
                  prefix={<MailOutlined />}
                  placeholder="Digite seu e-mail"
                />
              </Form.Item>

              <Form.Item
                name="username"
                label="Nome de Usuário"
                rules={[
                  { required: true, message: 'Nome de usuário é obrigatório' },
                  { min: 3, message: 'Nome de usuário deve ter pelo menos 3 caracteres' }
                ]}
              >
                <Input 
                  prefix={<UserOutlined />}
                  placeholder="Digite seu nome de usuário"
                />
              </Form.Item>

              <Form.Item style={{ marginBottom: 0 }}>
                <Space>
                  <Button
                    type="primary"
                    htmlType="submit"
                    icon={<SaveOutlined />}
                    loading={updateProfileMutation.isPending}
                  >
                    Salvar Alterações
                  </Button>
                  <Button
                    icon={<ReloadOutlined />}
                    onClick={() => profileForm.resetFields()}
                  >
                    Redefinir
                  </Button>
                </Space>
              </Form.Item>
            </Form>
          </Card>
        </Col>

        {/* Password Change */}
        <Col xs={24} lg={12}>
          <Card 
            title={
              <Space>
                <LockOutlined />
                Alterar Senha
              </Space>
            }
          >
            <Form
              form={passwordForm}
              layout="vertical"
              onFinish={onPasswordSubmit}
            >
              <Form.Item
                name="current_password"
                label="Senha Atual"
                rules={[
                  { required: true, message: 'Senha atual é obrigatória' }
                ]}
              >
                <Input.Password 
                  prefix={<LockOutlined />}
                  placeholder="Digite sua senha atual"
                />
              </Form.Item>

              <Form.Item
                name="new_password"
                label="Nova Senha"
                rules={[
                  { required: true, message: 'Nova senha é obrigatória' },
                  { min: 8, message: 'Senha deve ter pelo menos 8 caracteres' }
                ]}
              >
                <Input.Password 
                  prefix={<LockOutlined />}
                  placeholder="Digite sua nova senha"
                />
              </Form.Item>

              <Form.Item
                name="confirm_password"
                label="Confirmar Nova Senha"
                dependencies={['new_password']}
                rules={[
                  { required: true, message: 'Confirmação de senha é obrigatória' },
                  ({ getFieldValue }) => ({
                    validator(_, value) {
                      if (!value || getFieldValue('new_password') === value) {
                        return Promise.resolve();
                      }
                      return Promise.reject(new Error('As senhas não coincidem'));
                    },
                  }),
                ]}
              >
                <Input.Password 
                  prefix={<LockOutlined />}
                  placeholder="Confirme sua nova senha"
                />
              </Form.Item>

              <Form.Item style={{ marginBottom: 0 }}>
                <Space>
                  <Button
                    type="primary"
                    htmlType="submit"
                    icon={<SaveOutlined />}
                    loading={updatePasswordMutation.isPending}
                  >
                    Atualizar Senha
                  </Button>
                  <Button
                    onClick={() => passwordForm.resetFields()}
                  >
                    Cancelar
                  </Button>
                </Space>
              </Form.Item>
            </Form>
          </Card>
        </Col>
      </Row>
    </div>
  );
}