import React from 'react';
import { Metadata } from 'next';
import { getServerSession } from 'next-auth';
import { redirect } from 'next/navigation';
import { authOptions } from '../api/auth/[...nextauth]/route';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { 
  FiTruck, 
  FiMap, 
  FiActivity, 
  FiDollarSign, 
  FiCalendar, 
  FiClock, 
  FiAward,
  FiBell,
  FiPlus,
  FiMessageCircle
} from 'react-icons/fi';

// Layout and components
import MainLayout from '@/components/layout/MainLayout';
import StatsCard from '@/components/dashboard/StatsCard';
import TruckCard from '@/components/dashboard/TruckCard';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import Badge from '@/components/ui/Badge';

// Define metadata
export const metadata: Metadata = {
  title: 'Dashboard | FleetTrackPro',
  description: 'Monitor and manage your fleet operations in real-time',
};

// Interface for truck data
interface Truck {
  id: number;
  plate_number: string;
  model?: string;
  year?: number;
  status: 'active' | 'inactive' | 'maintenance' | 'en_route';
  driver_name?: string;
  current_latitude?: number;
  current_longitude?: number;
  destination_city?: string;
  destination_state?: string;
  last_maintenance?: string;
}

export default async function DashboardPage() {
  const session = await getServerSession(authOptions);

  if (!session) {
    redirect('/login');
  }

  // Fetch truck data from API
  // This would normally come from your backend
  const trucks: Truck[] = [
    {
      id: 1,
      plate_number: 'CA-3845-TR',
      model: 'Kenworth T680',
      year: 2023,
      status: 'active',
      driver_name: 'Michael Johnson',
      current_latitude: 37.7749,
      current_longitude: -122.4194,
      destination_city: 'Los Angeles',
      destination_state: 'CA',
      last_maintenance: '2023-11-15',
    },
    {
      id: 2,
      plate_number: 'TX-9274-FL',
      model: 'Peterbilt 579',
      year: 2022,
      status: 'en_route',
      driver_name: 'David Martinez',
      current_latitude: 32.7767,
      current_longitude: -96.7970,
      destination_city: 'Houston',
      destination_state: 'TX',
      last_maintenance: '2023-10-28',
    },
    {
      id: 3,
      plate_number: 'NY-5519-TR',
      model: 'Freightliner Cascadia',
      year: 2021,
      status: 'maintenance',
      driver_name: 'Robert Williams',
      last_maintenance: '2023-12-02',
    },
    {
      id: 4,
      plate_number: 'FL-7823-KW',
      model: 'Volvo VNL',
      year: 2023,
      status: 'inactive',
      last_maintenance: '2023-11-10',
    }
  ];

  // Staggered animation variants
  const containerVariants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0, transition: { duration: 0.5 } },
  };

  // Format date for display
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    }).format(date);
  };

  return (
    <MainLayout>
      <div className="container mx-auto px-4 py-12">
        {/* Welcome section */}
        <div className="mb-12">
          <motion.h1 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-3xl md:text-4xl font-bold font-heading text-text-light mb-2"
          >
            Welcome back, {session.user?.name || 'User'}
          </motion.h1>
          <motion.p 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.5 }}
            className="text-text-dark"
          >
            Here's what's happening with your fleet today
          </motion.p>
        </div>

        {/* Stats cards section */}
        <motion.div 
          variants={containerVariants}
          initial="hidden"
          animate="show"
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12"
        >
          <motion.div variants={itemVariants}>
            <StatsCard
              title="Active Trucks"
              value="24"
              change={{ value: 8, trend: 'up' }}
              icon={<FiTruck size={24} />}
              variant="primary"
            />
          </motion.div>

          <motion.div variants={itemVariants}>
            <StatsCard
              title="Total Distance"
              value="14,892 mi"
              change={{ value: 12, trend: 'up' }}
              icon={<FiMap size={24} />}
              variant="secondary"
            />
          </motion.div>

          <motion.div variants={itemVariants}>
            <StatsCard
              title="Efficiency Score"
              value="94.5%"
              change={{ value: 3, trend: 'up' }}
              icon={<FiActivity size={24} />}
              variant="success"
            />
          </motion.div>

          <motion.div variants={itemVariants}>
            <StatsCard
              title="Revenue"
              value="$127,839"
              change={{ value: 5, trend: 'up' }}
              icon={<FiDollarSign size={24} />}
              variant="accent"
            />
          </motion.div>
        </motion.div>

        {/* Main content area */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Trucks and map section */}
          <div className="lg:col-span-2 space-y-8">
            {/* Recent trucks section */}
            <Card variant="glass">
              <div className="p-6 border-b border-white/5">
                <div className="flex justify-between items-center">
                  <h2 className="text-xl font-semibold text-text-light">Your Fleet</h2>
                  <Link href="/trucks" legacyBehavior>
                    <a className="text-primary hover:text-primary-light text-sm transition-colors">
                      View all trucks
                    </a>
                  </Link>
                </div>
              </div>

              <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
                {trucks.slice(0, 4).map((truck) => (
                  <TruckCard
                    key={truck.id}
                    id={truck.id}
                    plateNumber={truck.plate_number}
                    model={truck.model}
                    year={truck.year}
                    status={truck.status}
                    driverName={truck.driver_name}
                    currentLocation={truck.current_latitude && truck.current_longitude ? {
                      city: 'Current Location',
                      state: ''
                    } : undefined}
                    destination={truck.destination_city || truck.destination_state ? {
                      city: truck.destination_city,
                      state: truck.destination_state
                    } : undefined}
                    lastMaintenance={truck.last_maintenance ? formatDate(truck.last_maintenance) : undefined}
                  />
                ))}

                <Card variant="outlined" className="flex flex-col items-center justify-center p-8">
                  <FiPlus className="text-primary text-4xl mb-4" />
                  <h3 className="text-lg font-medium text-text-light mb-2">Add New Truck</h3>
                  <p className="text-text-dark text-sm text-center mb-4">
                    Register a new vehicle to your fleet
                  </p>
                  <Button variant="primary">
                    Add Truck
                  </Button>
                </Card>
              </div>
            </Card>

            {/* Map card (placeholder for now) */}
            <Card variant="glass">
              <div className="p-6 border-b border-white/5">
                <div className="flex justify-between items-center">
                  <h2 className="text-xl font-semibold text-text-light">Fleet Map</h2>
                  <Button variant="text" size="sm">
                    Refresh
                  </Button>
                </div>
              </div>
              <div className="relative aspect-[16/9] bg-card-dark">
                {/* Map would be rendered here - using a placeholder for now */}
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-center text-text-dark">
                    <FiMap className="text-5xl mx-auto mb-4 text-primary/30" />
                    <p>Interactive map loading...</p>
                  </div>
                </div>
              </div>
            </Card>
          </div>

          {/* Side column */}
          <div className="space-y-8">
            {/* Upcoming maintenance */}
            <Card variant="glass">
              <div className="p-6 border-b border-white/5">
                <h2 className="text-xl font-semibold text-text-light">Upcoming Maintenance</h2>
              </div>
              <div className="p-4">
                <div className="space-y-4">
                  <div className="flex items-start p-3 rounded-lg hover:bg-white/5 transition-colors">
                    <div className="p-2 bg-warning/10 rounded-lg text-warning mr-4">
                      <FiCalendar size={20} />
                    </div>
                    <div>
                      <div className="flex justify-between items-center mb-1">
                        <h3 className="font-medium text-text-light">TX-9274-FL</h3>
                        <Badge variant="warning" size="xs">Tomorrow</Badge>
                      </div>
                      <p className="text-sm text-text-dark">Oil change and inspection</p>
                    </div>
                  </div>
                  
                  <div className="flex items-start p-3 rounded-lg hover:bg-white/5 transition-colors">
                    <div className="p-2 bg-info/10 rounded-lg text-info mr-4">
                      <FiCalendar size={20} />
                    </div>
                    <div>
                      <div className="flex justify-between items-center mb-1">
                        <h3 className="font-medium text-text-light">CA-3845-TR</h3>
                        <Badge variant="info" size="xs">Dec 15</Badge>
                      </div>
                      <p className="text-sm text-text-dark">Annual service and brake check</p>
                    </div>
                  </div>
                  
                  <div className="flex items-start p-3 rounded-lg hover:bg-white/5 transition-colors">
                    <div className="p-2 bg-info/10 rounded-lg text-info mr-4">
                      <FiCalendar size={20} />
                    </div>
                    <div>
                      <div className="flex justify-between items-center mb-1">
                        <h3 className="font-medium text-text-light">NY-5519-TR</h3>
                        <Badge variant="info" size="xs">Dec 22</Badge>
                      </div>
                      <p className="text-sm text-text-dark">Tire replacement</p>
                    </div>
                  </div>
                </div>
                
                <div className="mt-4 pt-4 border-t border-white/5">
                  <Button variant="outline" className="w-full">
                    Schedule Maintenance
                  </Button>
                </div>
              </div>
            </Card>
            
            {/* Recent activity */}
            <Card variant="glass">
              <div className="p-6 border-b border-white/5">
                <h2 className="text-xl font-semibold text-text-light">Recent Activity</h2>
              </div>
              <div className="p-4">
                <div className="space-y-4">
                  <div className="flex items-start p-3 rounded-lg hover:bg-white/5 transition-colors">
                    <div className="p-2 bg-success/10 rounded-lg text-success mr-4">
                      <FiTruck size={20} />
                    </div>
                    <div>
                      <h3 className="font-medium text-text-light">CA-3845-TR arrived at destination</h3>
                      <div className="flex items-center text-xs text-text-dark mt-1">
                        <FiClock className="mr-1" />
                        <span>1 hour ago</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-start p-3 rounded-lg hover:bg-white/5 transition-colors">
                    <div className="p-2 bg-primary/10 rounded-lg text-primary mr-4">
                      <FiAward size={20} />
                    </div>
                    <div>
                      <h3 className="font-medium text-text-light">David Martinez earned Safe Driver achievement</h3>
                      <div className="flex items-center text-xs text-text-dark mt-1">
                        <FiClock className="mr-1" />
                        <span>3 hours ago</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-start p-3 rounded-lg hover:bg-white/5 transition-colors">
                    <div className="p-2 bg-accent/10 rounded-lg text-accent mr-4">
                      <FiBell size={20} />
                    </div>
                    <div>
                      <h3 className="font-medium text-text-light">NY-5519-TR maintenance completed</h3>
                      <div className="flex items-center text-xs text-text-dark mt-1">
                        <FiClock className="mr-1" />
                        <span>5 hours ago</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-start p-3 rounded-lg hover:bg-white/5 transition-colors">
                    <div className="p-2 bg-secondary/10 rounded-lg text-secondary mr-4">
                      <FiMessageCircle size={20} />
                    </div>
                    <div>
                      <h3 className="font-medium text-text-light">New message from Dispatch</h3>
                      <div className="flex items-center text-xs text-text-dark mt-1">
                        <FiClock className="mr-1" />
                        <span>Yesterday</span>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="mt-4 pt-4 border-t border-white/5">
                  <Button variant="text" className="w-full">
                    View All Activity
                  </Button>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}