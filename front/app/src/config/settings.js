/**
 * Настройки приложения в зависимости от среды
 * PRODUCTION - продакшн среда (используется при сборке для production)
 * DEVELOPMENT - среда разработки
 */

// Определение среды: NODE_ENV или VITE_APP_ENV
const isProduction = process.env.NODE_ENV === 'production' ||
                     import.meta.env?.VITE_APP_ENV?.toLowerCase() === 'production'

export const settings = {
  backend: {
    baseUrl: isProduction ? '' : 'http://192.168.0.24:8001/api/v1',
    timeout: 30000,
    retries: 3
  },
  keycloak: {
    url: isProduction ? 'https://myfinsi.ru' : 'http://192.168.0.24:8080',
    realm: 'alkal_realm',
    clientId: 'public-client',
    redirectUri: isProduction ? 'https://myfinsi.ru' : 'http://192.168.0.24:5173'
  }
}

export default settings
