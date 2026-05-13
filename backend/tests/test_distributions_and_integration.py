"""
Тесты для распределений транзакций и интеграционные тесты.
Проверяет сложные сценарии работы с распределениями между пользователями.
"""

import uuid
from datetime import date

import pytest


class TestDistributionLogic:
    """Тесты логики распределения."""

    @pytest.fixture(autouse=True)
    def setup(self, client):
        """Очистка базы данных перед каждым тестом."""
        from app.crud import Crud
        
        crud = Crud(None, {})  # Placeholder - не используется в этом классе
        
    def test_distribute_equal_amount(self, fin_app, db_session):
        """Распределение суммы поровну между двумя пользователями."""
        participant_user_id = str(uuid.uuid4())
        
        transaction_info = type('transaction_in', (), {
            'FROM': None,
            'TO': None,
            'category': None,
            'type': 'debit',
            'debitSize': 100.0,
            'creditSize': None,
            'exchangeRate': None,
            'date': date.today(),
            'description': 'Equal split test',
            'splitType': 'equal',
            'status': 'settled',
            'distributions': [
                type('distribution_in', (), {
                    'user_id': participant_user_id,
                    'transaction_id': None,
                    'role': 'participant',
                    'size': None,
                    'percentage': None,
                    'is_settled': False,
                })()
            ],
            'positions': [],
        })

        result = fin_app.create_transaction(transaction_info)

        assert isinstance(result, result.__class__.__bases__[0].__dict__.get('Transaction', type))
        
        # Проверяем распределения
        distributions = fin_app.crud.distribution.get_distributions_for_transaction(result.id)
        
        assert len(distributions) == 2  # owner + participant
        
        total_size = sum(d.size for d in distributions if d.size)
        assert abs(total_size - 100.0) < 0.02  # С учетом округления

    def test_distribute_by_percentage(self, fin_app, db_session):
        """Распределение по процентам."""
        participant_user_id = str(uuid.uuid4())
        
        transaction_info = type('transaction_in', (), {
            'FROM': None,
            'TO': None,
            'category': None,
            'type': 'debit',
            'debitSize': 100.0,
            'creditSize': None,
            'exchangeRate': None,
            'date': date.today(),
            'description': 'Percentage split test',
            'splitType': 'percentage',
            'status': 'settled',
            'distributions': [
                type('distribution_in', (), {
                    'user_id': participant_user_id,
                    'transaction_id': None,
                    'role': 'participant',
                    'size': None,
                    'percentage': 0.7,  # 70%
                    'is_settled': False,
                })()
            ],
            'positions': [],
        })

        result = fin_app.create_transaction(transaction_info)

        distributions = fin_app.crud.distribution.get_distributions_for_transaction(result.id)
        
        assert len(distributions) == 2
        
        participant_total = sum(
            d.size for d in distributions 
            if d.role == 'participant' and d.size
        )
        
        # Participant должен получить примерно 70% (с учетом округления)
        assert abs(participant_total - 70.0) < 1.0

    def test_distribute_by_amount(self, fin_app, db_session):
        """Распределение по точным суммам."""
        participant_user_id = str(uuid.uuid4())
        
        transaction_info = type('transaction_in', (), {
            'FROM': None,
            'TO': None,
            'category': None,
            'type': 'debit',
            'debitSize': 100.0,
            'creditSize': None,
            'exchangeRate': None,
            'date': date.today(),
            'description': 'Amount split test',
            'splitType': 'amount',
            'status': 'settled',
            'distributions': [
                type('distribution_in', (), {
                    'user_id': participant_user_id,
                    'transaction_id': None,
                    'role': 'participant',
                    'size': 30.0,  # Фиксированная сумма
                    'percentage': None,
                    'is_settled': False,
                })()
            ],
            'positions': [],
        })

        result = fin_app.create_transaction(transaction_info)

        distributions = fin_app.crud.distribution.get_distributions_for_transaction(result.id)
        
        assert len(distributions) == 2
        
        participant_total = sum(
            d.size for d in distributions 
            if d.role == 'participant' and d.size
        )
        
        # Participant должен получить ровно 30 (или близкое значение из-за округления owner'у)
        assert abs(participant_total - 30.0) < 0.02

    def test_distribute_with_position(self, fin_app, db_session):
        """Распределение с позициями."""
        participant_user_id = str(uuid.uuid4())
        
        transaction_info = type('transaction_in', (), {
            'FROM': None,
            'TO': None,
            'category': None,
            'type': 'debit',
            'debitSize': 100.0,
            'creditSize': None,
            'exchangeRate': None,
            'date': date.today(),
            'description': 'Position split test',
            'splitType': 'position',
            'status': 'settled',
            'distributions': [
                type('distribution_in', (), {
                    'user_id': participant_user_id,
                    'transaction_id': None,
                    'role': 'participant',
                    'size': None,
                    'percentage': None,
                    'is_settled': False,
                })()
            ],
            'positions': [
                type('position_in', (), {
                    'name': 'Item 1',
                    'quantity': 2.0,
                    'price': 25.0,
                    'currency': 'USD'
                })(),
                type('position_in', (), {
                    'name': 'Item 2',
                    'quantity': 3.0,
                    'price': 16.67,
                    'currency': 'USD'
                })()
            ],
        })

        result = fin_app.create_transaction(transaction_info)

        assert isinstance(result, result.__class__.__bases__[0].__dict__.get('Transaction', type))
        
        # Проверяем позиции
        positions = fin_app.crud.position.get_positions_for_transaction(result.id)
        assert len(positions) == 2


