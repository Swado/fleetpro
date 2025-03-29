import React from 'react';
import Link from 'next/link';
import { FiGithub, FiTwitter, FiLinkedin, FiMail } from 'react-icons/fi';

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="bg-background-light border-t border-white/5">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Logo and about */}
          <div className="md:col-span-1">
            <Link href="/" legacyBehavior>
              <a className="flex items-center mb-4">
                <span className="text-xl font-bold text-primary mr-1">Fleet</span>
                <span className="text-xl font-bold text-text-light">TrackPro</span>
              </a>
            </Link>
            <p className="text-text-dark text-sm mb-4">
              Intelligent fleet management solutions for the modern transportation industry.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-text-dark hover:text-primary transition-colors">
                <FiTwitter size={20} />
              </a>
              <a href="#" className="text-text-dark hover:text-primary transition-colors">
                <FiLinkedin size={20} />
              </a>
              <a href="#" className="text-text-dark hover:text-primary transition-colors">
                <FiGithub size={20} />
              </a>
              <a href="mailto:contact@fleettrackpro.com" className="text-text-dark hover:text-primary transition-colors">
                <FiMail size={20} />
              </a>
            </div>
          </div>
          
          {/* Product */}
          <div>
            <h3 className="text-text-light font-semibold mb-4">Product</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/features" legacyBehavior>
                  <a className="text-text-dark hover:text-primary text-sm transition-colors">Features</a>
                </Link>
              </li>
              <li>
                <Link href="/pricing" legacyBehavior>
                  <a className="text-text-dark hover:text-primary text-sm transition-colors">Pricing</a>
                </Link>
              </li>
              <li>
                <Link href="/fleet-services" legacyBehavior>
                  <a className="text-text-dark hover:text-primary text-sm transition-colors">Fleet Services</a>
                </Link>
              </li>
              <li>
                <Link href="/roadmap" legacyBehavior>
                  <a className="text-text-dark hover:text-primary text-sm transition-colors">Roadmap</a>
                </Link>
              </li>
            </ul>
          </div>
          
          {/* Company */}
          <div>
            <h3 className="text-text-light font-semibold mb-4">Company</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/about" legacyBehavior>
                  <a className="text-text-dark hover:text-primary text-sm transition-colors">About Us</a>
                </Link>
              </li>
              <li>
                <Link href="/careers" legacyBehavior>
                  <a className="text-text-dark hover:text-primary text-sm transition-colors">Careers</a>
                </Link>
              </li>
              <li>
                <Link href="/blog" legacyBehavior>
                  <a className="text-text-dark hover:text-primary text-sm transition-colors">Blog</a>
                </Link>
              </li>
              <li>
                <Link href="/contact" legacyBehavior>
                  <a className="text-text-dark hover:text-primary text-sm transition-colors">Contact</a>
                </Link>
              </li>
            </ul>
          </div>
          
          {/* Resources */}
          <div>
            <h3 className="text-text-light font-semibold mb-4">Resources</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/documentation" legacyBehavior>
                  <a className="text-text-dark hover:text-primary text-sm transition-colors">Documentation</a>
                </Link>
              </li>
              <li>
                <Link href="/help" legacyBehavior>
                  <a className="text-text-dark hover:text-primary text-sm transition-colors">Support Center</a>
                </Link>
              </li>
              <li>
                <Link href="/privacy" legacyBehavior>
                  <a className="text-text-dark hover:text-primary text-sm transition-colors">Privacy Policy</a>
                </Link>
              </li>
              <li>
                <Link href="/terms" legacyBehavior>
                  <a className="text-text-dark hover:text-primary text-sm transition-colors">Terms of Service</a>
                </Link>
              </li>
            </ul>
          </div>
        </div>
        
        <div className="mt-12 pt-8 border-t border-white/5 flex flex-col md:flex-row justify-between items-center">
          <p className="text-text-dark text-sm mb-4 md:mb-0">
            &copy; {currentYear} FleetTrackPro. All rights reserved.
          </p>
          <div className="flex space-x-6">
            <Link href="/privacy" legacyBehavior>
              <a className="text-text-dark hover:text-primary text-sm transition-colors">Privacy</a>
            </Link>
            <Link href="/terms" legacyBehavior>
              <a className="text-text-dark hover:text-primary text-sm transition-colors">Terms</a>
            </Link>
            <Link href="/cookies" legacyBehavior>
              <a className="text-text-dark hover:text-primary text-sm transition-colors">Cookies</a>
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;