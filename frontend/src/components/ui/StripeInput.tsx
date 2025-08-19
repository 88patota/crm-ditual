import React from 'react';
import { clsx } from 'clsx';

export interface StripeInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
}

const StripeInput = React.forwardRef<HTMLInputElement, StripeInputProps>(
  ({ className, label, error, helperText, id, ...props }, ref) => {
    const inputId = id || label?.toLowerCase().replace(/\s+/g, '-');
    
    return (
      <div className="stripe-form-group">
        {label && (
          <label
            htmlFor={inputId}
            className="stripe-form-label"
          >
            {label}
          </label>
        )}
        <input
          id={inputId}
          className={clsx(
            'stripe-input',
            error && 'border-red-300 focus:border-red-500 focus:shadow-red-100',
            className
          )}
          ref={ref}
          {...props}
        />
        {error && (
          <p className="text-sm text-red-600 mt-1">{error}</p>
        )}
        {helperText && !error && (
          <p className="text-sm text-gray-500 mt-1">{helperText}</p>
        )}
      </div>
    );
  }
);

StripeInput.displayName = 'StripeInput';

export default StripeInput;