module.exports = {
  purge: false,
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class', // Включаем поддержку тёмной темы
  theme: {
    extend: {
      colors: {
        'sidebar': '#1A1D1F',
        'main': '#F4F4F4',
        'surface': '#FFFFFF',
        'primary': '#6366f1',
      },
      screens: {
        'xs': '480px',  // Добавляем breakpoint для очень маленьких экранов
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
        '2xl': '1536px',
      },
    },
  },
  plugins: [],
}
