import React from 'react';
import { motion } from 'framer-motion';
import Card from '../ui/Card';
import Button from '../ui/Button';

interface RewardCardProps {
  id: number;
  name: string;
  description: string;
  icon: string; // Font Awesome icon class
  pointsRequired: number;
  currentPoints: number;
  redeemed: boolean;
  status?: 'pending' | 'approved' | 'rejected';
  redeemedAt?: string;
  className?: string;
  onRedeem?: (id: number) => void;
}

const RewardCard: React.FC<RewardCardProps> = ({
  id,
  name,
  description,
  icon,
  pointsRequired,
  currentPoints,
  redeemed,
  status,
  redeemedAt,
  className,
  onRedeem,
}) => {
  // Check if user has enough points
  const canRedeem = currentPoints >= pointsRequired && !redeemed;
  
  // Status badge style
  const statusBadge = {
    pending: 'bg-warning/15 text-warning border border-warning/30',
    approved: 'bg-success/15 text-success border border-success/30',
    rejected: 'bg-error/15 text-error border border-error/30',
  };
  
  return (
    <Card 
      variant={redeemed ? 'glass' : 'default'}
      className={`h-full ${className}`}
    >
      <div className="p-6">
        <div className="flex flex-col items-center text-center mb-4">
          <motion.div
            whileHover={{ scale: 1.1, rotate: 5 }}
            transition={{ type: 'spring', stiffness: 300 }}
            className={`w-16 h-16 flex items-center justify-center rounded-full mb-4 ${
              redeemed 
                ? 'bg-card-light text-primary' 
                : canRedeem 
                  ? 'bg-primary text-white shadow-glow-primary' 
                  : 'bg-card-light text-text-dark'
            }`}
          >
            <i className={`${icon} text-2xl`}></i>
          </motion.div>
          
          <h3 className="text-lg font-semibold text-text-light mb-1">{name}</h3>
          
          {redeemed && status && (
            <span className={`text-xs px-2 py-0.5 rounded-full ${statusBadge[status]}`}>
              {status.charAt(0).toUpperCase() + status.slice(1)}
            </span>
          )}
        </div>
        
        <p className="text-text-dark text-sm text-center mb-6">
          {description}
        </p>
        
        {!redeemed && (
          <>
            <div className="flex justify-between items-center mb-2">
              <span className="text-text-dark text-sm">Your Points</span>
              <span className={`text-sm font-medium ${
                canRedeem ? 'text-success' : 'text-text-light'
              }`}>
                {currentPoints} / {pointsRequired}
              </span>
            </div>
            
            <div className="w-full h-2 bg-background-light rounded-full overflow-hidden mb-6">
              <motion.div 
                initial={{ width: 0 }}
                animate={{ width: `${Math.min(100, (currentPoints / pointsRequired) * 100)}%` }}
                transition={{ duration: 1, ease: "easeOut" }}
                className={`h-full ${
                  canRedeem 
                    ? 'bg-success' 
                    : 'bg-primary'
                }`}
              />
            </div>
          </>
        )}
        
        <div className="flex justify-center">
          {redeemed ? (
            <div className="text-text-dark text-sm text-center">
              {redeemedAt && (
                <span>Redeemed on {redeemedAt}</span>
              )}
            </div>
          ) : (
            <Button 
              variant={canRedeem ? 'primary' : 'glass'}
              glow={canRedeem}
              disabled={!canRedeem}
              onClick={() => canRedeem && onRedeem && onRedeem(id)}
            >
              {canRedeem 
                ? 'Redeem Reward' 
                : `Need ${pointsRequired - currentPoints} more points`}
            </Button>
          )}
        </div>
      </div>
    </Card>
  );
};

export default RewardCard;