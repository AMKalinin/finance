/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        'primary-hover': '#2563EB',
        success: '#10B981',
        danger: '#EF4444',
        warning: '#F59E0B',
      },
    },
  },
}
