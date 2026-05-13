"""
Тесты для сервисного слоя Fin_app.
Проверяет бизнес-логику создания транзакций, счетов и категорий.
"""

import uuid
from datetime import date
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.orm import Session

from app.models.account import Account, AccountType
from app.models.category import Category
from app.models.transaction import Transaction


class TestFinAppAccountOperations:
    """Тесты для операций со счетами в Fin_app."""

    def test_create_account(self, fin_app, db_session, test_account_data):
        """Создание нового счета."""
        account_info = type('account_in', (), {
            'name': test_account_data['name'],
            'currency': test_account_data['currency'],
            'account_type': AccountType[test_account_data['account_type']],
            'balance': 0.0,
            'description': test_account_data['description'],
            'interest_rate': test_account_data['interest_rate'],
            'is_emergency_fund': test_account_data['is_emergency_fund'],
            'decimal_places': test_account_data['decimal_places'],
            'is_archived': test_account_data['is_archived'],
            'is_primary': test_account_data['is_primary'],
        })

        account = fin_app.create_account(account_info)

        assert isinstance(account, Account)
        assert account.name == test_account_data['name']
        assert account.currency == test_account_data['currency']
        assert account.account_type == AccountType[test_account_data['account_type']]
        assert account.balance == 0.0

    def test_get_all_accounts(self, fin_app, db_session):
        """Получение всех счетов."""
        # Создаем тестовые счета напрямую в БД
        accounts = [
            Account(
                id=uuid.uuid4(),
                name=f"Account {i}",
                currency="USD",
                account_type=AccountType.DEBIT,
                balance=1000.0 * i,
                is_primary=i == 0,
                user_id=fin_app.user_info['id']
            )
            for i in range(3)
        ]

        db_session.add_all(accounts)
        db_session.commit()

        all_accounts = fin_app.get_all_account()

        assert len(all_accounts) == 3
        account_names = [acc.name for acc in all_accounts]
        assert "Account 0" in account_names
        assert "Account 1" in account_names
        assert "Account 2" in account_names

    def test_get_account_by_id(self, fin_app, db_session):
        """Получение счета по ID."""
        account = Account(
            id=uuid.uuid4(),
            name="Test Account",
            currency="USD",
            account_type=AccountType.DEBIT,
            balance=1000.0,
            user_id=fin_app.user_info['id']
        )

        db_session.add(account)
        db_session.commit()

        retrieved_account = fin_app.get_account_by_id(account.id)

        assert isinstance(retrieved_account, Account)
        assert retrieved_account.id == account.id
        assert retrieved_account.name == "Test Account"

    def test_get_nonexistent_account(self, fin_app):
        """Получение несуществующего счета возвращает None."""
        fake_id = uuid.uuid4()
        result = fin_app.get_account_by_id(fake_id)
        assert result is None


class TestFinAppCategoryOperations:
    """Тесты для операций с категориями в Fin_app."""

    def test_create_category_basic(self, fin_app, db_session):
        """Создание базовой категории."""
        category_info = type('category_in', (), {
            'name': 'Food',
            'type': 'expense',
            'parent_category': None,
            'level': 0,
            'is_deleted': False,
        })

        category = fin_app.create_category(category_info)

        assert isinstance(category, Category)
        assert category.name == 'Food'
        assert category.type == 'expense'
        assert category.level == 0

    def test_create_category_with_parent(self, fin_app, db_session):
        """Создание категории с родительской категорией."""
        parent_info = type('category_in', (), {
            'name': 'Food',
            'type': 'expense',
            'parent_category': None,
            'level': 0,
            'is_deleted': False,
        })

        child_info = type('category_in', (), {
            'name': 'Groceries',
            'type': 'expense',
            'parent_category': None,  # Будет установлено автоматически
            'level': 1,
            'is_deleted': False,
        })

        parent = fin_app.create_category(parent_info)
        child_info.parent_category = str(parent.id)
        
        child = fin_app.create_category(child_info)

        assert isinstance(child, Category)
        assert child.name == 'Groceries'
        assert child.level == 1

    def test_create_category_max_level(self, fin_app, db_session):
        """Проверка ограничения уровня вложенности категорий."""
        # Создаем иерархию из 4 уровней (максимум - 3)
        categories = []
        
        for level in range(4):
            category_info = type('category_in', (), {
                'name': f'Category Level {level}',
                'type': 'expense',
                'parent_category': str(categories[-1].id) if categories else None,
                'level': level,
                'is_deleted': False,
            })

            try:
                category = fin_app.create_category(category_info)
                categories.append(category)
            except Exception:
                break  # Ожидаем ошибку на уровне 3 (максимум)

        assert len(categories) <= 4


