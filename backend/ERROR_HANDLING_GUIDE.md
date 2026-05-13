# Руководство по обработке ошибок в Finance API

## 📋 Обзор системы обработки ошибок

Finance Backend использует централизованную систему обработки ошибок с автоматической конвертацией кастомных исключений в HTTP-ответы.

### Основные принципы

1. **Все ошибки наследуются от `BaseAPIError`** - это обеспечивает единообразие
2. **Автоматическая обработка** - все исключения перехватываются и форматируются
3. **Логирование** - каждая ошибка логируется с контекстом запроса
4. **Четкие коды ошибок** - каждый тип ошибки имеет уникальный код

---

## 🎯 Кастомные исключения

### Базовый класс

```python
from app.err.errors import BaseAPIError

# Использование:
raise BaseAPIError(
    message="Сообщение для пользователя",
    detail="Подробное описание ошибки",
    code="CUSTOM_ERROR_CODE",  # Уникальный код ошибки
    status_code=400
)
```

### Категории исключений

#### 🔐 Аутентификация и авторизация

| Исключение | HTTP Status | Описание |
|------------|-------------|----------|
| `AuthenticationError` | 401 | Неверные учетные данные или токен истек |
| `AuthorizationError` | 403 | Недостаточно прав для выполнения действия |

#### ⚠️ Валидация данных

| Исключение | HTTP Status | Описание |
|------------|-------------|----------|
| `ValidationError` | 422 | Ошибка валидации входных данных (поля, типы) |
| `InvalidUUIDError` | 422 | Неверный формат UUID |
| `InvalidDateError` | 422 | Неверный формат даты (не YYYY-MM-DD) |

#### 🔍 Найдено или нет

| Исключение | HTTP Status | Описание |
|------------|-------------|----------|
| `NotFoundError` | 404 | Ресурс не найден |
| `AccountNotFoundError` | 404 | Учетная запись не найдена |
| `CategoryNotFoundError` | 404 | Категория не найдена |
| `TransactionNotFoundError` | 404 | Транзакция не найдена |
| `UserNotFoundError` | 404 | Пользователь не найден |
| `FriendNotFoundError` | 404 | Друг не найден |
| `DistributionNotFoundError` | 404 | Распределение не найдено |
| `PositionNotFoundError` | 404 | Позиция не найдена |

#### 💾 База данных

| Исключение | HTTP Status | Описание |
|------------|-------------|----------|
| `DatabaseError` | 500 | Общая ошибка базы данных |

#### 📊 Бизнес-логика

| Исключение | HTTP Status | Описание |
|------------|-------------|----------|
| `SubscriptionError` | 402 | Доступно только для платных подписок |
| `MaxCategoryLevelError` | 400 | Достигнут максимальный уровень вложенности категорий |
| `InsufficientFundsError` | 400 | Недостаточно средств на счете |

#### 🔄 Транзакции и распределения

| Исключение | HTTP Status | Описание |
|------------|-------------|----------|
| `InvalidTransactionTypeError` | 400 | Некорректный тип транзакции |
| `SplitError` | 400 | Ошибка при создании распределения (сумма != 100%) |
| `DistributionError` | 400 | Ошибка создания/обновления распределения |

#### 👥 Друзья и подписки

| Исключение | HTTP Status | Описание |
|------------|-------------|----------|
| `AlreadyFriendError` | 409 | Пользователь уже в друзьях |
| `PendingRequestError` | 409 | Запрос в дружбе еще не подтвержден |

---

## 🚀 Использование в коде

### Пример 1: Проверка существования ресурса

```python
from app.err.errors import AccountNotFoundError, NotFoundError

def get_account_by_id(db: Session, account_id: UUID) -> Account:
    """Получить учетную запись по ID."""
    account = db.query(Account).filter(Account.id == account_id).first()
    
    if not account:
        raise AccountNotFoundError(str(account_id))
    
    return account

# Или универсально:
account = get_account_by_id(db, account_id) or \
    raise NotFoundError("Учетная запись", str(account_id))
```

### Пример 2: Валидация входных данных

```python
from app.err.errors import InvalidUUIDError, ValidationError

def create_transaction(transaction_data: dict):
    # Проверка UUID
    try:
        account_id = UUID(transaction_data['account_id'])
    except ValueError:
        raise InvalidUUIDError("account_id")
    
    # Проверка даты
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', transaction_data['date']):
        raise InvalidDateError()
```

### Пример 3: Проверка прав доступа

```python
from app.err.errors import AuthorizationError, UserNotFoundError

def update_account(account_id: UUID, user_info: dict):
    account = get_account_by_id(db, account_id)
    
    if account.user_id != user_info['sub']:
        raise AuthorizationError("Вы не можете редактировать этот счет")
```

### Пример 4: Проверка баланса

```python
from app.err.errors import InsufficientFundsError

def withdraw_money(account_id: UUID, amount: float):
    account = get_account_by_id(db, account_id)
    
    if account.balance < amount:
        raise InsufficientFundsError(str(account.name))
    
    account.balance -= amount
```

### Пример 5: Проверка распределения

```python
from app.err.errors import SplitError

def create_distribution(transaction_id: UUID, share_percentage: float):
    # Получить все существующие распределения
    existing_distributions = get_all_distributions(transaction_id)
    
    total_share = sum(d.percentage for d in existing_distributions) + share_percentage
    
    if abs(total_share - 100.0) > 0.01:
        raise SplitError(f"Сумма долей должна составлять 100%, сейчас: {total_share}%")
```

