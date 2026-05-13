# Тесты для Finance Backend

Этот каталог содержит автоматические тесты для проекта finance-backend (FastAPI + SQLAlchemy).

## Структура тестов

```
tests/
├── conftest.py              # Конфигурация pytest и fixtures
├── __init__.py              # Инициализация пакета
├── test_main.py             # Базовые тесты (проверка работы)
├── test_models_schemas.py   # Тесты моделей и Pydantic схем (работают ✓)
├── test_crud_operations.py  # Тесты CRUD операций
└── README.md                # Эта документация
```

## Запуск тестов

### Установка зависимостей (если не установлены)
```bash
poetry install --with dev
```

### Запустить все тесты
```bash
pytest tests/ -v
```

### Запустить конкретный файл тестов
```bash
pytest tests/test_models_schemas.py -v
```

### Запустить с покрытием кода
```bash
pip install pytest-cov
pytest tests/ --cov=app --cov-report=html --cov-report=term-missing
```

## Статус тестов

### ✅ Рабочие тесты (23 passed)

**test_models_schemas.py** - Все тесты моделей и схем работают:
- Валидация Pydantic схем (transaction_in, transaction_out, account_in, category_in и т.д.)
- Создание объектов SQLAlchemy моделей
- Валидация UUID и дат
- Проверка граничных значений

### ⚠️ Тесты с проблемами (7 failed)

**test_crud_operations.py** - Некоторые тесты требуют доработки:
- Проблемы с валидацией UUID для user_id
- NOT NULL ограничения в моделях Transaction
- Требуются исправления fixtures

### ❌ Тесты с ошибками сборки (43 errors)

**API и интеграционные тесты** - Проблемы с моками:
- `app.main` не содержит атрибута `override_get_db`
- Проблемы с зависимостями Keycloak OAuth2
- Требуется настройка правильного патчинга для TestClient

## Основные Fixtures

```python
# Моковая информация о пользователе (Keycloak format)
@pytest.fixture
def mock_user_info():
    return {
        "id": str(uuid.uuid4()),
        "sub": str(uuid.uuid4()),  # Subject (Keycloak user ID)
        "email": "test@example.com",
        "name": "Test User"
    }

# Тестовая сессия базы данных
@pytest.fixture
def db_session():
    return TestingSessionLocal()

# Fin_app сервис для тестирования бизнес-логики
@pytest.fixture
def fin_app(db_session, mock_user_info):
    return Fin_app(db=db_session, user_info=mock_user_info)
```

## Примеры использования

### Тест модели SQLAlchemy
```python
def test_account_creation(self):
    """Создание объекта счета."""
    from app.models.account import Account, AccountType
    
    account = Account(
        id=uuid.uuid4(),
        name="Test Account",
        currency="USD",
        account_type=AccountType.DEBIT,
        balance=1000.0,
        user_id=uuid.uuid4()
    )
    
    assert isinstance(account.id, uuid.UUID)
    assert account.account_type == AccountType.DEBIT
```

### Тест Pydantic схемы
```python
def test_transaction_in_valid(self):
    """Валидация валидного входного объекта транзакции."""
    from app.schemas.transaction import transaction_in
    
    data = {
        "FROM": None,
        "TO": None,
        "category": None,
        "type": "debit",
        "debitSize": 100.0,
        "creditSize": None,
        "date": date.today().isoformat(),
        "description": "Test transaction",
        "status": "settled"
    }

    result = transaction_in(**data)
    
    assert result.type == "debit"
    assert result.debit_size == 100.0
```

## Советы по написанию новых тестов

1. **Используйте fixtures** для повторного использования кода настройки
2. **Называйте тесты понятно**: `test_<функция>_<ожидаемое_поведение>`
3. **Проверяйте только одно поведение в каждом тесте** (One assertion per test)
4. **Для API тестов** используйте правильные mock'и для зависимостей
5. **Тестируйте как happy path, так и edge cases**

## Устранение проблем с тестами

### Проблема: AttributeError: 'module' object has no attribute 'override_get_db'
**Решение**: Добавьте `override_get_db` в модуль app.main или используйте dependency_overrides правильно:

```python
from fastapi.testclient import TestClient

app = create_fastapi_app()
app.dependency_overrides[get_db] = override_get_db

with TestClient(app) as client:
    response = client.get("/some-endpoint")
```

### Проблема: KeyError: 'sub' при создании Crud объекта
**Решение**: Убедитесь, что mock_user содержит поле 'sub':

```python
mock_user = {
    "id": str(uuid.uuid4()),
    "sub": str(uuid.uuid4()),  # Обязательно для Keycloak совместимости
    "email": "test@example.com",
    "name": "Test User"
}
```

### Проблема: NOT NULL constraint failed в Transaction
**Решение**: Установите значение для credit_size:

```python
transaction_info = transaction_in(
    ...,
    debitSize=100.0,
    creditSize=50.0,  # Не None!
    ...
)
```

## Запуск тестов с метками

```bash
# Только unit-тесты (быстрые, без базы данных)
pytest -m unit -v

# Интеграционные тесты (требуют базу данных)
pytest -m integration -v

# Пропустить медленные тесты
pytest --ignore=tests/test_distributions_and_integration.py
```

## Известные проблемы и TODO

- [ ] Исправить API тесты с моками для TestClient
- [ ] Добавить тесты для Keycloak аутентификации (требует running Keycloak server)
- [ ] Добавить асинхронные тесты для async endpoints
- [ ] Настроить coverage threshold в CI/CD

## Лицензия

Тесты распространяются под той же лицензией, что и основной проект.
