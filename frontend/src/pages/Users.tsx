import { useState } from 'react';
import { 
  Card, 
  Row, 
  Col, 
  Statistic, 
  Typography, 
  Space, 
  List, 
  Avatar, 
  Tag, 
  Button,
  Modal,
  Form,
  Input,
  Select,
  Switch,
  App,
  Popconfirm,
  Badge,
  Divider,
  Tooltip
} from 'antd';
import { 
  UserOutlined, 
  TeamOutlined, 
  UserAddOutlined, 
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  FilterOutlined,
  UserSwitchOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  MoreOutlined
} from '@ant-design/icons';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { authService } from '../services/authService';
import type { RegisterRequest, User } from '../types/auth';

const { Title, Text } = Typography;
const { Option } = Select;

export default function Users() {
  const queryClient = useQueryClient();
  const { message } = App.useApp();

  const getErrorMessage = (error: unknown): string => {
    if (typeof error === 'object' && error !== null && 'response' in error) {
      const axiosError = error as { response?: { data?: { detail?: string } } };
      if (axiosError.response?.data?.detail) {
        return axiosError.response.data.detail;
      }
    }
    return 'Ocorreu um erro inesperado. Tente novamente.';
  };
  const [searchText, setSearchText] = useState('');
  const [isCreateModalVisible, setIsCreateModalVisible] = useState(false);
  const [isEditModalVisible, setIsEditModalVisible] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [createForm] = Form.useForm();
  const [editForm] = Form.useForm();

  const { data: users = [], isLoading } = useQuery({
    queryKey: ['users'],
    queryFn: authService.getAllUsers,
  });

  const createUserMutation = useMutation({
    mutationFn: authService.createUser,
    onSuccess: () => {
      message.success('Usuário criado com sucesso!');
      queryClient.invalidateQueries({ queryKey: ['users'] });
      setIsCreateModalVisible(false);
      createForm.resetFields();
    },
    onError: (error: unknown) => {
      message.error(getErrorMessage(error));
    },
  });

  const updateUserMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<User> }) =>
      authService.updateUser(id, data),
    onSuccess: () => {
      message.success('Usuário atualizado com sucesso!');
      queryClient.invalidateQueries({ queryKey: ['users'] });
      setIsEditModalVisible(false);
      setEditingUser(null);
    },
    onError: (error: unknown) => {
      message.error(getErrorMessage(error));
    },
  });

  const deleteUserMutation = useMutation({
    mutationFn: authService.deleteUser,
    onSuccess: () => {
      message.success('Usuário deletado com sucesso!');
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
    onError: (error: unknown) => {
      message.error(getErrorMessage(error));
    },
  });

  const stats = [
    {
      title: 'Total de Usuários',
      value: users.length,
      prefix: <UserOutlined className="stats-icon users" />,
      color: '#1890ff',
      bgColor: '#e6f7ff',
    },
    {
      title: 'Usuários Ativos',
      value: users.filter(u => u.is_active).length,
      prefix: <TeamOutlined className="stats-icon active" />,
      color: '#52c41a',
      bgColor: '#f6ffed',
    },
    {
      title: 'Administradores',
      value: users.filter(u => u.role === 'admin').length,
      prefix: <UserSwitchOutlined className="stats-icon admin" />,
      color: '#fa541c',
      bgColor: '#fff2e8',
    },
    {
      title: 'Equipe de Vendas',
      value: users.filter(u => u.role === 'vendas').length,
      prefix: <UserAddOutlined className="stats-icon sales" />,
      color: '#722ed1',
      bgColor: '#f9f0ff',
    },
  ];

  const filteredUsers = users.filter(user =>
    user.full_name.toLowerCase().includes(searchText.toLowerCase()) ||
    user.email.toLowerCase().includes(searchText.toLowerCase()) ||
    user.username.toLowerCase().includes(searchText.toLowerCase())
  );

  const getRoleColor = (role: string) => {
    switch (role) {
      case 'admin':
        return 'red';
      case 'vendas':
        return 'blue';
      default:
        return 'green';
    }
  };

  const getRoleText = (role: string) => {
    switch (role) {
      case 'admin':
        return 'Administrador';
      case 'vendas':
        return 'Vendas';
      default:
        return 'Usuário';
    }
  };

  const handleCreateUser = (values: RegisterRequest) => {
    createUserMutation.mutate(values);
  };

  const handleEditUser = (values: Partial<User>) => {
    if (editingUser) {
      updateUserMutation.mutate({ id: editingUser.id, data: values });
    }
  };

  const handleDeleteUser = (userId: number) => {
    deleteUserMutation.mutate(userId);
  };

  const handleEditClick = (user: User) => {
    setEditingUser(user);
    editForm.setFieldsValue({
      full_name: user.full_name,
      email: user.email,
      username: user.username,
      role: user.role,
      is_active: user.is_active,
    });
    setIsEditModalVisible(true);
  };

  const toggleUserStatus = (user: User) => {
    updateUserMutation.mutate({
      id: user.id,
      data: { is_active: !user.is_active },
    });
  };

  return (
    <Space direction="vertical" size="large" style={{ width: '100%' }}>
      {/* Header */}
      <div className="users-header">
        <Row justify="space-between" align="middle">
          <Col>
            <Space direction="vertical" size={4}>
              <Title level={2} style={{ margin: 0 }}>
                Gerenciar Usuários 👥
              </Title>
              <Text style={{ fontSize: '16px', color: '#8c8c8c' }}>
                Gerencie todos os usuários do sistema, suas permissões e status.
              </Text>
            </Space>
          </Col>
          <Col>
            <Space>
              <Button icon={<FilterOutlined />}>
                Filtros
              </Button>
              <Button 
                type="primary" 
                icon={<PlusOutlined />}
                onClick={() => setIsCreateModalVisible(true)}
              >
                Novo Usuário
              </Button>
            </Space>
          </Col>
        </Row>
      </div>

      {/* Stats Cards */}
      <Row gutter={[16, 16]}>
        {stats.map((stat, index) => (
          <Col xs={24} sm={12} lg={6} key={index}>
            <Card className="stats-card" hoverable>
              <Statistic
                title={stat.title}
                value={stat.value}
                prefix={
                  <div 
                    style={{ 
                      backgroundColor: stat.bgColor,
                      color: stat.color,
                      borderRadius: '8px',
                      padding: '8px',
                      display: 'inline-block',
                      marginRight: '12px'
                    }}
                  >
                    {stat.prefix}
                  </div>
                }
                valueStyle={{ fontSize: '24px', fontWeight: 'bold', color: stat.color }}
              />
            </Card>
          </Col>
        ))}
      </Row>

      {/* Search and Users List */}
      <Row gutter={[16, 16]}>
        <Col span={24}>
          <Card 
            title={
              <Space>
                <TeamOutlined />
                <span>Lista de Usuários ({filteredUsers.length})</span>
              </Space>
            }
            extra={
              <Space>
                <Input.Search
                  placeholder="Buscar usuários..."
                  allowClear
                  style={{ width: 300 }}
                  onSearch={setSearchText}
                  onChange={(e) => setSearchText(e.target.value)}
                />
                <Button type="link" icon={<MoreOutlined />} />
              </Space>
            }
            loading={isLoading}
          >
            <List
              itemLayout="horizontal"
              dataSource={filteredUsers}
              pagination={{
                pageSize: 10,
                showSizeChanger: true,
                showQuickJumper: true,
                showTotal: (total, range) => 
                  `${range[0]}-${range[1]} de ${total} usuários`,
              }}
              renderItem={(user) => (
                <List.Item
                  actions={[
                    <Tooltip title={user.is_active ? 'Desativar' : 'Ativar'}>
                      <Button
                        type="text"
                        icon={user.is_active ? <CloseCircleOutlined /> : <CheckCircleOutlined />}
                        onClick={() => toggleUserStatus(user)}
                        style={{ 
                          color: user.is_active ? '#ff4d4f' : '#52c41a'
                        }}
                      />
                    </Tooltip>,
                    <Tooltip title="Editar">
                      <Button
                        type="text"
                        icon={<EditOutlined />}
                        onClick={() => handleEditClick(user)}
                      />
                    </Tooltip>,
                    <Popconfirm
                      title="Deletar usuário"
                      description={`Tem certeza que deseja deletar ${user.full_name}?`}
                      onConfirm={() => handleDeleteUser(user.id)}
                      okText="Sim"
                      cancelText="Não"
                    >
                      <Tooltip title="Deletar">
                        <Button
                          type="text"
                          danger
                          icon={<DeleteOutlined />}
                        />
                      </Tooltip>
                    </Popconfirm>,
                  ]}
                >
                  <List.Item.Meta
                    avatar={
                      <Avatar 
                        size={48}
                        style={{ 
                          backgroundColor: getRoleColor(user.role) === 'red' ? '#ff4d4f' : 
                                           getRoleColor(user.role) === 'blue' ? '#1890ff' : '#52c41a',
                          fontSize: '18px',
                          fontWeight: 'bold'
                        }}
                      >
                        {user.full_name.charAt(0).toUpperCase()}
                      </Avatar>
                    }
                    title={
                      <Space>
                        <Text strong style={{ fontSize: '16px' }}>
                          {user.full_name}
                        </Text>
                        <Tag color={getRoleColor(user.role)}>
                          {getRoleText(user.role)}
                        </Tag>
                        <Badge 
                          status={user.is_active ? "success" : "default"} 
                          text={user.is_active ? "Ativo" : "Inativo"}
                        />
                      </Space>
                    }
                    description={
                      <Space direction="vertical" size={4}>
                        <Text type="secondary">
                          ✉️ {user.email}
                        </Text>
                        <Text type="secondary">
                          👤 @{user.username}
                        </Text>
                        <Text type="secondary" style={{ fontSize: '12px' }}>
                          📅 Criado em {new Date(user.created_at).toLocaleDateString('pt-BR')}
                        </Text>
                      </Space>
                    }
                  />
                </List.Item>
              )}
            />
          </Card>
        </Col>
      </Row>

      {/* Create User Modal */}
      <Modal
        title={
          <Space>
            <UserAddOutlined />
            <span>Criar Novo Usuário</span>
          </Space>
        }
        open={isCreateModalVisible}
        onCancel={() => setIsCreateModalVisible(false)}
        footer={null}
        width={600}
      >
        <Divider />
        <Form
          form={createForm}
          layout="vertical"
          onFinish={handleCreateUser}
          requiredMark={false}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                label="Nome Completo"
                name="full_name"
                rules={[{ required: true, message: 'Nome completo é obrigatório' }]}
              >
                <Input placeholder="Digite o nome completo" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label="Email"
                name="email"
                rules={[
                  { required: true, message: 'Email é obrigatório' },
                  { type: 'email', message: 'Email inválido' }
                ]}
              >
                <Input placeholder="Digite o email" />
              </Form.Item>
            </Col>
          </Row>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                label="Username"
                name="username"
                rules={[{ required: true, message: 'Username é obrigatório' }]}
              >
                <Input placeholder="Digite o username" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label="Função"
                name="role"
                rules={[{ required: true, message: 'Função é obrigatória' }]}
              >
                <Select placeholder="Selecione uma função">
                  <Option value="vendas">Vendas</Option>
                  <Option value="admin">Administrador</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            label="Senha"
            name="password"
            rules={[
              { required: true, message: 'Senha é obrigatória' },
              { min: 8, message: 'Senha deve ter pelo menos 8 caracteres' }
            ]}
          >
            <Input.Password placeholder="Digite a senha" />
          </Form.Item>

          <Divider />
          
          <Space style={{ width: '100%', justifyContent: 'flex-end' }}>
            <Button onClick={() => setIsCreateModalVisible(false)}>
              Cancelar
            </Button>
            <Button 
              type="primary" 
              htmlType="submit"
              loading={createUserMutation.isPending}
            >
              Criar Usuário
            </Button>
          </Space>
        </Form>
      </Modal>

      {/* Edit User Modal */}
      <Modal
        title={
          <Space>
            <EditOutlined />
            <span>Editar Usuário</span>
          </Space>
        }
        open={isEditModalVisible}
        onCancel={() => setIsEditModalVisible(false)}
        footer={null}
        width={600}
      >
        <Divider />
        <Form
          form={editForm}
          layout="vertical"
          onFinish={handleEditUser}
          requiredMark={false}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                label="Nome Completo"
                name="full_name"
                rules={[{ required: true, message: 'Nome completo é obrigatório' }]}
              >
                <Input placeholder="Digite o nome completo" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label="Email"
                name="email"
                rules={[
                  { required: true, message: 'Email é obrigatório' },
                  { type: 'email', message: 'Email inválido' }
                ]}
              >
                <Input placeholder="Digite o email" />
              </Form.Item>
            </Col>
          </Row>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                label="Username"
                name="username"
                rules={[{ required: true, message: 'Username é obrigatório' }]}
              >
                <Input placeholder="Digite o username" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label="Função"
                name="role"
                rules={[{ required: true, message: 'Função é obrigatória' }]}
              >
                <Select placeholder="Selecione uma função">
                  <Option value="vendas">Vendas</Option>
                  <Option value="admin">Administrador</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            label="Status do Usuário"
            name="is_active"
            valuePropName="checked"
          >
            <Switch 
              checkedChildren="Ativo" 
              unCheckedChildren="Inativo"
            />
          </Form.Item>

          <Divider />
          
          <Space style={{ width: '100%', justifyContent: 'flex-end' }}>
            <Button onClick={() => setIsEditModalVisible(false)}>
              Cancelar
            </Button>
            <Button 
              type="primary" 
              htmlType="submit"
              loading={updateUserMutation.isPending}
            >
              Salvar Alterações
            </Button>
          </Space>
        </Form>
      </Modal>
    </Space>
  );
}