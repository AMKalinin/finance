"""
Тесты для CRUD операций.
Проверяет базовые операции с БД: создание, чтение, обновление, удаление.
"""

import uuid
from datetime import date

import pytest
from sqlalchemy.orm import Session

from app.models.account import Account, AccountType


def get_mock_user():
    """Возвращает моковую информацию о пользователе."""
    return {
        "id": str(uuid.uuid4()),
        "sub": str(uuid.uuid4()),  # Subject (Keycloak user ID)
        "email": "test@example.com",
        "name": "Test User"
    }


class TestCRUDAccount:
    """Тесты для CRUD операций со счетами."""

    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        """Очистка базы данных перед каждым тестом."""
        # Очистим все данные из таблиц
        from app.models.category import Category
        from app.models.transaction import Transaction
        
        for obj in [Account, Category, Transaction]:
            try:
                for item in db_session.query(obj).all():
                    db_session.delete(item)
            except Exception:
                pass
        db_session.commit()

    @pytest.fixture
    def crud(self, db_session):
        from app.crud import Crud
        
        mock_user = get_mock_user()
        
        return Crud(db=db_session, user_info=mock_user)

    def test_create_account(self, db_session, crud):
        """Создание счета."""
        account_data = {
            'id': uuid.uuid4(),
            'name': 'Testing Account',
            'currency': 'USD',
            'account_type': AccountType.DEBIT,
            'balance': 500.0,
            'user_id': crud.user.id if hasattr(crud.user, 'id') else mock_user['sub']
        }

        account = crud.account.create_account(account_data)

        assert isinstance(account, Account)
        assert account.name == 'Testing Account'
        
        # Проверяем сохранение в БД через get_by_id
        result = crud.account.get_by_id(account.id)
        assert result is not None
        assert result.name == 'Testing Account'

    def test_get_by_id(self, db_session):
        """Получение счета по ID."""
        from app.crud import Crud
        
        mock_user = get_mock_user()
        crud = Crud(db=db_session, user_info=mock_user)
        
        account = Account(
            id=uuid.uuid4(),
            name="CRUD Test Account",
            currency="EUR",
            account_type=AccountType.SAVINGS,
            balance=2000.0,
            user_id=str(uuid.uuid4())  # Используем новый UUID для пользователя
        )

        db_session.add(account)
        db_session.commit()

        result = crud.account.get_by_id(account.id)

        assert isinstance(result, Account)
        assert result.name == "CRUD Test Account"

    def test_get_all(self, db_session):
        """Получение всех счетов."""
        from app.crud import Crud
        
        mock_user = get_mock_user()
        crud = Crud(db=db_session, user_info=mock_user)
        
        accounts_to_create = [
            Account(
                id=uuid.uuid4(),
                name=f"Account {i}",
                currency="USD",
                account_type=AccountType.DEBIT,
                balance=float(i * 100),
                user_id=str(uuid.uuid4())  # Используем новый UUID для пользователя
            )
            for i in range(5)
        ]

        for acc in accounts_to_create:
            db_session.add(acc)
        db_session.commit()

        all_accounts = crud.account.get_all()

        assert len(all_accounts) == 5


class TestCRUDTransaction:
    """Тесты для CRUD операций с транзакциями."""

    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        """Очистка базы данных перед каждым тестом."""
        from app.models.transaction import Transaction_type, Transaction_status, Split_type
        
        # Удаляем справочники и транзакции
        for model in [Transaction_type, Transaction_status, Split_type]:
            try:
                db_session.query(model).delete()
            except Exception:
                pass
        
        from app.models.transaction import Transaction
        try:
            db_session.query(Transaction).delete()
        except Exception:
            pass
        db_session.commit()

    @pytest.fixture
    def crud(self, db_session):
        from app.crud import Crud
        
        mock_user = get_mock_user()
        
        return Crud(db=db_session, user_info=mock_user)

    def test_create_transaction(self, db_session):
        """Создание транзакции."""
        from app.service.fin_app import Fin_app
        
        mock_user = get_mock_user()
        fin_app = Fin_app(db=db_session, user_info=mock_user)
        
        # Используем правильный класс Pydantic схемы с creditSize
        from app.schemas.transaction import transaction_in
        
        transaction_info = transaction_in(
            FROM=None,
            TO=None,
            category=None,
            type='debit',
            debitSize=100.0,
            creditSize=50.0,  # Устанавливаем значение для NOT NULL поля
            exchangeRate=None,
            date=date.today(),
            description='Test transaction',
            splitType=None,
            status='settled'
        )

        result = fin_app.create_transaction(transaction_info)

        assert isinstance(result, Transaction)
        assert result.type == "debit"

    def test_get_transaction_by_id(self, db_session):
        """Получение транзакции по ID."""
        from app.crud import Crud
        
        mock_user = get_mock_user()
        crud = Crud(db=db_session, user_info=mock_user)
        
        from app.models.transaction import Transaction
        
        transaction = Transaction(
            id=uuid.uuid4(),
            from_account_id=None,
            to_account_id=None,
            category=None,
            type="debit",
            debit_size=200.0,
            credit_size=100.0,  # Устанавливаем значение для NOT NULL поля
            exchange_rate=1.0,
            date=date.today(),
            description="Get by ID test",
            split_type=None,
            status='settled'
        )

        db_session.add(transaction)
        db_session.commit()

        result = crud.transaction.get_by_id(transaction.id)

        assert isinstance(result, Transaction)
        assert result.description == "Get by ID test"


