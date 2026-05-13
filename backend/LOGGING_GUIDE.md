# 📝 Руководство по логированию в Finance Backend

## 🎯 Обзор системы логирования

Finance Backend использует продвинутую систему логирования с поддержкой:
- **Структурированных логов** (JSON формат для продакшена)
- **Контекста запросов** (request ID, пользователь, счет, транзакция)
- **Цветного вывода** в режиме разработки
- **Ротации файлов** (автоматическое разделение по размеру)

---

## 🚀 Быстрый старт

### 1. Импорт логгера

```python
from app.logging_config import get_logger, logger

# Получите логгер для вашего модуля
logger = get_logger(__name__)

# Или используйте глобальный логгер
from app.logging_config import logger
```

### 2. Базовое использование

```python
logger.debug("Подробная информация для отладки")
logger.info("Обычная информационная запись")
logger.warning("Предупреждение, но приложение продолжает работать")
logger.error("Ошибка, требующая внимания")
logger.critical("Критическая ошибка, приложение может не функционировать")
```

### 3. Логирование с контекстом

```python
# Добавление контекста запроса
logger.info(
    "Транзакция создана",
    extra={
        "user_id": str(user_id),
        "account_id": str(account_id),
        "transaction_id": str(transaction_id)
    }
)
```

---

## 📊 Форматы логов

### Текстовый формат (разработка)

```text
[INFO] [2025-01-15 14:30:22] finance.api - Account created successfully
[INFO] [2025-01-15 14:30:23] [abc12345] finance.http - Request: GET /api/v1/account/
```

### JSON формат (продакшен)

```json
{
  "timestamp": "2025-01-15T14:30:22.123456",
  "level": "INFO",
  "logger": "finance.api",
  "message": "Account created successfully",
  "module": "account.py",
  "function": "create_account",
  "line": 42,
  "request_id": "abc12345",
  "user_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

## 🔧 Настройка логирования

### Через конфигурацию

В `app/core/config.py`:

```python
class Settings:
    DEBUG: bool = True  # Если True - текстовый формат, иначе JSON
    
LOG_LEVEL: str = "DEBUG" if DEBUG else "INFO"
```

### Программная настройка

```python
from app.logging_config import setup_logging

# Текстовый лог в консоль (для разработки)
logger = setup_logging(
    log_level="DEBUG",
    log_format="text"
)

# JSON лог в файл (для продакшена)
logger = setup_logging(
    log_level="INFO",
    log_format="json",
    log_file="/var/log/finance-api/app.log",
    max_bytes=10*1024*1024,  # 10 MB
    backup_count=5            # Хранить 5 старых файлов
)
```

---

## 📦 Контекст запроса

### RequestIDFilter

Каждому HTTP запросу присваивается уникальный ID:

```python
# В логах будет видно:
[INFO] [2025-01-15 14:30:22] [abc12345] finance.http - Request: GET /api/v1/account/
[INFO] [2025-01-15 14:30:23] [abc12345] finance.http - Response: GET /api/v1/account/ - 200 OK
```

### StructuredLogger

Позволяет добавлять контекст к каждому логированию:

```python
from app.logging_config import logger, log_request_context

# Логирование с контекстом пользователя и транзакции
logger.info(
    "Создание транзакции",
    extra={
        "user_id": str(user.id),
        "account_id": str(account.id),
        "transaction_id": str(transaction.id)
    }
)

# Или через bind (для цепочки логов одного запроса)
request_logger = logger.bind(
    user_id=str(user.id),
    account_id=str(account.id)
)

request_logger.info("Начало обработки транзакции")
request_logger.info("Транзакция успешно создана")
```

---

## 🎨 Middleware для HTTP запросов

### RequestLoggingMiddleware

Автоматически логирует все HTTP запросы и ответы:

```python
from app.main import create_fastapi_app

app = create_fastapi_app()

# Добавление middleware (автоматически в режиме разработки)
app.add_middleware(RequestLoggingMiddleware)
```

#### Пример логов из middleware:

**Входящий запрос:**
```json
{
  "timestamp": "2025-01-15T14:30:22.123456",
  "level": "INFO",
  "logger": "finance.http",
  "message": "Request: GET /api/v1/account/",
  "http_path": "/api/v1/account/",
  "http_method": "GET",
  "query_params": "",
  "client_host": "192.168.1.100"
}
```

**Исходящий ответ:**
```json
{
  "timestamp": "2025-01-15T14:30:22.456789",
  "level": "INFO",
  "logger": "finance.http",
  "message": "Response: GET /api/v1/account/ - 200 OK",
  "http_path": "/api/v1/account/",
  "http_method": "GET",
  "status_code": 200,
  "duration_ms": 333.33,
  "request_id": "abc12345"
}
```

---

## 🐛 Отладка и поиск проблем

### Поиск по request ID

Все логи одного запроса имеют одинаковый `request_id`:

```bash
# Найти все логи для конкретного запроса
grep "abc12345" /var/log/finance-api/app.log

# Или в текстовом формате
grep "\[abc12345\]" /var/log/finance-api/app.log
```

### Поиск ошибок по пользователю

```bash
# Найти все логи с указанием user_id
grep "user_id.*550e8400" /var/log/finance-api/app.log | jq -r 'select(.level == "ERROR")'
```

### Поиск проблемных запросов (медленных)

```bash
# Найти запросы, которые выполнялись дольше 1 секунды
grep '"duration_ms":' /var/log/finance-api/app.log | jq -s 'map(select(.duration_ms > 1000))'
```

---

## 📁 Структура логов

### Логи по модулям

| Модуль | Назначение | Пример имени логгера |
|--------|------------|---------------------|
| `finance.app` | Основной код приложения | `finance.app.main` |
| `finance.api` | REST API эндпоинты | `finance.api.deps` |
| `finance.crud` | Работа с БД | `finance.crud.transaction` |
| `finance.service` | Бизнес-логика | `finance.service.fin_app` |
| `finance.err` | Обработка ошибок | `finance.err.handlers` |
| `finance.http` | HTTP запросы/ответы | `finance.http.middleware` |

### Логи по уровням

```bash
# Только ошибки и выше
grep '"level": "ERROR"' app.log
grep '"level": "CRITICAL"' app.log

