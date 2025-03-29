import React from 'react';
import clsx from 'clsx';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'accent' | 'glass' | 'outline' | 'text' | string;
  size?: 'xs' | 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  icon?: React.ReactNode;
  iconPosition?: 'left' | 'right';
  glow?: boolean;
}

const Button: React.FC<ButtonProps> = ({
  children,
  className,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  icon,
  iconPosition = 'left',
  glow = false,
  disabled,
  ...props
}) => {
  // Base classes
  const baseClasses = 'inline-flex items-center justify-center rounded-lg font-medium transition-all duration-200 focus:outline-none';
  
  // Size classes
  const sizeClasses = {
    xs: 'text-xs px-2 py-1',
    sm: 'text-sm px-3 py-1.5',
    md: 'text-sm px-4 py-2',
    lg: 'text-base px-6 py-3',
  };
  
  // Variant classes
  const variantClasses: Record<string, string> = {
    primary: 'bg-primary hover:bg-primary-dark text-white border border-primary/30 ' + 
      (glow ? 'shadow-glow-primary' : ''),
    secondary: 'bg-secondary hover:bg-secondary-dark text-white border border-secondary/30 ' + 
      (glow ? 'shadow-glow-secondary' : ''),
    accent: 'bg-accent hover:bg-accent-dark text-white border border-accent/30 ' + 
      (glow ? 'shadow-glow-accent' : ''),
    glass: 'bg-white/10 hover:bg-white/15 text-text-light backdrop-blur-sm border border-white/20',
    outline: 'bg-transparent hover:bg-white/5 text-text-light border border-white/20',
    text: 'bg-transparent hover:bg-white/5 text-text-dark hover:text-text',
  };
  
  // Disabled classes
  const disabledClasses = 'opacity-60 cursor-not-allowed';

  // Get variant class or default to primary if not found
  const variantClass = variantClasses[variant] || variantClasses.primary;
  
  // Get size class or default to medium if not found
  const sizeClass = size in sizeClasses ? sizeClasses[size as keyof typeof sizeClasses] : sizeClasses.md;

  // Handle hover and active states with CSS instead of framer-motion
  const hoverClass = !(disabled || isLoading) ? 'hover:scale-[1.02] active:scale-[0.98]' : '';

  return (
    <button
      className={clsx(
        baseClasses,
        sizeClass,
        variantClass,
        hoverClass,
        'transform transition-transform duration-200',
        (disabled || isLoading) && disabledClasses,
        className,
      )}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? (
        <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      ) : (
        <>
          {icon && iconPosition === 'left' && <span className="mr-2">{icon}</span>}
          {children}
          {icon && iconPosition === 'right' && <span className="ml-2">{icon}</span>}
        </>
      )}
    </button>
  );
};

export default Button;