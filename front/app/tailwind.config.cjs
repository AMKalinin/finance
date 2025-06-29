module.exports = {
  purge: false,
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'sidebar': '#1A1D1F',
        'main': '#F4F4F4',
      }
    },
  },
  plugins: [],
}
