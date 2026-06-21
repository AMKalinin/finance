import Keycloak from 'keycloak-js'

// Конфигурация Keycloak
const keycloakConfig = {
  url: import.meta.env.VITE_KEYCLOAK_URL || 'http://localhost:8080',
  realm: import.meta.env.VITE_KEYCLOAK_REALM || 'finance',
  clientId: import.meta.env.VITE_KEYCLOAK_CLIENT_ID || 'finance-frontend',
}

let keycloak = null
let initialized = false

export const initKeycloak = async () => {
  if (initialized) return keycloak

  if (!keycloak) {
    keycloak = new Keycloak({
      url: keycloakConfig.url,
      realm: keycloakConfig.realm,
      clientId: keycloakConfig.clientId,
    })

    try {
      await keycloak.init({
        onLoad: 'login-required',
        silentCheckSsoRedirectUri: window.location.origin + '/silent-check-sso.html',
        checkLoginIframe: false,
      })
      initialized = true
    } catch (error) {
      console.error('Keycloak init failed:', error)
      initialized = false
      throw error
    }
  }
  return keycloak
}

export const isUserAuthenticated = () => {
  return keycloak?.authenticated || false
}

export const login = async (redirectUri) => {
  await initKeycloak()
  return keycloak.login({ redirectUri })
}

export const logout = async (redirectUri) => {
  if (!keycloak) {
    await initKeycloak()
  }
  return keycloak.logout({ redirectUri })
}

export const getToken = async () => {
  if (!keycloak) {
    await initKeycloak()
  }

  // Обновляем токен если он истекает
  if (keycloak?.isTokenExpired()) {
    try {
      const refreshed = await keycloak.updateToken(300)
      if (refreshed) {
        console.log('Token refreshed')
      }
    } catch (error) {
      console.error('Failed to refresh token:', error)
      return null
    }
  }

  return keycloak?.token || null
}

export const getUsername = () => {
  return keycloak?.tokenParsed?.preferred_username || keycloak?.tokenParsed?.email || null
}

export const getUserInfo = () => {
  return keycloak?.tokenParsed || null
}

export const getKeycloakInstance = () => {
  return keycloak
}
