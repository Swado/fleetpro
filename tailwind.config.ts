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
        // Main brand colors
        primary: {
          DEFAULT: '#3B82F6', // Blue
          dark: '#2563EB',
          light: '#60A5FA',
        },
        secondary: {
          DEFAULT: '#8B5CF6', // Purple
          dark: '#7C3AED',
          light: '#A78BFA',
        },
        accent: {
          DEFAULT: '#EC4899', // Pink
          dark: '#DB2777',
          light: '#F472B6',
        },
        
        // UI colors
        background: {
          DEFAULT: '#0F172A', // Dark blue/slate base
          light: '#1E293B',
          dark: '#0B1120',
        },
        card: {
          DEFAULT: '#1E293B',
          light: '#334155',
          dark: '#0F172A',
        },
        text: {
          DEFAULT: '#E2E8F0', // Light text
          light: '#F8FAFC',
          dark: '#94A3B8',
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