import React from 'react';
import clsx from 'clsx';

export interface BadgeProps {
  variant?: 'primary' | 'secondary' | 'accent' | 'success' | 'warning' | 'error' | 'info' | string;
  size?: 'xs' | 'sm' | 'md';
  outline?: boolean;
  children: React.ReactNode;
  className?: string;
}

const Badge: React.FC<BadgeProps> = ({
  variant = 'primary',
  size = 'md',
  outline = false,
  children,
  className,
}) => {
  // Base classes
  const baseClasses = 'inline-flex items-center justify-center font-medium rounded-full';
  
  // Size classes
  const sizeClasses: Record<string, string> = {
    xs: 'text-xs px-1.5 py-0.5',
    sm: 'text-xs px-2 py-0.5',
    md: 'text-sm px-2.5 py-1',
  };
  
  // Variant classes
  const variantColors: Record<string, Record<string, string>> = {
    primary: {
      solid: 'bg-primary/10 text-primary',
      outline: 'bg-transparent text-primary border border-primary/30',
    },
    secondary: {
      solid: 'bg-secondary/10 text-secondary',
      outline: 'bg-transparent text-secondary border border-secondary/30',
    },
    accent: {
      solid: 'bg-accent/10 text-accent',
      outline: 'bg-transparent text-accent border border-accent/30',
    },
    success: {
      solid: 'bg-success/10 text-success',
      outline: 'bg-transparent text-success border border-success/30',
    },
    warning: {
      solid: 'bg-warning/10 text-warning',
      outline: 'bg-transparent text-warning border border-warning/30',
    },
    error: {
      solid: 'bg-error/10 text-error',
      outline: 'bg-transparent text-error border border-error/30',
    },
    info: {
      solid: 'bg-info/10 text-info',
      outline: 'bg-transparent text-info border border-info/30',
    },
  };
  
  // Get the appropriate size class
  const sizeClass = size in sizeClasses ? sizeClasses[size] : sizeClasses.md;
  
  // Get the appropriate variant color
  const style = outline ? 'outline' : 'solid';
  const variantColor = variant in variantColors 
    ? variantColors[variant][style] 
    : variantColors.primary[style];
  
  return (
    <span
      className={clsx(
        baseClasses,
        sizeClass,
        variantColor,
        className
      )}
    >
      {children}
    </span>
  );
};

export default Badge;