# Finance Backend

Backend-сервис для управления личными финансами. REST API на базе **FastAPI** с аутентификацией через **Keycloak** и хранением данных в **PostgreSQL** (по умолчанию **SQLite**).

## Архитектура

```
app/
├── api/                      # REST-эндпоинты
│   ├── deps.py               # Зависимости (DB-сессии, Keycloak, сервисы)
│   └── api_v1/
│       ├── api.py            # Маршрутизатор v1
│       └── endpoints/
│           ├── account.py    # CRUD счетов
│           ├── category.py   # CRUD категорий
│           ├── transaction.py # CRUD транзакций, распределений, позиций
│           └── user.py       # Профиль пользователя, друзья
├── core/
│   ├── config.py             # Конфигурация (DB, Keycloak)
│   └── utils.py              # Утилиты (декоратор commit)
├── crud/                     # Слой данных (CRUD-операции)
│   ├── crud_base.py
│   ├── crud_account.py
│   ├── crud_category.py
│   ├── crud_distribution.py
│   ├── crud_position.py
│   ├── crud_transaction.py
│   └── crud_user.py
├── db/
│   ├── base_class.py         # SQLAlchemy Base
│   ├── init_db.py            # Инициализация БД
│   └── session.py            # Движок и сессии
├── err/
│   └── errors.py             # Кастомные исключения
├── models/                   # SQLAlchemy-модели
│   ├── account.py            # Счета (debit, savings, credit, loan)
│   ├── category.py           # Категории расходов/доходов (дерево)
│   ├── transaction.py        # Транзакции (debit, transfer, adding)
│   ├── position.py           # Позиции в транзакциях
│   ├── user.py               # Пользователи, подписки
│   ├── friends.py            # Дружбы между пользователями
│   └── ...
├── schemas/                  # Pydantic-схемы запросов/ответов
├── service/                  # Бизнес-логика
│   ├── fin_app.py            # Сервис финансов (счета, транзакции, категории)
│   └── user_service.py       # Сервис пользователя (профиль, друзья)
└── main.py                   # Точка входа (FastAPI app)
```

## Сущности

| Модель | Описание |
|---|---|
| **User** | Пользователь с типом подписки (`free`/платная) |
| **Account** | Счёт: дебетовый, накопительный, кредитный, долг (взял/дал) |
| **Category** | Иерархическая категория расходов/доходов (до 3 уровней) |
| **Transaction** | Транзакция: расход (`debit`), пополнение (`adding`), перевод (`transfer`) |
| **Position** | Позиция (актив) в рамках транзакции |
| **Transaction_distribution_user** | Распределение доли транзакции между пользователями |
| **Friends** | Отношения дружбы между пользователями |

## API-эндпоинты

Все эндпоинты доступны по префиксу `/api/v1`. Требуется Bearer-токен от Keycloak.

### Accounts (`/api/v1/account`)

| Метод | Путь | Описание |
|---|---|---|
| `GET` | `/` | Получить все счета пользователя |
| `GET` | `/{id}` | Получить счёт по ID |
| `POST` | `/create` | Создать счёт |
| `PUT` | `/{id}/name` | Обновить имя |
| `PUT` | `/{id}/description` | Обновить описание |
| `PUT` | `/{id}/interest_rate` | Обновить процентную ставку |
| `PUT` | `/{id}/emergency_fund` | Обновить флаг «аварийный фонд» |
| `PUT` | `/{id}/decimal_places` | Обновить кол-во знаков после запятой |
| `PUT` | `/{id}/archived` | Архивировать/разархивировать |
| `PUT` | `/{id}/primary` | Установить/снять «основной» счёт |
| `DELETE` | `/{id}` | Удалить счёт |

### Categories (`/api/v1/category`)

| Метод | Путь | Описание |
|---|---|---|
| `GET` | `/` | Получить все категории |
| `POST` | `/create` | Создать категорию |
| `PATCH` | `/` | Обновить категорию |
| `DELETE` | `/{id}` | Удалить категорию |

### Transactions (`/api/v1/transaction`)

| Метод | Путь | Описание |
|---|---|---|
| `GET` | `/all` | Все транзакции |
| `GET` | `/by_period` | Транзакции за период |
| `GET` | `/by_period_type` | Транзакции за период + тип |
| `POST` | `/create` | Создать транзакцию |
| `PUT` | `/{id}/date` | Обновить дату |
| `PUT` | `/{id}/size` | Обновить сумму |
| `PUT` | `/{id}/description` | Обновить описание |
| `DELETE` | `/{id}` | Удалить транзакцию |
| `POST` | `/distribution` | Добавить распределение |
| `PATCH` | `/distribution` | Обновить распределение |
| `DELETE` | `/distribution` | Удалить распределение |
| `POST` | `/position` | Добавить позицию |
| `PATCH` | `/position` | Обновить позицию |

### Users (`/api/v1/user`)

| Метод | Путь | Описание |
|---|---|---|
| `GET` | `/info` | Информация о пользователе |
| `GET` | `/friends` | Список друзей |
| `POST` | `/friend` | Добавить друга |
| `PUT` | `/friend/accept` | Принять запрос в друзья |
| `PUT` | `/friend/reject` | Отклонить запрос в друзья |
| `DELETE` | `/friend` | Удалить друга |

## Быстрый старт

### Требования

- **Python 3.12+**
- **Poetry** (менеджер зависимостей)

### Установка

```bash
# Установка зависимостей
poetry install

# Копирование и настройка переменных окружения
cp .env.example .env   # или отредактировать существующий .env
```

### Запуск

```bash
# Production (4 воркера, без hot-reload)
./run.sh

# Development (1 воркер, с hot-reload)
./run_dev.sh
```

Сервер стартует на `0.0.0.0:8001`.

### Docker

```bash
docker build -t finance-backend .
docker run -p 8001:8001 --env-file .env finance-backend
```

### Тесты

```bash
poetry run pytest
```

### Линтинг и форматирование

```bash
poetry run flake8 app/
poetry run black app/
poetry run isort app/
```

## Переменные окружения

| Переменная | Описание | Пример |
|---|---|---|
| `POSTGRES_SERVER` | Тип БД | `postgresql` / `sqlite` |
| `POSTGRES_USER` | Логин PostgreSQL | `postgres` |
| `POSTGRES_PASSWORD` | Пароль PostgreSQL | `qwerty` |
| `POSTGRES_HOSTNAME` | Хост PostgreSQL | `127.0.0.1` |
| `POSTGRES_PORT` | Порт PostgreSQL | `5432` |
| `POSTGRES_DB` | Имя БД | `my_test_db` |
| `KC_URL` | URL Keycloak | `http://192.168.0.24:8080/` |
| `KC_CLIENT_NAME` | Имя клиента Keycloak | `finsi-client` |
| `KC_REALM_NAME` | Realm Keycloak | `alkal_realm` |
| `KC_CLIENT_SECRET_KEY_FINSI_API` | Секрет клиента | `...` |
| `HOST` | Хост сервера | `0.0.0.0` |
| `PORT` | Порт сервера | `8001` |

> **Примечание:** По умолчанию в `config.py` переопределён URI на `sqlite:///finance_db.sqlite` для локальной разработки без PostgreSQL.

## Технологии

- **FastAPI** — веб-фреймворк
- **SQLAlchemy 2.0** — ORM
- **Uvicorn** — ASGI-сервер
- **Keycloak** — аутентификация (OAuth2 / OpenID Connect)
- **Poetry** — управление зависимостями
- **Black / isort / flake8** — форматирование и линтинг
- **pytest** — тесты
