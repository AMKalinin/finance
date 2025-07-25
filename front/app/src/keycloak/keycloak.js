import Keycloak from 'keycloak-js'

const keycloakConfig = {
  url: 'https://myfinsi.ru',
  realm: 'alkal_realm',
  clientId: 'public-client'
}

const keycloak = new Keycloak(keycloakConfig)

export const initKeycloak = () => {
  return keycloak.init({
    onLoad: 'login-required', // автоматически перенаправляет на страницу входа
    checkLoginIframe: false,
    pkceMethod: 'S256',
    redirectUri: 'https://myfinsi.ru'
  })
}

export const getKeycloak = () => keycloak

export const logout = () => {
  return keycloak.logout()
}

export const getToken = () => {
  return keycloak.token
}

export const isAuthenticated = () => {
  return !!keycloak.authenticated
}

export const updateToken = (minValidity = 5) => {
  return keycloak.updateToken(minValidity)
}

export const getUserInfo = () => {
  try {
    keycloak.updateToken(30)
    return keycloak.tokenParsed
  } catch (error) {
    console.error('Failed to get user info', error)
    return null
  }
}

