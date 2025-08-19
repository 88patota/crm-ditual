import React from 'react';
import { clsx } from 'clsx';
import { AlertCircle } from 'lucide-react';

export interface ModernTextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  helperText?: string;
  resize?: 'none' | 'vertical' | 'horizontal' | 'both';
  variant?: 'default' | 'filled';
}

const ModernTextarea = React.forwardRef<HTMLTextAreaElement, ModernTextareaProps>(
  ({ 
    className, 
    label, 
    error, 
    helperText, 
    resize = 'vertical',
    variant = 'default',
    disabled,
    required,
    id, 
    ...props 
  }, ref) => {
    const inputId = id || label?.toLowerCase().replace(/\s+/g, '-');

    const resizeClasses = {
      none: 'resize-none',
      vertical: 'resize-y',
      horizontal: 'resize-x',
      both: 'resize'
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

        {/* Textarea Container */}
        <div className="relative">
          <textarea
            ref={ref}
            id={inputId}
            disabled={disabled}
            className={clsx(
              // Base styles
              'w-full border rounded-lg transition-all duration-200 ease-in-out',
              'placeholder-gray-400 focus:outline-none',
              'px-3 py-2 text-sm min-h-[80px]',
              
              // Resize
              resizeClasses[resize],
              
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
          />

          {/* Error Icon */}
          {error && (
            <div className="absolute right-3 top-3">
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

ModernTextarea.displayName = 'ModernTextarea';

export default ModernTextarea;