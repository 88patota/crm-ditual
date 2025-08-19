import React from 'react';
import { clsx } from 'clsx';

interface StripeButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  children: React.ReactNode;
}

const StripeButton = React.forwardRef<HTMLButtonElement, StripeButtonProps>(
  ({ className, variant = 'primary', size = 'md', loading, children, disabled, ...props }, ref) => {
    const baseClasses = 'stripe-button';
    const variantClasses = {
      primary: 'stripe-button-primary',
      secondary: 'stripe-button-secondary',
      outline: 'stripe-button-secondary border-gray-300',
    };
    
    const sizeClasses = {
      sm: 'px-3 py-1.5 text-xs min-h-8',
      md: 'px-4 py-2.5 text-sm min-h-10',
      lg: 'px-6 py-3 text-base min-h-12',
    };

    return (
      <button
        className={clsx(
          baseClasses,
          variantClasses[variant],
          sizeClasses[size],
          {
            'opacity-50 cursor-not-allowed': disabled || loading,
          },
          className
        )}
        ref={ref}
        disabled={disabled || loading}
        {...props}
      >
        {loading && (
          <div className="stripe-loading mr-2" />
        )}
        {children}
      </button>
    );
  }
);

StripeButton.displayName = 'StripeButton';

export default StripeButton;