"""
Тесты для моделей и Pydantic схем.
Проверяет валидацию данных и работу с базовыми моделями SQLAlchemy.
"""

import uuid
from datetime import date

import pytest
from pydantic import ValidationError


class TestTransactionSchema:
    """Тесты для схем транзакций."""

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
            "exchangeRate": None,
            "date": date.today().isoformat(),
            "description": "Test transaction",
            "splitType": None,
            "status": "settled"
        }

        result = transaction_in(**data)

        assert result.type == "debit"
        assert result.debit_size == 100.0
        assert result.status == "settled"

    def test_transaction_in_with_transfer(self):
        """Валидация транзакции типа transfer."""
        from app.schemas.transaction import transaction_in
        
        data = {
            "FROM": str(uuid.uuid4()),
            "TO": str(uuid.uuid4()),
            "category": None,
            "type": "transfer",
            "debitSize": 100.0,
            "creditSize": 100.0,
            "exchangeRate": 1.5,
            "date": date.today().isoformat(),
            "description": "Transfer between accounts",
            "splitType": None,
            "status": "settled"
        }

        result = transaction_in(**data)

        assert result.type == "transfer"
        assert result.FROM is not None
        assert result.TO is not None

    def test_transaction_out_serialization(self):
        """Сериализация выходного объекта транзакции."""
        from app.schemas.transaction import transaction_out, distribution_out
        
        data = {
            "id": str(uuid.uuid4()),
            "from_account_id": None,
            "to_account_id": None,
            "category": None,
            "type": "debit",
            "debit_size": 100.0,
            "credit_size": None,
            "exchange_rate": None,
            "date": date.today().isoformat(),
            "description": "Test transaction",
            "split_type": None,
            "status": "settled",
            "transaction_distribution_user": [
                {
                    "user_id": str(uuid.uuid4()),
                    "transaction_id": str(uuid.uuid4()),
                    "distribution_user_role": "owner",
                    "distribution_status": "settled",
                    "size": 100.0,
                    "is_deleted": False
                }
            ],
            "positions": []
        }

        result = transaction_out(**data)

        assert result.id is not None
        assert result.debit_size == 100.0

    def test_transaction_in_invalid_type(self):
        """Проверка валидации невалидного типа транзакции."""
        from app.schemas.transaction import transaction_in
        
        data = {
            "FROM": None,
            "TO": None,
            "category": None,
            "type": "invalid_type",  # Невалидный тип
            "debitSize": 100.0,
            "creditSize": None,
            "exchangeRate": None,
            "date": date.today().isoformat(),
            "description": "Test transaction",
            "splitType": None,
            "status": "settled"
        }

        with pytest.raises(ValidationError):
            transaction_in(**data)


class TestAccountSchema:
    """Тесты для схем счетов."""

    def test_account_in_valid(self):
        """Валидация валидного входного объекта счета."""
        from app.schemas.account import account_in
        
        data = {
            "name": "Test Account",
            "currency": "USD",
            "account_type": "debit",
            "balance": 1000.0,
            "description": "Test account",
            "interest_rate": 5.0,
            "is_emergency_fund": False,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": True
        }

        result = account_in(**data)

        assert result.name == "Test Account"
        assert result.currency == "USD"
        assert result.is_primary is True

    def test_account_out_serialization(self):
        """Сериализация выходного объекта счета."""
        from app.schemas.account import account_out
        
        data = {
            "id": str(uuid.uuid4()),
            "name": "Test Account",
            "currency": "USD",
            "account_type": "debit",
            "balance": 1000.0,
            "description": "Test account",
            "interest_rate": 5.0,
            "is_emergency_fund": False,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": True
        }

        result = account_out(**data)

        assert result.id is not None
        assert result.name == "Test Account"


class TestCategorySchema:
    """Тесты для схем категорий."""

    def test_category_in_valid(self):
        """Валидация валидного входного объекта категории."""
        from app.schemas.category import category_in
        
        data = {
            "name": "Food",
            "type": "expense",
            "parent_category": None,
            "level": 0,
            "is_deleted": False
        }

        result = category_in(**data)

        assert result.name == "Food"
        assert result.type == "expense"
        assert result.level == 0


class TestDistributionSchema:
    """Тесты для схем распределений."""

    def test_distribution_in_valid(self):
        """Валидация ввалидного входного объекта распределения."""
        from app.schemas.distribution import distribution_in
        
        data = {
            "user_id": str(uuid.uuid4()),
            "transaction_id": str(uuid.uuid4()),
            "role": "owner",
            "size": 50.0,
            "is_settled": False
        }

        result = distribution_in(**data)

        assert result.role == "owner"
        assert result.size == 50.0

    def test_distribution_in_with_percentage(self):
        """Валидация распределения с процентами."""
        from app.schemas.distribution import distribution_in
        
        data = {
            "user_id": str(uuid.uuid4()),
            "transaction_id": str(uuid.uuid4()),
            "role": "participant",
            "size": None,
            "percentage": 0.5,
            "is_settled": False
        }

        result = distribution_in(**data)

        assert result.percentage == 0.5


class TestPositionSchema:
    """Тесты для схем позиций."""

    def test_position_in_valid(self):
        """Валидация валидного входного объекта позиции."""
        from app.schemas.position import position_in
        
        data = {
            "transaction_id": str(uuid.uuid4()),
            "name": "Stock",
            "quantity": 10.0,
            "price": 25.0,
            "currency": "USD"
        }

        result = position_in(**data)

        assert result.name == "Stock"
        assert result.quantity == 10.0
        assert result.price == 25.0


