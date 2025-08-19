import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Form, Input, Button, Card, Typography, Space, Alert, Divider } from 'antd';
import { UserOutlined, LockOutlined, EyeInvisibleOutlined, EyeTwoTone } from '@ant-design/icons';
import { useAuth } from '../contexts/AuthContext';

const { Title, Text, Paragraph } = Typography;

interface LoginForm {
  username: string;
  password: string;
}

function AntLogin() {
  const { login } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [form] = Form.useForm();

  const onFinish = async (values: LoginForm) => {
    try {
      setLoading(true);
      setError(null);
      await login({ username: values.username, password: values.password });
    } catch (error: unknown) {
      const axiosError = error as { response?: { data?: { detail?: string | Array<{ msg: string }> } } };
      const errorDetail = axiosError?.response?.data?.detail;
      let errorMessage = 'Erro ao fazer login';
      
      if (typeof errorDetail === 'string') {
        errorMessage = errorDetail;
      } else if (Array.isArray(errorDetail)) {
        errorMessage = errorDetail.map((err: { msg: string }) => err.msg).join(', ');
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const demoCredentials = [
    {
      role: 'Administrador',
      description: 'Acesso completo ao sistema - Gerenciar usuários, orçamentos e configurações',
      username: 'admin',
      password: 'admin123',
      color: 'blue',
    },
    {
      role: 'Vendedor (João)',
      description: 'Perfil de vendas - Criar e gerenciar orçamentos, exportar propostas PDF',
      username: 'vendedor',
      password: 'vendedor123',
      color: 'green',
    },
    {
      role: 'Vendedor (Maria)',
      description: 'Perfil de vendas - Criar e gerenciar orçamentos, exportar propostas PDF',
      username: 'vendedor2',
      password: 'vendedor123',
      color: 'orange',
    },
  ];

  const fillCredentials = (username: string, password: string) => {
    form.setFieldsValue({ username, password });
  };

  return (
    <div className="login-container">
      <Card className="login-card" bordered={false}>
        <div className="login-header">
          <div className="login-logo">C</div>
          <Title level={2} style={{ color: 'white', margin: 0 }}>
            Bem-vindo de volta
          </Title>
          <Paragraph style={{ color: 'rgba(255, 255, 255, 0.8)', margin: '8px 0 0 0' }}>
            Entre com suas credenciais para acessar o sistema
          </Paragraph>
        </div>

        <div className="login-form">
          {error && (
            <Alert
              message="Erro de Login"
              description={error}
              type="error"
              showIcon
              style={{ marginBottom: 24 }}
            />
          )}

          <Form
            form={form}
            name="login"
            onFinish={onFinish}
            layout="vertical"
            size="large"
          >
            <Form.Item
              name="username"
              label="Usuário"
              rules={[{ required: true, message: 'Por favor, digite seu usuário!' }]}
            >
              <Input 
                prefix={<UserOutlined />} 
                placeholder="Digite seu usuário"
              />
            </Form.Item>

            <Form.Item
              name="password"
              label="Senha"
              rules={[{ required: true, message: 'Por favor, digite sua senha!' }]}
            >
              <Input.Password
                prefix={<LockOutlined />}
                placeholder="Digite sua senha"
                iconRender={(visible) => (visible ? <EyeTwoTone /> : <EyeInvisibleOutlined />)}
              />
            </Form.Item>

            <Form.Item style={{ marginBottom: 16 }}>
              <Button 
                type="primary" 
                htmlType="submit" 
                loading={loading}
                block
                style={{
                  height: 48,
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  border: 'none',
                  fontSize: '16px',
                  fontWeight: 500
                }}
              >
                Entrar
              </Button>
            </Form.Item>

            <Divider>ou</Divider>

            <Button block style={{ height: 40 }}>
              <Link to="/register" style={{ textDecoration: 'none' }}>
                Criar nova conta
              </Link>
            </Button>
          </Form>

          {/* Demo Credentials */}
          <Card 
            size="small" 
            style={{ 
              marginTop: 24, 
              background: '#f8f9fa',
              border: '1px solid #e9ecef'
            }}
          >
            <Space direction="vertical" style={{ width: '100%' }} size="middle">
              <div style={{ textAlign: 'center' }}>
                <Title level={5} style={{ margin: 0, color: '#495057' }}>
                  🎯 Credenciais de Demonstração
                </Title>
                <Text type="secondary" style={{ fontSize: '12px' }}>
                  Clique em uma das opções abaixo para preencher automaticamente
                </Text>
              </div>

              {demoCredentials.map((credential, index) => (
                <Card 
                  key={index}
                  size="small" 
                  style={{ 
                    background: 'white',
                    cursor: 'pointer',
                    border: `1px solid ${credential.color === 'blue' ? '#1890ff' : credential.color === 'green' ? '#52c41a' : '#fa8c16'}`,
                    borderRadius: '6px'
                  }}
                  hoverable
                  onClick={() => fillCredentials(credential.username, credential.password)}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div style={{ flex: 1 }}>
                      <div style={{ marginBottom: '4px' }}>
                        <Text strong style={{ fontSize: '13px', color: '#262626' }}>
                          {credential.role}
                        </Text>
                      </div>
                      <div style={{ marginBottom: '6px' }}>
                        <Text style={{ fontSize: '11px', color: '#8c8c8c', lineHeight: '1.3' }}>
                          {credential.description}
                        </Text>
                      </div>
                      <div>
                        <Text code style={{ fontSize: '11px', marginRight: '8px' }}>
                          {credential.username}
                        </Text>
                        <Text code style={{ fontSize: '11px' }}>
                          {credential.password}
                        </Text>
                      </div>
                    </div>
                    <div style={{ marginLeft: '12px' }}>
                      <Button 
                        type="primary" 
                        size="small"
                        style={{
                          backgroundColor: credential.color === 'blue' ? '#1890ff' : credential.color === 'green' ? '#52c41a' : '#fa8c16',
                          borderColor: credential.color === 'blue' ? '#1890ff' : credential.color === 'green' ? '#52c41a' : '#fa8c16',
                          fontSize: '11px'
                        }}
                      >
                        Usar
                      </Button>
                    </div>
                  </div>
                </Card>
              ))}
            </Space>
          </Card>

          {/* Status */}
          <div style={{ 
            textAlign: 'center', 
            marginTop: 24,
            paddingTop: 16,
            borderTop: '1px solid #f0f0f0'
          }}>
            <Space size="small">
              <div style={{
                width: 8,
                height: 8,
                borderRadius: '50%',
                background: '#52c41a',
                display: 'inline-block',
                animation: 'pulse 2s infinite'
              }} />
              <Text style={{ fontSize: '12px', color: '#8c8c8c' }}>
                Sistema online e funcionando
              </Text>
            </Space>
            <div style={{ marginTop: 4 }}>
              <Text style={{ fontSize: '11px', color: '#bfbfbf' }}>
                Versão 2.0 - Powered by Ant Design
              </Text>
            </div>
          </div>
        </div>
      </Card>

      <style>{`
        @keyframes pulse {
          0% { opacity: 1; }
          50% { opacity: 0.5; }
          100% { opacity: 1; }
        }
      `}</style>
    </div>
  );
}

export default AntLogin;