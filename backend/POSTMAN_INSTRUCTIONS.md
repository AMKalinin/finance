# Postman Collection для Finance API

## 📦 Обзор коллекции

В эту коллекцию включены все эндпоинты Finance Backend API (FastAPI):
- **User & Friends** — управление пользователями и друзьями
- **Account Management** — учетные записи (банковские счета, карты, наличные)
- **Category Management** — категории расходов/доходов с поддержкой вложенности
- **Transaction Management** — транзакции (расходы, доходы, переводы)
- **Distribution Management** — распределение совместных расходов
- **Position Management** — управление позициями (активы: акции, криптовалюты)

## 🚀 Установка и использование

### 1. Импорт коллекции

В Postman нажмите:
- `File` → `Import`
- Выберите файл `postman_collection.json`
- Также импортируйте `postman_environment.json` как окружение

**Обновления:**
- Добавлена пагинация для всех списков (skip, limit)
- Новые эндпоинты: `/account/archived`, `/account/primary`
- Новые эндпоинты категорий: `/category/type/expenses`, `/category/type/income`

### 2. Настройка окружения

Выберите окружение **Finance API - Environment** из выпадающего списка в правом верхнем углу.

Переменные окружения:
| Переменная | Описание | Значение по умолчанию |
|------------|----------|----------------------|
| `baseUrl` | Базовый URL API | `http://localhost:8000/api/v1` |
| `userId` | UUID пользователя | Заполняется автоматически |
| `accountId` | UUID учетной записи | Заполняется после создания счета |
| `categoryId` | UUID категории | Заполняется после создания категории |
| `transactionId` | UUID транзакции | Заполняется после создания транзакции |

### 3. Запуск сервера

Перед тестированием запустите сервер:

