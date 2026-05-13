"""
Кастомные исключения для приложения Finance Backend.
Все ошибки наследуются от BaseAPIError, который автоматически конвертируется в HTTP 400/401/403/404/500.
"""

from fastapi import HTTPException, status
from typing import Optional


class BaseAPIError(Exception):
    """Базовый класс для всех API ошибок."""
    
    def __init__(
        self,
        message: str,
        detail: Optional[str] = None,
        code: Optional[str] = None,
        status_code: int = 400
    ):
        self.message = message
        self.detail = detail or message
        self.code = code or type(self).__name__
        self.status_code = status_code
        
        super().__init__(self.message)


class AuthenticationError(BaseAPIError):
    """Ошибка аутентификации."""
    
    def __init__(self, message: str = "Неверные учетные данные"):
        super().__init__(message, code="AUTHENTICATION_ERROR", status_code=status.HTTP_401_UNAUTHORIZED)


class AuthorizationError(BaseAPIError):
    """Ошибка авторизации (нет прав)."""
    
    def __init__(self, message: str = "Доступ запрещен"):
        super().__init__(message, code="AUTHORIZATION_ERROR", status_code=status.HTTP_403_FORBIDDEN)


class ValidationError(BaseAPIError):
    """Ошибка валидации входных данных."""
    
    def __init__(self, message: str, field: Optional[str] = None):
        detail = f"{field}: {message}" if field else message
        super().__init__(message, detail=detail, code="VALIDATION_ERROR", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class NotFoundError(BaseAPIError):
    """Ресурс не найден."""
    
    def __init__(self, resource_name: str, identifier: Optional[str] = None):
        message = f"{resource_name} не найден"
        if identifier:
            message += f": {identifier}"
        super().__init__(message, code="NOT_FOUND_ERROR", status_code=status.HTTP_404_NOT_FOUND)


class DatabaseError(BaseAPIError):
    """Ошибка базы данных."""
    
    def __init__(self, message: str = "Ошибка базы данных"):
        super().__init__(message, code="DATABASE_ERROR", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# === Ошибки бизнес-логики ===

class SubscriptionError(BaseAPIError):
    """Ограничение подписки."""
    
    def __init__(self, message: str = "Доступно только для платных подписок"):
        super().__init__(message, code="SUBSCRIPTION_ERROR", status_code=status.HTTP_402_PAYMENT_REQUIRED)


class MaxCategoryLevelError(BaseAPIError):
    """Ограничение уровня вложенности категорий."""
    
    def __init__(self, message: str = "Максимальный уровень вложенности категорий достигнут"):
        super().__init__(message, code="MAX_CATEGORY_LEVEL_ERROR", status_code=status.HTTP_400_BAD_REQUEST)


class CreateCategoryError(BaseAPIError):
    """Ошибка при создании категории."""
    
    def __init__(self, message: str = "Не удалось создать категорию"):
        super().__init__(message, code="CREATE_CATEGORY_ERROR", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AcceptFriendError(BaseAPIError):
    """Ошибка подтверждения дружбы."""
    
    def __init__(self, message: str = "Не удалось подтвердить дружбу"):
        super().__init__(message, code="ACCEPT_FRIEND_ERROR", status_code=status.HTTP_400_BAD_REQUEST)


class DistributionError(BaseAPIError):
    """Ошибка распределения транзакции."""
    
    def __init__(self, message: str = "Ошибка при создании/обновлении распределения"):
        super().__init__(message, code="DISTRIBUTION_ERROR", status_code=status.HTTP_400_BAD_REQUEST)


class TransactionNotFoundError(BaseAPIError):
    """Транзакция не найдена."""
    
    def __init__(self, transaction_id: str = None):
        message = "Транзакция не найдена"
        if transaction_id:
            message += f": {transaction_id}"
        super().__init__(message, code="TRANSACTION_NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)


class TransactionDailyLimitError(BaseAPIError):
    """Превышение дневного лимита транзакций."""
    
    def __init__(self, message: str = "Достигнут дневной лимит транзакций"):
        super().__init__(message, code="TRANSACTION_DAILY_LIMIT_ERROR", status_code=status.HTTP_402_PAYMENT_REQUIRED)


class DistributionNotFoundError(BaseAPIError):
    """Распределение не найдено."""
    
    def __init__(self, transaction_id: str = None):
        message = "Распределение не найдено"
        if transaction_id:
            message += f": {transaction_id}"
        super().__init__(message, code="DISTRIBUTION_NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)


class AccountNotFoundError(BaseAPIError):
    """Учетная запись не найдена."""
    
    def __init__(self, account_id: str = None):
        message = "Учетная запись не найдена"
        if account_id:
            message += f": {account_id}"
        super().__init__(message, code="ACCOUNT_NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)


class AccountLimitError(BaseAPIError):
    """Превышение лимита на количество счетов."""
    
    def __init__(self, message: str = "Достигнут лимит на создание счетов"):
        super().__init__(message, code="ACCOUNT_LIMIT_ERROR", status_code=status.HTTP_402_PAYMENT_REQUIRED)


class CategoryNotFoundError(BaseAPIError):
    """Категория не найдена."""
    
    def __init__(self, category_id: str = None):
        message = "Категория не найдена"
        if category_id:
            message += f": {category_id}"
        super().__init__(message, code="CATEGORY_NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)


class CategoryLimitError(BaseAPIError):
    """Превышение лимита на создание категорий."""
    
    def __init__(self, message: str = "Достигнут лимит на создание категорий"):
        super().__init__(message, code="CATEGORY_LIMIT_ERROR", status_code=status.HTTP_402_PAYMENT_REQUIRED)


class UserNotFoundError(BaseAPIError):
    """Пользователь не найден."""
    
    def __init__(self, user_id: str = None):
        message = "Пользователь не найден"
        if user_id:
            message += f": {user_id}"
        super().__init__(message, code="USER_NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)


class FriendNotFoundError(BaseAPIError):
    """Друг не найден."""
    
    def __init__(self, friend_id: str = None):
        message = "Друг не найден"
        if friend_id:
            message += f": {friend_id}"
        super().__init__(message, code="FRIEND_NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)


class InvalidUUIDError(ValidationError):
    """Некорректный формат UUID."""
    
    def __init__(self, field: str = "id"):
        super().__init__("Неверный формат UUID", field=field)


class InvalidDateError(ValidationError):
    """Некорректный формат даты."""
    
    def __init__(self, field: str = "date"):
        super().__init__("Неверный формат даты. Используйте YYYY-MM-DD", field=field)


class InsufficientFundsError(BaseAPIError):
    """Недостаточно средств на счете."""
    
    def __init__(self, account_name: str = None):
        message = "Недостаточно средств"
        if account_name:
            message += f" на счете '{account_name}'"
        super().__init__(message, code="INSUFFICIENT_FUNDS", status_code=status.HTTP_400_BAD_REQUEST)


class InvalidTransactionTypeError(BaseAPIError):
    """Некорректный тип транзакции."""
    
    def __init__(self, message: str = "Недопустимая комбинация типа транзакции и параметров"):
        super().__init__(message, code="INVALID_TRANSACTION_TYPE", status_code=status.HTTP_400_BAD_REQUEST)


class SplitError(BaseAPIError):
    """Ошибка при создании распределения (сумма != 100%)."""
    
    def __init__(self, message: str = "Сумма долей должна составлять 100%"):
        super().__init__(message, code="SPLIT_ERROR", status_code=status.HTTP_400_BAD_REQUEST)


class DuplicateEntryError(BaseAPIError):
    """Дубликат записи."""
    
    def __init__(self, resource_name: str = None):
        message = f"Запись '{resource_name}' уже существует" if resource_name else "Запись уже существует"
        super().__init__(message, code="DUPLICATE_ENTRY", status_code=status.HTTP_409_CONFLICT)


class AlreadyFriendError(BaseAPIError):
    """Пользователь уже в друзьях."""
    
    def __init__(self, friend_id: str = None):
        message = "Пользователь уже добавлен в друзья"
        if friend_id:
            message += f": {friend_id}"
        super().__init__(message, code="ALREADY_FRIEND", status_code=status.HTTP_409_CONFLICT)


class PendingRequestError(BaseAPIError):
    """Ожидает подтверждения запроса."""
    
    def __init__(self, friend_id: str = None):
        message = "Запрос в дружбе еще не подтвержден"
        if friend_id:
            message += f": {friend_id}"
        super().__init__(message, code="PENDING_REQUEST", status_code=status.HTTP_409_CONFLICT)


class InvalidDistributionRoleError(BaseAPIError):
    """Некорректная роль в распределении."""
    
    def __init__(self, message: str = "Роль должна быть 'owner' или 'participant'"):
        super().__init__(message, code="INVALID_DISTRIBUTION_ROLE", status_code=status.HTTP_400_BAD_REQUEST)


class InvalidSplitTypeError(BaseAPIError):
    """Некорректный тип сплита."""
    
    def __init__(self, message: str = "Тип сплита должен быть 'equal', 'percentage', 'amount' или 'position'"):
        super().__init__(message, code="INVALID_SPLIT_TYPE", status_code=status.HTTP_400_BAD_REQUEST)


class PositionNotFoundError(BaseAPIError):
    """Позиция не найдена."""
    
    def __init__(self, position_id: str = None):
        message = "Позиция не найдена"
        if position_id:
            message += f": {position_id}"
        super().__init__(message, code="POSITION_NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)


class InvalidAccountType(BaseAPIError):
    """Некорректный тип учетной записи."""
    
    def __init__(self, account_type: str = None):
        message = f"Недопустимый тип счетa: {account_type}" if account_type else "Недопустимый тип счета"
        super().__init__(message, code="INVALID_ACCOUNT_TYPE", status_code=status.HTTP_400_BAD_REQUEST)
