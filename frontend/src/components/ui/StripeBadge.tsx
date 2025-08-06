import React from 'react';
import { clsx } from 'clsx';

interface StripeBadgeProps {
  children: React.ReactNode;
  variant?: 'primary' | 'success' | 'warning' | 'error' | 'neutral';
  size?: 'sm' | 'md';
  className?: string;
}

export default function StripeBadge({ 
  children, 
  variant = 'neutral', 
  size = 'md',
  className 
}: StripeBadgeProps) {
  const baseClasses = 'stripe-badge';
  
  const variantClasses = {
    primary: 'stripe-badge-primary',
    success: 'stripe-badge-success',
    warning: 'stripe-badge-warning',
    error: 'stripe-badge-error',
    neutral: 'bg-gray-100 text-gray-700',
  };

  const sizeClasses = {
    sm: 'text-xs px-2 py-1',
    md: 'text-xs px-2.5 py-1.5',
  };

  return (
    <span 
      className={clsx(
        baseClasses,
        variantClasses[variant],
        sizeClasses[size],
        className
      )}
    >
      {children}
    </span>
  );
}