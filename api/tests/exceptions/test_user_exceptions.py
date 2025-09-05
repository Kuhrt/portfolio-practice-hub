import pytest

from exceptions.common.user_exceptions import (
    UserAlreadyExistsError,
    UserDataValidationError,
    UserNotFoundError,
    UserServiceError,
)


class TestUserServiceError:
    """Test cases for UserServiceError exception."""

    @pytest.mark.parametrize(
        "message,user_id",
        [
            ("Service error occurred", None),
            ("Service error occurred", "user-123"),
            ("Custom error message", "user-456"),
            ("Another error", None),
        ],
    )
    def test_user_service_error_creation(self, message, user_id):
        """Test UserServiceError creation with various parameters."""
        error = UserServiceError(message, user_id=user_id)

        assert str(error) == message
        assert error.message == message
        assert error.user_id == user_id

    def test_user_service_error_inheritance(self):
        """Test that UserServiceError inherits from Exception."""
        error = UserServiceError("Service error occurred")

        assert isinstance(error, Exception)
        assert isinstance(error, UserServiceError)

    def test_user_service_error_message_property(self):
        """Test that the message property works correctly."""
        error = UserServiceError("Custom error message")

        assert error.message == "Custom error message"
        assert str(error) == "Custom error message"


class TestUserNotFoundError:
    """Test cases for UserNotFoundError exception."""

    @pytest.mark.parametrize(
        "user_id",
        [
            "user-123",
            "550e8400-e29b-41d4-a716-446655440000",
            "test-user-id",
            "12345",
            "admin-user",
        ],
    )
    def test_user_not_found_error_creation(self, user_id):
        """Test UserNotFoundError creation with various user IDs."""
        error = UserNotFoundError(user_id)

        expected_message = f"User with ID {user_id} not found"
        assert str(error) == expected_message
        assert error.message == expected_message
        assert error.user_id == user_id

    def test_user_not_found_error_inheritance(self):
        """Test that UserNotFoundError inherits from the correct base classes."""
        error = UserNotFoundError("user-123")

        assert isinstance(error, Exception)
        assert isinstance(error, UserServiceError)
        assert isinstance(error, UserNotFoundError)

    def test_user_not_found_error_message_format(self):
        """Test that the error message format is consistent."""
        user_id = "test-user-456"
        error = UserNotFoundError(user_id)

        expected_message = f"User with ID {user_id} not found"
        assert error.message == expected_message
        assert str(error) == expected_message


class TestUserAlreadyExistsError:
    """Test cases for UserAlreadyExistsError exception."""

    @pytest.mark.parametrize(
        "identifier,identifier_type,expected_message",
        [
            (
                "user-123",
                "keycloak_user_id",
                "User with keycloak_user_id user-123 already exists",
            ),
            (
                "test@example.com",
                "email",
                "User with email test@example.com already exists",
            ),
            ("testuser", "username", "User with username testuser already exists"),
            (
                "550e8400-e29b-41d4-a716-446655440000",
                "uuid",
                "User with uuid 550e8400-e29b-41d4-a716-446655440000 already exists",
            ),
        ],
    )
    def test_user_already_exists_error_creation(
        self, identifier, identifier_type, expected_message
    ):
        """Test UserAlreadyExistsError creation with various identifier types."""
        error = UserAlreadyExistsError(identifier, identifier_type)

        assert str(error) == expected_message
        assert error.message == expected_message
        assert error.user_id == identifier
        assert error.identifier == identifier
        assert error.identifier_type == identifier_type

    def test_user_already_exists_error_default_identifier_type(self):
        """Test that the default identifier type is keycloak_user_id."""
        identifier = "user-123"
        error = UserAlreadyExistsError(identifier)

        expected_message = f"User with keycloak_user_id {identifier} already exists"
        assert str(error) == expected_message
        assert error.identifier_type == "keycloak_user_id"

    def test_user_already_exists_error_inheritance(self):
        """Test that UserAlreadyExistsError inherits from the correct base classes."""
        error = UserAlreadyExistsError("user-123")

        assert isinstance(error, Exception)
        assert isinstance(error, UserServiceError)
        assert isinstance(error, UserAlreadyExistsError)


class TestUserDataValidationError:
    """Test cases for UserDataValidationError exception."""

    @pytest.mark.parametrize(
        "message,field,user_id",
        [
            ("Invalid email format", "email", None),
            ("Invalid data", "username", "user-123"),
            ("General validation error", None, None),
            ("Password required", "password", "user-456"),
            ("Invalid phone number", "phone", None),
        ],
    )
    def test_user_data_validation_error_creation(self, message, field, user_id):
        """Test UserDataValidationError creation with various parameters."""
        error = UserDataValidationError(message, field, user_id)

        assert str(error) == message
        assert error.message == message
        assert error.field == field
        assert error.user_id == user_id

    def test_user_data_validation_error_inheritance(self):
        """Test that UserDataValidationError inherits from the correct base classes."""
        error = UserDataValidationError("Validation error", "field")

        assert isinstance(error, Exception)
        assert isinstance(error, UserServiceError)
        assert isinstance(error, UserDataValidationError)

    def test_user_data_validation_error_properties(self):
        """Test that all properties work correctly."""
        message = "Custom validation message"
        field = "test_field"
        user_id = "test-user-123"

        error = UserDataValidationError(message, field, user_id)

        assert error.message == message
        assert str(error) == message
        assert error.field == field
        assert error.user_id == user_id
