import React from 'react';
import { clsx } from 'clsx';
import { Check, Minus } from 'lucide-react';

export interface ModernCheckboxProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'> {
  label?: string;
  description?: string;
  error?: string;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'default' | 'card';
  indeterminate?: boolean;
}

const ModernCheckbox = React.forwardRef<HTMLInputElement, ModernCheckboxProps>(
  ({ 
    className, 
    label, 
    description,
    error, 
    size = 'md', 
    variant = 'default',
    disabled,
    checked,
    indeterminate = false,
    id, 
    ...props 
  }, ref) => {
    const inputId = id || label?.toLowerCase().replace(/\s+/g, '-');

    const sizeClasses = {
      sm: 'h-4 w-4',
      md: 'h-5 w-5',
      lg: 'h-6 w-6'
    };

    const iconSizeClasses = {
      sm: 'h-3 w-3',
      md: 'h-3.5 w-3.5',
      lg: 'h-4 w-4'
    };

    if (variant === 'card') {
      return (
        <label
          htmlFor={inputId}
          className={clsx(
            'relative flex p-4 border rounded-lg cursor-pointer transition-all duration-200',
            checked 
              ? 'border-purple-200 bg-purple-50 ring-1 ring-purple-200' 
              : 'border-gray-200 bg-white hover:border-gray-300',
            disabled && 'opacity-50 cursor-not-allowed',
            error && 'border-red-300 bg-red-50',
            className
          )}
        >
          <div className="flex items-start">
            <div className="relative flex items-center">
              <input
                ref={ref}
                id={inputId}
                type="checkbox"
                disabled={disabled}
                checked={checked}
                className="sr-only"
                {...props}
              />
              <div
                className={clsx(
                  'flex items-center justify-center border rounded transition-all duration-200',
                  sizeClasses[size],
                  checked || indeterminate
                    ? 'bg-purple-600 border-purple-600'
                    : 'bg-white border-gray-300',
                  !disabled && 'hover:border-purple-400',
                  disabled && 'opacity-50'
                )}
              >
                {checked && (
                  <Check className={clsx('text-white', iconSizeClasses[size])} />
                )}
                {indeterminate && !checked && (
                  <Minus className={clsx('text-white', iconSizeClasses[size])} />
                )}
              </div>
            </div>
            {(label || description) && (
              <div className="ml-3 flex-1">
                {label && (
                  <p className={clsx(
                    'font-medium text-gray-900',
                    size === 'sm' && 'text-sm',
                    size === 'md' && 'text-sm',
                    size === 'lg' && 'text-base'
                  )}>
                    {label}
                  </p>
                )}
                {description && (
                  <p className="text-sm text-gray-500 mt-1">{description}</p>
                )}
              </div>
            )}
          </div>
        </label>
      );
    }

    return (
      <div className="flex items-start">
        <div className="relative flex items-center">
          <input
            ref={ref}
            id={inputId}
            type="checkbox"
            disabled={disabled}
            checked={checked}
            className="sr-only"
            {...props}
          />
          <label
            htmlFor={inputId}
            className={clsx(
              'flex items-center justify-center border rounded cursor-pointer transition-all duration-200',
              sizeClasses[size],
              checked || indeterminate
                ? 'bg-purple-600 border-purple-600'
                : 'bg-white border-gray-300',
              !disabled && 'hover:border-purple-400',
              disabled && 'opacity-50 cursor-not-allowed',
              error && 'border-red-500',
              className
            )}
          >
            {checked && (
              <Check className={clsx('text-white', iconSizeClasses[size])} />
            )}
            {indeterminate && !checked && (
              <Minus className={clsx('text-white', iconSizeClasses[size])} />
            )}
          </label>
        </div>
        
        {(label || description) && (
          <div className="ml-2 flex-1">
            {label && (
              <label
                htmlFor={inputId}
                className={clsx(
                  'block font-medium cursor-pointer',
                  size === 'sm' && 'text-sm',
                  size === 'md' && 'text-sm',
                  size === 'lg' && 'text-base',
                  error ? 'text-red-600' : 'text-gray-900',
                  disabled && 'text-gray-400 cursor-not-allowed'
                )}
              >
                {label}
              </label>
            )}
            {description && (
              <p className="text-sm text-gray-500 mt-0.5">{description}</p>
            )}
          </div>
        )}
        
        {error && (
          <p className="text-xs text-red-600 mt-1">{error}</p>
        )}
      </div>
    );
  }
);

ModernCheckbox.displayName = 'ModernCheckbox';

export default ModernCheckbox;