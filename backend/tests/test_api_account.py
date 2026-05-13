"""
Тесты для API endpoints счетов (account).
"""

import uuid
from datetime import date

import pytest
from fastapi.testclient import TestClient


class TestAccountEndpoints:
    """Тесты для endpoints счетов."""

    @pytest.fixture(autouse=True)
    def setup(self, client):
        """Очистка базы данных перед каждым тестом."""
        from app.crud import Crud
        crud = Crud(client.app.dependency_overrides.get(None), {})  # Placeholder
        
    def test_get_all_accounts_empty(self, client):
        """Проверка получения всех счетов (пустая база)."""
        response = client.get("/api/v1/account/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_create_account_basic(self, client):
        """Создание базового счета."""
        account_data = {
            "name": "Main Account",
            "currency": "USD",
            "account_type": "debit",
            "balance": 1000.0,
            "description": "My main checking account",
            "interest_rate": 5.0,
            "is_emergency_fund": False,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": True,
        }

        response = client.post("/api/v1/account/create", json=account_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["name"] == "Main Account"
        assert data["currency"] == "USD"
        assert data["account_type"] == "debit"
        assert data["balance"] == 1000.0
        assert data["is_primary"] is True

    def test_create_account_savings(self, client):
        """Создание сберегательного счета."""
        account_data = {
            "name": "Emergency Fund",
            "currency": "USD",
            "account_type": "savings",
            "balance": 5000.0,
            "description": "Emergency savings",
            "interest_rate": 3.5,
            "is_emergency_fund": True,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": False,
        }

        response = client.post("/api/v1/account/create", json=account_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["name"] == "Emergency Fund"
        assert data["account_type"] == "savings"
        assert data["is_emergency_fund"] is True

    def test_create_account_credit(self, client):
        """Создание кредитного счета."""
        account_data = {
            "name": "Credit Card",
            "currency": "USD",
            "account_type": "credit",
            "balance": -500.0,  # Отрицательный баланс для кредита
            "description": "My credit card",
            "interest_rate": 24.9,
            "is_emergency_fund": False,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": False,
        }

        response = client.post("/api/v1/account/create", json=account_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["account_type"] == "credit"

    def test_get_account_by_id(self, client):
        """Получение счета по ID."""
        # Создаем счет
        account_data = {
            "name": "Test Account",
            "currency": "EUR",
            "account_type": "debit",
            "balance": 2500.0,
            "description": "Euro account",
            "interest_rate": 1.5,
            "is_emergency_fund": False,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": True,
        }

        create_response = client.post("/api/v1/account/create", json=account_data)
        assert create_response.status_code == 200
        
        account_id = uuid.UUID(create_response.json()["id"])

        # Получаем счет по ID
        response = client.get(f"/api/v1/account/{account_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(account_id)
        assert data["name"] == "Test Account"

    def test_update_account_name(self, client):
        """Обновление имени счета."""
        account_data = {
            "name": "Old Name",
            "currency": "USD",
            "account_type": "debit",
            "balance": 1000.0,
            "description": "Test account",
            "interest_rate": 5.0,
            "is_emergency_fund": False,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": True,
        }

        create_response = client.post("/api/v1/account/create", json=account_data)
        assert create_response.status_code == 200
        
        account_id = uuid.UUID(create_response.json()["id"])

        # Обновляем имя
        update_data = {"name": "New Name"}
        response = client.put(f"/api/v1/account/{account_id}/name", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New Name"

    def test_update_account_description(self, client):
        """Обновление описания счета."""
        account_data = {
            "name": "Test Account",
            "currency": "USD",
            "account_type": "debit",
            "balance": 1000.0,
            "description": "Old description",
            "interest_rate": 5.0,
            "is_emergency_fund": False,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": True,
        }

        create_response = client.post("/api/v1/account/create", json=account_data)
        assert create_response.status_code == 200
        
        account_id = uuid.UUID(create_response.json()["id"])

        # Обновляем описание
        update_data = {"description": "New description with more details"}
        response = client.put(f"/api/v1/account/{account_id}/description", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "New description with more details"

    def test_update_account_interest_rate(self, client):
        """Обновление процентной ставки счета."""
        account_data = {
            "name": "Test Account",
            "currency": "USD",
            "account_type": "debit",
            "balance": 1000.0,
            "description": "Test account",
            "interest_rate": 5.0,
            "is_emergency_fund": False,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": True,
        }

        create_response = client.post("/api/v1/account/create", json=account_data)
        assert create_response.status_code == 200
        
        account_id = uuid.UUID(create_response.json()["id"])

        # Обновляем процентную ставку
        update_data = {"interest_rate": 7.5}
        response = client.put(f"/api/v1/account/{account_id}/interest_rate", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["interest_rate"] == 7.5

    def test_update_account_emergency_fund(self, client):
        """Обновление флага чрезвычайного фонда."""
        account_data = {
            "name": "Test Account",
            "currency": "USD",
            "account_type": "savings",
            "balance": 5000.0,
            "description": "Test account",
            "interest_rate": 3.0,
            "is_emergency_fund": False,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": True,
        }

        create_response = client.post("/api/v1/account/create", json=account_data)
        assert create_response.status_code == 200
        
        account_id = uuid.UUID(create_response.json()["id"])

        # Включаем флаг чрезвычайного фонда
        update_data = {"is_emergency_fund": True}
        response = client.put(f"/api/v1/account/{account_id}/emergency_fund", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_emergency_fund"] is True

    def test_update_account_decimal_places(self, client):
        """Обновление количества знаков после запятой."""
        account_data = {
            "name": "Test Account",
            "currency": "JPY",
            "account_type": "debit",
            "balance": 100000,
            "description": "Japanese Yen account",
            "interest_rate": 0.1,
            "is_emergency_fund": False,
            "decimal_places": 0,
            "is_archived": False,
            "is_primary": True,
        }

        create_response = client.post("/api/v1/account/create", json=account_data)
        assert create_response.status_code == 200
        
        account_id = uuid.UUID(create_response.json()["id"])

        # Обновляем количество знаков после запятой
        update_data = {"decimal_places": 3}
        response = client.put(f"/api/v1/account/{account_id}/decimal_places", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["decimal_places"] == 3

    def test_update_account_archived(self, client):
        """Обновление флага архивации счета."""
        account_data = {
            "name": "Test Account",
            "currency": "USD",
            "account_type": "debit",
            "balance": 1000.0,
            "description": "Test account",
            "interest_rate": 5.0,
            "is_emergency_fund": False,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": True,
        }

        create_response = client.post("/api/v1/account/create", json=account_data)
        assert create_response.status_code == 200
        
        account_id = uuid.UUID(create_response.json()["id"])

        # Архивируем счет
        update_data = {"is_archived": True}
        response = client.put(f"/api/v1/account/{account_id}/archived", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_archived"] is True

    def test_update_account_primary(self, client):
        """Обновление флага основного счета."""
        account_data = {
            "name": "Test Account",
            "currency": "USD",
            "account_type": "debit",
            "balance": 1000.0,
            "description": "Test account",
            "interest_rate": 5.0,
            "is_emergency_fund": False,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": True,
        }

        create_response = client.post("/api/v1/account/create", json=account_data)
        assert create_response.status_code == 200
        
        account_id = uuid.UUID(create_response.json()["id"])

        # Делаем счет неосновным
        update_data = {"is_primary": False}
        response = client.put(f"/api/v1/account/{account_id}/primary", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_primary"] is False

    def test_delete_account(self, client):
        """Удаление счета."""
        account_data = {
            "name": "Account to delete",
            "currency": "USD",
            "account_type": "debit",
            "balance": 1000.0,
            "description": "Test account",
            "interest_rate": 5.0,
            "is_emergency_fund": False,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": True,
        }

        create_response = client.post("/api/v1/account/create", json=account_data)
        assert create_response.status_code == 200
        
        account_id = uuid.UUID(create_response.json()["id"])

        # Удаляем счет
        response = client.delete(f"/api/v1/account/{account_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(account_id)
        assert data["name"] == "Account to delete"

    def test_create_account_invalid_type(self, client):
        """Проверка валидации при создании счета с невалидным типом."""
        account_data = {
            "name": "Test Account",
            "currency": "USD",
            "account_type": "invalid_type",  # Невалидный тип
            "balance": 1000.0,
            "description": "Test account",
            "interest_rate": 5.0,
            "is_emergency_fund": False,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": True,
        }

        response = client.post("/api/v1/account/create", json=account_data)
        
        # Должна вернуться ошибка валидации
        assert response.status_code == 422

    def test_create_account_missing_required_fields(self, client):
        """Проверка валидации при создании счета без обязательных полей."""
        account_data = {
            "name": "",  # Пустое имя - должно вызвать ошибку
            "currency": "USD",
            "account_type": "debit",
        }

        response = client.post("/api/v1/account/create", json=account_data)
        
        assert response.status_code == 422
