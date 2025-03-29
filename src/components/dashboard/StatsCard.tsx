import React from 'react';
import clsx from 'clsx';
import Card from '../ui/Card';

interface StatsCardProps {
  title: string;
  value: string;
  change?: {
    value: number;
    trend: 'up' | 'down' | 'neutral';
  };
  icon: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'accent' | 'success' | 'warning' | 'error' | 'info';
  className?: string;
}

const StatsCard: React.FC<StatsCardProps> = ({
  title,
  value,
  change,
  icon,
  variant = 'primary',
  className,
}) => {
  // Map variants to colors
  const variantMap: Record<string, string> = {
    primary: 'text-primary',
    secondary: 'text-secondary',
    accent: 'text-accent',
    success: 'text-success',
    warning: 'text-warning',
    error: 'text-error',
    info: 'text-info',
  };

  // Get background variant color or default to primary
  const bgColor = `${variantMap[variant] || variantMap.primary} bg-${variant}/10 ring-${variant}/20`;
  
  // Get trend icon and color
  const getTrendData = () => {
    if (!change) return null;
    
    let trendColor = 'text-text-dark';
    let trendIcon = null;
    
    if (change.trend === 'up') {
      trendColor = 'text-success';
      trendIcon = (
        <svg className="w-3 h-3 mr-1" viewBox="0 0 24 24" fill="none">
          <path d="M12 5L12 19M12 5L18 11M12 5L6 11" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      );
    } else if (change.trend === 'down') {
      trendColor = 'text-error';
      trendIcon = (
        <svg className="w-3 h-3 mr-1" viewBox="0 0 24 24" fill="none">
          <path d="M12 19L12 5M12 19L18 13M12 19L6 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      );
    }
    
    return { trendColor, trendIcon };
  };
  
  const trendData = getTrendData();
  
  return (
    <Card variant="glass" className={clsx('h-full', className)}>
      <div className="p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="text-text-dark text-sm font-medium">{title}</div>
          <div className={clsx('p-2 rounded-lg ring-1', bgColor)}>
            {icon}
          </div>
        </div>
        
        <div className="flex flex-col">
          <div className="text-2xl font-bold text-text-light">{value}</div>
          
          {change && (
            <div className={clsx('text-xs flex items-center mt-1', trendData?.trendColor)}>
              {trendData?.trendIcon}
              <span>{change.value}% from last month</span>
            </div>
          )}
        </div>
      </div>
    </Card>
  );
};

export default StatsCard;