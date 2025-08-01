import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(
    //   {
    //   template: {
    //     compilerOptions: {
    //       isCustomElement: (tag) => tag === 'PortfolioChart.vue',
    //     },
    //   },
    // }
    ),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    host: '0.0.0.0',
    allowedHosts: ['myfinsi.ru'],
  }
})
