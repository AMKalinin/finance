"""
Тесты для API endpoints транзакций.
"""

import uuid
from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.transaction import Transaction


class TestTransactionEndpoints:
    """Тесты для endpoints транзакций."""

    @pytest.fixture(autouse=True)
    def setup(self, client, fin_app):
        """Настройка перед каждым тестом - очистка базы данных."""
        # Очистим распределения и позиции
        from app.crud import Crud
        crud = Crud(fin_app.db, fin_app.user_info)
        
        transactions = crud.transaction.get_all_transaction()
        for t in transactions:
            crud.distribution.delete_all_distributions(t.id)
            crud.position.delete_by_transaction_id(t.id)
            crud.transaction.delete(t.id)

    def test_get_all_transactions_empty(self, client, fin_app):
        """Проверка получения всех транзакций (пустая база)."""
        response = client.get("/api/v1/transaction/all")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_create_transaction_debit(self, client, fin_app, mock_user_info):
        """Создание транзакции типа debit."""
        # Сначала создадим счет
        account_data = {
            "name": "Test Account",
            "currency": "USD",
            "account_type": "debit",
            "balance": 1000.0,
            "description": "Account for testing",
            "interest_rate": 5.0,
            "is_emergency_fund": False,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": True,
        }

        # Создаем счет через API
        response = client.post("/api/v1/account/create", json=account_data)
        assert response.status_code == 200
        account_id = uuid.UUID(response.json()["id"])

        transaction_data = {
            "FROM": str(account_id),
            "TO": None,
            "category": None,
            "type": "debit",
            "debitSize": 100.0,
            "creditSize": None,
            "exchangeRate": None,
            "date": date.today().isoformat(),
            "description": "Test debit transaction",
            "splitType": None,
            "status": "settled",
        }

        response = client.post("/api/v1/transaction/create", json=transaction_data)
        assert response.status_code == 200
        data = response.json()
        
        assert data["type"] == "debit"
        assert data["debitSize"] == 100.0
        assert data["description"] == "Test debit transaction"

    def test_create_transaction_adding(self, client, fin_app):
        """Создание транзакции типа adding."""
        account_data = {
            "name": "Savings Account",
            "currency": "USD",
            "account_type": "savings",
            "balance": 0.0,
            "description": "Savings for testing",
            "interest_rate": 3.0,
            "is_emergency_fund": False,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": True,
        }

        response = client.post("/api/v1/account/create", json=account_data)
        assert response.status_code == 200
        account_id = uuid.UUID(response.json()["id"])

        transaction_data = {
            "FROM": None,
            "TO": str(account_id),
            "category": None,
            "type": "adding",
            "debitSize": 500.0,
            "creditSize": None,
            "exchangeRate": None,
            "date": date.today().isoformat(),
            "description": "Deposit to savings",
            "splitType": None,
            "status": "settled",
        }

        response = client.post("/api/v1/transaction/create", json=transaction_data)
        assert response.status_code == 200
        data = response.json()
        
        assert data["type"] == "adding"
        assert data["debitSize"] == 500.0

    def test_create_transaction_transfer(self, client, fin_app):
        """Создание транзакции типа transfer."""
        # Создаем два счета для перевода
        account1_data = {
            "name": "Checking Account",
            "currency": "USD",
            "account_type": "debit",
            "balance": 2000.0,
            "description": "Checking for testing",
            "interest_rate": 0.0,
            "is_emergency_fund": False,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": True,
        }

        account2_data = {
            "name": "Savings Account",
            "currency": "USD",
            "account_type": "savings",
            "balance": 0.0,
            "description": "Savings for testing",
            "interest_rate": 3.0,
            "is_emergency_fund": False,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": True,
        }

        response1 = client.post("/api/v1/account/create", json=account1_data)
        response2 = client.post("/api/v1/account/create", json=account2_data)

        assert response1.status_code == 200 and response2.status_code == 200
        
        from_account_id = uuid.UUID(response1.json()["id"])
        to_account_id = uuid.UUID(response2.json()["id"])

        transaction_data = {
            "FROM": str(from_account_id),
            "TO": str(to_account_id),
            "category": None,
            "type": "transfer",
            "debitSize": 100.0,
            "creditSize": 100.0,
            "exchangeRate": 1.0,
            "date": date.today().isoformat(),
            "description": "Transfer between accounts",
            "splitType": None,
            "status": "settled",
        }

        response = client.post("/api/v1/transaction/create", json=transaction_data)
        assert response.status_code == 200
        data = response.json()
        
        assert data["type"] == "transfer"
        assert data["from_account_id"] == str(from_account_id)
        assert data["to_account_id"] == str(to_account_id)

    def test_get_transactions_by_period(self, client, fin_app):
        """Получение транзакций за период."""
        # Создаем две транзакции с разными датами
        account_data = {
            "name": "Test Account",
            "currency": "USD",
            "account_type": "debit",
            "balance": 1000.0,
            "description": "Account for testing",
            "interest_rate": 5.0,
            "is_emergency_fund": False,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": True,
        }

        client.post("/api/v1/account/create", json=account_data)

        today = date.today()
        
        transaction1 = {
            "FROM": None,
            "TO": None,
            "category": None,
            "type": "debit",
            "debitSize": 100.0,
            "creditSize": None,
            "exchangeRate": None,
            "date": (today - timedelta(days=5)).isoformat(),
            "description": "Transaction 1",
            "splitType": None,
            "status": "settled",
        }

        transaction2 = {
            "FROM": None,
            "TO": None,
            "category": None,
            "type": "debit",
            "debitSize": 200.0,
            "creditSize": None,
            "exchangeRate": None,
            "date": (today - timedelta(days=1)).isoformat(),
            "description": "Transaction 2",
            "splitType": None,
            "status": "settled",
        }

        client.post("/api/v1/transaction/create", json=transaction1)
        client.post("/api/v1/transaction/create", json=transaction2)

        # Запрос транзакций за последние 3 дня
        response = client.get(
            f"/api/v1/transaction/by_period?from_date={today.isoformat()}&to_date={today.isoformat()}"
        )
        assert response.status_code == 200
        data = response.json()

    def test_get_transactions_by_type(self, client, fin_app):
        """Получение транзакций по типу за период."""
        account_data = {
            "name": "Test Account",
            "currency": "USD",
            "account_type": "debit",
            "balance": 1000.0,
            "description": "Account for testing",
            "interest_rate": 5.0,
            "is_emergency_fund": False,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": True,
        }

        client.post("/api/v1/account/create", json=account_data)

        today = date.today()

        # Создаем транзакции разных типов
        debit_transaction = {
            "FROM": None,
            "TO": None,
            "category": None,
            "type": "debit",
            "debitSize": 100.0,
            "creditSize": None,
            "exchangeRate": None,
            "date": today.isoformat(),
            "description": "Debit transaction",
            "splitType": None,
            "status": "settled",
        }

        adding_transaction = {
            "FROM": None,
            "TO": None,
            "category": None,
            "type": "adding",
            "debitSize": 200.0,
            "creditSize": None,
            "exchangeRate": None,
            "date": today.isoformat(),
            "description": "Adding transaction",
            "splitType": None,
            "status": "settled",
        }

        client.post("/api/v1/transaction/create", json=debit_transaction)
        client.post("/api/v1/transaction/create", json=adding_transaction)

        # Запрос только debit транзакций
        response = client.get(
            f"/api/v1/transaction/by_period_type?from_date={today.isoformat()}&to_date={today.isoformat()}&operation_type=debit"
        )
        assert response.status_code == 200
        data = response.json()

    def test_update_transaction_size(self, client, fin_app):
        """Обновление размера транзакции."""
        account_data = {
            "name": "Test Account",
            "currency": "USD",
            "account_type": "debit",
            "balance": 1000.0,
            "description": "Account for testing",
            "interest_rate": 5.0,
            "is_emergency_fund": False,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": True,
        }

        client.post("/api/v1/account/create", json=account_data)

        transaction = {
            "FROM": None,
            "TO": None,
            "category": None,
            "type": "debit",
            "debitSize": 100.0,
            "creditSize": None,
            "exchangeRate": None,
            "date": date.today().isoformat(),
            "description": "Test transaction to update",
            "splitType": None,
            "status": "settled",
        }

        create_response = client.post("/api/v1/transaction/create", json=transaction)
        assert create_response.status_code == 200
        
        transaction_id = uuid.UUID(create_response.json()["id"])

        # Обновляем размер
        update_data = {"size": 150.0}
        response = client.put(f"/api/v1/transaction/{transaction_id}/size", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["debitSize"] == 150.0

    def test_update_transaction_date(self, client, fin_app):
        """Обновление даты транзакции."""
        account_data = {
            "name": "Test Account",
            "currency": "USD",
            "account_type": "debit",
            "balance": 1000.0,
            "description": "Account for testing",
            "interest_rate": 5.0,
            "is_emergency_fund": False,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": True,
        }

        client.post("/api/v1/account/create", json=account_data)

        original_date = date(2025, 1, 1)
        new_date = date(2025, 6, 15)

        transaction = {
            "FROM": None,
            "TO": None,
            "category": None,
            "type": "debit",
            "debitSize": 100.0,
            "creditSize": None,
            "exchangeRate": None,
            "date": original_date.isoformat(),
            "description": "Test transaction to update date",
            "splitType": None,
            "status": "settled",
        }

        create_response = client.post("/api/v1/transaction/create", json=transaction)
        assert create_response.status_code == 200
        
        transaction_id = uuid.UUID(create_response.json()["id"])

        # Обновляем дату
        update_data = {"date": new_date.isoformat()}
        response = client.put(f"/api/v1/transaction/{transaction_id}/date", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert date.fromisoformat(data["date"]) == new_date

    def test_update_transaction_description(self, client, fin_app):
        """Обновление описания транзакции."""
        account_data = {
            "name": "Test Account",
            "currency": "USD",
            "account_type": "debit",
            "balance": 1000.0,
            "description": "Account for testing",
            "interest_rate": 5.0,
            "is_emergency_fund": False,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": True,
        }

        client.post("/api/v1/account/create", json=account_data)

        transaction = {
            "FROM": None,
            "TO": None,
            "category": None,
            "type": "debit",
            "debitSize": 100.0,
            "creditSize": None,
            "exchangeRate": None,
            "date": date.today().isoformat(),
            "description": "Original description",
            "splitType": None,
            "status": "settled",
        }

        create_response = client.post("/api/v1/transaction/create", json=transaction)
        assert create_response.status_code == 200
        
        transaction_id = uuid.UUID(create_response.json()["id"])

        # Обновляем описание
        update_data = {"description": "Updated description"}
        response = client.put(f"/api/v1/transaction/{transaction_id}/description", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "Updated description"

    def test_delete_transaction(self, client, fin_app):
        """Удаление транзакции."""
        account_data = {
            "name": "Test Account",
            "currency": "USD",
            "account_type": "debit",
            "balance": 1000.0,
            "description": "Account for testing",
            "interest_rate": 5.0,
            "is_emergency_fund": False,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": True,
        }

        client.post("/api/v1/account/create", json=account_data)

        transaction = {
            "FROM": None,
            "TO": None,
            "category": None,
            "type": "debit",
            "debitSize": 100.0,
            "creditSize": None,
            "exchangeRate": None,
            "date": date.today().isoformat(),
            "description": "Transaction to delete",
            "splitType": None,
            "status": "settled",
        }

        create_response = client.post("/api/v1/transaction/create", json=transaction)
        assert create_response.status_code == 200
        
        transaction_id = uuid.UUID(create_response.json()["id"])

        # Удаляем транзакцию
        response = client.delete(f"/api/v1/transaction/{transaction_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(transaction_id)