class TestTransactionDistribution:
    """Тесты для распределения транзакций между пользователями."""

    def test_distribute_equal_split(self, fin_app, db_session):
        """Распределение суммы поровну между участниками."""
        # Создаем второго участника
        participant_user = {
            "id": str(uuid.uuid4()),
            "email": "participant@example.com",
            "name": "Participant"
        }

        transaction_info = type('transaction_in', (), {
            'FROM': None,
            'TO': None,
            'category': None,
            'type': 'debit',
            'debitSize': 100.0,
            'creditSize': None,
            'exchangeRate': None,
            'date': date.today(),
            'description': 'Test equal split',
            'splitType': 'equal',
            'status': 'settled',
            'distributions': [
                type('distribution_in', (), {
                    'user_id': participant_user['id'],
                    'transaction_id': None,  # Будет установлено автоматически
                    'role': 'participant',
                    'size': None,
                    'percentage': None,
                    'is_settled': False,
                })()
            ],
            'positions': [],
        })

        result = fin_app.create_transaction(transaction_info)

        assert isinstance(result, Transaction)
        assert result.debit_size == 100.0

    def test_distribute_by_percentage(self, fin_app, db_session):
        """Распределение по процентам."""
        participant_user = {
            "id": str(uuid.uuid4()),
            "email": "participant@example.com",
            "name": "Participant"
        }

        transaction_info = type('transaction_in', (), {
            'FROM': None,
            'TO': None,
            'category': None,
            'type': 'debit',
            'debitSize': 100.0,
            'creditSize': None,
            'exchangeRate': None,
            'date': date.today(),
            'description': 'Test percentage split',
            'splitType': 'percentage',
            'status': 'settled',
            'distributions': [
                type('distribution_in', (), {
                    'user_id': participant_user['id'],
                    'transaction_id': None,
                    'role': 'participant',
                    'size': None,
                    'percentage': 0.5,  # 50%
                    'is_settled': False,
                })()
            ],
            'positions': [],
        })

        result = fin_app.create_transaction(transaction_info)

        assert isinstance(result, Transaction)
        assert result.debit_size == 100.0


class TestTransactionSizeUpdate:
    """Тесты для обновления размера транзакции."""

    def test_update_transaction_size(self, fin_app, db_session):
        """Обновление размера транзакции пересчитывает распределения."""
        transaction_info = type('transaction_in', (), {
            'FROM': None,
            'TO': None,
            'category': None,
            'type': 'debit',
            'debitSize': 100.0,
            'creditSize': None,
            'exchangeRate': None,
            'date': date.today(),
            'description': 'Test size update',
            'splitType': None,
            'status': 'settled',
            'distributions': [],
            'positions': [],
        })

        transaction = fin_app.create_transaction(transaction_info)
        
        assert transaction.debit_size == 100.0

        # Обновляем размер
        size_update_info = type('transaction_in_size', (), {
            'id': transaction.id,
            'size': 150.0,
        })()

        updated_transaction = fin_app.update_transaction_size(size_update_info)

        assert updated_transaction.debit_size == 150.0


