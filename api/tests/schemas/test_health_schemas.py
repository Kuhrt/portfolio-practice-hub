import pytest
from pydantic import ValidationError

from schemas.common import HealthCheckResponse


class TestHealthCheckResponse:
    def test_health_check_response_creation(self):
        response = HealthCheckResponse(status="OK", version="1.0.0")

        assert response.status == "OK"
        assert response.version == "1.0.0"

    def test_health_check_response_required_fields(self):
        with pytest.raises(ValidationError) as exc_info:
            HealthCheckResponse()

        errors = exc_info.value.errors()
        required_fields = {
            error["loc"][0] for error in errors if error["type"] == "missing"
        }
        assert "status" in required_fields
        assert "version" in required_fields

    def test_health_check_response_serialization(self):
        response = HealthCheckResponse(status="OK", version="1.0.0")
        data = response.model_dump()

        assert data["status"] == "OK"
        assert data["version"] == "1.0.0"

    def test_health_check_response_different_status(self):
        response = HealthCheckResponse(status="ERROR", version="2.0.0")

        assert response.status == "ERROR"
        assert response.version == "2.0.0"

    def test_health_check_response_from_dict(self):
        data = {"status": "OK", "version": "1.0.0"}
        response = HealthCheckResponse(**data)

        assert response.status == "OK"
        assert response.version == "1.0.0"