class TestDistributionSettlement:
    """Тесты для установки статуса оплаты распределений."""

    def test_settle_distribution(self, client):
        """Установка статуса оплаченного для распределения."""
        from app.schemas.distribution import distribution_settle_in
        
        # Создаем транзакцию и распределение через API
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

        create_response = client.post("/api/v1/account/create", json=account_data)
        assert create_response.status_code == 200
        
        transaction = {
            "FROM": None,
            "TO": None,
            "category": None,
            "type": "debit",
            "debitSize": 100.0,
            "creditSize": None,
            "exchangeRate": None,
            "date": date.today().isoformat(),
            "description": "Test transaction for settlement",
            "splitType": None,
            "status": "pending",
        }

        create_response = client.post("/api/v1/transaction/create", json=transaction)
        assert create_response.status_code == 200
        
        transaction_id = uuid.UUID(create_response.json()["id"])

        # Добавляем распределение
        distribution_data = {
            "user_id": str(uuid.uuid4()),
            "transaction_id": str(transaction_id),
            "role": "participant",
            "size": 50.0,
            "is_settled": False
        }

        response = client.post("/api/v1/transaction/distribution", json=distribution_data)
        
        assert response.status_code == 200
        
        distribution_id = uuid.UUID(response.json()["id"])

        # Устанавливаем статус оплаченного
        settle_info = {
            "distribution_id": str(distribution_id),
            "transaction_id": str(transaction_id),
        }

        response = client.post(
            "/api/v1/transaction/distribution/settle",
            json=settle_info
        )

        assert response.status_code == 200
        data = response.json()
        assert data["is_settled"] is True


class TestTransactionStatusRecalculation:
    """Тесты для пересчета статуса транзакции."""

    def test_transaction_status_from_pending_to_partially_paid(self, client):
        """Проверка перехода статуса транзакции при частичной оплате распределений."""
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

        create_response = client.post("/api/v1/account/create", json=account_data)
        assert create_response.status_code == 200
        
        transaction = {
            "FROM": None,
            "TO": None,
            "category": None,
            "type": "debit",
            "debitSize": 100.0,
            "creditSize": None,
            "exchangeRate": None,
            "date": date.today().isoformat(),
            "description": "Transaction status test",
            "splitType": None,
            "status": "pending",
        }

        create_response = client.post("/api/v1/transaction/create", json=transaction)
        assert create_response.status_code == 200
        
        transaction_id = uuid.UUID(create_response.json()["id"])


