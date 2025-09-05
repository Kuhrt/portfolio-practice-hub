import uuid
from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException, status

from adapters.http.user_service_http_adapter import UserServiceHttpAdapter
from exceptions.common import (
    UserDataValidationError,
    UserNotFoundError,
    UserServiceError,
    UserSettingsServiceError,
    UserSettingsValidationError,
)
from models.common.user_models import SessionType, Theme, User, UserSettings
from schemas.common import UserProfileUpdate, UserSettingsUpdate


class TestUserServiceHttpAdapter:
    def test_get_profile_and_settings_success(self, sample_user_with_settings):
        mock_user_service = Mock()
        mock_user_settings_service = Mock()

        mock_user_service.get_user_and_settings.return_value = sample_user_with_settings

        adapter = UserServiceHttpAdapter(mock_user_service, mock_user_settings_service)

        result = adapter.get_profile_and_settings(sample_user_with_settings.id)

        assert result.profile.id == sample_user_with_settings.id
        assert (
            result.settings.default_session_type
            == sample_user_with_settings.settings.default_session_type.value
        )
        mock_user_service.get_user_and_settings.assert_called_once_with(
            sample_user_with_settings.id
        )

    def test_get_profile_and_settings_user_not_found(self):
        mock_user_service = Mock()
        mock_user_settings_service = Mock()
        mock_user_service.get_user_and_settings.return_value = None

        adapter = UserServiceHttpAdapter(mock_user_service, mock_user_settings_service)
        user_id = uuid.uuid4()

        with pytest.raises(HTTPException) as exc_info:
            adapter.get_profile_and_settings(user_id)

        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc_info.value.detail == "User not found"

    def test_get_profile_and_settings_validation_error(self):
        mock_user_service = Mock()
        mock_user_settings_service = Mock()
        mock_user_service.get_user_and_settings.side_effect = UserDataValidationError(
            "Invalid data", "field"
        )

        adapter = UserServiceHttpAdapter(mock_user_service, mock_user_settings_service)
        user_id = uuid.uuid4()

        with pytest.raises(HTTPException) as exc_info:
            adapter.get_profile_and_settings(user_id)

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid user data" in exc_info.value.detail

    def test_get_profile_and_settings_service_error(self):
        mock_user_service = Mock()
        mock_user_settings_service = Mock()
        mock_user_service.get_user_and_settings.side_effect = UserServiceError(
            "Service error"
        )

        adapter = UserServiceHttpAdapter(mock_user_service, mock_user_settings_service)
        user_id = uuid.uuid4()

        with pytest.raises(HTTPException) as exc_info:
            adapter.get_profile_and_settings(user_id)

        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert exc_info.value.detail == "Internal server error"

    def test_get_profile_and_settings_by_user_success(self, sample_user_with_settings):
        mock_user_service = Mock()
        mock_user_settings_service = Mock()

        adapter = UserServiceHttpAdapter(mock_user_service, mock_user_settings_service)

        result = adapter.get_profile_and_settings_by_user(sample_user_with_settings)

        assert result.profile.id == sample_user_with_settings.id
        assert (
            result.settings.default_session_type
            == sample_user_with_settings.settings.default_session_type.value
        )

    def test_get_profile_and_settings_by_user_missing_settings(self, sample_user):
        mock_user_service = Mock()
        mock_user_settings_service = Mock()
        mock_settings = UserSettings(
            id=uuid.uuid4(),
            user_id=sample_user.id,
            default_session_type=SessionType.FREE_PLAY,
            theme=Theme.SYSTEM,
        )
        mock_user_settings_service.get_user_settings.return_value = mock_settings

        adapter = UserServiceHttpAdapter(mock_user_service, mock_user_settings_service)

        result = adapter.get_profile_and_settings_by_user(sample_user)

        assert result.profile.id == sample_user.id
        assert result.settings.default_session_type == SessionType.FREE_PLAY.value
        mock_user_settings_service.get_user_settings.assert_called_once_with(
            sample_user.id
        )

    def test_get_profile_and_settings_by_user_settings_validation_error(
        self, sample_user
    ):
        mock_user_service = Mock()
        mock_user_settings_service = Mock()
        mock_user_settings_service.get_user_settings.side_effect = (
            UserSettingsValidationError("Settings validation error")
        )

        adapter = UserServiceHttpAdapter(mock_user_service, mock_user_settings_service)

        with pytest.raises(HTTPException) as exc_info:
            adapter.get_profile_and_settings_by_user(sample_user)

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid user settings data" in exc_info.value.detail

    def test_get_profile_and_settings_by_user_settings_service_error(self, sample_user):
        mock_user_service = Mock()
        mock_user_settings_service = Mock()
        mock_user_settings_service.get_user_settings.side_effect = (
            UserSettingsServiceError("Settings service error")
        )

        adapter = UserServiceHttpAdapter(mock_user_service, mock_user_settings_service)

        with pytest.raises(HTTPException) as exc_info:
            adapter.get_profile_and_settings_by_user(sample_user)

        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert exc_info.value.detail == "Internal server error"

    def test_update_user_profile_success(self, sample_user):
        mock_user_service = Mock()
        mock_user_settings_service = Mock()
        mock_user_service.update_user_profile.return_value = sample_user

        adapter = UserServiceHttpAdapter(mock_user_service, mock_user_settings_service)
        profile_update = UserProfileUpdate(display_name="New Name")

        result = adapter.update_user_profile(sample_user.id, profile_update)

        assert result.id == sample_user.id
        mock_user_service.update_user_profile.assert_called_once_with(
            sample_user.id, profile_update
        )

    def test_update_user_profile_user_not_found(self):
        mock_user_service = Mock()
        mock_user_settings_service = Mock()
        mock_user_service.update_user_profile.return_value = None

        adapter = UserServiceHttpAdapter(mock_user_service, mock_user_settings_service)
        user_id = uuid.uuid4()
        profile_update = UserProfileUpdate(display_name="New Name")

        with pytest.raises(HTTPException) as exc_info:
            adapter.update_user_profile(user_id, profile_update)

        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert f"User not found: {user_id}" in exc_info.value.detail

    def test_update_user_profile_not_found_error(self):
        mock_user_service = Mock()
        mock_user_settings_service = Mock()
        user_id = uuid.uuid4()
        mock_user_service.update_user_profile.side_effect = UserNotFoundError(
            str(user_id)
        )

        adapter = UserServiceHttpAdapter(mock_user_service, mock_user_settings_service)
        profile_update = UserProfileUpdate(display_name="New Name")

        with pytest.raises(HTTPException) as exc_info:
            adapter.update_user_profile(user_id, profile_update)

        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert f"User not found: {user_id}" in exc_info.value.detail

    def test_update_user_profile_validation_error(self):
        mock_user_service = Mock()
        mock_user_settings_service = Mock()
        mock_user_service.update_user_profile.side_effect = UserDataValidationError(
            "Validation error", "field"
        )

        adapter = UserServiceHttpAdapter(mock_user_service, mock_user_settings_service)
        user_id = uuid.uuid4()
        profile_update = UserProfileUpdate(display_name="New Name")

        with pytest.raises(HTTPException) as exc_info:
            adapter.update_user_profile(user_id, profile_update)

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid user data" in exc_info.value.detail

    def test_update_user_profile_service_error(self):
        mock_user_service = Mock()
        mock_user_settings_service = Mock()
        mock_user_service.update_user_profile.side_effect = UserServiceError(
            "Service error"
        )

        adapter = UserServiceHttpAdapter(mock_user_service, mock_user_settings_service)
        user_id = uuid.uuid4()
        profile_update = UserProfileUpdate(display_name="New Name")

        with pytest.raises(HTTPException) as exc_info:
            adapter.update_user_profile(user_id, profile_update)

        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert exc_info.value.detail == "Internal server error"

    def test_map_user_and_settings_to_response(self, sample_user_with_settings):
        mock_user_service = Mock()
        mock_user_settings_service = Mock()

        adapter = UserServiceHttpAdapter(mock_user_service, mock_user_settings_service)

        result = adapter._UserServiceHttpAdapter__map_user_and_settings_to_response(
            sample_user_with_settings
        )

        assert result.profile.id == sample_user_with_settings.id
        assert (
            result.settings.default_session_type
            == sample_user_with_settings.settings.default_session_type.value
        )
        assert result.settings.theme == sample_user_with_settings.settings.theme.value
