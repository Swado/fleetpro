import React from 'react';
import Link from 'next/link';
import { FiTruck, FiMapPin, FiUser, FiCalendar, FiClock } from 'react-icons/fi';
import clsx from 'clsx';
import Card from '../ui/Card';
import Badge from '../ui/Badge';

interface TruckCardProps {
  id: number;
  plateNumber: string;
  model?: string;
  year?: number;
  status: 'active' | 'inactive' | 'maintenance' | 'en_route';
  driverName?: string;
  currentLocation?: { city: string; state: string };
  destination?: { city?: string; state?: string };
  lastMaintenance?: string;
  className?: string;
}

const TruckCard: React.FC<TruckCardProps> = ({
  id,
  plateNumber,
  model,
  year,
  status,
  driverName,
  currentLocation,
  destination,
  lastMaintenance,
  className,
}) => {
  // Map status to badge variant
  const statusVariantMap: Record<string, string> = {
    active: 'success',
    inactive: 'error',
    maintenance: 'warning',
    en_route: 'info',
  };
  
  // Map status to readable text
  const statusTextMap: Record<string, string> = {
    active: 'Active',
    inactive: 'Inactive',
    maintenance: 'Maintenance',
    en_route: 'En Route',
  };
  
  // Get appropriate badge variant or default to 'info'
  const badgeVariant = statusVariantMap[status] || 'info';
  const statusText = statusTextMap[status] || 'Unknown';
  
  return (
    <Card 
      variant="glass"
      className={clsx('h-full flex flex-col', className)}
    >
      <div className="p-4 border-b border-white/5">
        <div className="flex justify-between items-center">
          <div className="flex items-center">
            <div className="p-2 bg-secondary/10 text-secondary rounded-lg mr-3">
              <FiTruck size={18} />
            </div>
            <div>
              <h3 className="font-semibold text-text-light">{plateNumber}</h3>
              {model && year && (
                <p className="text-xs text-text-dark">{year} {model}</p>
              )}
            </div>
          </div>
          <Badge variant={badgeVariant} size="sm">
            {statusText}
          </Badge>
        </div>
      </div>
      
      <div className="p-4 space-y-3 flex-grow">
        {driverName && (
          <div className="flex items-center text-sm">
            <FiUser className="text-text-dark mr-2 flex-shrink-0" />
            <span className={clsx(
              'truncate',
              status === 'active' ? 'text-success' :
              status === 'inactive' ? 'text-text-dark' :
              'text-text'
            )}>
              {driverName}
            </span>
          </div>
        )}
        
        {destination && (destination.city || destination.state) && (
          <div className="flex items-center text-sm">
            <FiMapPin className="text-text-dark mr-2 flex-shrink-0" />
            <span className="text-text truncate">
              {[destination.city, destination.state].filter(Boolean).join(', ')}
            </span>
          </div>
        )}
        
        {lastMaintenance && (
          <div className="flex items-center text-sm">
            <FiCalendar className="text-text-dark mr-2 flex-shrink-0" />
            <span className="text-text-dark">Last service: {lastMaintenance}</span>
          </div>
        )}
      </div>
      
      <div className="p-3 pt-0">
        <Link href={`/trucks/${id}`} legacyBehavior>
          <a className="text-xs text-primary hover:text-primary-light transition-colors flex items-center justify-end font-medium">
            View details
            <FiClock className="ml-1" />
          </a>
        </Link>
      </div>
    </Card>
  );
};

export default TruckCard;