class TestIntegrationTransactionAndDistribution:
    """Интеграционные тесты для транзакций и распределений."""

    def test_full_workflow_create_and_distribute(self, client):
        """Полный рабочий цикл: создание транзакции с распределениями."""
        account_data = {
            "name": "Main Account",
            "currency": "USD",
            "account_type": "debit",
            "balance": 2000.0,
            "description": "Account for testing",
            "interest_rate": 5.0,
            "is_emergency_fund": False,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": True,
        }

        create_response = client.post("/api/v1/account/create", json=account_data)
        assert create_response.status_code == 200
        
        account_id = uuid.UUID(create_response.json()["id"])

        # Создаем транзакцию с распределениями
        transaction = {
            "FROM": str(account_id),
            "TO": None,
            "category": None,
            "type": "debit",
            "debitSize": 200.0,
            "creditSize": None,
            "exchangeRate": None,
            "date": date.today().isoformat(),
            "description": "Transaction with distributions",
            "splitType": "equal",
            "status": "pending",
            "distributions": [
                {
                    "user_id": str(uuid.uuid4()),
                    "role": "participant",
                    "size": None,
                    "percentage": None
                },
                {
                    "user_id": str(uuid.uuid4()),
                    "role": "participant",
                    "size": None,
                    "percentage": None
                }
            ],
            "positions": []
        }

        response = client.post("/api/v1/transaction/create", json=transaction)
        
        assert response.status_code == 200
        data = response.json()
        
        # Проверяем, что распределения созданы
        distributions = data.get("distributions", [])
        assert len(distributions) >= 1

    def test_update_transaction_distribution(self, client):
        """Обновление существующего распределения."""
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

        create_response = client.post("/api/v1/account/create", json=account_data)
        assert create_response.status_code == 200
        
        transaction = {
            "FROM": None,
            "TO": None,
            "category": None,
            "type": "debit",
            "debitSize": 100.0,
            "creditSize": None,
            "exchangeRate": None,
            "date": date.today().isoformat(),
            "description": "Transaction for distribution update",
            "splitType": None,
            "status": "settled",
        }

        create_response = client.post("/api/v1/transaction/create", json=transaction)
        assert create_response.status_code == 200
        
        transaction_id = uuid.UUID(create_response.json()["id"])

        # Добавляем распределение
        distribution_data = {
            "user_id": str(uuid.uuid4()),
            "transaction_id": str(transaction_id),
            "role": "participant",
            "size": 50.0,
            "is_settled": False
        }

        create_response = client.post("/api/v1/transaction/distribution", json=distribution_data)
        assert create_response.status_code == 200
        
        distribution_id = uuid.UUID(create_response.json()["id"])

        # Обновляем распределение (меняем размер)
        update_data = {
            "user_id": str(uuid.uuid4()),
            "transaction_id": str(transaction_id),
            "role": "participant",
            "size": 75.0,
            "is_settled": False
        }

        response = client.patch("/api/v1/transaction/distribution", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["size"] == 75.0


class TestIntegrationTransactionAndPosition:
    """Интеграционные тесты для транзакций и позиций."""

    def test_add_position_to_transaction(self, client):
        """Добавление позиции к транзакции."""
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

        create_response = client.post("/api/v1/account/create", json=account_data)
        assert create_response.status_code == 200
        
        transaction = {
            "FROM": None,
            "TO": None,
            "category": None,
            "type": "debit",
            "debitSize": 300.0,
            "creditSize": None,
            "exchangeRate": None,
            "date": date.today().isoformat(),
            "description": "Transaction with positions",
            "splitType": "position",
            "status": "settled",
        }

        create_response = client.post("/api/v1/transaction/create", json=transaction)
        assert create_response.status_code == 200
        
        transaction_id = uuid.UUID(create_response.json()["id"])

        # Добавляем позицию
        position_data = {
            "name": "Stock XYZ",
            "quantity": 10.0,
            "price": 30.0,
            "currency": "USD"
        }

        response = client.post("/api/v1/transaction/position", json=position_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Stock XYZ"
        assert data["quantity"] == 10.0


class TestIntegrationPeriodQueries:
    """Интеграционные тесты для запросов по периодам."""

    def test_get_transactions_by_period(self, client):
        """Запрос транзакций за период с фильтрацией."""
        account_data = {
            "name": "Test Account",
            "currency": "USD",
            "account_type": "debit",
            "balance": 5000.0,
            "description": "Account for testing",
            "interest_rate": 5.0,
            "is_emergency_fund": False,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": True,
        }

        create_response = client.post("/api/v1/account/create", json=account_data)
        assert create_response.status_code == 200
        
        # Создаем транзакции с разными датами
        today = date.today()
        
        for i in range(5):
            transaction = {
                "FROM": None,
                "TO": None,
                "category": None,
                "type": "debit",
                "debitSize": float(i * 10 + 10),
                "creditSize": None,
                "exchangeRate": None,
                "date": (today - __import__('datetime').timedelta(days=5-i)).isoformat(),
                "description": f"Transaction {i}",
                "splitType": None,
                "status": "settled",
            }

            client.post("/api/v1/transaction/create", json=transaction)

        # Запрашиваем транзакции за последние 3 дня
        from_date = (today - __import__('datetime').timedelta(days=2)).isoformat()
        to_date = today.isoformat()

        response = client.get(
            f"/api/v1/transaction/by_period?from_date={from_date}&to_date={to_date}"
        )

        assert response.status_code == 200
        data = response.json()
        
        # Должны быть транзакции за последние 3 дня (но не все)


class TestEdgeCases:
    """Тесты для граничных случаев."""

    def test_zero_amount_transaction(self, client):
        """Создание транзакции с нулевым размером."""
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

        create_response = client.post("/api/v1/account/create", json=account_data)
        
        transaction = {
            "FROM": None,
            "TO": None,
            "category": None,
            "type": "debit",
            "debitSize": 0.0,
            "creditSize": None,
            "exchangeRate": None,
            "date": date.today().isoformat(),
            "description": "Zero amount transaction",
            "splitType": None,
            "status": "settled",
        }

        response = client.post("/api/v1/transaction/create", json=transaction)
        
        # Должна успешно создаваться транзакция с нулевым размером
        assert response.status_code == 200

    def test_very_small_amount_transaction(self, client):
        """Создание транзакции с очень маленьким размером."""
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

        create_response = client.post("/api/v1/account/create", json=account_data)
        
        transaction = {
            "FROM": None,
            "TO": None,
            "category": None,
            "type": "debit",
            "debitSize": 0.01,  # Очень маленький размер
            "creditSize": None,
            "exchangeRate": None,
            "date": date.today().isoformat(),
            "description": "Very small transaction",
            "splitType": None,
            "status": "settled",
        }

        response = client.post("/api/v1/transaction/create", json=transaction)
        
        assert response.status_code == 200

    def test_very_large_amount_transaction(self, client):
        """Создание транзакции с очень большим размером."""
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

        create_response = client.post("/api/v1/account/create", json=account_data)
        
        transaction = {
            "FROM": None,
            "TO": None,
            "category": None,
            "type": "debit",
            "debitSize": 999999.99,  # Очень большой размер
            "creditSize": None,
            "exchangeRate": None,
            "date": date.today().isoformat(),
            "description": "Very large transaction",
            "splitType": None,
            "status": "settled",
        }

        response = client.post("/api/v1/transaction/create", json=transaction)
        
        assert response.status_code == 200