class TestCRUDCategory:
    """Тесты для CRUD операций с категориями."""

    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        """Очистка базы данных перед каждым тестом."""
        from app.models.category import Category
        
        # Удаляем категории
        try:
            for cat in db_session.query(Category).all():
                db_session.delete(cat)
        except Exception:
            pass
        db_session.commit()

    @pytest.fixture
    def crud(self, db_session):
        from app.crud import Crud
        
        mock_user = get_mock_user()
        
        return Crud(db=db_session, user_info=mock_user)

    def test_create_category(self, db_session, crud):
        """Создание категории."""
        from app.models.category import Category as CategoryModel
        from app.schemas.category import category_in
        
        category_data = category_in(
            name='Groceries',
            type='expense',
            parent_category=None,
            level=0,
            is_deleted=False
        )

        result = crud.category.create_category(category_data)

        assert isinstance(result, CategoryModel)
        assert result.name == "Groceries"


class TestUserRelationships:
    """Тесты для связей пользователя."""

    @pytest.fixture
    def crud(self, db_session):
        from app.crud import Crud
        
        mock_user = get_mock_user()
        
        return Crud(db=db_session, user_info=mock_user)

    def test_get_user_info(self, crud):
        """Получение информации о пользователе."""
        # Проверяем, что пользователь существует в БД
        assert crud.user is not None


class TestDistributionOperations:
    """Тесты для операций с распределениями."""

    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        """Очистка базы данных перед каждым тестом."""
        from app.models.transaction import Transaction
        
        # Удаляем транзакции и распределения
        try:
            for t in db_session.query(Transaction).all():
                db_session.delete(t)
        except Exception:
            pass
        db_session.commit()

    @pytest.fixture
    def crud(self, db_session):
        from app.crud import Crud
        
        mock_user = get_mock_user()
        
        return Crud(db=db_session, user_info=mock_user)

    def test_create_distribution(self, db_session):
        """Создание распределения."""
        from app.service.fin_app import Fin_app
        
        mock_user = get_mock_user()
        fin_app = Fin_app(db=db_session, user_info=mock_user)
        
        from app.schemas.transaction import transaction_in
        
        transaction_info = transaction_in(
            FROM=None,
            TO=None,
            category=None,
            type='debit',
            debitSize=100.0,
            creditSize=50.0,  # Устанавливаем значение для NOT NULL поля
            exchangeRate=None,
            date=date.today(),
            description='Test distribution',
            splitType=None,
            status='settled'
        )

        result = fin_app.create_transaction(transaction_info)

        assert isinstance(result, Transaction)


class TestPositionOperations:
    """Тесты для операций с позициями."""

    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        """Очистка базы данных перед каждым тестом."""
        from app.models.transaction import Transaction
        
        # Удаляем транзакции и позиции
        try:
            for t in db_session.query(Transaction).all():
                db_session.delete(t)
        except Exception:
            pass
        db_session.commit()

    @pytest.fixture
    def crud(self, db_session):
        from app.crud import Crud
        
        mock_user = get_mock_user()
        
        return Crud(db=db_session, user_info=mock_user)

    def test_create_position(self, db_session):
        """Создание позиции."""
        from app.service.fin_app import Fin_app
        
        mock_user = get_mock_user()
        fin_app = Fin_app(db=db_session, user_info=mock_user)
        
        from app.schemas.transaction import transaction_in
        from app.schemas.position import position_in
        
        transaction_info = transaction_in(
            FROM=None,
            TO=None,
            category=None,
            type='debit',
            debitSize=100.0,
            creditSize=50.0,  # Устанавливаем значение для NOT NULL поля
            exchangeRate=None,
            date=date.today(),
            description='Test position',
            splitType=None,
            status='settled',
            positions=[position_in(name='Stock XYZ', quantity=10.0, price=25.0, currency='USD')]
        )

        result = fin_app.create_transaction(transaction_info)

        assert isinstance(result, Transaction)


class TestCRUDBase:
    """Базовые тесты для CRUD операций."""

    @pytest.fixture
    def crud(self, db_session):
        from app.crud import Crud
        
        mock_user = get_mock_user()
        
        return Crud(db=db_session, user_info=mock_user)

    def test_user_exists(self, crud):
        """Проверка, что пользователь существует в БД."""
        assert crud.user is not None
        
    def test_db_is_valid(self, db_session):
        """Проверка валидности сессии базы данных."""
        assert db_session is not None
