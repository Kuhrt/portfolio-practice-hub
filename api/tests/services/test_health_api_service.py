import pytest
from fastapi import HTTPException, status

from schemas.common import HealthCheckResponse
from services.api.health_api_service import HealthApiService


class TestHealthApiService:
    def test_ping_success(self):
        service = HealthApiService(simulate_failure=False)

        result = service.ping()

        assert isinstance(result, HealthCheckResponse)
        assert result.status == "OK"
        assert result.version == "1.0.0"

    def test_ping_simulate_failure(self):
        service = HealthApiService(simulate_failure=True)

        with pytest.raises(HTTPException) as exc_info:
            service.ping()

        assert exc_info.value.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert exc_info.value.detail == "Service is currently unavailable"

    def test_ping_default_parameters(self):
        service = HealthApiService()

        result = service.ping()

        assert result.status == "OK"
        assert result.version == "1.0.0"

    def test_service_initialization(self):
        service = HealthApiService(simulate_failure=True)

        assert service.simulate_failure is True

    def test_service_initialization_default(self):
        service = HealthApiService()

        assert service.simulate_failure is False

    def test_ping_response_serialization(self):
        service = HealthApiService()

        result = service.ping()
        data = result.model_dump()

        assert data["status"] == "OK"
        assert data["version"] == "1.0.0"
