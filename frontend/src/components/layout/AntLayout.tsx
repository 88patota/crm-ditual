import React, { useState } from 'react';
import { Layout, Menu, Avatar, Dropdown, Typography, Space, Button, Badge } from 'antd';
import { useLocation, Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import {
  DashboardOutlined,
  UserOutlined,
  TeamOutlined,
  LogoutOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  BellOutlined,
  SettingOutlined,
  FileTextOutlined,
} from '@ant-design/icons';
import type { MenuProps } from 'antd';

const { Header, Sider, Content } = Layout;
const { Title, Text } = Typography;

interface AntLayoutProps {
  children: React.ReactNode;
}

const AntLayout: React.FC<AntLayoutProps> = ({ children }) => {
  const { user, logout } = useAuth();
  const location = useLocation();
  const [collapsed, setCollapsed] = useState(false);

  const navigationItems = [
    {
      key: '/dashboard',
      icon: <DashboardOutlined />,
      label: <Link to="/dashboard">Dashboard</Link>,
    },
    {
      key: '/budgets',
      icon: <FileTextOutlined />,
      label: <Link to="/budgets">Orçamentos</Link>,
    },
    {
      key: '/profile',
      icon: <UserOutlined />,
      label: <Link to="/profile">Perfil</Link>,
    },
  ];

  // Add admin-only navigation
  if (user?.role === 'admin') {
    navigationItems.splice(-1, 0, {
      key: '/users',
      icon: <TeamOutlined />,
      label: <Link to="/users">Usuários</Link>,
    });
  }

  const userMenuItems: MenuProps['items'] = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: <Link to="/profile">Meu Perfil</Link>,
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: 'Configurações',
    },
    {
      type: 'divider',
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: 'Sair',
      onClick: logout,
    },
  ];

  const getCurrentPageTitle = () => {
    const currentItem = navigationItems.find(item => item.key === location.pathname);
    if (currentItem) {
      // Extract text from Link component
      return React.isValidElement(currentItem.label) && currentItem.label.props.children || 'Dashboard';
    }
    return 'Dashboard';
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider 
        trigger={null} 
        collapsible 
        collapsed={collapsed}
        style={{
          background: '#fff',
          boxShadow: '2px 0 8px 0 rgba(29, 35, 41, 0.05)',
        }}
        width={256}
      >
        <div style={{ 
          padding: collapsed ? '16px 8px' : '16px 24px', 
          borderBottom: '1px solid #f0f0f0',
          textAlign: 'center'
        }}>
          {!collapsed ? (
            <Space direction="vertical" size={4}>
              <div style={{
                width: 40,
                height: 40,
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white',
                fontSize: '18px',
                fontWeight: 'bold',
                margin: '0 auto'
              }}>
                C
              </div>
              <div>
                <Title level={5} style={{ margin: 0, color: '#262626' }}>
                  CRM Ditual
                </Title>
                <Text type="secondary" style={{ fontSize: '12px' }}>
                  Business Suite
                </Text>
              </div>
            </Space>
          ) : (
            <div style={{
              width: 32,
              height: 32,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              fontSize: '16px',
              fontWeight: 'bold',
              margin: '0 auto'
            }}>
              C
            </div>
          )}
        </div>

        <Menu
          mode="inline"
          selectedKeys={[location.pathname]}
          items={navigationItems}
          style={{ 
            border: 'none',
            marginTop: '16px'
          }}
        />

        {/* User info at bottom */}
        {!collapsed && (
          <div style={{
            position: 'absolute',
            bottom: 0,
            left: 0,
            right: 0,
            padding: '16px 24px',
            borderTop: '1px solid #f0f0f0',
            background: '#fafafa'
          }}>
            <Space>
              <Avatar 
                style={{ 
                  backgroundColor: '#1890ff',
                  fontSize: '14px'
                }}
                size="small"
              >
                {user?.full_name?.charAt(0).toUpperCase()}
              </Avatar>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ 
                  fontSize: '14px', 
                  fontWeight: 500,
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis'
                }}>
                  {user?.full_name}
                </div>
                <div style={{ 
                  fontSize: '12px', 
                  color: '#8c8c8c',
                  textTransform: 'capitalize'
                }}>
                  {user?.role}
                </div>
              </div>
            </Space>
          </div>
        )}
      </Sider>

      <Layout>
        <Header style={{ 
          padding: '0 24px', 
          background: '#fff',
          borderBottom: '1px solid #f0f0f0',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          height: '64px',
          lineHeight: '64px'
        }}>
          <Space size="middle" align="center">
            <Button
              type="text"
              icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
              onClick={() => setCollapsed(!collapsed)}
              style={{
                fontSize: '16px',
                width: 40,
                height: 40,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            />
            <Title level={4} style={{ margin: 0, color: '#262626', lineHeight: 1 }}>
              {getCurrentPageTitle()}
            </Title>
          </Space>

          <Space size="large" align="center">
            <Badge count={3} size="small" offset={[-2, 2]}>
              <Button 
                type="text" 
                icon={<BellOutlined />} 
                style={{
                  fontSize: '16px',
                  width: 40,
                  height: 40,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  borderRadius: '6px'
                }}
              />
            </Badge>
            
            <Dropdown 
              menu={{ items: userMenuItems }}
              trigger={['click']}
              placement="bottomRight"
              arrow={{ pointAtCenter: true }}
            >
              <div 
                style={{ 
                  cursor: 'pointer',
                  padding: '6px 12px',
                  borderRadius: '8px',
                  transition: 'all 0.2s ease',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '12px',
                  background: 'transparent'
                }}
                className="user-dropdown-trigger"
              >
                <Avatar 
                  style={{ 
                    backgroundColor: '#1890ff',
                    flexShrink: 0
                  }}
                  size={32}
                >
                  {user?.full_name?.charAt(0).toUpperCase()}
                </Avatar>
                <div style={{ 
                  textAlign: 'left',
                  lineHeight: 1.2,
                  minWidth: 0,
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'center'
                }}>
                  <div style={{ 
                    fontSize: '14px', 
                    fontWeight: 500,
                    color: '#262626',
                    whiteSpace: 'nowrap',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    maxWidth: '120px'
                  }}>
                    {user?.full_name}
                  </div>
                  <div style={{ 
                    fontSize: '12px', 
                    color: '#8c8c8c', 
                    textTransform: 'capitalize',
                    marginTop: '2px'
                  }}>
                    {user?.role === 'admin' ? 'Administrador' : 'Vendas'}
                  </div>
                </div>
              </div>
            </Dropdown>
          </Space>
        </Header>

        <Content style={{ 
          margin: '24px',
          minHeight: 'calc(100vh - 112px)'
        }}>
          {children}
        </Content>
      </Layout>
    </Layout>
  );
};

export default AntLayout;