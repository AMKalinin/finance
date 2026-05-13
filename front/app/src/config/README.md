# Конфигурация приложения

## Обзор

Файл `settings.js` содержит базовые настройки для подключения к бэкенду и Keycloak. Настройки автоматически выбираются в зависимости от среды запуска:

- **Production** (`NODE_ENV=production` или `VITE_APP_ENV=production`)
  - Backend: относительные пути (через nginx/proxy)
  - Keycloak: `https://myfinsi.ru`

- **Development** (по умолчанию, если не указана production)
  - Backend: `http://192.168.0.24:8001/api/v1`
  - Keycloak: `http://192.168.0.24:8080`

## Переменные окружения

### .env.development (для разработки)
```bash
VITE_APP_ENV=development
NODE_ENV=development
```

### .env.production (для продакшена)
```bash
VITE_APP_ENV=production
NODE_ENV=production
```

## Использование

### В API запросах
```javascript
import { settings } from '@/config/settings'

// Настройки автоматически применяются через axios.defaults
axios.get('/account/') // использует settings.backend.baseUrl
```

### В Keycloak конфигурации
```javascript
import { initKeycloak } from '@/keycloak/keycloak'

// Использует настройки из settings.keycloak
await initKeycloak()
```

## Запуск в разработке
```bash
npm run dev  # автоматически загружает .env.development
```

## Сборка для продакшена
```bash
npm run build  # автоматически загружает .env.production
```
