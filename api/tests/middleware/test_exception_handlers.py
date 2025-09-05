from unittest.mock import Mock

import pytest
from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from middleware.exception_handlers import (
    custom_http_exception_handler,
    http_domain_exception_handler,
    http_exception_handler,
    http_general_exception_handler,
    http_validation_exception_handler,
)
from schemas.common import ErrorResponse


class TestCustomHttpExceptionHandler:
    def test_custom_http_exception_handler_http_exception(self):
        request = Mock(spec=Request)
        request.method = "GET"
        request.url.path = "/api/test"

        exc = HTTPException(status_code=404, detail="Not found")

        response = custom_http_exception_handler(request, exc)

        assert isinstance(response, JSONResponse)
        assert response.status_code == 404

    def test_custom_http_exception_handler_validation_error(self):
        request = Mock(spec=Request)
        request.method = "POST"
        request.url.path = "/api/test"

        exc = RequestValidationError(
            [{"type": "missing", "loc": ["field"], "msg": "Field required"}]
        )

        response = custom_http_exception_handler(request, exc)

        assert isinstance(response, JSONResponse)
        assert response.status_code == 422

    def test_custom_http_exception_handler_domain_exception(self):
        request = Mock(spec=Request)
        request.method = "GET"
        request.url.path = "/api/test"

        class DomainException(Exception):
            __module__ = "exceptions.common"

        exc = DomainException("Domain error")

        response = custom_http_exception_handler(request, exc)

        assert isinstance(response, JSONResponse)
        assert response.status_code == 500

    def test_custom_http_exception_handler_general_exception(self):
        request = Mock(spec=Request)
        request.method = "GET"
        request.url.path = "/api/test"

        exc = Exception("General error")

        response = custom_http_exception_handler(request, exc)

        assert isinstance(response, JSONResponse)
        assert response.status_code == 500


class TestHttpExceptionHandler:
    def test_http_exception_handler_success(self):
        request = Mock(spec=Request)
        request.method = "GET"
        request.url.path = "/api/test"

        exc = HTTPException(status_code=404, detail="Not found")

        response = http_exception_handler(request, exc)

        assert isinstance(response, JSONResponse)
        assert response.status_code == 404

        content = response.body.decode()
        assert "Not found" in content
        assert "HTTPException" in content

    def test_http_exception_handler_different_status_codes(self):
        request = Mock(spec=Request)
        request.method = "GET"
        request.url.path = "/api/test"

        test_cases = [
            (400, "Bad Request"),
            (401, "Unauthorized"),
            (403, "Forbidden"),
            (500, "Internal Server Error"),
        ]

        for status_code, detail in test_cases:
            exc = HTTPException(status_code=status_code, detail=detail)
            response = http_exception_handler(request, exc)

            assert response.status_code == status_code
            content = response.body.decode()
            assert detail in content

    def test_http_exception_handler_response_structure(self):
        request = Mock(spec=Request)
        request.method = "POST"
        request.url.path = "/api/users"

        exc = HTTPException(status_code=400, detail="Invalid data")

        response = http_exception_handler(request, exc)

        assert isinstance(response, JSONResponse)
        assert response.status_code == 400

        content = response.body.decode()
        assert "error" in content
        assert "message" in content
        assert "timestamp" in content
        assert "path" in content


class TestHttpValidationExceptionHandler:
    def test_http_validation_exception_handler_success(self):
        request = Mock(spec=Request)
        request.method = "POST"
        request.url.path = "/api/test"

        validation_errors = [
            {"type": "missing", "loc": ["field1"], "msg": "Field required"},
            {"type": "value_error", "loc": ["field2"], "msg": "Invalid value"},
        ]
        exc = RequestValidationError(validation_errors)

        response = http_validation_exception_handler(request, exc)

        assert isinstance(response, JSONResponse)
        assert response.status_code == 422

        content = response.body.decode()
        assert "ValidationError" in content
        assert "validation_errors" in content

    def test_http_validation_exception_handler_response_structure(self):
        request = Mock(spec=Request)
        request.method = "POST"
        request.url.path = "/api/users"

        validation_errors = [
            {"type": "missing", "loc": ["email"], "msg": "Field required"}
        ]
        exc = RequestValidationError(validation_errors)

        response = http_validation_exception_handler(request, exc)

        assert isinstance(response, JSONResponse)
        assert response.status_code == 422

        content = response.body.decode()
        assert "error" in content
        assert "message" in content
        assert "details" in content
        assert "timestamp" in content
        assert "path" in content


class TestHttpDomainExceptionHandler:
    def test_http_domain_exception_handler_success(self):
        request = Mock(spec=Request)
        request.method = "GET"
        request.url.path = "/api/test"

        class DomainException(Exception):
            __module__ = "exceptions.common"

        exc = DomainException("Domain validation failed")

        response = http_domain_exception_handler(request, exc)

        assert isinstance(response, JSONResponse)
        assert response.status_code == 500

        content = response.body.decode()
        assert "DomainException" in content
        assert "Domain validation failed" in content

    def test_http_domain_exception_handler_response_structure(self):
        request = Mock(spec=Request)
        request.method = "POST"
        request.url.path = "/api/users"

        class UserValidationError(Exception):
            __module__ = "exceptions.common"

        exc = UserValidationError("User data is invalid")

        response = http_domain_exception_handler(request, exc)

        assert isinstance(response, JSONResponse)
        assert response.status_code == 500

        content = response.body.decode()
        assert "error" in content
        assert "message" in content
        assert "timestamp" in content
        assert "path" in content


class TestHttpGeneralExceptionHandler:
    def test_http_general_exception_handler_success(self):
        request = Mock(spec=Request)
        request.method = "GET"
        request.url.path = "/api/test"

        exc = Exception("Unexpected error occurred")

        response = http_general_exception_handler(request, exc)

        assert isinstance(response, JSONResponse)
        assert response.status_code == 500

        content = response.body.decode()
        assert "InternalServerError" in content
        assert "An unexpected error occurred" in content

    def test_http_general_exception_handler_response_structure(self):
        request = Mock(spec=Request)
        request.method = "POST"
        request.url.path = "/api/users"

        exc = RuntimeError("Something went wrong")

        response = http_general_exception_handler(request, exc)

        assert isinstance(response, JSONResponse)
        assert response.status_code == 500

        content = response.body.decode()
        assert "error" in content
        assert "message" in content
        assert "timestamp" in content
        assert "path" in content

    def test_http_general_exception_handler_different_exception_types(self):
        request = Mock(spec=Request)
        request.method = "GET"
        request.url.path = "/api/test"

        test_cases = [
            ValueError("Invalid value"),
            TypeError("Type error"),
            RuntimeError("Runtime error"),
            KeyError("Key not found"),
        ]

        for exc in test_cases:
            response = http_general_exception_handler(request, exc)

            assert isinstance(response, JSONResponse)
            assert response.status_code == 500

            content = response.body.decode()
            assert "InternalServerError" in content
            assert "An unexpected error occurred" in content
