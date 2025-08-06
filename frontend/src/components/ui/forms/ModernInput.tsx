import React, { useState } from 'react';
import { clsx } from 'clsx';
import { Eye, EyeOff, AlertCircle } from 'lucide-react';

export interface ModernInputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'> {
  label?: string;
  error?: string;
  helperText?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'default' | 'filled';
}

const ModernInput = React.forwardRef<HTMLInputElement, ModernInputProps>(
  ({ 
    className, 
    label, 
    error, 
    helperText, 
    leftIcon, 
    rightIcon, 
    size = 'md', 
    variant = 'default',
    type,
    disabled,
    required,
    id, 
    ...props 
  }, ref) => {
    const [showPassword, setShowPassword] = useState(false);

    
    const inputId = id || label?.toLowerCase().replace(/\s+/g, '-');
    const isPassword = type === 'password';
    const actualType = isPassword && showPassword ? 'text' : type;

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

        {/* Input Container */}
        <div className="relative">
          {/* Left Icon */}
          {leftIcon && (
            <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
              {leftIcon}
            </div>
          )}

          {/* Input */}
          <input
            ref={ref}
            id={inputId}
            type={actualType}
            disabled={disabled}
            className={clsx(
              // Base styles
              'w-full border rounded-lg transition-all duration-200 ease-in-out',
              'placeholder-gray-400 focus:outline-none',
              
              // Size variants
              sizeClasses[size],
              
              // Padding with icons
              leftIcon ? 'pl-10' : 'pl-3',
              rightIcon || isPassword ? 'pr-10' : 'pr-3',
              
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

          {/* Right Icon or Password Toggle */}
          <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
            {isPassword ? (
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="text-gray-400 hover:text-gray-600 transition-colors"
                tabIndex={-1}
              >
                {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </button>
            ) : rightIcon ? (
              <div className="text-gray-400">{rightIcon}</div>
            ) : null}
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
          <div className="mt-1.5 flex items-start space-x-1">
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

ModernInput.displayName = 'ModernInput';

export default ModernInput;