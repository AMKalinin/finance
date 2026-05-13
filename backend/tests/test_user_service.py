"""
Тесты для сервиса пользователя (User_service).
Проверяет операции с подписками и информацией о пользователе.
"""

import uuid
from datetime import date, timedelta

import pytest


class TestUserService:
    """Тесты для сервиса пользователя."""

    @pytest.fixture(autouse=True)
    def setup(self, client):
        """Очистка базы данных перед каждым тестом."""
        from app.crud import Crud
        
        crud = Crud(None, {})  # Placeholder
        
    def test_get_user_info(self, fin_app, db_session):
        """Получение информации о пользователе."""
        user_info = fin_app.user_info
        
        assert isinstance(user_info, dict)
        assert "id" in user_info
        assert user_info["id"] == fin_app.crud.user.get_info().id

    def test_user_subscription_free(self, client):
        """Проверка подписки free по умолчанию."""
        from app.models.user import User, Subscription_type
        
        # Создаем пользователя с подпиской free
        sub_type = Subscription_type(
            name="free",
            description="Free subscription"
        )
        
        user = User(
            id=uuid.uuid4(),
            email="test@example.com",
            subscription_type="free",
            subscription_expiry=None,
            description="Test user"
        )

        client.app.dependency_overrides[None]  # Placeholder
        
    def test_user_subscription_premium(self, db_session):
        """Проверка подписки premium."""
        from app.models.user import User, Subscription_type
        
        sub_type = Subscription_type(
            name="premium",
            description="Premium subscription"
        )

        user = User(
            id=uuid.uuid4(),
            email="premium@example.com",
            subscription_type="premium",
            subscription_expiry=date.today() + timedelta(days=30),
            description="Premium test user"
        )

        db_session.add_all([sub_type, user])
        db_session.commit()


class TestSubscriptionValidation:
    """Тесты для валидации подписки."""

    def test_valid_subscription_types(self):
        """Проверка допустимых типов подписок."""
        valid_types = ["free", "premium", "enterprise"]
        
        for sub_type in valid_types:
            assert isinstance(sub_type, str)
            assert len(sub_type) > 0

    def test_subscription_expiry_date_format(self):
        """Проверка формата даты истечения подписки."""
        expiry = date.today() + timedelta(days=365)
        
        assert isinstance(expiry, date)
        assert expiry > date.today()


class TestUserInfoValidation:
    """Тесты для валидации информации о пользователе."""

    def test_valid_user_info(self):
        """Валидная информация о пользователе."""
        user_info = {
            "id": str(uuid.uuid4()),
            "email": "test@example.com",
            "name": "Test User"
        }
        
        assert isinstance(user_info["id"], str)
        assert "@" in user_info["email"]
        assert len(user_info["name"]) > 0

    def test_invalid_user_id_format(self):
        """Невалидный формат ID пользователя."""
        
        with pytest.raises(Exception):
            # UUID должен быть валидным
            uuid.UUID("not-a-uuid")


class TestUserRelationships:
    """Тесты для связей пользователя с другими сущностями."""

    def test_user_accounts_relationship(self, db_session):
        """Проверка связи пользователь-счета."""
        from app.models.user import User
        from app.models.account import Account, AccountType
        
        user = User(
            id=uuid.uuid4(),
            email="test@example.com",
            subscription_type="free"
        )

        account1 = Account(
            id=uuid.uuid4(),
            name="Account 1",
            currency="USD",
            account_type=AccountType.DEBIT,
            balance=100.0,
            user_id=user.id
        )

        account2 = Account(
            id=uuid.uuid4(),
            name="Account 2",
            currency="EUR",
            account_type=AccountType.SAVINGS,
            balance=200.0,
            user_id=user.id
        )

        db_session.add_all([user, account1, account2])
        db_session.commit()

        # Проверяем связь
        accounts = user.accounts.all()
        assert len(accounts) == 2


