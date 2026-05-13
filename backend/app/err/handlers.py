"""
Глобальные обработчики ошибок для FastAPI приложения.
Все кастомные ошибки автоматически конвертируются в HTTP ответы.
"""

import logging
from typing import Union, Optional

from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.err.errors import BaseAPIError
from app.core.config import settings


logger = logging.getLogger(__name__)


async def base_api_error_handler(request: Request, exc: BaseAPIError) -> JSONResponse:
    """Обработчик для всех кастомных API ошибок."""
    logger.warning(
        f"BaseAPIError: {exc.code} - {exc.message}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "detail": exc.detail,
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.code,
            "message": exc.message,
            "detail": exc.detail,
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Обработчик для стандартных HTTP исключений FastAPI."""
    logger.warning(
        f"HTTPException: {exc.status_code} - {exc.detail}",
        extra={"path": request.url.path, "method": request.method}
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP_ERROR",
            "message": exc.detail,
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Обработчик ошибок валидации Pydantic/FastAPI."""
    
    # Форматируем ошибки валидации
    errors = []
    for error in exc.errors():
        field_path = ".".join(str(loc) for loc in error["loc"])
        errors.append({
            "field": field_path,
            "error_type": error.get("type", "unknown"),
            "message": error.get("msg", "Ошибка валидации")
        })
    
    logger.warning(
        f"ValidationError: {len(errors)} ошибок валидации",
        extra={
            "path": request.url.path,
            "method": request.method,
            "errors": errors
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "VALIDATION_ERROR",
            "message": "Ошибка валидации данных",
            "details": errors
        }
    )


async def pydantic_validation_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Обработчик для ошибок валидации Pydantic."""
    
    errors = []
    for error in exc.errors():
        field_path = ".".join(str(loc) for loc in error["loc"])
        errors.append({
            "field": field_path,
            "error_type": error.get("type", "unknown"),
            "message": error.get("msg", "Ошибка валидации")
        })
    
    logger.warning(
        f"PydanticValidationError: {len(errors)} ошибок",
        extra={"path": request.url.path, "method": request.method}
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "VALIDATION_ERROR",
            "message": "Ошибка валидации данных",
            "details": errors
        }
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """Обработчик для ошибок базы данных."""
    
    error_type = type(exc).__name__
    
    if isinstance(exc, IntegrityError):
        detail = "Нарушение целостности данных (дубликат, внешний ключ)"
        status_code = status.HTTP_409_CONFLICT
    else:
        detail = f"Ошибка базы данных: {error_type}"
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    logger.error(
        f"DatabaseError: {detail}",
        exc_info=True,
        extra={"path": request.url.path, "method": request.method}
    )
    
    return JSONResponse(
        status_code=status_code,
        content={
            "error": "DATABASE_ERROR",
            "message": detail,
            "exception_type": error_type
        }
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Обработчик для всех остальных необработанных исключений."""
    
    logger.error(
        f"Unhandled exception: {type(exc).__name__} - {exc}",
        exc_info=True,
        extra={"path": request.url.path, "method": request.method}
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "Внутренняя ошибка сервера",
            "detail": str(exc) if settings.DEBUG else None
        }
    )


def setup_exception_handlers(app):
    """Регистрация всех обработчиков ошибок в приложении."""
    
    from app.core.config import settings
    
    # Register custom API errors
    for error_class in [
        BaseAPIError,
        AuthenticationError,
        AuthorizationError,
        ValidationError,
        NotFoundError,
        DatabaseError,
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
        InvalidUUIDError,
        InvalidDateError,
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
    ]:
        app.add_exception_handler(error_class, base_api_error_handler)
    
    # Register standard exceptions
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ValidationError, pydantic_validation_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)


# Импортируем ошибки для импорта из handlers
from app.err.errors import (
    BaseAPIError,
    AuthenticationError,
    AuthorizationError,
    ValidationError,
    NotFoundError,
    DatabaseError,
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
    InvalidUUIDError,
    InvalidDateError,
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
)
