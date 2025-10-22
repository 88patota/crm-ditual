import React, { useState, useEffect } from 'react';
import { Input } from 'antd';
import { formatCurrencyAsYouType, convertBrazilianToNumeric, convertNumericToBrazilian } from '../../lib/utils';

interface CurrencyInputProps {
  value?: number;
  onChange?: (value: number) => void;
  placeholder?: string;
  disabled?: boolean;
  readOnly?: boolean;
  style?: React.CSSProperties;
  size?: 'small' | 'middle' | 'large';
  status?: 'error' | 'warning';
  prefix?: React.ReactNode;
  suffix?: React.ReactNode;
  addonBefore?: React.ReactNode;
  addonAfter?: React.ReactNode;
  className?: string;
  id?: string;
  name?: string;
  required?: boolean;
}

const CurrencyInput: React.FC<CurrencyInputProps> = ({
  value,
  onChange,
  placeholder = 'R$ 0,00',
  disabled = false,
  readOnly = false,
  style,
  size = 'middle',
  status,
  prefix,
  suffix,
  addonBefore,
  addonAfter,
  className,
  id,
  name,
  required = false,
}) => {
  const [displayValue, setDisplayValue] = useState<string>('');

  // Atualizar valor de exibição quando o valor prop mudar
  useEffect(() => {
    if (value !== undefined && value !== null && value !== 0) {
      setDisplayValue(convertNumericToBrazilian(value));
    } else {
      setDisplayValue('');
    }
  }, [value]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const inputValue = e.target.value;

    if (inputValue === '') {
      setDisplayValue('');
      onChange?.(0);
      return;
    }

    // Formatar durante a digitação
    const formatted = formatCurrencyAsYouType(inputValue);
    setDisplayValue(formatted);

    // Converter para número e chamar onChange
    const numericValue = convertBrazilianToNumeric(formatted);
    onChange?.(numericValue);
  };

  const handleBlur = () => {
    // Garantir formatação correta ao sair do campo
    if (displayValue && displayValue !== 'R$ 0,00') {
      const numericValue = convertBrazilianToNumeric(displayValue);
      if (numericValue > 0) {
        const properlyFormatted = convertNumericToBrazilian(numericValue);
        setDisplayValue(properlyFormatted);
      }
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    const char = e.key;
    const isNumber = /[0-9]/.test(char);
    const isComma = char === ',';
    const isDot = char === '.';
    const isBackspace = char === 'Backspace';
    const isDelete = char === 'Delete';
    const isArrow = ['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(char);
    const isTab = char === 'Tab';
    const isEnter = char === 'Enter';

    if (!isNumber && !isComma && !isDot && !isBackspace && !isDelete && !isArrow && !isTab && !isEnter) {
      e.preventDefault();
    }
  };

  return (
    <Input
      value={displayValue}
      onChange={handleChange}
      onBlur={handleBlur}
      onKeyPress={handleKeyPress}
      placeholder={placeholder}
      disabled={disabled}
      readOnly={readOnly}
      style={style}
      size={size}
      status={status}
      prefix={prefix}
      suffix={suffix}
      addonBefore={addonBefore}
      addonAfter={addonAfter}
      className={className}
      id={id}
      name={name}
      required={required}
    />
  );
};

export default CurrencyInput;