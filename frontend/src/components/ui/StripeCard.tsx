import React from 'react';
import { clsx } from 'clsx';

interface StripeCardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  padding?: 'none' | 'sm' | 'md' | 'lg';
}

export function StripeCard({ children, className, padding = 'md', ...props }: StripeCardProps) {
  const paddingClasses = {
    none: '',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  };

  return (
    <div 
      className={clsx('stripe-card', paddingClasses[padding], className)} 
      {...props}
    >
      {children}
    </div>
  );
}

interface StripeCardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

export function StripeCardHeader({ children, className, ...props }: StripeCardHeaderProps) {
  return (
    <div className={clsx('border-b border-gray-100 pb-4 mb-6', className)} {...props}>
      {children}
    </div>
  );
}

interface StripeCardTitleProps extends React.HTMLAttributes<HTMLHeadingElement> {
  children: React.ReactNode;
}

export function StripeCardTitle({ children, className, ...props }: StripeCardTitleProps) {
  return (
    <h3 className={clsx('text-lg font-semibold text-gray-900', className)} {...props}>
      {children}
    </h3>
  );
}

interface StripeCardDescriptionProps extends React.HTMLAttributes<HTMLParagraphElement> {
  children: React.ReactNode;
}

export function StripeCardDescription({ children, className, ...props }: StripeCardDescriptionProps) {
  return (
    <p className={clsx('text-sm text-gray-600 mt-1', className)} {...props}>
      {children}
    </p>
  );
}

interface StripeCardContentProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

export function StripeCardContent({ children, className, ...props }: StripeCardContentProps) {
  return (
    <div className={clsx(className)} {...props}>
      {children}
    </div>
  );
}

export default StripeCard;