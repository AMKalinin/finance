# Экспорт ошибок из app.err.errors для удобного импорта
from app.err.errors import (
    # Базовые ошибки
    BaseAPIError,
    AuthenticationError,
    AuthorizationError,
    ValidationError,
    NotFoundError,
    DatabaseError,
    
    # Ошибки бизнес-логики
    SubscriptionError,
    MaxCategoryLevelError,
    CreateCategoryError,
    AcceptFriendError,
    DistributionError,
    TransactionNotFoundError,
    DistributionNotFoundError,
    AccountNotFoundError,
    CategoryNotFoundError,
    UserNotFoundError,
    FriendNotFoundError,
    
    # Ошибки валидации
    InvalidUUIDError,
    InvalidDateError,
    
    # Ошибки транзакций и счетов
    InsufficientFundsError,
    InvalidTransactionTypeError,
    SplitError,
    DuplicateEntryError,
    AlreadyFriendError,
    PendingRequestError,
    InvalidDistributionRoleError,
    InvalidSplitTypeError,
    PositionNotFoundError,
    InvalidAccountType,
    
    # Ошибки лимитов подписки
    AccountLimitError,
    CategoryLimitError,
    TransactionDailyLimitError,
)

__all__ = [
    'BaseAPIError',
    'AuthenticationError',
    'AuthorizationError',
    'ValidationError',
    'NotFoundError',
    'DatabaseError',
    'SubscriptionError',
    'MaxCategoryLevelError',
    'CreateCategoryError',
    'AcceptFriendError',
    'DistributionError',
    'TransactionNotFoundError',
    'DistributionNotFoundError',
    'AccountNotFoundError',
    'CategoryNotFoundError',
    'UserNotFoundError',
    'FriendNotFoundError',
    'InvalidUUIDError',
    'InvalidDateError',
    'InsufficientFundsError',
    'InvalidTransactionTypeError',
    'SplitError',
    'DuplicateEntryError',
    'AlreadyFriendError',
    'PendingRequestError',
    'InvalidDistributionRoleError',
    'InvalidSplitTypeError',
    'PositionNotFoundError',
    'InvalidAccountType',
    'AccountLimitError',
    'CategoryLimitError',
    'TransactionDailyLimitError',
]
