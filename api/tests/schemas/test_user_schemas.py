import uuid
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from models.common.user_models import SessionType, Theme, User, UserSettings
from schemas.common import (
    UserProfileResponse,
    UserProfileUpdate,
    UserSettingsResponse,
    UserSettingsUpdate,
    UserWithSettingsResponse,
)


class TestUserProfileResponse:
    def test_user_profile_response_creation(self, sample_user: User):
        response = UserProfileResponse.model_validate(sample_user)

        assert response.id == sample_user.id
        assert response.email == sample_user.email
        assert response.username == sample_user.username
        assert response.first_name == sample_user.first_name
        assert response.last_name == sample_user.last_name
        assert response.display_name == sample_user.display_name
        assert response.timezone == sample_user.timezone
        assert response.last_login == sample_user.last_login
        assert response.created_at == sample_user.created_at

    def test_user_profile_response_serialization(self, sample_user: User):
        response = UserProfileResponse.model_validate(sample_user)
        data = response.model_dump()

        assert "id" in data
        assert "email" in data
        assert "username" in data
        assert "created_at" in data

    def test_user_profile_response_with_none_values(self):
        user_data = {
            "id": uuid.uuid4(),
            "email": "test@example.com",
            "username": "testuser",
            "first_name": None,
            "last_name": None,
            "display_name": None,
            "timezone": "UTC",
            "last_login": None,
            "created_at": datetime.now(timezone.utc),
        }

        response = UserProfileResponse(**user_data)

        assert response.first_name is None
        assert response.last_name is None
        assert response.display_name is None
        assert response.last_login is None


class TestUserSettingsResponse:
    def test_user_settings_response_creation(self, sample_user_settings: UserSettings):
        response = UserSettingsResponse.model_validate(sample_user_settings)

        assert (
            response.default_session_type
            == sample_user_settings.default_session_type.value
        )
        assert (
            response.preferred_tempo_range_min
            == sample_user_settings.preferred_tempo_range_min
        )
        assert (
            response.preferred_tempo_range_max
            == sample_user_settings.preferred_tempo_range_max
        )
        assert (
            response.default_difficulty_level
            == sample_user_settings.default_difficulty_level
        )
        assert (
            response.daily_practice_goal_minutes
            == sample_user_settings.daily_practice_goal_minutes
        )
        assert (
            response.weekly_practice_goal_sessions
            == sample_user_settings.weekly_practice_goal_sessions
        )
        assert response.theme == sample_user_settings.theme.value
        assert response.profile_public == sample_user_settings.profile_public
        assert (
            response.share_practice_stats == sample_user_settings.share_practice_stats
        )
        assert response.updated_at == sample_user_settings.updated_at

    def test_user_settings_response_serialization(
        self, sample_user_settings: UserSettings
    ):
        response = UserSettingsResponse.model_validate(sample_user_settings)
        data = response.model_dump()

        assert "default_session_type" in data
        assert "theme" in data
        assert "daily_practice_goal_minutes" in data


class TestUserSettingsUpdate:
    def test_user_settings_update_empty(self):
        update = UserSettingsUpdate()

        assert update.default_session_type is None
        assert update.preferred_tempo_range_min is None
        assert update.preferred_tempo_range_max is None
        assert update.default_difficulty_level is None
        assert update.daily_practice_goal_minutes is None
        assert update.weekly_practice_goal_sessions is None
        assert update.theme is None
        assert update.profile_public is None
        assert update.share_practice_stats is None

    def test_user_settings_update_partial(self):
        update = UserSettingsUpdate(
            default_session_type="structured",
            theme="dark",
            daily_practice_goal_minutes=60,
        )

        assert update.default_session_type == "structured"
        assert update.theme == "dark"
        assert update.daily_practice_goal_minutes == 60
        assert update.preferred_tempo_range_min is None

    def test_user_settings_update_validation(self):
        # UserSettingsUpdate schema doesn't have validation constraints
        # Validation happens at the model level, not schema level
        update = UserSettingsUpdate(daily_practice_goal_minutes=500)
        assert update.daily_practice_goal_minutes == 500

    def test_user_settings_update_model_dump_exclude_unset(self):
        update = UserSettingsUpdate(default_session_type="structured", theme="dark")

        data = update.model_dump(exclude_unset=True)

        assert "default_session_type" in data
        assert "theme" in data
        assert "daily_practice_goal_minutes" not in data


class TestUserProfileUpdate:
    def test_user_profile_update_empty(self):
        update = UserProfileUpdate()

        assert update.display_name is None
        assert update.timezone is None

    def test_user_profile_update_partial(self):
        update = UserProfileUpdate(
            display_name="New Display Name", timezone="America/New_York"
        )

        assert update.display_name == "New Display Name"
        assert update.timezone == "America/New_York"

    def test_user_profile_update_model_dump_exclude_unset(self):
        update = UserProfileUpdate(display_name="New Name")

        data = update.model_dump(exclude_unset=True)

        assert "display_name" in data
        assert "timezone" not in data


class TestUserWithSettingsResponse:
    def test_user_with_settings_response_creation(
        self, sample_user_with_settings: User
    ):
        profile = UserProfileResponse.model_validate(sample_user_with_settings)
        settings = UserSettingsResponse.model_validate(
            sample_user_with_settings.settings
        )

        response = UserWithSettingsResponse(profile=profile, settings=settings)

        assert response.profile.id == sample_user_with_settings.id
        assert (
            response.settings.default_session_type
            == sample_user_with_settings.settings.default_session_type.value
        )

    def test_user_with_settings_response_serialization(
        self, sample_user_with_settings: User
    ):
        profile = UserProfileResponse.model_validate(sample_user_with_settings)
        settings = UserSettingsResponse.model_validate(
            sample_user_with_settings.settings
        )

        response = UserWithSettingsResponse(profile=profile, settings=settings)
        data = response.model_dump()

        assert "profile" in data
        assert "settings" in data
        assert data["profile"]["id"] == sample_user_with_settings.id
        assert (
            data["settings"]["default_session_type"]
            == sample_user_with_settings.settings.default_session_type.value
        )
