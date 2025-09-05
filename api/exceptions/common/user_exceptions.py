"""
Domain exceptions for user-related business logic.
"""


class UserServiceError(Exception):
    """Base exception for user service errors"""

    def __init__(self, message: str, user_id: str | None = None):
        self.message = message
        self.user_id = user_id
        super().__init__(message)


class UserNotFoundError(UserServiceError):
    """Raised when a user is not found"""

    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__(f"User with ID {user_id} not found", user_id)


class UserAlreadyExistsError(UserServiceError):
    """Raised when trying to create a user that already exists"""

    def __init__(self, identifier: str, identifier_type: str = "keycloak_user_id"):
        self.identifier = identifier
        self.identifier_type = identifier_type
        super().__init__(
            f"User with {identifier_type} {identifier} already exists", identifier
        )


class UserDataValidationError(UserServiceError):
    """Raised when user data validation fails"""

    def __init__(
        self, message: str, field: str | None = None, user_id: str | None = None
    ):
        self.field = field
        super().__init__(message, user_id)
