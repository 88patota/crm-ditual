import React from 'react';
import { clsx } from 'clsx';
import { ChevronDown, AlertCircle } from 'lucide-react';

export interface ModernSelectProps extends Omit<React.SelectHTMLAttributes<HTMLSelectElement>, 'size'> {
  label?: string;
  error?: string;
  helperText?: string;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'default' | 'filled';
  placeholder?: string;
}

const ModernSelect = React.forwardRef<HTMLSelectElement, ModernSelectProps>(
  ({ 
    className, 
    label, 
    error, 
    helperText, 
    size = 'md', 
    variant = 'default',
    disabled,
    required,
    placeholder,
    children,
    id, 
    ...props 
  }, ref) => {
    const inputId = id || label?.toLowerCase().replace(/\s+/g, '-');

    const sizeClasses = {
      sm: 'h-8 text-sm',
      md: 'h-10 text-sm',
      lg: 'h-12 text-base'
    };

    return (
      <div className="w-full">
        {/* Label */}
        {label && (
          <label
            htmlFor={inputId}
            className={clsx(
              'block text-sm font-medium transition-colors duration-200 mb-2',
              error ? 'text-red-600' : 'text-gray-700',
              disabled && 'text-gray-400'
            )}
          >
            {label}
            {required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}

        {/* Select Container */}
        <div className="relative">
          <select
            ref={ref}
            id={inputId}
            disabled={disabled}
            className={clsx(
              // Base styles
              'w-full border rounded-lg transition-all duration-200 ease-in-out',
              'focus:outline-none appearance-none cursor-pointer',
              'pr-10 pl-3',
              
              // Size variants
              sizeClasses[size],
              
              // Variant styles
              variant === 'default' && [
                'bg-white border-gray-200',
                'hover:border-gray-300',
                !error && !disabled && 'focus:border-purple-500 focus:ring-1 focus:ring-purple-500/20',
              ],
              
              variant === 'filled' && [
                'bg-gray-50 border-gray-200',
                'hover:bg-white hover:border-gray-300',
                !error && !disabled && 'focus:bg-white focus:border-purple-500 focus:ring-1 focus:ring-purple-500/20',
              ],
              
              // Error state
              error && [
                'border-red-300 bg-red-50',
                'focus:border-red-500 focus:ring-1 focus:ring-red-500/20'
              ],
              
              // Disabled state
              disabled && [
                'bg-gray-50 border-gray-200 text-gray-400',
                'cursor-not-allowed'
              ],
              
              className
            )}
            {...props}
          >
            {placeholder && (
              <option value="" disabled>
                {placeholder}
              </option>
            )}
            {children}
          </select>

          {/* Chevron Icon */}
          <div className="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none">
            <ChevronDown className={clsx(
              'h-4 w-4 transition-colors',
              error ? 'text-red-400' : 'text-gray-400'
            )} />
          </div>

          {/* Error Icon */}
          {error && (
            <div className="absolute right-10 top-1/2 transform -translate-y-1/2">
              <AlertCircle className="h-4 w-4 text-red-500" />
            </div>
          )}
        </div>

        {/* Helper Text or Error */}
        {(error || helperText) && (
          <div className="mt-1.5">
            <p className={clsx(
              'text-xs',
              error ? 'text-red-600' : 'text-gray-500'
            )}>
              {error || helperText}
            </p>
          </div>
        )}
      </div>
    );
  }
);

ModernSelect.displayName = 'ModernSelect';

export default ModernSelect;