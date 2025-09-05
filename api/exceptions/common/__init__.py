"""
Domain exceptions for the service layer.

These exceptions represent business logic errors and can be handled differently
in different contexts (HTTP, CLI, background jobs, etc.).
"""

from .user_exceptions import (
    UserAlreadyExistsError,
    UserDataValidationError,
    UserNotFoundError,
    UserServiceError,
)
from .user_settings_exceptions import (
    UserSettingsNotFoundError,
    UserSettingsServiceError,
    UserSettingsValidationError,
)

__all__ = [
    # User exceptions
    "UserNotFoundError",
    "UserAlreadyExistsError",
    "UserDataValidationError",
    "UserServiceError",
    # User settings exceptions
    "UserSettingsNotFoundError",
    "UserSettingsValidationError",
    "UserSettingsServiceError",
]
