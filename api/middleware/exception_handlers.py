import logging
from datetime import datetime, timezone

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from schemas.common import ErrorResponse

logger = logging.getLogger(__name__)


def custom_http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle Exceptions for FastAPI endpoints"""
    if isinstance(exc, HTTPException):
        return http_exception_handler(request, exc)
    elif isinstance(exc, RequestValidationError):
        return http_validation_exception_handler(request, exc)
    else:
        # Check if it's a domain exception that leaked through
        if hasattr(exc, "__module__") and exc.__module__.startswith("exceptions."):
            return http_domain_exception_handler(request, exc)
        return http_general_exception_handler(request, exc)


def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTPException instances"""
    error_response = ErrorResponse(
        error=exc.__class__.__name__,
        message=exc.detail,
        timestamp=datetime.now(timezone.utc).isoformat(),
        path=str(request.url.path),
    )

    logger.warning(
        f"HTTP {exc.status_code} error on {request.method} {request.url.path}: {exc.detail}"
    )

    return JSONResponse(
        status_code=exc.status_code, content=error_response.model_dump()
    )


def http_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle Pydantic validation errors"""
    error_response = ErrorResponse(
        error="ValidationError",
        message="Request validation failed",
        details={"validation_errors": exc.errors()},
        timestamp=datetime.now(timezone.utc).isoformat(),
        path=str(request.url.path),
    )

    logger.warning(
        f"Validation error on {request.method} {request.url.path}: {exc.errors()}"
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.model_dump(),
    )


def http_domain_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle domain exceptions that leaked through to HTTP layer"""
    error_response = ErrorResponse(
        error=exc.__class__.__name__,
        message=str(exc),
        timestamp=datetime.now(timezone.utc).isoformat(),
        path=str(request.url.path),
    )

    logger.error(
        f"Domain exception leaked to HTTP layer on {request.method} {request.url.path}: {str(exc)}",
        exc_info=True,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump(),
    )


def http_general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions"""
    error_response = ErrorResponse(
        error="InternalServerError",
        message="An unexpected error occurred",
        timestamp=datetime.now(timezone.utc).isoformat(),
        path=str(request.url.path),
    )

    logger.error(
        f"Unexpected error on {request.method} {request.url.path}: {str(exc)}",
        exc_info=True,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump(),
    )
