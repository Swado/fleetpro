import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Main brand colors - from Flask app
        primary: {
          DEFAULT: '#2C3E50', // Flask primary color
          dark: '#1E2A35',
          light: '#3D5166',
        },
        accent: {
          DEFAULT: '#1E90FF', // Royal blue accent color
          dark: '#0066CC',
          light: '#00BFFF',
        },
        
        // UI colors - from Flask app
        background: {
          DEFAULT: '#000000', // Black background
          light: '#121212',
          dark: '#000000',
        },
        card: {
          DEFAULT: '#0A0A0A', // Very dark gray for cards
          light: '#101010',
          dark: '#050505',
        },
        text: {
          DEFAULT: '#E0E0E0', // Light silver text color
          light: '#FFFFFF', // White for highlights
          dark: '#AAAAAA',
        },
        border: {
          DEFAULT: '#333333', // Dark gray borders
          light: '#444444',
          dark: '#222222',
        },
        table: {
          header: {
            bg: '#121212', // Slightly lighter black for table headers
            text: '#FFFFFF', // White text for table headers
          }
        },
        
        // Status colors
        success: {
          DEFAULT: '#10B981', // Green
          light: '#34D399',
          dark: '#059669',
        },
        warning: {
          DEFAULT: '#F59E0B', // Amber
          light: '#FBBF24',
          dark: '#D97706',
        },
        error: {
          DEFAULT: '#EF4444', // Red
          light: '#F87171',
          dark: '#DC2626',
        },
        info: {
          DEFAULT: '#0EA5E9', // Sky blue
          light: '#38BDF8',
          dark: '#0284C7',
        },
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'SFMono-Regular', 'monospace'],
        heading: ['Manrope', 'Inter', 'ui-sans-serif', 'system-ui', '-apple-system', 'sans-serif'],
      },
      boxShadow: {
        'glass': '0 4px 30px rgba(0, 0, 0, 0.1)',
        'glow-primary': '0 0 15px rgba(59, 130, 246, 0.5)',
        'glow-secondary': '0 0 15px rgba(139, 92, 246, 0.5)',
        'glow-accent': '0 0 15px rgba(236, 72, 153, 0.5)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms')
  ],
};

export default config;