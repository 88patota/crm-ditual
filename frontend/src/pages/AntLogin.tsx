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

  return (
    <div className="login-container">
      <Card className="login-card" bordered={false}>
        <div className="login-header">
          <div className="login-logo">C</div>
          <Title level={2} style={{ color: 'white', margin: 0 }}>
            Bem-vindo de volta
          </Title>
          <Paragraph style={{ color: 'rgba(255, 255, 255, 0.8)', margin: '8px 0 0 0' }}>
            Acesse o sistema com suas credencias
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
                Sistema CRM - Acesso seguro com autenticação JWT
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
          background: linear-gradient(135deg, #f5f7fa 0%, #e4edf9 100%);
          padding: 20px;
        }
        
        .login-card {
          width: 100%;
          max-width: 420px;
          border-radius: 16px;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
          overflow: hidden;
        }
        
        .login-header {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          padding: 32px 24px;
          text-align: center;
          margin: -1px -1px 0 -1px;
        }
        
        .login-logo {
          width: 60px;
          height: 60px;
          border-radius: 16px;
          background: rgba(255, 255, 255, 0.2);
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 24px;
          font-weight: bold;
          color: white;
          margin: 0 auto 20px;
          backdrop-filter: blur(10px);
        }
        
        .login-form {
          padding: 32px 24px;
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