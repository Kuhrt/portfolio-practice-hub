import pytest

from exceptions.common.user_settings_exceptions import (
    UserSettingsNotFoundError,
    UserSettingsServiceError,
    UserSettingsValidationError,
)


class TestUserSettingsServiceError:
    def test_user_settings_service_error_creation(self):
        error = UserSettingsServiceError("Settings service error occurred")

        assert str(error) == "Settings service error occurred"
        assert error.message == "Settings service error occurred"
        assert error.user_id is None

    def test_user_settings_service_error_with_user_id(self):
        error = UserSettingsServiceError(
            "Settings service error occurred", user_id="user-123"
        )

        assert str(error) == "Settings service error occurred"
        assert error.message == "Settings service error occurred"
        assert error.user_id == "user-123"

    def test_user_settings_service_error_inheritance(self):
        error = UserSettingsServiceError("Settings service error occurred")

        assert isinstance(error, Exception)
        assert isinstance(error, UserSettingsServiceError)

    def test_user_settings_service_error_message_property(self):
        error = UserSettingsServiceError("Custom settings error message")

        assert error.message == "Custom settings error message"
        assert str(error) == "Custom settings error message"


class TestUserSettingsNotFoundError:
    def test_user_settings_not_found_error_creation(self):
        user_id = "user-123"
        error = UserSettingsNotFoundError(user_id)

        assert str(error) == f"User settings for user {user_id} not found"
        assert error.message == f"User settings for user {user_id} not found"
        assert error.user_id == user_id

    def test_user_settings_not_found_error_different_user_ids(self):
        test_cases = [
            "user-123",
            "550e8400-e29b-41d4-a716-446655440000",
            "test-user-id",
            "12345",
        ]

        for user_id in test_cases:
            error = UserSettingsNotFoundError(user_id)

            assert str(error) == f"User settings for user {user_id} not found"
            assert error.user_id == user_id

    def test_user_settings_not_found_error_inheritance(self):
        error = UserSettingsNotFoundError("user-123")

        assert isinstance(error, Exception)
        assert isinstance(error, UserSettingsServiceError)
        assert isinstance(error, UserSettingsNotFoundError)

    def test_user_settings_not_found_error_message_format(self):
        user_id = "test-user-456"
        error = UserSettingsNotFoundError(user_id)

        expected_message = f"User settings for user {user_id} not found"
        assert error.message == expected_message
        assert str(error) == expected_message


class TestUserSettingsValidationError:
    def test_user_settings_validation_error_creation(self):
        message = "Invalid theme value"
        field = "theme"
        error = UserSettingsValidationError(message, field)

        assert str(error) == message
        assert error.message == message
        assert error.field == field
        assert error.user_id is None

    def test_user_settings_validation_error_with_user_id(self):
        message = "Invalid settings data"
        field = "daily_practice_goal_minutes"
        user_id = "user-123"
        error = UserSettingsValidationError(message, field, user_id)

        assert str(error) == message
        assert error.message == message
        assert error.field == field
        assert error.user_id == user_id

    def test_user_settings_validation_error_without_field(self):
        message = "General settings validation error"
        error = UserSettingsValidationError(message)

        assert str(error) == message
        assert error.message == message
        assert error.field is None
        assert error.user_id is None

    def test_user_settings_validation_error_different_fields(self):
        test_cases = [
            ("Invalid theme", "theme"),
            ("Daily goal too high", "daily_practice_goal_minutes"),
            ("Invalid session type", "default_session_type"),
            ("Tempo range invalid", "preferred_tempo_range_min"),
            ("General settings validation error", None),
        ]

        for message, field in test_cases:
            error = UserSettingsValidationError(message, field)

            assert str(error) == message
            # Handle None case properly
            if field is None:
                assert error.field is None
            else:
                assert error.field == field

    def test_user_settings_validation_error_inheritance(self):
        error = UserSettingsValidationError("Settings validation error", "field")

        assert isinstance(error, Exception)
        assert isinstance(error, UserSettingsServiceError)
        assert isinstance(error, UserSettingsValidationError)

    def test_user_settings_validation_error_message_property(self):
        message = "Custom settings validation message"
        error = UserSettingsValidationError(message, "field")

        assert error.message == message
        assert str(error) == message

    def test_user_settings_validation_error_field_property(self):
        field = "test_field"
        error = UserSettingsValidationError("Error message", field)

        assert error.field == field

    def test_user_settings_validation_error_user_id_property(self):
        user_id = "test-user-123"
        error = UserSettingsValidationError("Error message", "field", user_id)

        assert error.user_id == user_id

    def test_user_settings_validation_error_common_validation_scenarios(self):
        validation_scenarios = [
            ("Theme must be one of: light, dark, system", "theme"),
            (
                "Daily practice goal must be between 5 and 480 minutes",
                "daily_practice_goal_minutes",
            ),
            (
                "Weekly practice goal must be between 1 and 14 sessions",
                "weekly_practice_goal_sessions",
            ),
            (
                "Tempo range minimum must be between 40 and 300",
                "preferred_tempo_range_min",
            ),
            (
                "Tempo range maximum must be between 40 and 300",
                "preferred_tempo_range_max",
            ),
            ("Difficulty level must be between 1 and 5", "default_difficulty_level"),
        ]

        for message, field in validation_scenarios:
            error = UserSettingsValidationError(message, field)

            assert str(error) == message
            assert error.field == field
            assert error.message == message
