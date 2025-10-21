import { useState, useEffect } from 'react';
import { Form, Input, Button, Card, Typography, Space, Alert } from 'antd';
import { UserOutlined, LockOutlined, EyeInvisibleOutlined, EyeTwoTone } from '@ant-design/icons';
import { useAuth } from '../hooks/useAuth';
import { useNavigate } from 'react-router-dom';

const { Text } = Typography;

interface LoginForm {
  username: string;
  password: string;
}

function AntLogin() {
  const { login, isAuthenticated, user } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [form] = Form.useForm();

  // Redirecionar quando o usuário estiver autenticado e carregado
  useEffect(() => {
    if (isAuthenticated && user) {
      navigate('/dashboard');
    }
  }, [isAuthenticated, user, navigate]);

  const onFinish = async (values: LoginForm) => {
    try {
      setLoading(true);
      setError(null);
      await login({ username: values.username, password: values.password });
      // O redirecionamento será feito automaticamente pelo useEffect quando o usuário for carregado
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

  return (
    <div className="login-container">
      <Card className="login-card" bordered={false}>
        <div className="login-header">
          <div className="text-center mb-10">
            <div className="flex items-center justify-center mb-6">
              <div>
                <div style={{
                  fontSize: '3.2rem',
                  fontFamily: '"Inter", "SF Pro Display", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                  fontWeight: '700',
                  color: '#e11d48',
                  lineHeight: '1.1',
                  letterSpacing: '-0.02em',
                  marginBottom: '12px'
                }}>
                  LoenCRM
                </div>
                <div style={{
                  fontSize: '1rem',
                  fontFamily: '"Inter", sans-serif',
                  fontWeight: '500',
                  color: '#374151',
                  letterSpacing: '0.05em',
                  textAlign: 'center'
                }}>
                  Conecte. Entenda. Cresça.
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="login-form">
          {error && (
            <Alert
              message="Erro de Login"
              description={error}
              type="error"
              showIcon
              style={{ 
                marginBottom: 24,
                backgroundColor: '#fef2f2',
                border: '1px solid #fecaca',
                borderRadius: '8px'
              }}
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
              label={<span style={{ color: '#374151', fontWeight: 500 }}>Usuário</span>}
              rules={[{ required: true, message: 'Por favor, digite seu usuário!' }]}
            >
              <Input 
                prefix={<UserOutlined style={{ color: '#9ca3af' }} />} 
                placeholder="Digite seu usuário"
                style={{
                  borderRadius: '8px',
                  border: '1px solid #d1d5db',
                  padding: '8px 12px'
                }}
              />
            </Form.Item>

            <Form.Item
              name="password"
              label={<span style={{ color: '#374151', fontWeight: 500 }}>Senha</span>}
              rules={[{ required: true, message: 'Por favor, digite sua senha!' }]}
            >
              <Input.Password
                prefix={<LockOutlined style={{ color: '#9ca3af' }} />}
                placeholder="Digite sua senha"
                style={{
                  borderRadius: '8px',
                  border: '1px solid #d1d5db',
                  padding: '8px 12px'
                }}
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
                  background: '#e11d48',
                  borderColor: '#e11d48',
                  borderRadius: '8px',
                  fontSize: '16px',
                  fontWeight: 500,
                  boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)'
                }}
              >
                Entrar
              </Button>
            </Form.Item>
          </Form>

          {/* Status */}
          <div style={{ 
            textAlign: 'center', 
            marginTop: 24,
            paddingTop: 16,
            borderTop: '1px solid #f1f5f9'
          }}>
            <Space size="small">
              <div style={{
                width: 8,
                height: 8,
                borderRadius: '50%',
                background: '#10b981',
                display: 'inline-block',
                animation: 'pulse 2s infinite'
              }} />
              <Text style={{ fontSize: '12px', color: '#64748b' }}>
                Sistema online e funcionando
              </Text>
            </Space>
            <div style={{ marginTop: 4 }}>
              <Text style={{ fontSize: '11px', color: '#94a3b8' }}>
                LoenCRM - Acesso seguro com autenticação JWT
              </Text>
            </div>
          </div>
        </div>
      </Card>

      <style>{`
        .login-container {
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          background: #f8fafc;
          padding: 20px;
        }
        
        .login-card {
          width: 100%;
          max-width: 420px;
          border-radius: 16px;
          box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
          overflow: hidden;
          border: 1px solid #e2e8f0;
        }
        
        .login-header {
          background: #ffffff;
          padding: 32px 24px;
          text-align: center;
          margin: -1px -1px 0 -1px;
          border-bottom: 1px solid #f1f5f9;
        }
        
        .login-form {
          padding: 32px 24px;
          background: #ffffff;
        }
        
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