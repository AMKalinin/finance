"""
Базовые тесты для проверки работоспособности проекта.
Эти тесты должны всегда проходить.
"""


def test_project_structure():
    """Проверка структуры проекта."""
    import os
    
    # Проверим основные директории
    assert os.path.exists("app"), "Директория app не найдена"
    assert os.path.exists("tests"), "Директория tests не найдена"
    
    # Проверим важные файлы
    assert os.path.exists("pyproject.toml"), "Файл pyproject.toml не найден"
    assert os.path.exists("pytest.ini"), "Файл pytest.ini не найден"


def test_import_app():
    """Проверка импорта приложения."""
    from app.main import create_fastapi_app
    
    app = create_fastapi_app()
    
    assert app is not None
    assert hasattr(app, 'router')


def test_import_models():
    """Проверка импорта моделей."""
    from app.models.account import Account, AccountType
    from app.models.transaction import Transaction, Transaction_type
    from app.models.category import Category
    from app.models.user import User
    
    # Проверим что модели доступны
    assert Account is not None
    assert AccountType is not None
    assert Transaction is not None
    assert Category is not None
    assert User is not None


def test_import_schemas():
    """Проверка импорта Pydantic схем."""
    from app.schemas.transaction import (
        transaction_in,
        transaction_out,
        transaction_in_size,
        transaction_in_date,
        distribution_in,
        position_in,
    )
    from app.schemas.account import account_in, account_out
    
    # Проверим что схемы доступны
    assert transaction_in is not None
    assert transaction_out is not None
    assert account_in is not None
    assert account_out is not None


def test_import_crud():
    """Проверка импорта CRUD операций."""
    from app.crud import Crud
    
    # Проверим что CRUD класс доступен
    assert Crud is not None


def test_import_services():
    """Проверка импорта сервисов."""
    from app.service.fin_app import Fin_app
    from app.service.user_service import User_service
    
    # Проверим что сервисы доступны
    assert Fin_app is not None
    assert User_service is not None


def test_api_router_exists():
    """Проверка наличия роутера API."""
    from fastapi.routing import APIRouter
    
    from app.api.api_v1.api import api_router
    
    # Проверим что роутер существует и имеет маршруты
    assert api_router is not None
    assert len(api_router.routes) > 0


def test_settings_loaded():
    """Проверка загрузки настроек."""
    from app.core.config import settings
    
    # Проверим основные настройки
    assert hasattr(settings, 'API_V1_STR')
    assert settings.API_V1_STR == "/api/v1"