---

## 📝 Ответы API

### Успешный ответ (200 OK)

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Счет в рублях",
  "balance": 50000.0
}
```

### Ошибка (например, 404 Not Found)

```json
{
  "error": "ACCOUNT_NOT_FOUND",
  "message": "Учетная запись не найдена: 550e8400-e29b-41d4-a716-446655440000",
  "detail": "Учетная запись не найдена: 550e8400-e29b-41d4-a716-446655440000"
}
```

### Ошибка валидации (422 Unprocessable Entity)

```json
{
  "error": "VALIDATION_ERROR",
  "message": "Ошибка валидации данных",
  "details": [
    {
      "field": "body.date",
      "error_type": "value_error.datetime",
      "message": "неверный формат даты"
    }
  ]
}
```

### Ошибка сервера (500 Internal Server Error)

```json
{
  "error": "DATABASE_ERROR",
  "message": "Ошибка базы данных: Нарушение целостности данных",
  "exception_type": "IntegrityError"
}
```

---

## 🐛 Обработка ошибок в зависимостях

### Зависимость для получения пользователя

```python
from fastapi import Depends
from app.api.deps import get_current_user, get_db
from app.service.fin_app import Fin_app

# В эндпоинте:
def create_transaction(
    transaction_data: TransactionCreate,
    fin_app: Fin_app = Depends(get_fin_service)  # Использует авторизацию
):
    ...
```

### Обработка ошибок в зависимости `get_db`

```python
from app.err.errors import DatabaseError

def get_db() -> Generator[SessionLocal, None, None]:
    db = SessionLocal()
    try:
        yield db
        db.commit()  # Коммитим при успехе
    except Exception as e:
        logger.error(f"Database error: {e}")
        db.rollback()  # Откатываем при ошибке
        raise DatabaseError(f"Ошибка базы данных: {str(e)}")
    finally:
        db.close()
```

---

## 📊 Логирование ошибок

Все ошибки логируются автоматически. Пример лога:

```
2025-01-15 14:30:22 - app.err.handlers - WARNING - BaseAPIError: ACCOUNT_NOT_FOUND - Учетная запись не найдена
path: /api/v1/account/550e8400-e29b-41d4-a716-446655440000
method: GET
detail: Учетная запись не найдена: 550e8400-e29b-41d4-a716-446655440000
```

### Настройка уровня логирования

В `main.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,  # DEBUG для детальной отладки
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

## 🧪 Тестирование обработки ошибок

### Пример теста с Pytest

```python
import pytest
from fastapi.testclient import TestClient
from app.err.errors import AccountNotFoundError, NotFoundError

def test_account_not_found(client: TestClient):
    """Проверка обработки несуществующей учетной записи."""
    
    # Создаем UUID, которого нет в базе
    fake_id = "00000000-0000-0000-0000-000000000000"
    
    response = client.get(f"/api/v1/account/{fake_id}")
    
    assert response.status_code == 404
    data = response.json()
    
    assert "error" in data
    assert data["error"] == "ACCOUNT_NOT_FOUND"


def test_invalid_uuid_format(client: TestClient):
    """Проверка обработки невалидного UUID."""
    
    response = client.get("/api/v1/account/not-a-uuid")
    
    # Это может вызвать ошибку валидации или NotFoundError
    assert response.status_code in [422, 404]
```

---

## 🔄 Расширение системы ошибок

### Добавление нового типа ошибки

1. Создайте класс исключения в `app/err/errors.py`:

```python
class PermissionDeniedError(BaseAPIError):
    """Ошибка при недостатке прав."""
    
    def __init__(self, resource: str = None):
        message = f"Нет доступа к '{resource}'" if resource else "Нет доступа"
        super().__init__(message, code="PERMISSION_DENIED", status_code=403)
```

2. Добавьте в список обработчиков в `app/err/handlers.py`:

```python
for error_class in [
    # ... существующие классы
    PermissionDeniedError,  # Добавить новый
]:
    app.add_exception_handler(error_class, base_api_error_handler)
```

---

## 📚 Полезные ссылки

- [FastAPI Exceptions](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [Pydantic Validation Errors](https://docs.pydantic.dev/usage/validation_errors/)
- [HTTP Status Codes RFC 7231](https://tools.ietf.org/html/rfc7231)

---

## ⚡ Best Practices

1. **Всегда используйте кастомные исключения** вместо `raise HTTPException(...)`
2. **Добавляйте контекст в message** - что именно не найдено/ошибкалось
3. **Используйте detail для технической информации** (stack trace, параметры)
4. **Логгируйте все ошибки** с достаточным контекстом для отладки
5. **Не раскрывайте детали ошибок пользователю в production**

---

## 🚨 Troubleshooting

### Проблема: Ошибка не перехватывается

**Решение:** Проверьте, что класс исключения добавлен в список обработчиков в `handlers.py`.

### Проблема: Странное поведение с BaseException

**Решение:** Не наследуйте от `BaseException`, только от `Exception` или `BaseAPIError`.

### Проблема: Конфликт статус-кодов

**Решение:** Убедитесь, что каждый тип ошибки имеет уникальный `status_code` и `code`.