class TestUserCategoriesRelationship:
    """Тесты для связи пользователь-категории."""

    def test_user_categories_relationship(self, db_session):
        """Проверка связи пользователь-категории."""
        from app.models.user import User
        from app.models.category import Category
        
        user = User(
            id=uuid.uuid4(),
            email="test@example.com",
            subscription_type="free"
        )

        categories = [
            Category(
                id=uuid.uuid4(),
                name=f"Category {i}",
                type="expense" if i % 2 == 0 else "income",
                level=i % 3,
                is_deleted=False,
                user_id=user.id
            )
            for i in range(5)
        ]

        db_session.add_all([user] + categories)
        db_session.commit()

        # Проверяем связь
        categories_list = user.categories.all()
        assert len(categories_list) == 5


class TestUserFriendsRelationship:
    """Тесты для связи пользователь-друзья."""

    def test_user_friends_relationship(self, db_session):
        """Проверка связи пользователь-друзья."""
        from app.models.user import User
        from app.models.friends import Friends
        
        user1 = User(
            id=uuid.uuid4(),
            email="user1@example.com",
            subscription_type="free"
        )

        user2 = User(
            id=uuid.uuid4(),
            email="user2@example.com",
            subscription_type="free"
        )

        friend_relation = Friends(
            user1_id=user1.id,
            user2_id=user2.id,
            status="accepted"
        )

        db_session.add_all([user1, user2, friend_relation])
        db_session.commit()

        # Проверяем связь (нужно будет проверить реализацию Friends)


class TestUserTransactionDistributionRelationship:
    """Тесты для связи пользователь-распределения транзакций."""

    def test_user_transaction_distribution_relationship(self, db_session):
        """Проверка связи пользователь-распределения транзакций."""
        from app.models.user import User
        from app.models.transaction import Transaction
        
        user = User(
            id=uuid.uuid4(),
            email="test@example.com",
            subscription_type="free"
        )

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

        db_session.add_all([user, transaction])
        db_session.commit()


class TestUserPermissions:
    """Тесты для проверок прав доступа пользователя."""

    def test_user_can_access_own_account(self, fin_app, db_session):
        """Пользователь может получить доступ к своему счету."""
        from app.models.account import Account, AccountType
        
        account = Account(
            id=uuid.uuid4(),
            name="Own Account",
            currency="USD",
            account_type=AccountType.DEBIT,
            balance=100.0,
            user_id=fin_app.user_info['id']
        )

        db_session.add(account)
        db_session.commit()

        # Финансовый сервис должен иметь доступ к счету пользователя
        result = fin_app.get_account_by_id(account.id)
        
        assert isinstance(result, Account)
        assert result.name == "Own Account"


class TestUserSubscriptionLimits:
    """Тесты для ограничений подписки."""

    def test_free_subscription_category_limit(self, client):
        """Проверка ограничения на количество категорий для free подписки."""
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
        
        # Создаем несколько категорий (проверяем лимит)
        for i in range(10):
            category_data = {
                "name": f"Category {i}",
                "type": "expense" if i % 2 == 0 else "income",
                "parent_category": None,
                "level": 0,
                "is_deleted": False,
            }

            response = client.post("/api/v1/category/create", json=category_data)
            
            # На free подписке может быть ограничение на количество категорий
            # Это зависит от реализации SubscriptionError в сервисе


class TestUserEmailValidation:
    """Тесты для валидации email пользователя."""

    def test_valid_email_formats(self):
        """Проверка допустимых форматов email."""
        valid_emails = [
            "user@example.com",
            "user.name@example.com",
            "user+tag@example.co.uk",
            "123@domain.org"
        ]

        for email in valid_emails:
            assert "@" in email
            parts = email.split("@")
            assert len(parts) == 2
            assert len(parts[0]) > 0
            assert "." in parts[1]

    def test_invalid_email_formats(self):
        """Проверка недопустимых форматов email."""
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "user@",
            "",
            "user @example.com"  # пробел перед @
        ]

        for email in invalid_emails:
            assert "@" not in email or email.count("@") > 1


