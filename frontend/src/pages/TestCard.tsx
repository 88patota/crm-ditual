import React from 'react';
import { Row, Col } from 'antd';
import { DollarOutlined } from '@ant-design/icons';
import { StatsCard } from '../components/ui/DashboardCard';
import '../styles/DashboardCard.css';

const TestCard: React.FC = () => {
  return (
    <div style={{ padding: '24px' }}>
      <h2>Teste Individual de Component</h2>
      <Row gutter={[16, 16]}>
        <Col span={6}>
          <StatsCard
            title="Vendas Hoje"
            value="R$ 12.450"
            prefix={<DollarOutlined />}
            color="#52c41a"
            trend={{ value: 15, isPositive: true }}
            description="vs ontem"
          />
        </Col>
      </Row>
    </div>
  );
};

export default TestCard;