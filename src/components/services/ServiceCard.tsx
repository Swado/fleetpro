import React from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import Card from '../ui/Card';
import Button from '../ui/Button';

interface ServiceCardProps {
  id: string;
  title: string;
  description: string;
  icon: React.ReactNode;
  ctaText?: string;
  ctaLink?: string;
  variant?: 'primary' | 'secondary' | 'accent' | string;
  glow?: boolean;
  className?: string;
}

const ServiceCard: React.FC<ServiceCardProps> = ({
  id,
  title,
  description,
  icon,
  ctaText = 'Learn More',
  ctaLink,
  variant = 'primary',
  glow = false,
  className,
}) => {
  // Determine the correct link
  const href = ctaLink || `/fleet-services/${id}`;
  
  // Map variants to colors
  const colorMap: Record<string, string> = {
    primary: 'text-primary',
    secondary: 'text-secondary',
    accent: 'text-accent',
  };
  
  // Get the appropriate text color or default to primary
  const textColorClass = variant && variant in colorMap ? colorMap[variant] : colorMap.primary;
  
  return (
    <Card 
      variant="glass"
      className={`h-full flex flex-col ${className}`}
    >
      <motion.div 
        whileHover={{ y: -5, scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        transition={{ type: 'spring', stiffness: 300 }}
        className="p-6 flex flex-col h-full"
      >
        <div className={`mb-4 text-3xl ${textColorClass}`}>
          {icon}
        </div>
        
        <h3 className="text-xl font-semibold text-text-light mb-3">{title}</h3>
        
        <p className="text-text-dark mb-6 flex-grow">
          {description}
        </p>
        
        <div className="mt-auto">
          <Link href={href} legacyBehavior>
            <a>
              <Button 
                variant={variant} 
                glow={glow}
                className="w-full"
              >
                {ctaText}
              </Button>
            </a>
          </Link>
        </div>
      </motion.div>
    </Card>
  );
};

export default ServiceCard;