# Предупреждения и выше
grep '"level": "WARNING"' app.log

# Все логи
cat app.log
```

---

## 🧪 Примеры использования

### Пример 1: Логирование в эндпоинте

```python
from fastapi import APIRouter, Depends
from app.logging_config import get_logger

logger = get_logger(__name__)

@router.get("/{id}")
def get_account(id: UUID):
    logger.info(f"Получение счета", extra={"account_id": str(id)})
    
    try:
        account = db.query(Account).filter(Account.id == id).first()
        
        if not account:
            logger.warning(f"Счет не найден", extra={"account_id": str(id)})
            raise AccountNotFoundError(str(id))
        
        logger.info(f"Счет получен успешно", extra={"account_id": str(id)})
        return account
        
    except Exception as e:
        logger.error(
            f"Ошибка при получении счета",
            extra={
                "account_id": str(id),
                "error_type": type(e).__name__
            },
            exc_info=True  # Записать stack trace
        )
        raise
```

### Пример 2: Логирование в CRUD операциях

```python
from app.logging_config import get_logger

logger = get_logger(__name__)

def create_transaction(db: Session, transaction_data: dict):
    logger.info(
        "Создание транзакции",
        extra={
            "transaction_type": transaction_data.get("type"),
            "amount": transaction_data.get("debit_size")
        }
    )
    
    try:
        # ... логика создания
        
        logger.info(
            "Транзакция успешно создана",
            extra={"transaction_id": str(transaction.id)}
        )
        
        return transaction
        
    except Exception as e:
        logger.error(
            f"Ошибка при создании транзакции: {e}",
            exc_info=True
        )
        raise
```

### Пример 3: Логирование в обработчиках ошибок

```python
from app.err.handlers import base_api_error_handler, get_logger

logger = get_logger(__name__)

async def base_api_error_handler(request: Request, exc: BaseAPIError):
    logger.warning(
        f"BaseAPIError: {exc.code} - {exc.message}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "detail": exc.detail,
            "status_code": exc.status_code
        }
    )
    
    return JSONResponse(...)
```

---

## 🔍 Анализ логов

### Просмотр логов в реальном времени

```bash
# В режиме разработки (текстовый вывод)
tail -f /var/log/finance-api/app.log

# Или через journalctl (если используется systemd)
journalctl -u finance-api -f
```

### Поиск ошибок в логах

```bash
# Python JSON формат
grep '"level": "ERROR"' app.log | jq '.'

# Текстовый формат
grep "ERROR" app.log

# Только критические ошибки
grep "CRITICAL" app.log
```

### Анализ производительности

```bash
# Найти самые медленные запросы (топ 10)
grep '"duration_ms":' app.log | \
    jq -s 'sort_by(.duration_ms) | reverse | .[0:10]'
```

---

## 🎯 Best Practices

### ✅ Делайте

1. **Используйте контекст** для трассировки запросов
2. **Логгируйте ошибки с exc_info=True** для stack trace
3. **Разделяйте уровни логирования**: DEBUG для отладки, INFO для информации, ERROR для проблем
4. **Не логгируйте чувствительные данные** (пароли, токены, PII)

### ❌ Не делайте

1. **Не используйте print()** - только logger
2. **Не логгируйте полные объекты** - только нужные поля
3. **Не оставляйте DEBUG логи в production**
4. **Не храните логи без ротации** (будет заполнен диск)

---

## 📊 Мониторинг и алертинг

### Prometheus metrics

```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).add()
```

### Логирование метрик

```python
logger.info(
    "Метрика: транзакций_создано",
    extra={"metric": "transactions_created", "value": 1}
)
```

---

## 🔄 Ротация логов

Файлы логов автоматически разделяются по размеру:

- **max_bytes**: Максимальный размер одного файла (по умолчанию 10 MB)
- **backup_count**: Количество сохраняемых файлов (по умолчанию 5)

Пример структуры после ротации:
```
/var/log/finance-api/
├── app.log              # Текущий файл
├── app.log.1            # Предыдущий (до 10 MB)
├── app.log.2.gz         # Архивированный (сжатый)
├── app.log.3.gz
└── app.log.4.gz
```

---

## 📞 Troubleshooting

### Проблема: Логи не появляются в консоли

**Решение:** Проверьте уровень логирования:
```python
logger.setLevel(logging.DEBUG)  # Для отладки
```

### Проблема: JSON формат ломается

**Решение:** Убедитесь, что все значения сериализуемы:
```python
# ❌ Неверно
extra={"object": some_object}

# ✅ Верно
extra={"object_id": str(some_object.id)}
```

### Проблема: Логи слишком подробные

**Решение:** Увеличьте уровень логирования:
```python
setup_logging(log_level="WARNING")  # Только предупреждения и ошибки
```

---

## 📚 Дополнительные ресурсы

- [Python logging HOWTO](https://docs.python.org/3/howto/logging.html)
- [Structlog -结构化 логирование](https://www.structlog.org/)
- [JSON logging best practices](https://github.com/oliver-gierke/structured-logging)

---

**Дата:** 9 мая 2025  
**Версия системы логирования:** 1.0.0
