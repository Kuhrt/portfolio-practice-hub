import pytest
from pydantic import ValidationError

from schemas.common import ErrorDetail, ErrorResponse


class TestErrorDetail:
    def test_error_detail_creation(self):
        detail = ErrorDetail(
            field="email", message="Invalid email format", code="INVALID_EMAIL"
        )

        assert detail.field == "email"
        assert detail.message == "Invalid email format"
        assert detail.code == "INVALID_EMAIL"

    def test_error_detail_minimal(self):
        detail = ErrorDetail(message="Something went wrong")

        assert detail.field is None
        assert detail.message == "Something went wrong"
        assert detail.code is None

    def test_error_detail_required_message(self):
        with pytest.raises(ValidationError) as exc_info:
            ErrorDetail()

        errors = exc_info.value.errors()
        required_fields = {
            error["loc"][0] for error in errors if error["type"] == "missing"
        }
        assert "message" in required_fields

    def test_error_detail_serialization(self):
        detail = ErrorDetail(
            field="username",
            message="Username already exists",
            code="DUPLICATE_USERNAME",
        )

        data = detail.model_dump()

        assert data["field"] == "username"
        assert data["message"] == "Username already exists"
        assert data["code"] == "DUPLICATE_USERNAME"


class TestErrorResponse:
    def test_error_response_creation(self):
        response = ErrorResponse(
            error="ValidationError",
            message="Request validation failed",
            details={"field": "email", "issue": "invalid format"},
            timestamp="2024-01-01T00:00:00Z",
            path="/api/users",
        )

        assert response.error == "ValidationError"
        assert response.message == "Request validation failed"
        assert response.details == {"field": "email", "issue": "invalid format"}
        assert response.timestamp == "2024-01-01T00:00:00Z"
        assert response.path == "/api/users"

    def test_error_response_minimal(self):
        response = ErrorResponse(
            error="InternalServerError", message="An unexpected error occurred"
        )

        assert response.error == "InternalServerError"
        assert response.message == "An unexpected error occurred"
        assert response.details is None
        assert response.timestamp is None
        assert response.path is None

    def test_error_response_required_fields(self):
        with pytest.raises(ValidationError) as exc_info:
            ErrorResponse()

        errors = exc_info.value.errors()
        required_fields = {
            error["loc"][0] for error in errors if error["type"] == "missing"
        }
        assert "error" in required_fields
        assert "message" in required_fields

    def test_error_response_with_details_dict(self):
        details = {
            "validation_errors": [
                {"field": "email", "message": "Invalid email format"},
                {"field": "password", "message": "Password too short"},
            ],
            "request_id": "req-123",
        }

        response = ErrorResponse(
            error="ValidationError",
            message="Multiple validation errors",
            details=details,
        )

        assert response.details == details
        assert len(response.details["validation_errors"]) == 2

    def test_error_response_serialization(self):
        response = ErrorResponse(
            error="NotFoundError", message="Resource not found", path="/api/users/123"
        )

        data = response.model_dump()

        assert data["error"] == "NotFoundError"
        assert data["message"] == "Resource not found"
        assert data["path"] == "/api/users/123"
        assert "timestamp" in data or data["timestamp"] is None
