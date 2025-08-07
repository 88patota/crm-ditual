import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Form, Input, Button, Card, Typography, Space, Alert, Row, Col, Divider, Tag } from 'antd';
import { UserOutlined, LockOutlined, EyeInvisibleOutlined, EyeTwoTone } from '@ant-design/icons';
import { useAuth } from '../contexts/AuthContext';

const { Title, Text, Paragraph } = Typography;

interface LoginForm {
  username: string;
  password: string;
}

const AntLogin: React.FC = () => {
  const { login } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [form] = Form.useForm();

  const onFinish = async (values: LoginForm) => {
    try {
      setLoading(true);
      setError(null);
      await login({ username: values.username, password: values.password });
    } catch (error: any) {
      const errorDetail = error.response?.data?.detail;
      let errorMessage = 'Erro ao fazer login';
      
      if (typeof errorDetail === 'string') {
        errorMessage = errorDetail;
      } else if (Array.isArray(errorDetail)) {
        errorMessage = errorDetail.map(err => err.msg).join(', ');
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const demoCredentials = [
    {
      role: 'Administrator',
      description: 'Acesso completo ao sistema',
      username: 'admin',
      password: 'admin123',
      color: 'blue',
    },
    {
      role: 'Sales Representative',
      description: 'Acesso limitado',
      username: 'vendedor1',
      password: 'venda123456',
      color: 'green',
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
                    border: '1px solid #dee2e6'
                  }}
                  hoverable
                  onClick={() => fillCredentials(credential.username, credential.password)}
                >
                  <Row align="middle" justify="space-between">
                    <Col>
                      <Space direction="vertical" size={0}>
                        <Space size="small">
                          <Text strong style={{ fontSize: '14px' }}>
                            {credential.role}
                          </Text>
                          <Tag color={credential.color} style={{ fontSize: '10px', margin: 0 }}>
                            {credential.description}
                          </Tag>
                        </Space>
                        <Space size="small">
                          <Text code style={{ fontSize: '11px' }}>
                            {credential.username}
                          </Text>
                          <Text code style={{ fontSize: '11px' }}>
                            {credential.password}
                          </Text>
                        </Space>
                      </Space>
                    </Col>
                    <Col>
                      <Button size="small" type="link">
                        Usar
                      </Button>
                    </Col>
                  </Row>
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
};

export default AntLogin;