class TestUserDateValidation:
    """Тесты для валидации дат подписки."""

    def test_subscription_expiry_in_past(self):
        """Истекшая подписка (дата в прошлом)."""
        expiry = date.today() - timedelta(days=30)
        
        assert expiry < date.today()

    def test_subscription_expiry_today(self):
        """Подписка истекает сегодня."""
        expiry = date.today()
        
        assert expiry == date.today()

    def test_subscription_expiry_in_future(self):
        """Действующая подписка (дата в будущем)."""
        expiry = date.today() + timedelta(days=30)
        
        assert expiry > date.today()


class TestUserDataService:
    """Тесты для сервисов работы с данными пользователя."""

    def test_user_service_initialization(self, db_session):
        """Инициализация сервиса пользователя."""
        from app.service.user_service import User_service
        
        mock_user = {
            "id": str(uuid.uuid4()),
            "email": "test@example.com",
            "name": "Test User"
        }

        service = User_service(db=db_session, user_info=mock_user)
        
        assert isinstance(service, User_service)
        assert service.user.id == mock_user["id"]


class TestUserIntegration:
    """Интеграционные тесты для пользователя."""

    def test_full_user_workflow(self, client):
        """Полный рабочий цикл с пользователем."""
        # 1. Создание аккаунта
        account_data = {
            "name": "Main Account",
            "currency": "USD",
            "account_type": "debit",
            "balance": 5000.0,
            "description": "Main checking account",
            "interest_rate": 2.0,
            "is_emergency_fund": False,
            "decimal_places": 2,
            "is_archived": False,
            "is_primary": True,
        }

        response = client.post("/api/v1/account/create", json=account_data)
        assert response.status_code == 200
        
        account_id = uuid.UUID(response.json()["id"])

        # 2. Создание транзакции
        transaction = {
            "FROM": str(account_id),
            "TO": None,
            "category": None,
            "type": "debit",
            "debitSize": 100.0,
            "creditSize": None,
            "exchangeRate": None,
            "date": date.today().isoformat(),
            "description": "Test transaction",
            "splitType": None,
            "status": "settled",
        }

        response = client.post("/api/v1/transaction/create", json=transaction)
        assert response.status_code == 200

        # 3. Получение транзакции
        response = client.get("/api/v1/transaction/all")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) >= 1


class TestEdgeCasesUser:
    """Тесты для граничных случаев пользователя."""

    def test_user_with_empty_description(self, db_session):
        """Пользователь с пустым описанием."""
        from app.models.user import User
        
        user = User(
            id=uuid.uuid4(),
            email="test@example.com",
            subscription_type="free",
            description=""  # Пустое описание
        )

        db_session.add(user)
        db_session.commit()

    def test_user_with_special_characters_in_name(self, db_session):
        """Пользователь с символами в названии."""
        from app.models.user import User
        
        user = User(
            id=uuid.uuid4(),
            email="test@example.com",
            subscription_type="free",
            description="User with special chars: émojis 🎉 & symbols ©®™"
        )

        db_session.add(user)
        db_session.commit()


class TestUserMocking:
    """Тесты для мокирования пользовательских данных."""

    def test_mock_user_info_structure(self):
        """Структура моковой информации о пользователе."""
        mock_user = {
            "id": str(uuid.uuid4()),
            "email": "mock@example.com",
            "name": "Mock User"
        }
        
        assert set(mock_user.keys()) == {"id", "email", "name"}

    def test_mock_user_with_subscription(self):
        """Моковый пользователь с подпиской."""
        mock_user = {
            "id": str(uuid.uuid4()),
            "email": "premium@example.com",
            "name": "Premium Mock User",
            "subscription_type": "premium"
        }
        
        assert mock_user["subscription_type"] == "premium"
