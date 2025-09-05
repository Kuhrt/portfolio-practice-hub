import uuid
from unittest.mock import patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from exceptions.common import UserSettingsServiceError, UserSettingsValidationError
from models.common.user_models import SessionType, Theme, User, UserSettings
from schemas.common import UserSettingsUpdate
from services.common.user_settings_service import UserSettingsService


class TestUserSettingsService:
    def test_get_user_settings_existing_settings(
        self, mock_db_session, mock_redis_client, sample_user_settings
    ):
        # Mock database query to return existing settings
        mock_db_session.execute.return_value.scalar_one_or_none.return_value = (
            sample_user_settings
        )

        service = UserSettingsService(mock_db_session, mock_redis_client)

        result = service.get_user_settings(sample_user_settings.user_id)

        assert result.id == sample_user_settings.id
        assert result.user_id == sample_user_settings.user_id
        assert result.default_session_type == sample_user_settings.default_session_type

    def test_get_user_settings_creates_default_settings(
        self, mock_db_session, mock_redis_client, sample_user
    ):
        # Mock database query to return None (no existing settings)
        mock_db_session.execute.return_value.scalar_one_or_none.return_value = None

        service = UserSettingsService(mock_db_session, mock_redis_client)

        result = service.get_user_settings(sample_user.id)

        assert result.user_id == sample_user.id
        assert result.default_session_type == SessionType.FREE_PLAY
        assert result.theme == Theme.SYSTEM
        assert result.daily_practice_goal_minutes == 30

    def test_get_user_settings_database_error(
        self, mock_db_session, mock_redis_client, sample_user
    ):
        service = UserSettingsService(mock_db_session, mock_redis_client)

        with patch.object(
            mock_db_session, "execute", side_effect=SQLAlchemyError("Database error")
        ):
            with pytest.raises(UserSettingsServiceError) as exc_info:
                service.get_user_settings(sample_user.id)

            assert "Failed to get or create user settings" in str(exc_info.value)

    def test_update_user_settings_success(
        self, mock_db_session, mock_redis_client, sample_user_settings
    ):
        # Mock database query to return existing settings
        mock_db_session.execute.return_value.scalar_one_or_none.return_value = (
            sample_user_settings
        )

        service = UserSettingsService(mock_db_session, mock_redis_client)
        settings_update = UserSettingsUpdate(
            default_session_type="structured",
            theme="dark",
            daily_practice_goal_minutes=60,
            profile_public=True,
        )

        result = service.update_user_settings(
            sample_user_settings.user_id, settings_update
        )

        assert result.default_session_type == SessionType.STRUCTURED
        assert result.theme == Theme.DARK
        assert result.daily_practice_goal_minutes == 60
        assert result.profile_public is True
        assert result.updated_at is not None

    def test_update_user_settings_partial_update(
        self, mock_db_session, mock_redis_client, sample_user_settings
    ):
        # Mock database query to return existing settings
        mock_db_session.execute.return_value.scalar_one_or_none.return_value = (
            sample_user_settings
        )

        service = UserSettingsService(mock_db_session, mock_redis_client)
        settings_update = UserSettingsUpdate(theme="light")

        original_session_type = sample_user_settings.default_session_type
        original_daily_goal = sample_user_settings.daily_practice_goal_minutes

        result = service.update_user_settings(
            sample_user_settings.user_id, settings_update
        )

        assert result.theme == Theme.LIGHT
        assert result.default_session_type == original_session_type
        assert result.daily_practice_goal_minutes == original_daily_goal

    def test_update_user_settings_empty_update(
        self, mock_db_session, mock_redis_client, sample_user_settings
    ):
        # Mock database query to return existing settings
        mock_db_session.execute.return_value.scalar_one_or_none.return_value = (
            sample_user_settings
        )

        service = UserSettingsService(mock_db_session, mock_redis_client)
        settings_update = UserSettingsUpdate()

        original_updated_at = sample_user_settings.updated_at

        result = service.update_user_settings(
            sample_user_settings.user_id, settings_update
        )

        assert result.updated_at is not None
        assert result.updated_at != original_updated_at

    def test_update_user_settings_database_error(
        self, mock_db_session, mock_redis_client, sample_user_settings
    ):
        service = UserSettingsService(mock_db_session, mock_redis_client)
        settings_update = UserSettingsUpdate(theme="dark")

        with patch.object(
            mock_db_session, "execute", side_effect=SQLAlchemyError("Database error")
        ):
            with pytest.raises(UserSettingsServiceError) as exc_info:
                service.update_user_settings(
                    sample_user_settings.user_id, settings_update
                )

            assert "Failed to get or create user settings" in str(exc_info.value)

    def test_get_or_create_user_settings_existing(
        self, mock_db_session, mock_redis_client, sample_user_settings
    ):
        # Mock database query to return existing settings
        mock_db_session.execute.return_value.scalar_one_or_none.return_value = (
            sample_user_settings
        )

        service = UserSettingsService(mock_db_session, mock_redis_client)

        result = service._UserSettingsService__get_or_create_user_settings(
            sample_user_settings.user_id
        )

        assert result.id == sample_user_settings.id
        assert result.user_id == sample_user_settings.user_id

    def test_get_or_create_user_settings_creates_new(
        self, mock_db_session, mock_redis_client, sample_user
    ):
        # Mock database query to return None (no existing settings)
        mock_db_session.execute.return_value.scalar_one_or_none.return_value = None

        service = UserSettingsService(mock_db_session, mock_redis_client)

        result = service._UserSettingsService__get_or_create_user_settings(
            sample_user.id
        )

        assert result.user_id == sample_user.id
        assert result.default_session_type == SessionType.FREE_PLAY
        assert result.theme == Theme.SYSTEM

    def test_get_or_create_user_settings_database_error(
        self, mock_db_session, mock_redis_client, sample_user
    ):
        service = UserSettingsService(mock_db_session, mock_redis_client)

        with patch.object(
            mock_db_session, "execute", side_effect=SQLAlchemyError("Database error")
        ):
            with pytest.raises(UserSettingsServiceError) as exc_info:
                service._UserSettingsService__get_or_create_user_settings(
                    sample_user.id
                )

            assert "Failed to get or create user settings" in str(exc_info.value)

    def test_update_user_settings_validation_error(
        self, mock_db_session, mock_redis_client, sample_user_settings
    ):
        service = UserSettingsService(mock_db_session, mock_redis_client)

        with patch.object(
            UserSettingsUpdate, "model_dump", side_effect=ValueError("Validation error")
        ):
            with pytest.raises(UserSettingsServiceError) as exc_info:
                settings_update = UserSettingsUpdate(theme="dark")
                service.update_user_settings(
                    sample_user_settings.user_id, settings_update
                )

            assert "Unexpected error occurred" in str(exc_info.value)

    def test_get_user_settings_validation_error(
        self, mock_db_session, mock_redis_client, sample_user
    ):
        service = UserSettingsService(mock_db_session, mock_redis_client)

        with patch.object(
            service,
            "_UserSettingsService__get_or_create_user_settings",
            side_effect=UserSettingsValidationError("Validation error"),
        ):
            with pytest.raises(UserSettingsValidationError) as exc_info:
                service.get_user_settings(sample_user.id)

            assert "Validation error" in str(exc_info.value)

    def test_update_user_settings_validation_error(
        self, mock_db_session, mock_redis_client, sample_user_settings
    ):
        service = UserSettingsService(mock_db_session, mock_redis_client)

        with patch.object(
            service,
            "_UserSettingsService__get_or_create_user_settings",
            side_effect=UserSettingsValidationError("Validation error"),
        ):
            with pytest.raises(UserSettingsValidationError) as exc_info:
                settings_update = UserSettingsUpdate(theme="dark")
                service.update_user_settings(
                    sample_user_settings.user_id, settings_update
                )

            assert "Validation error" in str(exc_info.value)
