import { clsx } from 'clsx';
import type { LucideIcon } from 'lucide-react';
import { TrendingUp, TrendingDown } from 'lucide-react';

interface StripeMetricCardProps {
  title: string;
  value: string | number;
  description?: string;
  icon?: LucideIcon;
  trend?: {
    value: number;
    isPositive: boolean;
  };
  className?: string;
  variant?: 'default' | 'primary' | 'success' | 'warning' | 'error';
}

const variantStyles = {
  default: {
    bg: 'bg-white',
    iconBg: 'bg-gray-50',
    iconColor: 'text-gray-600',
    accent: 'border-l-gray-300'
  },
  primary: {
    bg: 'bg-white',
    iconBg: 'bg-purple-50',
    iconColor: 'text-purple-600',
    accent: 'border-l-purple-500'
  },
  success: {
    bg: 'bg-white',
    iconBg: 'bg-green-50',
    iconColor: 'text-green-600',
    accent: 'border-l-green-500'
  },
  warning: {
    bg: 'bg-white',
    iconBg: 'bg-orange-50',
    iconColor: 'text-orange-600',
    accent: 'border-l-orange-500'
  },
  error: {
    bg: 'bg-white',
    iconBg: 'bg-red-50',
    iconColor: 'text-red-600',
    accent: 'border-l-red-500'
  }
};

export default function StripeMetricCard({
  title,
  value,
  description,
  icon: Icon,
  trend,
  className,
  variant = 'default'
}: StripeMetricCardProps) {
  const styles = variantStyles[variant];
  
  return (
    <div className={clsx(
      'relative p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-all duration-300 hover:-translate-y-1',
      styles.bg,
      'border-l-4',
      styles.accent,
      className
    )}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center justify-between mb-2">
            <p className="text-sm font-medium text-gray-600 uppercase tracking-wide">{title}</p>
            {Icon && (
              <div className={clsx(
                'flex h-10 w-10 items-center justify-center rounded-xl',
                styles.iconBg
              )}>
                <Icon className={clsx('h-5 w-5', styles.iconColor)} />
              </div>
            )}
          </div>
          
          <p className="text-3xl font-bold text-gray-900 mb-2">{value}</p>
          
          {description && (
            <p className="text-sm text-gray-500 mb-3">{description}</p>
          )}
          
          {trend && (
            <div className="flex items-center">
              <div className={clsx(
                'flex items-center px-2 py-1 rounded-full text-xs font-medium',
                trend.isPositive 
                  ? 'bg-green-50 text-green-700' 
                  : 'bg-red-50 text-red-700'
              )}>
                {trend.isPositive ? (
                  <TrendingUp className="h-3 w-3 mr-1" />
                ) : (
                  <TrendingDown className="h-3 w-3 mr-1" />
                )}
                {trend.isPositive ? '+' : ''}{trend.value}%
              </div>
              <span className="text-xs text-gray-500 ml-2">vs last month</span>
            </div>
          )}
        </div>
      </div>

      {/* Subtle background pattern */}
      <div className="absolute top-0 right-0 w-32 h-32 opacity-5 overflow-hidden">
        <div className="absolute top-4 right-4 w-20 h-20 rounded-full bg-gradient-to-br from-purple-400 to-blue-400"></div>
        <div className="absolute top-8 right-8 w-12 h-12 rounded-full bg-gradient-to-br from-purple-300 to-blue-300"></div>
      </div>
    </div>
  );
}