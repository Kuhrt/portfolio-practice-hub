"""
Domain exceptions for user settings-related business logic.
"""


class UserSettingsServiceError(Exception):
    """Base exception for user settings service errors"""

    def __init__(self, message: str, user_id: str | None = None):
        self.message = message
        self.user_id = user_id
        super().__init__(message)


class UserSettingsNotFoundError(UserSettingsServiceError):
    """Raised when user settings are not found"""

    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__(f"User settings for user {user_id} not found", user_id)


class UserSettingsValidationError(UserSettingsServiceError):
    """Raised when user settings data validation fails"""

    def __init__(
        self, message: str, field: str | None = None, user_id: str | None = None
    ):
        self.field = field
        super().__init__(message, user_id)