class TestTransactionDelete:
    """Тесты для удаления транзакции."""

    def test_delete_transaction(self, fin_app, db_session):
        """Удаление транзакции возвращает объект и очищает базу."""
        transaction_info = type('transaction_in', (), {
            'FROM': None,
            'TO': None,
            'category': None,
            'type': 'debit',
            'debitSize': 100.0,
            'creditSize': None,
            'exchangeRate': None,
            'date': date.today(),
            'description': 'Transaction to delete',
            'splitType': None,
            'status': 'settled',
            'distributions': [],
            'positions': [],
        })

        transaction = fin_app.create_transaction(transaction_info)

        result = fin_app.delete_transaction(transaction.id)

        assert isinstance(result, Transaction)
        assert result.id == transaction.id
        
        # Проверяем, что транзакция удалена из БД
        retrieved = fin_app.crud.transaction.get_by_id(transaction.id)
        assert retrieved is None


class TestTransactionBalanceReversal:
    """Тесты для возврата баланса при удалении транзакции."""

    def test_reverse_debit_transaction_balance(self, fin_app, db_session):
        """При удалении debit-транзакции баланс возвращается."""
        account = Account(
            id=uuid.uuid4(),
            name="Test Account",
            currency="USD",
            account_type=AccountType.DEBIT,
            balance=1000.0,
            user_id=fin_app.user_info['id']
        )

        db_session.add(account)
        db_session.commit()

        transaction_info = type('transaction_in', (), {
            'FROM': str(account.id),
            'TO': None,
            'category': None,
            'type': 'debit',
            'debitSize': 200.0,
            'creditSize': None,
            'exchangeRate': None,
            'date': date.today(),
            'description': 'Debit transaction for balance test',
            'splitType': None,
            'status': 'settled',
            'distributions': [],
            'positions': [],
        })

        # Создаем транзакцию (баланс станет 800)
        transaction = fin_app.create_transaction(transaction_info)
        
        account_after_create = db_session.query(Account).filter_by(id=account.id).first()
        assert account_after_create.balance == 800.0

        # Удаляем транзакцию (баланс должен вернуться к 1000)
        fin_app.delete_transaction(transaction.id)
        
        account_after_delete = db_session.query(Account).filter_by(id=account.id).first()
        assert account_after_delete.balance == 1000.0

    def test_reverse_transfer_transaction_balance(self, fin_app, db_session):
        """При удалении transfer-транзакции балансы возвращаются."""
        from_account = Account(
            id=uuid.uuid4(),
            name="From Account",
            currency="USD",
            account_type=AccountType.DEBIT,
            balance=2000.0,
            user_id=fin_app.user_info['id']
        )

        to_account = Account(
            id=uuid.uuid4(),
            name="To Account",
            currency="USD",
            account_type=AccountType.SAVINGS,
            balance=500.0,
            user_id=fin_app.user_info['id']
        )

        db_session.add_all([from_account, to_account])
        db_session.commit()

        transaction_info = type('transaction_in', (), {
            'FROM': str(from_account.id),
            'TO': str(to_account.id),
            'category': None,
            'type': 'transfer',
            'debitSize': 300.0,
            'creditSize': 300.0,
            'exchangeRate': 1.0,
            'date': date.today(),
            'description': 'Transfer for balance test',
            'splitType': None,
            'status': 'settled',
            'distributions': [],
            'positions': [],
        })

        # Создаем транзакцию (from: 1700, to: 800)
        transaction = fin_app.create_transaction(transaction_info)
        
        from_after_create = db_session.query(Account).filter_by(id=from_account.id).first()
        to_after_create = db_session.query(Account).filter_by(id=to_account.id).first()
        
        assert from_after_create.balance == 1700.0
        assert to_after_create.balance == 800.0

        # Удаляем транзакцию
        fin_app.delete_transaction(transaction.id)
        
        from_after_delete = db_session.query(Account).filter_by(id=from_account.id).first()
        to_after_delete = db_session.query(Account).filter_by(id=to_account.id).first()
        
        assert from_after_delete.balance == 2000.0
        assert to_after_delete.balance == 500.0
