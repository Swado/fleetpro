'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion } from 'framer-motion';
import { FiMenu, FiX, FiBell, FiUser, FiMessageSquare } from 'react-icons/fi';
import Button from '../ui/Button';

const Navbar: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const pathname = usePathname();

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  // Navigation items
  const navItems = [
    { href: '/dashboard', label: 'Dashboard' },
    { href: '/trucks', label: 'Fleet' },
    { href: '/drivers', label: 'Drivers' },
    { href: '/analytics', label: 'Analytics' },
    { href: '/fleet-services', label: 'Services' },
  ];

  return (
    <header className="fixed w-full z-50 backdrop-blur-md bg-background/80 border-b border-white/10">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" legacyBehavior>
            <a className="flex items-center">
              <span className="text-xl font-bold text-primary mr-1">Fleet</span>
              <span className="text-xl font-bold text-text-light">TrackPro</span>
            </a>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex space-x-8">
            {navItems.map((item) => (
              <Link key={item.href} href={item.href} legacyBehavior>
                <a
                  className={`text-sm font-medium transition-colors hover:text-primary ${
                    pathname === item.href ? 'text-primary' : 'text-text-light'
                  }`}
                >
                  {item.label}
                </a>
              </Link>
            ))}
          </nav>

          {/* Desktop Actions */}
          <div className="hidden md:flex items-center space-x-4">
            <button className="p-2 text-text-dark hover:text-text-light relative">
              <FiBell size={20} />
              <span className="absolute top-1 right-1 w-2 h-2 bg-primary rounded-full"></span>
            </button>
            <button className="p-2 text-text-dark hover:text-text-light relative">
              <FiMessageSquare size={20} />
              <span className="absolute top-1 right-1 w-2 h-2 bg-primary rounded-full"></span>
            </button>
            <div className="h-6 w-px bg-white/10"></div>
            <Link href="/profile" legacyBehavior>
              <a className="flex items-center p-1 rounded-full border border-white/10 text-text-light hover:border-white/20 transition-colors">
                <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-primary">
                  <FiUser size={16} />
                </div>
              </a>
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden">
            <button
              onClick={toggleMenu}
              className="p-2 text-text-light focus:outline-none"
            >
              {isMenuOpen ? <FiX size={24} /> : <FiMenu size={24} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.2 }}
          className="md:hidden bg-card border-b border-white/10"
        >
          <div className="container mx-auto px-4 py-4">
            <nav className="flex flex-col space-y-4">
              {navItems.map((item) => (
                <Link key={item.href} href={item.href} legacyBehavior>
                  <a
                    className={`px-4 py-2 rounded-lg ${
                      pathname === item.href
                        ? 'bg-primary/10 text-primary'
                        : 'text-text-light hover:bg-white/5'
                    }`}
                    onClick={() => setIsMenuOpen(false)}
                  >
                    {item.label}
                  </a>
                </Link>
              ))}
            </nav>
            <div className="mt-4 pt-4 border-t border-white/10 flex items-center justify-between">
              <Link href="/profile" legacyBehavior>
                <a className="flex items-center space-x-2 text-text-light">
                  <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-primary">
                    <FiUser size={16} />
                  </div>
                  <span>Profile</span>
                </a>
              </Link>
              <Link href="/logout" legacyBehavior>
                <a>
                  <Button variant="outline" size="sm">
                    Logout
                  </Button>
                </a>
              </Link>
            </div>
          </div>
        </motion.div>
      )}
    </header>
  );
};

export default Navbar;