import React from 'react';
import { motion } from 'framer-motion';
import Card from '../ui/Card';

interface AchievementCardProps {
  name: string;
  description: string;
  icon: string; // Font Awesome icon class
  category: string;
  points: number;
  progress: number; // 0-100 percentage
  earned: boolean;
  earnedAt?: string;
  className?: string;
}

const AchievementCard: React.FC<AchievementCardProps> = ({
  name,
  description,
  icon,
  category,
  points,
  progress,
  earned,
  earnedAt,
  className,
}) => {
  // Category color mapping
  const categoryColors = {
    efficiency: 'text-primary',
    safety: 'text-success',
    maintenance: 'text-secondary',
    delivery: 'text-accent',
    default: 'text-info',
  };
  
  // Get color class based on category
  const colorClass = categoryColors[category as keyof typeof categoryColors] || categoryColors.default;
  
  return (
    <Card 
      variant={earned ? 'gradient' : 'glass'}
      className={`h-full ${className}`}
    >
      <div className="p-6">
        <div className="flex flex-col items-center text-center mb-4">
          <motion.div
            whileHover={{ scale: 1.1, rotate: earned ? 10 : 0 }}
            transition={{ type: 'spring', stiffness: 300 }}
            className={`w-16 h-16 flex items-center justify-center rounded-full mb-4 ${
              earned 
                ? 'bg-gradient-to-br from-primary to-accent text-white shadow-glow-primary' 
                : `bg-card ${colorClass}`
            }`}
          >
            <i className={`${icon} text-2xl`}></i>
          </motion.div>
          
          <h3 className="text-lg font-semibold text-text-light">{name}</h3>
          <span className={`text-sm ${colorClass} mt-1`}>{category}</span>
        </div>
        
        <p className="text-text-dark text-sm text-center mb-6">
          {description}
        </p>
        
        <div className="flex justify-between items-center mb-2">
          <span className="text-text-dark text-sm">Progress</span>
          <span className="text-text-light text-sm font-medium">{progress}%</span>
        </div>
        
        <div className="w-full h-2 bg-background-light rounded-full overflow-hidden mb-4">
          <motion.div 
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 1, ease: "easeOut" }}
            className={`h-full ${
              earned 
                ? 'bg-gradient-to-r from-primary to-accent' 
                : colorClass.replace('text-', 'bg-')
            }`}
          />
        </div>
        
        <div className="flex justify-between items-center">
          <div className="flex items-center">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="text-warning mr-1">
              <path d="M12 15.713L18.01 19.213L16.597 12.361L21.991 7.794L14.926 7.192L12 0.787L9.074 7.192L2.009 7.794L7.403 12.361L5.99 19.213L12 15.713Z" fill="currentColor"/>
            </svg>
            <span className="text-text-light font-medium">{points} points</span>
          </div>
          
          {earned && earnedAt && (
            <span className="text-text-dark text-xs">
              Earned on {earnedAt}
            </span>
          )}
        </div>
      </div>
    </Card>
  );
};

export default AchievementCard;