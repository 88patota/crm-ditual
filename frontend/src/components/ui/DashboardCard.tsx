import React from 'react';
import { Card } from 'antd';
import { clsx } from 'clsx';

interface BaseDashboardCardProps {
  className?: string;
  children: React.ReactNode;
  hoverable?: boolean;
  height?: number | string;
  title?: string;
}

export const BaseDashboardCard: React.FC<BaseDashboardCardProps> = ({
  className,
  children,
  hoverable = true,
  height,
  title,
  ...props
}) => {
  return (
    <Card
      className={clsx('dashboard-card', className)}
      hoverable={hoverable}
      style={{ height }}
      title={title}
      {...props}
    >
      {children}
    </Card>
  );
};

interface StatsCardProps {
  title: string;
  value: string | number;
  prefix?: React.ReactNode;
  suffix?: string;
  trend?: {
    value: number;
    isPositive: boolean;
  };
  description?: string;
  color?: string;
  className?: string;
}

export const StatsCard: React.FC<StatsCardProps> = ({
  title,
  value,
  prefix,
  suffix,
  trend,
  description,
  color = '#1890ff',
  className
}) => {
  return (
    <BaseDashboardCard className={clsx('stats-card', className)} height={140}>
      <div style={{ 
        textAlign: 'center', 
        height: '100%', 
        display: 'flex', 
        flexDirection: 'column', 
        justifyContent: 'space-between', 
        padding: '8px 0' 
      }}>
        {prefix && (
          <div style={{ marginBottom: '8px' }}>
            <div style={{ color, fontSize: '24px' }}>
              {prefix}
            </div>
          </div>
        )}
        <div style={{ 
          flex: 1, 
          display: 'flex', 
          flexDirection: 'column', 
          justifyContent: 'center' 
        }}>
          <div style={{ 
            fontSize: '11px', 
            color: '#8c8c8c', 
            marginBottom: '6px', 
            lineHeight: 1.2 
          }}>
            {title}
          </div>
          <div style={{ 
            color, 
            fontSize: '22px', 
            fontWeight: 'bold', 
            lineHeight: 1.4, 
            paddingBottom: '2px',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap'
          }}>
            {value}{suffix}
          </div>
        </div>
        {(trend || description) && (
          <div style={{ marginTop: '4px' }}>
            {trend && (
              <div style={{ 
                fontSize: '11px', 
                color: trend.isPositive ? '#52c41a' : '#ff4d4f',
                marginBottom: '2px' 
              }}>
                {trend.isPositive ? '+' : ''}{trend.value}%
              </div>
            )}
            {description && (
              <div style={{ 
                fontSize: '10px', 
                color: '#8c8c8c', 
                lineHeight: 1.2 
              }}>
                {description}
              </div>
            )}
          </div>
        )}
      </div>
    </BaseDashboardCard>
  );
};

interface StatusCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  color: string;
  description?: string;
  className?: string;
}

export const StatusCard: React.FC<StatusCardProps> = ({
  title,
  value,
  icon,
  color,
  description,
  className
}) => {
  return (
    <BaseDashboardCard className={clsx('status-card', className)} height={120}>
      <div style={{ 
        display: 'flex', 
        alignItems: 'center', 
        gap: 12, 
        height: '100%' 
      }}>
        <div style={{
          backgroundColor: `${color}15`,
          color: color,
          borderRadius: '8px',
          padding: '8px',
          fontSize: '18px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          minWidth: '36px',
          minHeight: '36px',
          flexShrink: 0
        }}>
          {icon}
        </div>
        <div style={{ flex: 1, minWidth: 0, overflow: 'hidden' }}>
          <div style={{ 
            fontSize: '11px', 
            color: '#8c8c8c', 
            marginBottom: '2px', 
            lineHeight: 1.2 
          }}>
            {title}
          </div>
          <div style={{
            margin: 0,
            color: color,
            fontSize: '16px',
            fontWeight: 'bold',
            lineHeight: 1.4,
            whiteSpace: 'nowrap',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            paddingBottom: '1px',
            minHeight: '20px',
            display: 'flex',
            alignItems: 'center'
          }}>
            {value}
          </div>
          {description && (
            <div style={{ 
              fontSize: '10px', 
              color: '#8c8c8c', 
              lineHeight: 1.2 
            }}>
              {description}
            </div>
          )}
        </div>
      </div>
    </BaseDashboardCard>
  );
};

interface ProgressCardProps {
  title: string;
  progress: number;
  status?: 'active' | 'success' | 'exception' | 'normal';
  description?: string;
  className?: string;
}

export const ProgressCard: React.FC<ProgressCardProps> = ({
  title,
  progress,
  status = 'active',
  description,
  className
}) => {
  const getProgressColor = () => {
    switch (status) {
      case 'success':
        return '#52c41a';
      case 'exception':
        return '#ff4d4f';
      case 'active':
        return '#1890ff';
      default:
        return '#1890ff';
    }
  };

  return (
    <BaseDashboardCard 
      className={clsx('progress-card', className)} 
      height={180}
      title={title}
    >
      <div style={{ 
        height: '100%', 
        display: 'flex', 
        flexDirection: 'column', 
        justifyContent: 'space-between' 
      }}>
        <div style={{ 
          width: '100%', 
          backgroundColor: '#f5f5f5', 
          borderRadius: '6px', 
          overflow: 'hidden',
          marginBottom: '16px'
        }}>
          <div
            style={{
              width: `${progress}%`,
              height: '8px',
              backgroundColor: getProgressColor(),
              borderRadius: '6px',
              transition: 'width 0.3s ease'
            }}
          />
        </div>
        
        <div style={{ textAlign: 'center', marginBottom: '8px' }}>
          <div style={{ 
            fontSize: '20px', 
            fontWeight: 'bold', 
            color: getProgressColor(),
            lineHeight: 1.4,
            paddingBottom: '2px'
          }}>
            {progress.toFixed(1)}%
          </div>
        </div>
        
        {description && (
          <div style={{ 
            fontSize: '12px', 
            color: '#8c8c8c', 
            textAlign: 'center',
            lineHeight: 1.2
          }}>
            {description}
          </div>
        )}
      </div>
    </BaseDashboardCard>
  );
};

interface InfoCardProps {
  title: string;
  items: Array<{
    label: string;
    value: string;
    color?: string;
  }>;
  className?: string;
}

export const InfoCard: React.FC<InfoCardProps> = ({
  title,
  items,
  className
}) => {
  return (
    <BaseDashboardCard 
      className={clsx('info-card', className)}
      title={title}
    >
      <div className="card-info-section">
        <div className="card-info-grid">
          {items.map((item, index) => (
            <div key={index} className="card-info-item">
              <div className="card-label">{item.label}</div>
              <div 
                className="card-value" 
                style={{ color: item.color || '#1890ff' }}
              >
                {item.value}
              </div>
            </div>
          ))}
        </div>
      </div>
    </BaseDashboardCard>
  );
};

export { BaseDashboardCard as DashboardCard };