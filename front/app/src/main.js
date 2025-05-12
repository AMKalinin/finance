// import './assets/main.css'

import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router/router'
import { initKeycloak, getToken } from './keycloak/keycloak.js'
import axios from 'axios'



axios.interceptors.request.use(
  (config) => {
    const token = getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)


const app = createApp(App)

initKeycloak()
  .then((authenticated) => {
    if (!authenticated) {
      console.warn('User is not authenticated')
    }
    app.use(router)
    app.mount('#app')
  })
  .catch((error) => {
    console.error('Keycloak initialization failed', error)
  })

