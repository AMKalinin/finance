# Отладка API запросов в FinanceApp Frontend

## 📋 Что изменилось

В этом документе описаны изменения, которые были внесены для обеспечения корректной загрузки реальных счетов и категорий из бэкенда.

---

## 🔧 Основные изменения

### 1. Улучшенная обработка ответов от API

Файл: `src/api/client.js`

```javascript
// Обработка разных форматов ответа от API
const data = response.data || {}
return {
  ...response,
  data: {
    items: (data.items || data) || [],
    total: data.total || 0,
    totalPages: Math.ceil((data.total || 0) / (params?.limit || 20))
  }
}
```

**Почему это важно:** Бэкенд может возвращать данные в разных форматах. Этот код обрабатывает оба варианта:
- `response.data.items` - стандартный формат пагинации
- `response.data` - если items нет, берем всё как items

### 2. Улучшенная загрузка счетов и категорий

Файл: `src/components/Modals/CreateTransactionModal.vue`

```javascript
async function loadAccounts() {
  loadingAccounts.value = true
  try {
    const response = await accountApi.getAll()
    const data = response.data || {}
    // Обработка разных форматов ответа от API
    const items = (data.items || data) || []
    
    accounts.value = items.map(acc => ({
      id: acc.id,
      name: acc.name,
      type: acc.type || acc.account_type,
      currency: acc.currency,
      balance: acc.balance
    }))
  } catch (error) {
    console.error('Ошибка загрузки счетов:', error)
    accounts.value = []
  } finally {
    loadingAccounts.value = false
  }
}
```

**Когда вызывается:** При открытии модального окна создания транзакции.

### 3. Логирование запросов и ответов

Файл: `src/api/client.js`

Добавлено логирование в консоль браузера для отладки:

```javascript
// Логирование запросов
console.log('📡 REQUEST:', {
  url: config.url,
  method: config.method,
  params: config.params,
})

// Логирование ответов
console.log('✅ RESPONSE:', {
  url: response.config.url,
  status: response.status,
  dataLength: JSON.stringify(response.data).length
})
```

---

## 🚀 Как проверить работу

### Шаг 1: Заполнить базу тестовыми данными

Если в базе данных нет счетов и категорий, выполните:

```bash
cd /home/alex/Documents/finance/backend/app
poetry run python scripts/seed_sample_data.py
# ИЛИ
./scripts/init_sample_data.sh
```

### Шаг 2: Запустить фронтенд

```bash
cd /home/alex/Documents/finance/frontend
npm run dev
```

### Шаг 3: Открыть модальное окно создания транзакции

1. Перейдите на страницу **Транзакции** (`/transactions`)
2. Нажмите кнопку **"➕ Создать транзакцию"**
3. Откроется модальное окно - в консоли браузера (F12 → Console) вы увидите:
   ```
   📊 Loading accounts...
   📡 REQUEST: { url: '/api/v1/account/', ... }
   ✅ RESPONSE: { status: 200, dataLength: 5678 }
   ```

### Шаг 4: Проверить в консоли браузера

Откройте консоль (F12 → Console) и проверьте:

```javascript
// Должно быть видно:
📊 Loading accounts...
📡 REQUEST: { url: '/api/v1/account/', ... }
✅ RESPONSE: { status: 200, dataLength: 5678 }

// В модальном окне должны появиться:
• Счет списания: [выпадающий список с реальными счетами]
• Категория: [выпадающий список с реальными категориями]
```

---

## 🔍 Возможные проблемы и решения

### Проблема 1: Пустые выпадающие списки

**Симптомы:**
- В модальном окне "Счет" и "Категория" пустые
- В консоли видно `📡 REQUEST` но нет данных в ответе

**Причины:**
1. Нет счетов/категорий в базе данных
2. Бэкенд не возвращает данные правильно
3. Пользователь не авторизован (Keycloak)

**Решение:**
```bash
# 1. Проверьте, что вы вошли в систему
# 2. Заполните базу тестовыми данными
cd /home/alex/Documents/finance/backend/app
poetry run python scripts/seed_sample_data.py
```

### Проблема 2: Ошибка 401 Unauthorized

**Симптомы:**
- В консоли: `Error: 401 Unauthorized`
- Перенаправление на страницу входа

**Причины:**
- Сессия Keycloak истекла
- Нет токена авторизации

**Решение:**
```bash
# Просто войдите в систему заново
# Токен автоматически обновится при следующем запросе
```

### Проблема 3: Ошибка соединения с бэкендом

**Симптомы:**
- В консоли: `Network Error` или `Failed to fetch`
- Нет ответа от `/api/v1/account/`

**Причины:**
- Бэкенд не запущен
- API_BASE_URL неверный в .env файле

**Решение:**
```bash
# Проверьте .env файл в frontend/
cat /home/alex/Documents/finance/frontend/.env

# Должно быть:
VITE_API_BASE_URL=/api/v1  # или http://localhost:8001/api/v1

# Запустите бэкенд
cd /home/alex/Documents/finance/backend/app
uvicorn main:app --reload
```

---

## 📊 Структура данных в базе

### Пример счета (Account)

```json
{
  "id": "uuid-тут",
  "name": "Сбербанк",
  "currency": "RUB",
  "balance": 50000.0,
  "account_type": "debit",
  "description": "Сбербанк (тестовый счет)"
}
```

### Пример категории (Category)

```json
{
  "id": "uuid-тут",
  "name": "Еда",
  "type": "expense",
  "level": 1,
  "parent_id": null
}
```

---

## 🎯 Как добавить свои данные

### Добавить счет вручную

```bash
cd /home/alex/Documents/finance/backend/app
poetry run python -c "
from app.crud.crud_account import CRUD_account
from schemas.account import account_in
crud = CRUD_account()
acc = crud.create_account(account_in(
    name='Мой счет',
    currency='RUB',
    balance=10000.0,
    account_type='debit'
))
print(f'Создан счет: {acc.name}')
"
```

### Добавить категорию вручную

```bash
cd /home/alex/Documents/finance/backend/app
poetry run python -c "
from app.crud.crud_category import CRUD_category
from schemas.category import category_in
crud = CRUD_category()
cat = crud.create_category(category_in(
    name='Моя категория',
    type='expense',
    level=1,
    parent_category=None
))
print(f'Создана категория: {cat.name}')
"
```

---

## 📚 Дополнительные ресурсы

- [src/api/client.js](../../src/api/client.js) - API клиент с логированием
- [src/components/Modals/CreateTransactionModal.vue](../../src/components/Modals/CreateTransactionModal.vue) - Модальное окно создания транзакций
- [scripts/seed_sample_data.py](../../../backend/scripts/seed_sample_data.py) - Скрипт заполнения БД тестовыми данными

---

**Последнее обновление:** 2026-06-15
