import React from 'react';
import { clsx } from 'clsx';

interface FormGroupProps {
  children: React.ReactNode;
  className?: string;
  spacing?: 'sm' | 'md' | 'lg';
}

export function FormGroup({ children, className, spacing = 'md' }: FormGroupProps) {
  const spacingClasses = {
    sm: 'space-y-3',
    md: 'space-y-4',
    lg: 'space-y-6'
  };

  return (
    <div className={clsx(spacingClasses[spacing], className)}>
      {children}
    </div>
  );
}

interface FormFieldsetProps {
  children: React.ReactNode;
  legend?: string;
  description?: string;
  className?: string;
}

export function FormFieldset({ children, legend, description, className }: FormFieldsetProps) {
  return (
    <fieldset className={clsx('space-y-4', className)}>
      {legend && (
        <legend className="text-base font-semibold text-gray-900">
          {legend}
        </legend>
      )}
      {description && (
        <p className="text-sm text-gray-600 -mt-1">{description}</p>
      )}
      <div className="space-y-4">
        {children}
      </div>
    </fieldset>
  );
}

interface FormRowProps {
  children: React.ReactNode;
  columns?: 1 | 2 | 3 | 4;
  gap?: 'sm' | 'md' | 'lg';
  className?: string;
}

export function FormRow({ children, columns = 2, gap = 'md', className }: FormRowProps) {
  const gridClasses = {
    1: 'grid-cols-1',
    2: 'grid-cols-1 md:grid-cols-2',
    3: 'grid-cols-1 md:grid-cols-3',
    4: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4'
  };

  const gapClasses = {
    sm: 'gap-3',
    md: 'gap-4',
    lg: 'gap-6'
  };

  return (
    <div className={clsx(
      'grid',
      gridClasses[columns],
      gapClasses[gap],
      className
    )}>
      {children}
    </div>
  );
}

export default FormGroup;