import React from 'react';
import clsx from 'clsx';

interface CardProps {
  variant?: 'default' | 'glass' | 'outlined' | 'elevated' | 'gradient';
  className?: string;
  children: React.ReactNode;
}

const Card: React.FC<CardProps> = ({
  variant = 'default',
  className,
  children,
}) => {
  const baseClasses = 'rounded-xl overflow-hidden';
  
  const variantClasses: Record<string, string> = {
    default: 'bg-card border border-white/5',
    glass: 'bg-card/80 backdrop-blur-sm border border-white/10',
    outlined: 'bg-transparent border border-white/10',
    elevated: 'bg-card border border-white/5 shadow-md',
    gradient: 'bg-gradient-to-br from-primary/20 via-card to-accent/20 border border-white/10 shadow-glass',
  };
  
  return (
    <div 
      className={clsx(
        baseClasses,
        variantClasses[variant],
        className
      )}
    >
      {children}
    </div>
  );
};

export default Card;