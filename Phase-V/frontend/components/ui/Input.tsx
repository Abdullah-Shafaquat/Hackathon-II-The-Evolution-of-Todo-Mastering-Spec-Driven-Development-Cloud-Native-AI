import { InputHTMLAttributes, forwardRef } from 'react';

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  fullWidth?: boolean;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      label,
      error,
      helperText,
      fullWidth = true,
      className = '',
      id,
      ...props
    },
    ref
  ) => {
    const inputId = id || label?.toLowerCase().replace(/\s+/g, '-');

    // Full width on mobile, max-width on desktop
    const widthStyles = fullWidth ? 'w-full sm:max-w-md' : '';

    const baseStyles = 'px-3 py-2 border rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-offset-1 placeholder:text-gray-400';

    const stateStyles = error
      ? 'border-red-600 focus:ring-red-500 focus:border-red-500'
      : 'border-gray-700 focus:ring-white focus:border-white';

    const disabledStyles = props.disabled
      ? 'bg-gray-800 text-gray-500 cursor-not-allowed'
      : 'bg-gray-800 text-white';

    const combinedClassName = `${baseStyles} ${stateStyles} ${disabledStyles} ${widthStyles} ${className}`;

    return (
      <div className={fullWidth ? 'w-full' : ''}>
        {label && (
          <label
            htmlFor={inputId}
            className="block text-sm font-medium text-white mb-1"
          >
            {label}
            {props.required && <span className="text-white ml-1">*</span>}
          </label>
        )}

        <input
          ref={ref}
          id={inputId}
          className={combinedClassName}
          aria-invalid={error ? 'true' : 'false'}
          aria-describedby={
            error
              ? `${inputId}-error`
              : helperText
              ? `${inputId}-helper`
              : undefined
          }
          {...props}
        />

        {error && (
          <p
            id={`${inputId}-error`}
            className="mt-1 text-sm text-red-400 font-medium"
            role="alert"
          >
            {error}
          </p>
        )}

        {helperText && !error && (
          <p
            id={`${inputId}-helper`}
            className="mt-1 text-sm text-gray-400"
          >
            {helperText}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export default Input;
