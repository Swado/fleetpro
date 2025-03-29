import React from 'react';
import { Metadata } from 'next';
import { 
  FiShield, 
  FiFileText, 
  FiCreditCard, 
  FiTool, 
  FiDroplet, 
  FiTruck, 
  FiPackage,
  FiAward
} from 'react-icons/fi';
import { motion } from 'framer-motion';
import { getServerSession } from 'next-auth';
import { redirect } from 'next/navigation';
import { authOptions } from '../api/auth/[...nextauth]/route';

// Layout imports
import MainLayout from '@/components/layout/MainLayout';
import ServiceCard from '@/components/services/ServiceCard';

export const metadata: Metadata = {
  title: 'Fleet Services | FleetTrackPro',
  description: 'Comprehensive fleet services and support for your transportation operations',
};

export default async function FleetServicesPage() {
  const session = await getServerSession(authOptions);

  if (!session) {
    redirect('/login');
  }

  // Fleet services data
  const services = [
    {
      id: 'insurance',
      title: 'Insurance Services',
      description: 'Comprehensive insurance solutions tailored for commercial trucking fleets. Get competitive rates and specialized coverage.',
      icon: <FiShield size={28} />,
      ctaText: 'Get Coverage',
      variant: 'primary',
      glow: true,
    },
    {
      id: 'legal',
      title: 'Legal Support',
      description: 'Expert legal advice and representation for regulatory compliance, accident claims, and commercial transportation law.',
      icon: <FiFileText size={28} />,
      ctaText: 'Consult Now',
      variant: 'secondary',
    },
    {
      id: 'payments',
      title: 'Payment Processing',
      description: 'Fast, secure payment solutions for freight bills, driver compensation, and operational expenses with real-time tracking.',
      icon: <FiCreditCard size={28} />,
      ctaText: 'Process Payment',
      variant: 'accent',
      glow: true,
    },
    {
      id: 'maintenance',
      title: 'Maintenance Scheduling',
      description: 'Proactive maintenance planning and service tracking to minimize downtime and extend vehicle lifespan.',
      icon: <FiTool size={28} />,
      ctaText: 'Schedule Service',
      variant: 'primary',
    },
    {
      id: 'fuel',
      title: 'Fuel Management',
      description: 'Optimize fuel consumption with route planning, discounted networks, and consumption analytics.',
      icon: <FiDroplet size={28} />,
      ctaText: 'View Fuel Stations',
      variant: 'secondary',
    },
    {
      id: 'parts',
      title: 'Parts & Equipment',
      description: 'Access to quality replacement parts, accessories, and equipment for your entire fleet at competitive prices.',
      icon: <FiTruck size={28} />,
      ctaText: 'Browse Catalog',
      variant: 'accent',
    },
    {
      id: 'loadboard',
      title: 'Load Board Integration',
      description: 'Connect with our network of shippers to find and book freight loads that match your fleet capacity and routes.',
      icon: <FiPackage size={28} />,
      ctaText: 'Find Loads',
      variant: 'primary',
      glow: true,
    },
    {
      id: 'training',
      title: 'Driver Training',
      description: 'Comprehensive training programs for safety, efficiency, compliance, and professional development.',
      icon: <FiAward size={28} />,
      ctaText: 'Enroll Now',
      variant: 'secondary',
    },
  ];

  // Animation variants for staggered animations
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

  return (
    <MainLayout>
      <div className="container mx-auto px-4 py-12">
        {/* Header section */}
        <div className="text-center mb-16">
          <motion.h1 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-4xl md:text-5xl font-bold font-heading text-text-light mb-4"
          >
            Fleet Services
          </motion.h1>
          <motion.p 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.5 }}
            className="text-text-dark max-w-3xl mx-auto"
          >
            Comprehensive support services designed to optimize your fleet operations,
            reduce costs, and enhance performance.
          </motion.p>
        </div>

        {/* Services grid */}
        <motion.div 
          variants={containerVariants}
          initial="hidden"
          animate="show"
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
        >
          {services.map((service) => (
            <motion.div key={service.id} variants={itemVariants}>
              <ServiceCard {...service} />
            </motion.div>
          ))}
        </motion.div>

        {/* Support section */}
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.7 }}
          className="mt-20 bg-card/60 backdrop-blur-md border border-white/10 rounded-2xl p-8 md:p-10 shadow-glass"
        >
          <div className="grid md:grid-cols-2 gap-10 items-center">
            <div>
              <h2 className="text-2xl md:text-3xl font-bold font-heading text-text-light mb-4">
                Need Custom Fleet Solutions?
              </h2>
              <p className="text-text-dark mb-6">
                Our fleet specialists can create tailored service packages to meet your unique operational requirements,
                whatever the size of your fleet.
              </p>
              <div className="flex space-x-4">
                <button className="py-3 px-6 bg-primary hover:bg-primary-dark text-white rounded-lg transition-colors duration-200 shadow-glow-primary">
                  Contact a Specialist
                </button>
                <button className="py-3 px-6 bg-transparent hover:bg-white/5 text-text-light border border-white/20 rounded-lg transition-colors duration-200">
                  View All Services
                </button>
              </div>
            </div>
            <div className="hidden md:block">
              <div className="relative">
                <div className="absolute -top-5 -left-5 right-5 bottom-5 border-2 border-primary/20 rounded-2xl"></div>
                <div className="relative bg-card-light rounded-2xl overflow-hidden h-64">
                  {/* Replace with actual image if needed */}
                  <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-transparent to-accent/10"></div>
                  <div className="flex items-center justify-center h-full">
                    <FiTruck className="text-primary w-32 h-32 opacity-20" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </MainLayout>
  );
}