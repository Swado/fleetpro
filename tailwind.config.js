/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
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
      },
    },
  },
  plugins: [],
}