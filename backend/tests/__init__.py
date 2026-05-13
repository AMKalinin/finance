"""
Package для тестов проекта finance-backend.
Содержит все модули с тестами и константы конфигурации.
"""

from .conftest import (
    # Fixtures
    setup_test_db,
    db_session,
    client,
    mock_user_info,
    fin_app,
    test_account_data,
    test_transaction_data,
    test_category_data,
    test_distribution_data,
    test_position_data,
)

# Импортируем все тестовые модули для автоматического обнаружения
from . import (
    test_main,
    test_api_transaction,
    test_api_account,
    test_service_fin_app,
    test_crud_operations,
    test_models_schemas,
    test_distributions_and_integration,
    test_user_service,
)

__all__ = [
    "setup_test_db",
    "db_session",
    "client",
    "mock_user_info",
    "fin_app",
    "test_account_data",
    "test_transaction_data",
    "test_category_data",
    "test_distribution_data",
    "test_position_data",
]
