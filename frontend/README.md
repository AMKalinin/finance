# 💰 FinanceApp Frontend

Веб-приложение для управления личными финансами на Vue.js 3 с интеграцией Keycloak, поддержкой темизации и мультиязычностью.

![Vue.js](https://img.shields.io/badge/Vue.js-3.5-green) ![Vite](https://img.shields.io/badge/Vite-7-blue) ![Tailwind CSS](https://img.shields.io/badge/Tailwind-CSS-orange) ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🌟 Возможности

- ✅ **Аутентификация через Keycloak** - SSO, автоматическое обновление токенов
- ✅ **Светлая и тёмная темы** - Переключение тем с поддержкой системных настроек
- ✅ **Мультиязычность (RU/EN)** - Полная локализация интерфейса
- ✅ **Mock API** - Работа без бэкенда для демонстрации и тестирования
- ✅ **Адаптивный дизайн** - Полная поддержка мобильных устройств и десктопов
- ✅ **Оффлайн режим** - Очередь запросов при отсутствии сети

---

## 🚀 Быстрый старт

### Предварительные требования
- Node.js 18+ 
- npm 9+

### Установка и запуск

```bash
cd /home/alex/Documents/finance/frontend
npm install
npm run dev
```

Откройте **http://localhost:5173** в браузере.

Приложение работает в демо-режиме сразу после запуска!

---

## 📱 Основные функции

### Управление финансами
- 💎 Общий баланс всех счетов с динамикой изменения
- 💰 Управление банковскими счетами (создание, редактирование, архивация)
- 📋 История транзакций с фильтрацией и поиском
- 📁 Категории расходов/доходов с древовидной структурой

### Социальные функции
- 👥 Друзья и совместные транзакции
- 🔔 Уведомления о запросах в друзья и платежах

### Настройки
- 🌙 Переключение светлой/тёмной темы
- 🌐 Язык интерфейса (Русский/English)
- ⚙️ Персонализация отображения данных

---

## 🎨 Интерфейс приложения

### Навигация
```
[Логотип] [Главная][Счета][Транзакции][Категории][Друзья] [🔍][🔔][☀️/🌙][RU/EN][АК][🔒]
```

### Страницы приложения

| Страница | Описание | Иконка |
|----------|----------|--------|
| Главная (Dashboard) | Дашборд, статистика, последние транзакции | 📊 |
| Счета (Accounts) | Управление банковскими счетами и балансами | 💰 |
| Транзакции (Transactions) | История операций с фильтрацией | 📋 |
| Категории (Categories) | Категории расходов/доходов | 📁 |
| Друзья (Friends) | Совместные финансы и друзья | 👥 |

---

## 🛠️ Технологии

### Фронтенд стек
- **Vue.js 3.5** - Progressive JavaScript framework с Composition API
- **Vite 7** - Быстрый build tool и dev server
- **Tailwind CSS 4** - Utility-first CSS framework
- **Pinia 3** - State management для Vue.js
- **Vue Router 4.5** - Официальный роутер

### Интеграции
- **Keycloak JS 25** - Аутентификация и авторизация
- **Axios 1.7** - HTTP клиент
- **Chart.js 4.4 & vue-chartjs 5.3** - Графики и визуализация данных

### Локализация
- **vue-i18n 11.1** - Мультиязычность (русский/английский)

---

## 📁 Структура проекта

```
frontend/
├── public/                    # Статические файлы
│   └── silent-check-sso.html # Для Keycloak SSO
│
├── src/                      # Исходный код
│   ├── api/                  # API клиенты и mock данные
│   │   └── client.js         # Axios конфигурация + Mock
│   │
│   ├── assets/css/           # Стили
│   │   └── tailwind.css      # Tailwind CSS с кастомизацией
│   │
│   ├── components/           # Vue компоненты
│   │   └── Header.vue        # Верхняя панель навигации
│   │
│   ├── i18n/                 # Локализация
│   │   └── index.js          # RU/EN переводы
│   │
│   ├── keycloak/             # Keycloak интеграция
│   │   ├── keycloak-init.js  # Инициализация и утилиты
│   │   └── keycloak.json     # Конфигурация клиента
│   │
│   ├── router/               # Vue Router
│   │   └── index.js          # Конфигурация роутера
│   │
│   ├── stores/               # Pinia store'ы
│   │   ├── languageStore.js  # Управление языком
│   │   ├── themeStore.js     # Управление темой
│   │   └── userStore.js      # Информация о пользователе
│   │
│   ├── views/                # Страницы приложения
│   │   ├── DashboardView.vue
│   │   ├── AccountsView.vue
│   │   ├── TransactionsView.vue
│   │   ├── CategoriesView.vue
│   │   ├── FriendsView.vue
│   │   └── LoginView.vue
│   │
│   ├── App.vue               # Корневой компонент
│   └── main.js               # Точка входа
│
├── .env.example              # Переменные окружения (пример)
├── package.json              # npm зависимости
├── vite.config.js            # Vite конфигурация
├── tailwind.config.js        # Tailwind CSS настройки
└── README.md                 # Эта документация
```

---

## 🔐 Авторизация через Keycloak

### Режимы работы

#### 1. Демо-режим (по умолчанию)
Приложение работает с mock данными и симулированной авторизацией:
- Все функции доступны без реального бэкенда
- Сессия сохраняется в localStorage
- Идеально для демонстрации и тестирования UI

#### 2. Реальный режим
Для работы с реальным Keycloak сервером:

**1. Установите Keycloak:**
```bash
docker run -d \
  --name keycloak \
  -p 8080:8080 \
  -e KEYCLOAK_ADMIN=admin \
  -e KEYCLOAK_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak:25.0 start-dev
```

**2. Настройте realm:**
- Зайдите в админку: http://localhost:8080/admin
- Создайте realm `finance-app`
- Создайте клиента `finance-frontend`
- Настройте redirect URI: `http://localhost:5173/`

**3. Обновите конфиг:**
```bash
cat > .env << 'EOF'
VITE_API_BASE_URL=http://localhost:8000/api/v1
EOF
```

---

## 🌍 Локализация

### Поддерживаемые языки
- **Русский (ru)** - Язык по умолчанию
- **English (en)**

### Переключение языка
Кнопка **RU/EN** в правом верхнем углу интерфейса.

### Добавление нового языка
1. Откройте `src/i18n/index.js`
2. Добавьте переводы в объект `messages`:

```javascript
const messages = {
  en: { ... },
  ru: { ... },
  es: { ... } // Испанский
}
```

3. Обновите функцию переключения языка в `languageStore.js`

---

## 🎨 Темизация

### Поддерживаемые темы
- **Светлая** - По умолчанию, подходит для дневного использования
- **Тёмная** - Для ночного использования, снижает нагрузку на глаза
- **Авто** - Автоматическое переключение по системным настройкам

### Переключение тем
Кнопка **☀️/🌙** в правом верхнем углу интерфейса.

---

## 📊 API Интеграция

### Mock данные (демо-режим)

Приложение использует mock данные для демонстрации функционала:

```javascript
const mockData = {
  accounts: [
    { id, name, type, currency, balance, isPrimary },
    // ...
  ],
  transactions: [
    { id, type, fromAccountId, categoryId, amount, date, status },
    // ...
  ],
  categories: [
    { id, name, type, parentId },
    // ...
  ]
}
```

### Реальные API endpoints (FastAPI бэкенд)

#### Счета
```javascript
GET    /api/v1/account/           # Получить все счета
POST   /api/v1/account/create     # Создать счет
GET    /api/v1/account/{id}       # Получить счёт по ID
PUT    /api/v1/account/{id}/balance  # Обновить баланс
DELETE /api/v1/account/{id}       # Удалить счёт
GET    /api/v1/account/archived   # Архивированные счета
```

#### Транзакции
```javascript
GET    /api/v1/transaction/all          # Все транзакции
GET    /api/v1/transaction/by_period    # По периоду
POST   /api/v1/transaction/create       # Создать транзакцию
```

#### Категории
```javascript
GET    /api/v1/category/              # Все категории
GET    /api/v1/category/type/expenses # Расходы
GET    /api/v1/category/type/income   # Доходы
POST   /api/v1/category/create        # Создать категорию
```

#### Пользователь
```javascript
GET    /api/v1/user/info    # Информация о пользователе
GET    /api/v1/user/friends # Друзья
```

---

## 🚀 Скрипты разработки

```bash
npm run dev           # Запустить dev сервер (http://localhost:5173)
npm run build         # Сборка для продакшена (dist/)
npm run preview       # Просмотр сборки локально
```

### Использование start.sh

Для быстрого запуска используйте скрипт:

```bash
./start.sh
```

---

## 📱 Адаптивность

| Размер экрана | Breakpoint | Особенности |
|---------------|------------|-------------|
| Mobile        | < 768px    | Bottom navigation, карточный вид |
| Tablet        | 768-1024px | Боковая панель/табы |
| Desktop       | > 1024px   | Полная боковая панель навигации |

---

## 🧪 Тестирование

### Ручное тестирование
1. Переключение тем и языков
2. Навигация между страницами
3. Создание/редактирование данных (mock)
4. Ошибки сети (отключить интернет, проверить очередь запросов)
5. Адаптивность на разных устройствах

---

## 🐛 Решение проблем

| Проблема | Решение |
|----------|---------|
| Приложение не запускается | Проверьте Node.js >= 18, выполните `rm -rf node_modules && npm install` |
| Не работают стили | Перезапустите dev сервер, проверьте Tailwind CSS |
| Ошибки Keycloak | В демо-режиме приложение работает без реального Keycloak |
| API запросы не работают | Проверьте VITE_API_BASE_URL в .env файле |

---

## 📚 Документация

- **[QUICKSTART.md](./QUICKSTART.md)** - Быстрый старт за 1 минуту
- **[setup.md](./setup.md)** - Подробные инструкции по настройке
- **[project-summary.md](./project-summary.md)** - Сводка проекта и архитектуры
- **[SUMMARY.md](./SUMMARY.md)** - Итоговая сводка

---

## 🤝 Вклад в проект

### Как внести изменения

1. Fork репозиторий
2. Создайте feature branch: `git checkout -b feature/amazing-feature`
3. Commit ваши изменения: `git commit -m 'Add amazing feature'`
4. Push в branch: `git push origin feature/amazing-feature`
5. Откройте Pull Request

### Конвенции commits
- `feat:` - Новая функция
- `fix:` - Исправление бага
- `docs:` - Изменения документации
- `style:` - Форматирование, отсутствие логики изменений
- `refactor:` - Рефакторинг кода
- `test:` - Добавление тестов
- `chore:` - Обновление зависимостей, конфигурации

---

## 📄 Лицензия

MIT License - см. файл LICENSE в корне проекта.

---

## 👥 Команда разработчиков

**FinanceApp Team** - 2025

---

## 🙏 Благодарности

- [Vue.js team](https://vuejs.org/) за отличный фреймворк
- [Keycloak](https://www.keycloak.org/) за безопасную аутентификацию
- [Tailwind CSS](https://tailwindcss.com/) за удобный CSS framework

---

**Версия**: 1.0.0  
**Дата создания**: 2025-05-13  
**Статус**: ✅ Готово к использованию
