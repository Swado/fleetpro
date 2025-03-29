import React from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { FiTruck, FiMap, FiActivity, FiTool, FiMessageCircle, FiAward, FiArrowRight, FiShield, FiUser } from 'react-icons/fi';
import { useInView } from 'react-intersection-observer';
import MainLayout from '@/components/layout/MainLayout';
import Button from '@/components/ui/Button';

export default function HomePage() {
  return (
    <MainLayout>
      {/* Hero Section */}
      <section className="relative pt-32 pb-20 md:pt-40 md:pb-28">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold font-heading text-text-light leading-tight mb-6">
                Intelligent Fleet Management for the Modern Era
              </h1>
              <p className="text-lg text-text-dark mb-8 max-w-lg">
                Optimize your transportation operations with our cutting-edge platform that brings together real-time tracking, 
                data analytics, and driver engagement tools.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Button 
                  variant="primary" 
                  size="lg" 
                  glow
                  className="px-8"
                >
                  Start Free Trial
                </Button>
                <Button 
                  variant="glass" 
                  size="lg"
                  className="px-8"
                >
                  Book a Demo
                </Button>
              </div>
              <div className="mt-10 grid grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-primary mb-1">99.8%</div>
                  <div className="text-sm text-text-dark">Uptime</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-primary mb-1">5,000+</div>
                  <div className="text-sm text-text-dark">Fleet Vehicles</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-primary mb-1">28%</div>
                  <div className="text-sm text-text-dark">Cost Reduction</div>
                </div>
              </div>
            </motion.div>
            
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.7, delay: 0.2 }}
              className="relative hidden lg:block"
            >
              <div className="relative z-10">
                <div className="bg-card-light rounded-2xl p-6 shadow-glass overflow-hidden">
                  <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-primary/5 via-transparent to-accent/5"></div>
                  <div className="relative">
                    {/* Dashboard Mockup would go here */}
                    <div className="bg-card rounded-xl p-4 mb-6">
                      <div className="flex justify-between items-center mb-6">
                        <div className="flex space-x-3 items-center">
                          <div className="w-10 h-10 rounded-full bg-primary flex items-center justify-center text-white">
                            <FiTruck />
                          </div>
                          <div>
                            <h3 className="text-text-light font-semibold">Fleet Overview</h3>
                            <p className="text-xs text-text-dark">Real-time status</p>
                          </div>
                        </div>
                        <div className="flex space-x-1">
                          <div className="w-2 h-2 rounded-full bg-success"></div>
                          <div className="w-2 h-2 rounded-full bg-text-dark/20"></div>
                          <div className="w-2 h-2 rounded-full bg-text-dark/20"></div>
                        </div>
                      </div>
                      <div className="space-y-4">
                        <div className="bg-card-light p-3 rounded-lg">
                          <div className="flex justify-between items-center">
                            <div className="flex items-center">
                              <div className="w-2 h-2 rounded-full bg-success mr-2"></div>
                              <span className="text-text-light text-sm">Active Trucks</span>
                            </div>
                            <span className="font-bold text-primary">24</span>
                          </div>
                        </div>
                        <div className="bg-card-light p-3 rounded-lg">
                          <div className="flex justify-between items-center">
                            <div className="flex items-center">
                              <div className="w-2 h-2 rounded-full bg-warning mr-2"></div>
                              <span className="text-text-light text-sm">Maintenance</span>
                            </div>
                            <span className="font-bold text-warning">3</span>
                          </div>
                        </div>
                        <div className="bg-card-light p-3 rounded-lg">
                          <div className="flex justify-between items-center">
                            <div className="flex items-center">
                              <div className="w-2 h-2 rounded-full bg-error mr-2"></div>
                              <span className="text-text-light text-sm">Issues</span>
                            </div>
                            <span className="font-bold text-error">1</span>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-card rounded-xl p-4">
                        <div className="flex items-center justify-between mb-3">
                          <div className="text-sm text-text-dark">Distance</div>
                          <FiMap className="text-secondary text-lg" />
                        </div>
                        <div className="text-2xl font-bold text-text-light mb-1">
                          14,892 <span className="text-sm font-normal text-text-dark">mi</span>
                        </div>
                        <div className="text-xs text-success flex items-center">
                          <svg className="w-3 h-3 mr-1" viewBox="0 0 24 24" fill="none">
                            <path d="M12 5L12 19M12 5L18 11M12 5L6 11" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                          </svg>
                          12% from last month
                        </div>
                      </div>
                      <div className="bg-card rounded-xl p-4">
                        <div className="flex items-center justify-between mb-3">
                          <div className="text-sm text-text-dark">Efficiency</div>
                          <FiActivity className="text-accent text-lg" />
                        </div>
                        <div className="text-2xl font-bold text-text-light mb-1">
                          94.5<span className="text-sm font-normal text-text-dark">%</span>
                        </div>
                        <div className="text-xs text-success flex items-center">
                          <svg className="w-3 h-3 mr-1" viewBox="0 0 24 24" fill="none">
                            <path d="M12 5L12 19M12 5L18 11M12 5L6 11" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                          </svg>
                          3% increase
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="absolute -top-12 -right-12 w-32 h-32 bg-gradient-to-br from-primary via-primary to-accent rounded-full blur-3xl opacity-20"></div>
                <div className="absolute -bottom-12 -left-12 w-32 h-32 bg-gradient-to-br from-secondary via-secondary to-accent rounded-full blur-3xl opacity-20"></div>
              </div>
              <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-full h-full border-2 border-white/5 rounded-2xl -rotate-3 scale-105 z-0"></div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gradient-to-b from-background to-background-light">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <motion.h2 
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              viewport={{ once: true, margin: "-100px" }}
              className="text-3xl md:text-4xl font-bold font-heading text-text-light mb-4"
            >
              Powerful Features for Modern Fleet Management
            </motion.h2>
            <motion.p 
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              transition={{ delay: 0.2, duration: 0.5 }}
              viewport={{ once: true, margin: "-100px" }}
              className="text-text-dark max-w-2xl mx-auto"
            >
              Our comprehensive platform offers everything you need to optimize operations, 
              reduce costs, and increase driver satisfaction.
            </motion.p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: <FiMap />,
                title: "Real-Time GPS Tracking",
                description: "Monitor your entire fleet with precision GPS tracking and get instant notifications on vehicle status and location changes."
              },
              {
                icon: <FiActivity />,
                title: "Performance Analytics",
                description: "Detailed insights into vehicle performance, driver behavior, fuel efficiency, and maintenance needs with actionable recommendations."
              },
              {
                icon: <FiAward />,
                title: "Driver Gamification",
                description: "Motivate your drivers with achievement systems, rewards, and leaderboards that recognize and incentivize safe, efficient driving."
              },
              {
                icon: <FiTool />,
                title: "Maintenance Management",
                description: "Automate maintenance scheduling, track service history, and receive alerts for upcoming service needs to prevent breakdowns."
              },
              {
                icon: <FiMessageCircle />,
                title: "Communication Hub",
                description: "Seamless communication between dispatchers, drivers, and administrative staff with voice, text, and document sharing."
              },
              {
                icon: <FiShield />,
                title: "Compliance Assurance",
                description: "Stay compliant with regulations through automated logging, document management, and regulatory update notifications."
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true, margin: "-100px" }}
                className="bg-card/90 backdrop-blur-sm border border-white/5 rounded-xl p-6 hover:shadow-glow-primary transition-all duration-300"
              >
                <div className="w-12 h-12 flex items-center justify-center rounded-lg bg-primary/10 text-primary text-xl mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-text-light mb-3">{feature.title}</h3>
                <p className="text-text-dark mb-4">{feature.description}</p>
                <Link href="/features" legacyBehavior>
                  <a className="text-primary hover:text-primary-light transition-colors flex items-center">
                    Learn more
                    <FiArrowRight className="ml-2" />
                  </a>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <motion.h2 
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              viewport={{ once: true, margin: "-100px" }}
              className="text-3xl md:text-4xl font-bold font-heading text-text-light mb-4"
            >
              Trusted by Industry Leaders
            </motion.h2>
            <motion.p 
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              transition={{ delay: 0.2, duration: 0.5 }}
              viewport={{ once: true, margin: "-100px" }}
              className="text-text-dark max-w-2xl mx-auto"
            >
              See what transportation professionals are saying about our platform
            </motion.p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                quote: "We've seen a 28% reduction in operational costs and a 15% boost in driver retention since implementing FleetTrackPro.",
                name: "Sarah Johnson",
                title: "Operations Director, TransGlobal Logistics"
              },
              {
                quote: "The gamification features have transformed our driver culture. Our safety incidents are down 40% and driver satisfaction is at an all-time high.",
                name: "Michael Rodriguez",
                title: "Fleet Manager, Horizon Transport"
              },
              {
                quote: "The real-time analytics and maintenance scheduling have virtually eliminated unexpected downtime for our fleet of 200+ vehicles.",
                name: "Jessica Chen",
                title: "CEO, Pacific Route Carriers"
              }
            ].map((testimonial, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true, margin: "-100px" }}
                className="bg-gradient-to-br from-card to-card-light border border-white/10 rounded-xl p-6 relative"
              >
                <div className="absolute -top-4 left-6 text-primary text-4xl">"</div>
                <div className="pt-4">
                  <p className="text-text mb-6">{testimonial.quote}</p>
                  <div className="flex items-center">
                    <div className="w-10 h-10 rounded-full bg-primary flex items-center justify-center text-white mr-4">
                      <FiUser />
                    </div>
                    <div>
                      <h4 className="font-semibold text-text-light">{testimonial.name}</h4>
                      <p className="text-sm text-text-dark">{testimonial.title}</p>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
            viewport={{ once: true, margin: "-100px" }}
            className="bg-gradient-to-br from-primary/20 via-card to-accent/20 border border-white/10 rounded-2xl p-10 md:p-16 text-center relative overflow-hidden"
          >
            <div className="absolute top-0 left-0 w-full h-full">
              <div className="absolute top-0 right-0 w-80 h-80 bg-primary opacity-10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/3"></div>
              <div className="absolute bottom-0 left-0 w-80 h-80 bg-accent opacity-10 rounded-full blur-3xl translate-y-1/2 -translate-x-1/3"></div>
            </div>

            <div className="relative z-10">
              <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold font-heading text-text-light mb-6">
                Ready to Transform Your Fleet Operations?
              </h2>
              <p className="text-lg text-text-dark mb-10 max-w-2xl mx-auto">
                Join thousands of transportation companies already optimizing their operations, 
                reducing costs, and improving driver satisfaction with FleetTrackPro.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button 
                  variant="primary" 
                  size="lg" 
                  glow
                  className="px-8"
                >
                  Start Your Free Trial
                </Button>
                <Button 
                  variant="glass" 
                  size="lg"
                  className="px-8"
                >
                  Request a Demo
                </Button>
              </div>
              <p className="text-text-dark mt-6 text-sm">
                No credit card required. 14-day free trial.
              </p>
            </div>
          </motion.div>
        </div>
      </section>
    </MainLayout>
  );
}