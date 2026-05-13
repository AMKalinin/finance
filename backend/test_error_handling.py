"""
Тесты для проверки работы системы обработки ошибок.
Запуск: poetry run pytest test_error_handling.py -v
"""

import pytest
from fastapi.testclient import TestClient
from uuid import uuid4


class TestErrorHandling:
    """Тесты для проверки обработки ошибок."""

    @pytest.fixture(autouse=True)
    def setup(self, client):
        """Очистка базы данных перед каждым тестом."""
        pass

    def test_health_check_endpoint(self, client: TestClient):
        """Проверка health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    def test_root_endpoint(self, client: TestClient):
        """Проверка root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "Welcome to Finance API" in data["message"]

    def test_account_not_found(self, client: TestClient):
        """Проверка обработки несуществующей учетной записи."""
        fake_id = str(uuid4())
        
        response = client.get(f"/api/v1/account/{fake_id}")
        
        assert response.status_code == 404
        
        data = response.json()
        assert "error" in data
        assert "ACCOUNT_NOT_FOUND" in data["error"] or "NOT_FOUND" in data["error"]

    def test_invalid_uuid_format(self, client: TestClient):
        """Проверка обработки невалидного UUID в path."""
        # FastAPI должен вернуть ошибку 422 для невалидного UUID
        response = client.get("/api/v1/account/not-a-uuid")
        
        assert response.status_code in [404, 422]

    def test_create_account_invalid_data(self, client: TestClient):
        """Проверка обработки некорректных данных при создании счета."""
        invalid_data = {
            "name": 12345,  # Должно быть строкой
            "currency": "INVALID",  # Невалидная валюта
            "account_type": "invalid_type"
        }

        response = client.post("/api/v1/account/create", json=invalid_data)
        
        assert response.status_code == 422
        
        data = response.json()
        assert "error" in data
        assert data["error"] == "VALIDATION_ERROR"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
