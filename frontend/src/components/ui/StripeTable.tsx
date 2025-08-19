import React from 'react';
import { clsx } from 'clsx';

interface StripeTableProps {
  children: React.ReactNode;
  className?: string;
}

export function StripeTable({ children, className }: StripeTableProps) {
  return (
    <div className="overflow-hidden">
      <table className={clsx('stripe-table', className)}>
        {children}
      </table>
    </div>
  );
}

interface StripeTableHeaderProps {
  children: React.ReactNode;
  className?: string;
}

export function StripeTableHeader({ children, className }: StripeTableHeaderProps) {
  return (
    <thead className={className}>
      {children}
    </thead>
  );
}

interface StripeTableBodyProps {
  children: React.ReactNode;
  className?: string;
}

export function StripeTableBody({ children, className }: StripeTableBodyProps) {
  return (
    <tbody className={className}>
      {children}
    </tbody>
  );
}

interface StripeTableRowProps {
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
}

export function StripeTableRow({ children, className, onClick }: StripeTableRowProps) {
  return (
    <tr 
      className={clsx(
        onClick && 'cursor-pointer',
        className
      )}
      onClick={onClick}
    >
      {children}
    </tr>
  );
}

interface StripeTableHeadProps {
  children: React.ReactNode;
  className?: string;
}

export function StripeTableHead({ children, className }: StripeTableHeadProps) {
  return (
    <th className={className}>
      {children}
    </th>
  );
}

interface StripeTableCellProps {
  children: React.ReactNode;
  className?: string;
}

export function StripeTableCell({ children, className }: StripeTableCellProps) {
  return (
    <td className={className}>
      {children}
    </td>
  );
}

export default StripeTable;