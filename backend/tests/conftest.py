"""
Конфигурация pytest-тестов для finance-backend проекта.
Содержит fixtures для настройки базы данных, тестовых клиентов и моков.
"""

import os
import uuid
from datetime import date
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Используем SQLite для тестов
SQLALCHEMY_DATABASE_URL = "sqlite:///test_finance_db.sqlite"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Переопределение зависимости get_db для использования тестовой БД."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Импортируем после определения engine
from app.core.config import settings
from app.db.base_class import Base
from app.main import create_fastapi_app
from app.service.fin_app import Fin_app
from app.service.user_service import User_service

settings.SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URL.replace("sqlite:///test_", "sqlite:///")


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Создаем базу данных перед запуском тестов и очищаем после."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session() -> Generator:
    """Тестовая сессия базы данных."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session):
    """Тестовый клиент FastAPI."""
    with patch("app.api.deps.get_db", side_effect=override_get_db), \
         patch("app.main.override_get_db", side_effect=override_get_db):
        app = create_fastapi_app()
        app.dependency_overrides[settings] = MagicMock()
        yield TestClient(app)


@pytest.fixture
def mock_user_info():
    """Мок пользовательской информации для тестирования Fin_app.
    
    Структура соответствует данным от Keycloak.
    """
    return {
        "id": str(uuid.uuid4()),
        "sub": str(uuid.uuid4()),  # Subject (Keycloak user ID)
        "email": "test@example.com",
        "name": "Test User"
    }


@pytest.fixture
def fin_app(db_session, mock_user_info):
    """Fin_app сервис с тестовой сессией и пользователем."""
    return Fin_app(db=db_session, user_info=mock_user_info)


# ============================================================================ #
#                               Тестовые данные                                #
# ============================================================================ #

@pytest.fixture
def test_account_data():
    """Тестовые данные для создания счета."""
    return {
        "name": "Test Account",
        "currency": "USD",
        "account_type": "debit",
        "balance": 1000.0,
        "description": "Test account for testing",
        "interest_rate": 5.0,
        "is_emergency_fund": False,
        "decimal_places": 2,
        "is_archived": False,
        "is_primary": True,
    }


@pytest.fixture
def test_transaction_data():
    """Тестовые данные для создания транзакции."""
    return {
        "FROM": None,
        "TO": None,
        "category": None,
        "type": "debit",
        "debitSize": 100.0,
        "creditSize": None,
        "exchangeRate": None,
        "date": date.today(),
        "description": "Test transaction",
        "splitType": None,
        "status": "settled",
    }


@pytest.fixture
def test_category_data():
    """Тестовые данные для создания категории."""
    return {
        "name": "Food",
        "type": "expense",
        "parent_category": None,
        "level": 0,
        "is_deleted": False,
    }


@pytest.fixture
def test_distribution_data():
    """Тестовые данные для распределения."""
    return {
        "user_id": str(uuid.uuid4()),
        "transaction_id": str(uuid.uuid4()),
        "role": "owner",
        "size": 50.0,
        "is_settled": False,
    }


@pytest.fixture
def test_position_data():
    """Тестовые данные для позиции."""
    return {
        "transaction_id": str(uuid.uuid4()),
        "name": "Stock",
        "quantity": 10.0,
        "price": 25.0,
        "currency": "USD",
    }