```bash
# В проекте finance/backend
cd /home/alex/Documents/finance/backend

# Вариант 1: Скрипт запуска
./run.sh

# Вариант 2: Для разработки
./run_dev.sh

# Или вручную
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📝 Примеры использования

### 1. Создание учетной записи и сохранение ID

```json
// POST /account/create
{
  "name": "Счет в рублях",
  "currency": "RUB",
  "balance": 50000,
  "description": "Основной банковский счет",
  "interest_rate": null,
  "is_emergency_fund": false,
  "decimal_places": 2,
  "is_archived": false,
  "is_primary": true,
  "account_type": "bank"
}
```

После успешного создания сохраните `id` из ответа в переменную `accountId`.

### 2. Создание транзакции с распределением

```json
// POST /transaction/create
{
  "FROM": null,
  "TO": "{{accountId}}",
  "category": null,
  "type": "debit",
  "debitSize": 5000,
  "creditSize": null,
  "exchangeRate": null,
  "date": "2025-01-15",
  "description": "Покупка продуктов",
  "splitType": "equal",
  "status": "settled"
}
```

### 3. Добавление распределения к транзакции

```json
// POST /transaction/distribution
{
  "userId": null,
  "transactionId": "{{transactionId}}",
  "role": "participant",
  "size": 2500,
  "percentage": null
}
```

### 4. Добавление позиции (актив) к транзакции

```json
// POST /transaction/position
{
  "name": "AAPL",
  "transactionId": "{{transactionId}}",
  "price": 150.25,
  "quantity": 10
}
```

## 🔄 Автоматизация переменных (Postman Tests)

Добавьте следующие тесты для автоматического сохранения ID в переменные:

### Для создания учетной записи (`/account/create`)

```javascript
pm.test("Save account ID", function () {
    var jsonData = pm.response.json();
    pm.environment.set("accountId", jsonData.id);
});
```

### Для создания категории (`/category/create`)

```javascript
pm.test("Save category ID", function () {
    var jsonData = pm.response.json();
    pm.environment.set("categoryId", jsonData.id);
});
```

### Для создания транзакции (`/transaction/create`)

```javascript
pm.test("Save transaction ID", function () {
    var jsonData = pm.response.json();
    pm.environment.set("transactionId", jsonData.id);
});
```

## 🧪 Рекомендуемый порядок тестирования

1. **Get All Accounts** — проверить начальные данные
2. **Create Account - Basic** — создать новый счет, сохранить `accountId`
3. **Get All Categories (Structured)** — проверить категории
4. **Create Category - Root Level** — создать категорию, сохранить `categoryId`
5. **Create Transaction - Debit** — создать расход, сохранить `transactionId`
6. **Add Distribution to Transaction** — добавить распределение
7. **Settle Distribution** — пометить как оплаченное
8. **Get Transactions by Period** — проверить транзакции за период

## 🔑 Типы учетных записей (account_type)

| Значение | Описание |
|----------|----------|
| `bank` | Банковский счет/карта |
| `cash` | Наличные |
| `card` | Кредитная карта |
| `crypto` | Криптовалюта |
| `investment` | Инвестиции |

## 📊 Типы транзакций (type)

| Значение | Описание |
|----------|----------|
| `debit` | Расход (деньги уходят со счета) |
| `adding` | Доход/пополнение (деньги приходят на счет) |
| `transfer` | Перевод между счетами |

## ⚠️ Важные замечания

1. **UUID format**: Все UUID должны быть в стандартном формате: `550e8400-e29b-41d4-a716-446655440000`
2. **Дата**: Используйте формат YYYY-MM-DD (например, `2025-01-15`)
3. **Статусы транзакций**: 
   - `pending` — ожидает подтверждения
   - `partially_paid` — частично оплачено
   - `settled` — полностью оплачено

## 🌐 Переменные окружения для продакшена

Для тестирования на удаленном сервере измените переменную `baseUrl`:

```json
{
  "baseUrl": "https://your-api-domain.com/api/v1"
}
```

## 📄 Структура коллекции

```
Finance API Collection
├── User & Friends
│   ├── Get User Info
│   ├── Get Friends List
│   ├── Add Friend
│   ├── Accept Friend Request
│   ├── Reject Friend Request
│   └── Delete Friend
├── Account Management
│   ├── Get All Accounts
│   ├── Create Account - Basic
│   ├── Get Account by ID
│   ├── Update Account Balance
│   ├── Update Account Name
│   ├── Update Account Description
│   ├── Update Interest Rate
│   ├── Update Emergency Fund Flag
│   ├── Update Decimal Places
│   ├── Update Archived Status
│   ├── Update Primary Status
│   └── Delete Account
├── Category Management
│   ├── Get All Categories (Structured)
│   ├── Create Category - Root Level
│   ├── Create Category - Subcategory
│   ├── Update Category Name
│   └── Delete Category
├── Transaction Management - Basic
│   ├── Get All Transactions
│   ├── Get Transactions by Period
│   ├── Get Transactions by Period and Type
│   ├── Create Transaction - Debit
│   ├── Create Transaction - Adding
│   ├── Create Transaction - Transfer
│   ├── Update Transaction Date
│   ├── Update Transaction Size
│   ├── Update Transaction Description
│   └── Delete Transaction
├── Transaction Distribution Management
│   ├── Add Distribution to Transaction
│   ├── Update Distribution
│   ├── Delete Distribution
│   └── Settle Distribution
└── Transaction Position Management
    ├── Add Position to Transaction
    └── Update Position
```

## 🐛 Устранение неполадок

### Ошибка 401 Unauthorized
Убедитесь, что вы используете правильный URL и сервер запущен.

### Ошибка 404 Not Found
Проверьте, что UUID существуют в базе данных. Используйте GET запросы для получения существующих ID.

### Ошибка 422 Validation Error
Проверьте формат входных данных:
- UUID должен быть в правильном формате
- Дата должна быть YYYY-MM-DD
- Числовые значения должны быть корректными типами

## 📞 Поддержка

При возникновении проблем проверьте:
1. Сервер запущен и доступен по `http://localhost:8000`
2. База данных (finance_db.sqlite) существует и не повреждена
3. Все зависимости установлены (`poetry install`)
