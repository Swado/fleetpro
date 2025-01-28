import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: '#F5F6FA',
        primary: {
          DEFAULT: '#2C3E50',
          dark: '#1a252f',
          light: '#34495E',
        },
        accent: {
          DEFAULT: '#E67E22',
          dark: '#d35400',
          light: '#f39c12',
        },
        text: '#34495E',
      },
    },
  },
  plugins: [],
}

export default config