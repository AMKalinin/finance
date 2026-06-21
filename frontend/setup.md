# 🚀 Быстрый старт FinanceApp Frontend

## Предварительные требования

- **Node.js** версии 18 или выше ([скачать](https://nodejs.org/))
- **npm** (входит в состав Node.js)

## Установка и запуск

### 1. Перейдите в директорию проекта

```bash
cd /home/alex/Documents/finance/frontend
```

### 2. Установите зависимости

```bash
npm install
```

### 3. Запустите сервер разработки

```bash
npm run dev
```

Сервер запустится на: **http://localhost:5173**

## 🎯 Режимы работы

### Демонстрационный режим (по умолчанию)

Приложение работает с мокированными данными без реального бэкенда. Идеально для демонстрации и тестирования UI.

- Все функции работают с mock данными
- Авторизация симулируется через localStorage
- API запросы имитируются

### Режим с реальным бэкендом

Для работы с реальным FastAPI бэкэндом:

1. **Запустите Keycloak сервер** (опционально, для реальной аутентификации)

```bash
docker run -d \
  --name keycloak \
  -p 8080:8080 \
  -e KEYCLOAK_ADMIN=admin \
  -e KEYCLOAK_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak:25.0 start-dev
```

2. **Настройте Keycloak realm**:
   - Зайдите в админку: http://localhost:8080/admin
   - Создайте realm `finance-app`
   - Создайте клиента `finance-frontend`
   - Настройте redirect URI: `http://localhost:5173/`

3. **Запустите FastAPI бэкенд** (опционально):

```bash
cd /home/alex/Documents/finance/backend
uvicorn main:app --reload --port 8000
```

4. **Обновите переменные окружения**:

Создайте файл `.env` в корне frontend:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

5. **Отключите демо-режим** (в `src/keycloak/keycloak-init.js`):

Замените демо-логику на реальную интеграцию с Keycloak.

## 📱 Доступные функции в демо-режиме

### 🔐 Авторизация
- Вход через симулированную форму Keycloak
- Автоматическая проверка аутентификации
- Защита маршрутов

### 🎨 Темы и язык
- Переключение светлой/тёмной темы (☀️/🌙)
- Переключение языка (RU/EN)
- Режим "Авто" для системных настроек

### 💰 Управление счетами
- Просмотр списка счетов
- Создание новых счетов
- Архивация счетов
- Отображение баланса и процентов

### 📊 Транзакции
- Список всех транзакций
- Фильтрация по типу (расходы, доходы, переводы)
- Пагинация результатов
- Детали каждой транзакции

### 📁 Категории
- Древовидная структура категорий
- Разделение на расходы/доходы/переводы
- Вложенность до 3 уровней

### 👥 Друзья
- Запросы на добавление в друзья
- Список друзей с активной активностью
- Совместные транзакции (UI)

## 🔧 Настройка проекта

### Изменение API URL

В файле `vite.config.js` измените прокси:

```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8000', // Ваш бэкенд
    changeOrigin: true,
  },
},
```

### Добавление новых страниц

1. Создайте файл в `src/views/NewPageView.vue`
2. Добавьте маршрут в `src/router/index.js`:

```javascript
{
  path: '/new-page',
  name: 'NewPage',
  component: () => import('@/views/NewPageView.vue'),
}
```

### Изменение стилей

Используйте Tailwind CSS utility classes или добавьте кастомные стили в `src/assets/css/tailwind.css`.

## 🐛 Отладка

### Просмотр консоли разработчика

Откройте DevTools (F12) и перейдите на вкладку Console.

### Проверка состояния приложения

```javascript
// В консоли браузера:
console.log(store.themeStore.isDark);
console.log(store.languageStore.currentLocale);
```

### Сброс демо-данных

```javascript
localStorage.clear();
location.reload();
```

## 📞 Поддержка

При возникновении проблем проверьте:

1. Node.js установлен и версия >= 18
2. Все зависимости установлены (`node_modules`)
3. Порт 5173 не занят другим процессом
4. Файл `package.json` содержит все зависимости

## 📚 Дополнительные ресурсы

- [Vue.js Documentation](https://vuejs.org/)
- [Vite Documentation](https://vitejs.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [Keycloak Documentation](https://www.keycloak.org/documentation.html)

## 📄 Лицензия

MIT License - см. файл LICENSE в корне проекта.
