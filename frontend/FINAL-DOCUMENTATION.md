# 📚 Полная документация FinanceApp Frontend

## Оглавление

1. [Введение](#введение)
2. [Архитектура приложения](#архитектура-приложения)
3. [Структура проекта](#структура-проекта)
4. [Настройка окружения](#настройка-окружения)
5. [Компоненты и их описание](#компоненты-и-их-описание)
6. [State management (Pinia)](#state-management-pinia)
7. [Роутинг и навигация](#роутинг-и-навигация)
8. [API интеграция](#api-интеграция)
9. [Keycloak авторизация](#keycloak-авторизация)
10. [Темизация и локализация](#темизация-и-локализация)
11. [Разработка и тестирование](#разработка-и-тестирование)
12. [Production deployment](#production-deployment)

---

## Введение

### Назначение проекта

FinanceApp Frontend - современное веб-приложение для управления личными финансами, разработанное на Vue.js 3 с использованием современных технологий и лучших практик разработки.

### Целевая аудитория

- Пользователи для отслеживания личных финансов
- Администраторы (при наличии подписки)
- Разработчики для интеграции и расширения функционала

### Основные характеристики

| Характеристика | Значение |
|----------------|----------|
| Фреймворк | Vue.js 3.x с Composition API |
| Build tool | Vite 7.x |
| CSS framework | Tailwind CSS 4.x |
| State management | Pinia 3.x |
| Authentication | Keycloak JS 25.x |
| Localization | vue-i18n 11.1 |

---

## Архитектура приложения

### Общий обзор архитектуры

```
┌─────────────────────────────────────────────────────┐
│                  User Browser                       │
├─────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────┐   │
│  │         FinanceApp Frontend (SPA)           │   │
│  ├─────────────────────────────────────────────┤   │
│  │  Router      │  Components    │  Views     │   │
│  │  ─────────   │  ───────────   │  ───────   │   │
│  │  Vue Router  │  Header, etc.  │  Dashboard │   │
│  └─────────────────────────────────────────────┘   │
│                            │                        │
│                   ┌────────▼────────┐              │
│                   │   Pinia Stores  │              │
│                   │  Theme, Lang,   │              │
│                   │    User         │              │
│                   └────────┬────────┘              │
│                            │                        │
│                   ┌────────▼────────┐              │
│                   │     Axios       │              │
│                   │    Client       │              │
│                   └────────┬────────┘              │
└───────────────────────────┼────────────────────────┘
                            │ HTTP/HTTPS
┌───────────────────────────▼────────────────────────┐
│           Backend Services                        │
├────────────────────────────────────────────────────┤
│  ┌──────────────┐    ┌──────────────────────────┐ │
│  │ FastAPI      │    │     Keycloak             │ │
│  │ REST API     │    │   Authentication         │ │
│  └──────────────┘    └──────────────────────────┘ │
└────────────────────────────────────────────────────┘
```

### Принципы архитектуры

1. **Single Page Application (SPA)** - Все приложение загружается один раз, навигация между страницами происходит без перезагрузки
2. **Component-based** - Компоненты изолированы и переиспользуемы
3. **State management** - Централизованное управление состоянием через Pinia
4. **API abstraction** - Абстракция над API запросами с mock данными для тестирования
5. **Security first** - Безопасная обработка токенов авторизации

---

## Структура проекта

### Полная структура файлов

```
frontend/
├── .env.example              # Пример переменных окружения
├── .gitignore               # Git игнор файлы
├── index.html               # HTML шаблон приложения
├── package.json             # npm зависимости и скрипты
├── postcss.config.js        # PostCSS конфигурация для Tailwind
├── tailwind.config.js       # Конфигурация Tailwind CSS
│   ├── content              # Пули к файлам для анализа
│   ├── darkMode             # 'class' - переключение через класс
│   └── theme                # Расширения тем
├── vite.config.js           # Vite конфигурация
│   ├── plugins              # Vue plugin
│   ├── resolve.alias        # Путь к @ (src)
│   └── server.proxy         # Прокси для API запросов
│
├── public/                  # Статические файлы (доступны по URL)
│   └── silent-check-sso.html  # Для Keycloak SSO проверки
│
├── src/                     # Исходный код
│   ├── api/                 # API клиенты и mock данные
│   │   └── client.js        # Основная логика API
│   │       ├── axios.create()     # Axios instance
│   │       ├── interceptors         # Request/Response interceptors
│   │       ├── mockData               # Mock данные для тестирования
│   │       └── API clients          # accountApi, transactionApi, etc.
│   │
│   ├── assets/css/          # Статические стили
│   │   └── tailwind.css     # Tailwind с кастомизацией
│   │       ├── @tailwind directives
│   │       ├── Custom animations
│   │       └── Custom components
│   │
│   ├── components/          # Переиспользуемые компоненты
│   │   └── Header.vue       # Верхняя панель навигации
│   │       ├── Logo & Branding
│   │       ├── Navigation Menu
│   │       ├── Theme Toggle Button
│   │       ├── Language Toggle Button
│   │       ├── User Actions (Avatar, Logout)
│   │
│   ├── i18n/                # Локализация
│   │   └── index.js         # Конфигурация vue-i18n
│   │       ├── createI18n()
│   │       ├── messages.ru  # Русские переводы
│   │       └── messages.en  # Английские переводы
│   │
│   ├── keycloak/            # Keycloak интеграция
│   │   ├── keycloak-init.js         # Инициализация и утилиты
│   │   │   ├── getKeycloakInstance()
│   │   │   ├── isUserAuthenticated()
│   │   │   ├── login()
│   │   │   ├── logout()
│   │   │   ├── getToken()
│   │   │   └── getUsername()
│   │   └── keycloak.json          # Конфигурация клиента Keycloak
│   │       ├── realm: "finance-app"
│   │       ├── resource: "finance-frontend"
│   │       └── public-client: true
│   │
│   ├── router/              # Vue Router конфигурация
│   │   └── index.js         # Роутер и микросхемы навигации
│   │       ├── createRouter()
│   │       ├── routes[]     # Массив маршрутов
│   │       └── beforeEach() # Глобальные микросхемы для защиты
│   │
│   ├── stores/              # Pinia store'ы
│   │   ├── languageStore.js      # Управление языком
│   │   │   ├── currentLocale (ref)
│   │   │   ├── setLanguage(lang)
│   │   │   └── toggleLanguage()
│   │   ├── themeStore.js         # Управление темой
│   │   │   ├── themeMode (ref)
│   │   │   ├── isDark (computed)
│   │   │   └── setThemeMode(mode)
│   │   └── userStore.js          # Информация о пользователе
│   │       ├── userInfo (ref)
│   │       ├── friends (ref)
│   │       ├── isLoading (ref)
│   │       └── fetchUserInfo()
│   │
│   ├── views/               # Страницы приложения (Views)
│   │   ├── DashboardView.vue    # Главная страница
│   │   │   ├── Total Balance Card
│   │   │   ├── Accounts Summary
│   │   │   ├── Expenses by Category
│   │   │   └── Recent Transactions
│   │   ├── AccountsView.vue     # Управление счетами
│   │   │   ├── Accounts Grid
│   │   │   ├── Search & Filters
│   │   │   ├── Account Cards
│   │   │   └── Archive Toggle
│   │   ├── TransactionsView.vue # Транзакции
│   │   │   ├── Transaction List
│   │   │   ├── Period Filter
│   │   │   ├── Type Filter (All/Expenses/Income)
│   │   │   └── Pagination
│   │   ├── CategoriesView.vue   # Категории
│   │   │   ├── Category Tree
│   │   │   ├── Filters (Expense/Income/Transfer)
│   │   │   └── Statistics Panel
│   │   ├── FriendsView.vue      # Друзья
│   │   │   ├── Friend Requests
│   │   │   ├── Friends List
│   │   │   └── Quick Actions
│   │   └── LoginView.vue        # Страница входа
│   │       ├── Keycloak Login Form
│   │       ├── Demo Mode Support
│   │       └── Security Features
│   │
│   ├── App.vue                # Корневой компонент
│   │   ├── Header Component
│   │   ├── Router View
│   │   └── Transition Effects
│   │
│   └── main.js                # Точка входа в приложение
│       ├── createApp(App)
│       ├── use(createPinia())
│       ├── use(i18n)
│       ├── use(router)
│       └── mount('#app')
│
├── README.md                  # Основная документация
├── QUICKSTART.md              # Быстрый старт
├── setup.md                   # Подробные инструкции
├── project-summary.md         # Сводка проекта
├── SUMMARY.md                 # Итоговая сводка
└── FINAL-DOCUMENTATION.md     # Эта документация
```

---

## Настройка окружения

### Переменные окружения

#### .env.example

```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:8000/api/v1

# Keycloak Configuration (optional)
VITE_KEYCLOAK_URL=https://your-keycloak-server.com/auth
VITE_KEYCLOAK_REALM=your-realm
VITE_KEYCLOAK_CLIENT_ID=finance-frontend
```

#### Использование переменных окружения

```javascript
// В коде
const API_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1'

// Доступные переменные:
import.meta.env.MODE          // 'development' | 'production' | 'test'
import.meta.env.BASE_URL      // Базовый URL для ассетов
import.meta.env.PROD          // true если build mode === 'production'
import.meta.env.DEV           // true если !PROD
```

### Настройка Tailwind CSS

#### tailwind.config.js

```javascript
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class', // Переключение через класс на <html>
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        'primary-hover': '#2563EB',
        success: '#10B981',
        danger: '#EF4444',
        warning: '#F59E0B',
      },
      fontFamily: {
        sans: ['Inter', ...],
        mono: ['JetBrains Mono', ...],
      }
    },
  },
}
```

### Настройка Vite

#### vite.config.js

```javascript
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'), // @ = src/
    },
  },
  server: {
    port: 5173,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})
```

---

## Компоненты и их описание

### Header.vue - Верхняя панель навигации

#### Структура компонента

```vue
<template>
  <header class="sticky top-0 z-50 bg-white dark:bg-gray-800">
    <!-- Logo Section -->
    <a href="#" @click.prevent="navigateTo('Dashboard')">
      <div class="logo-icon">₿</div>
      <span>FinanceApp</span>
    </a>

    <!-- Navigation Menu -->
    <nav class="header-nav">
      <button 
        v-for="page in pages" 
        :key="page.name"
        @click="navigateTo(page.name)"
        :class="{ active: currentPage === page.name }"
      >
        {{ page.icon }} {{ page.label }}
      </button>
    </nav>

    <!-- Actions Section -->
    <div class="header-actions">
      <button title="Search">🔍</button>
      <button title="Notifications">🔔</button>
      <button @click="toggleThemeMode" title="Toggle Theme">{{ themeIcon }}</button>
      <button @click="toggleLanguage" title="Switch Language">RU/EN</button>
      <div class="avatar">АК</div>
      <button @click="$emit('logout')">🔒</button>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useThemeStore } from '@/stores/themeStore'
import { useLanguageStore } from '@/stores/languageStore'

const themeStore = useThemeStore()
const languageStore = useLanguageStore()

function navigateTo(pageName) {
  router.push({ name: pageName })
}

const themeIcon = computed(() => 
  themeStore.isDark ? '🌙' : '☀️'
)

function toggleThemeMode() {
  const modes = ['light', 'dark', 'auto']
  const currentIndex = modes.indexOf(themeStore.themeMode)
  themeStore.setThemeMode(modes[(currentIndex + 1) % modes.length])
}

function toggleLanguage() {
  languageStore.toggleLanguage()
}
</script>
```

#### Состояние и props

| Prop | Type | Description |
|------|------|-------------|
| (none) | - | Компонент использует Pinia store'ы напрямую |

#### Events

| Event | Arguments | Description |
|-------|-----------|-------------|
| logout | - | Событие выхода из системы |

### DashboardView.vue - Главная страница

#### Основные блоки

1. **Action Buttons**
   - Создать транзакцию (primary button)
   - Добавить счёт (outline button)

2. **Total Balance Card**
   - Общий баланс всех счетов
   - Индикатор изменения за период (+12%)

3. **Accounts Summary**
   - Список основных счетов с балансом
   - Быстрая ссылка на страницу "Счета"

4. **Expenses & Income Cards**
   - Карточки расходов и доходов за месяц
   - Цветовая индикация (красный/зеленый)

5. **Expenses by Category**
   - Progress bars для категорий расходов
   - Распределение по категориям

6. **Recent Transactions**
   - Последние 3-5 транзакций
   - Краткая информация с иконками

7. **Quick Stats**
   - Всего счетов
   - Транзакций в периоде
   - Количество категорий

### AccountsView.vue - Управление счетами

#### Функциональность

1. **Поиск и фильтрация**
   - Поиск по названию счета
   - Фильтрация по типу (debit, savings, credit)
   - Переключение между активными/архивированными

2. **Сетка счетов**
   - Карточки с информацией о счете
   - Иконка основного счета (⭐)
   - Отображение процентной ставки

3. **Действия со счетом**
   - Редактировать
   - История операций
   - Архивировать/Восстановить

### TransactionsView.vue - Транзакции

#### Фильтры и сортировка

| Filter | Options | Description |
|--------|---------|-------------|
| Period | Май 2025, Этот месяц, Прошлый месяц, Кастомный | Выбор временного периода |
| Type | Все, Расходы, Доходы, Переводы | Фильтрация по типу операции |

#### Отображение транзакций

```vue
<div class="transaction-item">
  <div :class="['icon', type]">{{ icon }}</div>
  <div class="info">
    <h3>{{ name }}</h3>
    <p>{{ category }} | {{ account }}</p>
  </div>
  <span :class="amountClass">{{ formattedAmount }}</span>
  <span class="status-badge">{{ status }}</span>
</div>
```

---

## State management (Pinia)

### Theme Store

#### Хранимое состояние

```javascript
const themeMode = ref('light') // 'light' | 'dark' | 'auto'
const isDark = computed(() => {
  if (themeMode.value === 'auto') {
    return window.matchMedia('(prefers-color-scheme: dark)').matches
  }
  return themeMode.value === 'dark'
})
```

#### Actions

- `setThemeMode(mode)` - Установить тему
- `toggleTheme()` - Переключить между светлой/тёмной
- `updateSystemTheme()` - Обновить по системным настройкам

### Language Store

#### Хранимое состояние

```javascript
const currentLocale = ref('ru') // 'ru' | 'en'
```

#### Actions

- `setLanguage(lang)` - Установить язык
- `toggleLanguage()` - Переключить язык
- `t(key)` - Получить перевод (через useI18n)

### User Store

#### Хранимое состояние

```javascript
const userInfo = ref(null)
const friends = ref([])
const isLoading = ref(false)
```

#### Actions

- `fetchUserInfo()` - Загрузить информацию о пользователе
- `fetchFriends()` - Загрузить список друзей

---

## Роутинг и навигация

### Конфигурация роутера

```javascript
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/accounts',
    name: 'Accounts',
    component: () => import('@/views/AccountsView.vue'),
    meta: { requiresAuth: true },
  },
  // ... другие маршруты
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})
```

### Защита маршрутов

```javascript
router.beforeEach(async (to, from, next) => {
  const isAuthenticated = getToken() || isUserAuthenticated()
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.meta.guestOnly && isAuthenticated) {
    next('/')
  } else {
    next()
  }
})
```

### Навигация программно

```javascript
import { useRouter } from 'vue-router'

const router = useRouter()

// Переход по имени маршрута
router.push({ name: 'Accounts' })

// Переход по пути
router.push('/transactions')

// Навигация с параметрами
router.push({ 
  path: '/transaction',
  query: { id: 123 }
})

// Back/Forward навигация
router.back()
```

---

## API интеграция

### Axios конфигурация

#### Создание клиента

```javascript
import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})
```

#### Request Interceptor - Добавление токена

```javascript
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)
```

#### Response Interceptor - Обработка ошибок

```javascript
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - очистить токен и перенаправить на вход
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    } else if (!navigator.onLine) {
      // Offline mode - очередь запросов
      console.warn('No internet connection. Queueing request.')
      return queueRequest(error.config)
    }
    return Promise.reject(error)
  }
)
```

### Mock данные

#### Структура mock данных

```javascript
const mockData = {
  accounts: [
    {
      id: 1,
      name: 'Основной банковский',
      type: 'debit',
      currency: 'RUB',
      balance: 150000.00,
      isPrimary: true,
      interestRate: 5.5,
    },
    // ... другие счета
  ],
  transactions: [
    {
      id: 1,
      type: 'debit',
      fromAccountId: 1,
      categoryId: 1,
      amount: -3450.00,
      currency: 'RUB',
      description: 'Супермаркет "Лента"',
      date: '2025-05-15',
      status: 'settled'
    },
    // ... другие транзакции
  ],
  categories: [
    { id: 1, name: 'Еда и напитки', type: 'expense', parentId: null },
    // ... другие категории
  ]
}
```

#### Функция имитации задержки сети

```javascript
const simulateNetworkDelay = () => 
  new Promise(resolve => 
    setTimeout(resolve, Math.random() * 500 + 200)
  )
```

### API клиенты

#### Account API

```javascript
export const accountApi = {
  getAll: async (params = {}) => {
    await simulateNetworkDelay()
    return apiClient.get('/account/', { params })
  },
  
  getById: async (id) => {
    await simulateNetworkDelay()
    return mockData.accounts.find(a => a.id === id) || null
  },
  
  create: async (data) => {
    await simulateNetworkDelay()
    const newAccount = { ...data, id: Date.now(), isPrimary: false }
    mockData.accounts.push(newAccount)
    return newAccount
  },
  
  update: async (id, data) => {
    // ... реализация обновления
  },
  
  archive: async (id) => {
    // ... реализация архивации
  },
  
  archived: async () => {
    // ... получение архивированных счетов
  },
  
  primary: async () => {
    // ... получение основного счета
  },
}
```

#### Transaction API

```javascript
export const transactionApi = {
  getAll: async (params = {}) => {
    await simulateNetworkDelay()
    return apiClient.get('/transaction/all', { params })
  },
  
  getByPeriod: async (startDate, endDate) => {
    // ... получение по периоду
  },
  
  create: async (data) => {
    // ... создание транзакции
  },
  
  update: async (id, data) => {
    // ... обновление транзакции
  },
  
  delete: async (id) => {
    // ... удаление транзакции
  },
}
```

#### Category API

```javascript
export const categoryApi = {
  getAll: async () => {
    await simulateNetworkDelay()
    return apiClient.get('/category/')
  },
  
  getExpenses: async () => {
    // ... получение категорий расходов
  },
  
  getIncome: async () => {
    // ... получение категорий доходов
  },
  
  create: async (data) => {
    // ... создание категории
  },
  
  delete: async (id) => {
    // ... удаление категории
  },
}
```

---

## Keycloak авторизация

### Конфигурация Keycloak

#### keycloak.json

```json
{
  "realm": "finance-app",
  "auth-server-url": "http://localhost:8080",
  "ssl-required": "external",
  "resource": "finance-frontend",
  "public-client": true,
  "confidential-port": 0,
  "enable-cors": true,
  "use-resource-role-mappings": false
}
```

### Инициализация Keycloak

#### keycloak-init.js

```javascript
import Keycloak from 'keycloak-js'

let keycloak = null

export const getKeycloakInstance = async () => {
  if (!keycloak) {
    // Поддержка демо-режима без реального Keycloak
    await new Promise((resolve) => {
      const checkKeycloak = () => {
        if (window.Keycloak || localStorage.getItem('demo_token')) {
          resolve()
        } else {
          setTimeout(checkKeycloak, 100)
        }
      }
      checkKeycloak()
    })

    keycloak = new window.Keycloak('/src/keycloak/keycloak.json')
    
    try {
      await keycloak.init({
        onLoad: 'check-sso',
        silentCheckSsoRedirectUri: 
          window.location.origin + '/silent-check-sso.html',
        checkLoginIframe: false,
      })
    } catch (error) {
      console.warn('Keycloak init failed, running in demo mode:', error)
    }
  }
  return keycloak
}

export const isUserAuthenticated = () => {
  // В демо-режиме всегда считаем пользователя авторизованным
  if (!keycloak) return true
  return keycloak.isAuthenticated()
}

export const login = async (redirectUri) => {
  try {
    if (!keycloak) {
      await getKeycloakInstance()
    }
    
    // В демо-режиме симулируем успешный вход
    if (!window.Keycloak || !keycloak.isAuthenticated()) {
      localStorage.setItem('demo_token', 'mock-token-' + Date.now())
      return { success: true }
    }
    
    return keycloak.login({ redirectUri })
  } catch (error) {
    console.warn('Login failed, using demo mode:', error)
    localStorage.setItem('demo_token', 'mock-token-' + Date.now())
    return { success: true }
  }
}

export const logout = async (redirectUri) => {
  if (!keycloak) {
    await getKeycloakInstance()
  }
  
  // Очистка демо-токена при выходе
  localStorage.removeItem('demo_token')
  
  return keycloak.logout({ redirectUri })
}

export const getToken = () => {
  // В демо-режиме используем mock токен
  if (localStorage.getItem('demo_token')) {
    return localStorage.getItem('demo_token')
  }
  
  if (!keycloak || !keycloak.isAuthenticated()) {
    return null
  }
  return keycloak.token
}

export const getUsername = () => {
  // В демо-режиме используем mock имя пользователя
  if (localStorage.getItem('demo_token')) {
    return 'Demo User'
  }
  
  if (!keycloak || !keycloak.isAuthenticated()) {
    return null
  }
  return keycloak.tokenParsed?.preferred_username || 
         keycloak.tokenParsed?.email
}
```

### Flow авторизации

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Browser   │────▶│   Frontend   │────▶│  Keycloak   │
└─────────────┘     └──────────────┘     └─────────────┘
       ▲                   │                     │
       │                   ▼                     │
       │            ┌──────────────┐             │
       │◀───────────│  Token       │◀────────────┤
       │            │   Response   │             │
       └────────────┴──────────────┘             │
                                                 │
                                           ┌─────▼─────┐
                                           │  Session  │
                                           │  Created  │
                                           └───────────┘
```

---

## Темизация и локализация

### Система тем

#### Переключение тем

```javascript
const themeMode = ref('light') // 'light' | 'dark' | 'auto'

function setThemeMode(mode) {
  themeMode.value = mode
  localStorage.setItem('theme_mode', mode)
  
  if (mode === 'auto') {
    updateSystemTheme()
  } else {
    document.documentElement.classList.toggle('dark', mode === 'dark')
  }
}

function toggleTheme() {
  setThemeMode(themeMode.value === 'dark' ? 'light' : 'dark')
}
```

#### Адаптация к системным настройкам

```javascript
function updateSystemTheme() {
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
  
  const handleChange = (e) => {
    document.documentElement.classList.toggle('dark', e.matches)
  }
  
  handleChange(mediaQuery)
  mediaQuery.addEventListener('change', handleChange)
}

// Инициализация при загрузке
if (themeMode.value === 'auto') {
  updateSystemTheme()
} else {
  document.documentElement.classList.toggle('dark', themeMode.value === 'dark')
}
```

### Система локализации

#### Структура переводов

```javascript
const messages = {
  en: {
    nav: {
      dashboard: 'Dashboard',
      accounts: 'Accounts',
      transactions: 'Transactions',
      categories: 'Categories',
      friends: 'Friends',
    },
    actions: {
      createTransaction: 'Create Transaction',
      addAccount: 'Add Account',
      // ... другие переводы
    },
    dashboard: {
      totalBalance: 'Total Balance',
      myAccounts: 'My Accounts',
      expensesMay: 'Expenses (May)',
      incomeMay: 'Income (May)',
      // ... другие переводы
    }
  },
  ru: {
    nav: {
      dashboard: 'Главная',
      accounts: 'Счета',
      transactions: 'Транзакции',
      categories: 'Категории',
      friends: 'Друзья',
    },
    actions: {
      createTransaction: 'Создать транзакцию',
      addAccount: 'Добавить счёт',
      // ... другие переводы
    },
    dashboard: {
      totalBalance: 'Общий баланс',
      myAccounts: 'Мои счета',
      expensesMay: 'Расходы (май)',
      incomeMay: 'Доходы (май)',
      // ... другие переводы
    }
  }
}
```

#### Использование в компонентах

```vue
<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// Получение перевода
const dashboardTitle = t('dashboard.totalBalance') // "Общий баланс" или "Total Balance"

// Перевод с параметрами
const welcomeMessage = t('welcome', { name: 'Alex' }) // "Добро пожаловать, Alex!"
</script>

<template>
  <h1>{{ t('dashboard.totalBalance') }}</h1>
</template>
```

#### Переключение языка

```javascript
function toggleLanguage() {
  setLanguage(currentLocale.value === 'ru' ? 'en' : 'ru')
}
```

---

## Разработка и тестирование

### Команды разработки

```bash
# Запуск dev сервера на http://localhost:5173
npm run dev

# Сборка для продакшена (результат в dist/)
npm run build

# Просмотр сборки локально
npm run preview

# Установка зависимостей
npm install

# Очистка node_modules и установка заново
rm -rf node_modules && npm install

# Лinting (если настроен)
npm run lint
```

### Тестирование функциональности

#### Проверка переключения тем

1. Откройте приложение
2. Нажмите на иконку ☀️ или 🌙 в правом верхнем углу
3. Проверьте изменение цветов интерфейса
4. Попробуйте режим "Авто"
5. Обновите страницу - тема должна сохраниться

#### Проверка переключения языка

1. Нажмите на кнопку RU/EN в правом верхнем углу
2. Проверьте, что все тексты перевелись
3. Переключите обратно и убедитесь в обратном

#### Проверка навигации

1. Используйте меню навигации для перехода между страницами
2. Проверьте, что URL обновляется правильно
3. Попробуйте прямые ссылки на страницы
4. Нажмите кнопку "Назад" в браузере

#### Проверка работы с данными (Demo mode)

1. Создайте новую транзакцию через кнопку "Создать транзакцию"
2. Создайте новый счет через кнопку "Добавить счёт"
3. Отредактируйте существующий счет
4. Попробуйте архивировать счет
5. Проверьте, что данные сохраняются в localStorage

### Отладка

#### Просмотр состояния приложения

```javascript
// В консоли браузера:
console.log('Theme state:', store.themeStore)
console.log('Language state:', store.languageStore)
console.log('User state:', store.userStore)
```

#### Проверка API запросов

1. Откройте DevTools (F12) → Network tab
2. Выполните действие, которое делает API запрос
3. Посмотрите на запросы в Network tab
4. Проверьте headers и response data

#### Логи Keycloak

```javascript
// Включить логирование Keycloak
Keycloak.logger = {
  log: (msg) => console.log('[Keycloak]', msg),
  error: (msg) => console.error('[Keycloak]', msg),
}
```

---

## Production deployment

### Сборка для продакшена

```bash
npm run build
```

Результат сборки находится в папке `dist/`.

### Развёртывание на сервере

#### Вариант 1: Nginx (рекомендуется)

**nginx.conf:**

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    root /var/www/finance-frontend/dist;
    index index.html;
    
    # SPA routing support
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # API proxy (если бэкенд на том же сервере)
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Развёртывание:**

```bash
# Копирование файлов
sudo cp -r dist/* /var/www/finance-frontend/

# Настройка прав
sudo chown -R www-data:www-data /var/www/finance-frontend

# Перезапуск nginx
sudo systemctl restart nginx
```

#### Вариант 2: Docker

**Dockerfile:**

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**Сборка и запуск:**

```bash
docker build -t finance-frontend .
docker run -d -p 80:80 finance-frontend
```

### Оптимизация для продакшена

#### Tree shaking

Vite автоматически выполняет tree shaking, удаляя неиспользуемый код.

#### Code splitting

Компоненты загружаются лениво через динамические import:

```javascript
const DashboardView = () => import('@/views/DashboardView.vue')
```

#### Кэширование

Настройте заголовки для статики:

```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### Мониторинг и аналитика

#### Добавление аналитики

```javascript
// Google Analytics (пример)
if (import.meta.env.PROD) {
  const script = document.createElement('script')
  script.src = 'https://www.googletagmanager.com/gtag/js?id=UA-XXXXX-Y'
  script.async = true
  document.head.appendChild(script)
  
  window.dataLayer = window.dataLayer || []
  function gtag(){dataLayer.push(arguments)}
  window.gtag = gtag
  
  gtag('js', new Date())
  gtag('config', 'UA-XXXXX-Y')
}
```

---

## Заключение

### Итоги разработки

✅ Создано Vue.js 3 приложение для управления личными финансами  
✅ Интегрирована авторизация через Keycloak с поддержкой демо-режима  
✅ Реализована поддержка светлой и тёмной тем  
✅ Добавлена мультиязычность (русский/английский)  
✅ Настроена инфраструктура для работы с API бэкенда  
✅ Созданы mock данные для тестирования без бэ backend  
✅ Реализована полная адаптивность под мобильные устройства  

### Следующие шаги для развития

- [ ] PWA поддержка (offline режим, push уведомления)
- [ ] Экспорт данных в CSV/PDF
- [ ] Интеграция с банковскими API
- [ ] Advanced analytics с ML прогнозированием
- [ ] Мобильное приложение на Ionic/Capacitor
- [ ] Автоматические тесты (Jest, Cypress)

### Благодарности

Спасибо за внимание к проекту FinanceApp!

---

**Версия документации**: 1.0.0  
**Дата создания**: 2025-05-13  
**Статус**: ✅ Полная документация готова
