"""
Common error response schemas for API documentation.
"""

from typing import Any, Dict, Union

# Common error responses that can be reused across routes
COMMON_ERROR_RESPONSES: Dict[Union[int, str], Dict[str, Any]] = {
    400: {
        "description": "Bad Request - Invalid input data",
        "content": {
            "application/json": {
                "example": {
                    "error": "HTTPException",
                    "message": "Invalid user data: Email is required",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "path": "/api/users/me",
                }
            }
        },
    },
    401: {
        "description": "Unauthorized - Authentication required",
        "content": {
            "application/json": {
                "example": {
                    "error": "HTTPException",
                    "message": "Authentication required",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "path": "/api/users/me",
                }
            }
        },
    },
    404: {
        "description": "Not Found - Resource not found",
        "content": {
            "application/json": {
                "example": {
                    "error": "HTTPException",
                    "message": "User not found: 12345",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "path": "/api/users/12345",
                }
            }
        },
    },
    422: {
        "description": "Unprocessable Entity - Validation error",
        "content": {
            "application/json": {
                "example": {
                    "error": "ValidationError",
                    "message": "Request validation failed",
                    "details": {
                        "validation_errors": [
                            {
                                "loc": ["body", "email"],
                                "msg": "field required",
                                "type": "value_error.missing",
                            }
                        ]
                    },
                    "timestamp": "2024-01-15T10:30:00Z",
                    "path": "/api/users/me",
                }
            }
        },
    },
    500: {
        "description": "Internal Server Error - Unexpected error",
        "content": {
            "application/json": {
                "example": {
                    "error": "InternalServerError",
                    "message": "An unexpected error occurred",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "path": "/api/users/me",
                }
            }
        },
    },
}

# User-specific error responses
USER_ERROR_RESPONSES: Dict[Union[int, str], Dict[str, Any]] = {
    **COMMON_ERROR_RESPONSES,
    409: {
        "description": "Conflict - User already exists",
        "content": {
            "application/json": {
                "example": {
                    "error": "HTTPException",
                    "message": "User with keycloak_user_id abc123 already exists",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "path": "/api/users",
                }
            }
        },
    },
}