class TestTransactionModel:
    """Тесты для модели транзакции SQLAlchemy."""

    def test_transaction_creation(self):
        """Создание объекта транзакции."""
        from app.models.transaction import Transaction
        
        transaction = Transaction(
            id=uuid.uuid4(),
            from_account_id=None,
            to_account_id=None,
            category=None,
            type="debit",
            debit_size=100.0,
            credit_size=None,
            exchange_rate=1.0,
            date=date.today(),
            description="Test transaction",
            split_type=None,
            status='settled'
        )

        assert isinstance(transaction.id, uuid.UUID)
        assert transaction.type == "debit"
        assert transaction.debit_size == 100.0


class TestAccountModel:
    """Тесты для модели счета SQLAlchemy."""

    def test_account_creation(self):
        """Создание объекта счета."""
        from app.models.account import Account, AccountType
        
        account = Account(
            id=uuid.uuid4(),
            name="Test Account",
            currency="USD",
            account_type=AccountType.DEBIT,
            balance=1000.0,
            description="Test account",
            interest_rate=5.0,
            is_emergency_fund=False,
            decimal_places=2,
            is_archived=False,
            is_primary=True,
            user_id=uuid.uuid4()
        )

        assert isinstance(account.id, uuid.UUID)
        assert account.account_type == AccountType.DEBIT
        assert account.is_primary is True


class TestCategoryModel:
    """Тесты для модели категории SQLAlchemy."""

    def test_category_creation(self):
        """Создание объекта категории."""
        from app.models.category import Category
        
        category = Category(
            id=uuid.uuid4(),
            name="Food",
            type="expense",
            level=0,
            is_deleted=False,
            user_id=uuid.uuid4()
        )

        assert isinstance(category.id, uuid.UUID)
        assert category.type == "expense"
        assert category.level == 0


class TestTransactionTypeModel:
    """Тесты для модели типа транзакции SQLAlchemy."""

    def test_transaction_type_creation(self):
        """Создание объекта типа транзакции."""
        from app.models.transaction import Transaction_type
        
        transaction_type = Transaction_type(
            name="debit",
            description="Debit transaction - money leaving account"
        )

        assert transaction_type.name == "debit"


class TestTransactionStatusModel:
    """Тесты для модели статуса транзакции SQLAlchemy."""

    def test_transaction_status_creation(self):
        """Создание объекта статуса транзакции."""
        from app.models.transaction import Transaction_status
        
        status = Transaction_status(
            name="settled",
            description="Transaction is fully settled"
        )

        assert status.name == "settled"


class TestSubscriptionTypeModel:
    """Тесты для модели типа подписки SQLAlchemy."""

    def test_subscription_type_creation(self):
        """Создание объекта типа подписки."""
        from app.models.user import Subscription_type
        
        sub_type = Subscription_type(
            name="premium",
            description="Premium subscription with unlimited features"
        )

        assert sub_type.name == "premium"


class TestUUIDValidation:
    """Тесты для валидации UUID полей."""

    def test_valid_uuid_format(self):
        """Валидный формат UUID должен проходить проверку."""
        valid_uuid = str(uuid.uuid4())
        
        # Pydantic автоматически валидирует UUID поля
        from pydantic import BaseModel, Field
        
        class TestModel(BaseModel):
            id: uuid.UUID
        
        result = TestModel(id=valid_uuid)
        assert isinstance(result.id, uuid.UUID)

    def test_invalid_uuid_format(self):
        """Невалидный формат UUID должен вызывать ошибку."""
        
        from pydantic import BaseModel, Field
        
        class TestModel(BaseModel):
            id: uuid.UUID
        
        with pytest.raises(ValidationError):
            TestModel(id="not-a-valid-uuid")


class TestDateValidation:
    """Тесты для валидации дат."""

    def test_valid_date_format(self):
        """Валидный формат даты должен проходить проверку."""
        
        from pydantic import BaseModel, Field
        
        class TestModel(BaseModel):
            date_field: date
        
        result = TestModel(date_field=date.today())
        assert isinstance(result.date_field, date)

    def test_invalid_date_format(self):
        """Невалидный формат даты должен вызывать ошибку."""
        
        from pydantic import BaseModel, Field
        
        class TestModel(BaseModel):
            date_field: date
        
        with pytest.raises(ValidationError):
            TestModel(date_field="not-a-date")


class TestDecimalPlacesValidation:
    """Тесты для валидации количества знаков после запятой."""

    def test_valid_decimal_places(self):
        """Валидное количество знаков (0-10)."""
        
        from pydantic import BaseModel, Field
        
        class TestModel(BaseModel):
            decimal_places: int = Field(ge=0, le=10)
        
        result = TestModel(decimal_places=2)
        assert result.decimal_places == 2

    def test_invalid_decimal_places_too_low(self):
        """Невалидное количество знаков (меньше 0)."""
        
        from pydantic import BaseModel, Field
        
        class TestModel(BaseModel):
            decimal_places: int = Field(ge=0, le=10)
        
        with pytest.raises(ValidationError):
            TestModel(decimal_places=-1)

    def test_invalid_decimal_places_too_high(self):
        """Невалидное количество знаков (больше 10)."""
        
        from pydantic import BaseModel, Field
        
        class TestModel(BaseModel):
            decimal_places: int = Field(ge=0, le=10)
        
        with pytest.raises(ValidationError):
            TestModel(decimal_places=15)
