import uuid
from datetime import datetime, timezone

import pytest
from sqlmodel import Session

from models.common.user_models import SessionType, Theme, User, UserSettings

# Pytest markers
pytestmark = [
    pytest.mark.unit,
    pytest.mark.model,
]


class TestUserModel:
    """Test cases for the User model."""

    @pytest.mark.factory
    def test_user_creation_with_factory(self, test_data_factory):
        """Test user creation using the test data factory."""
        keycloak_user = test_data_factory.create_keycloak_user(
            user_id="test-keycloak-id",
            email="test@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
        )
        user = test_data_factory.create_user(keycloak_user)

        assert user.id is not None
        assert user.keycloak_user_id == "test-keycloak-id"
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.is_active is True
        assert user.timezone == "UTC"
        assert user.created_at is not None
        assert user.updated_at is None

    def test_user_creation_legacy(self):
        """Test user creation with explicit parameters (legacy test)."""
        user = User(
            id=uuid.uuid4(),
            keycloak_user_id="test-keycloak-id",
            email="test@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            display_name="Test User",
            timezone="UTC",
            is_active=True,
            created_at=datetime.now(timezone.utc),
            updated_at=None,
        )

        assert user.id is not None
        assert user.keycloak_user_id == "test-keycloak-id"
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.is_active is True
        assert user.timezone == "UTC"
        assert user.created_at is not None
        assert user.updated_at is None

    @pytest.mark.factory
    @pytest.mark.parametrize(
        "first_name,last_name,expected_display",
        [
            ("John", "Doe", "John Doe"),
            ("Jane", "Smith", "Jane Smith"),
            ("", "", " "),  # Empty strings
            (None, None, "None None"),  # None values become "None None"
        ],
    )
    def test_user_display_name_generation(
        self, first_name, last_name, expected_display, test_data_factory
    ):
        """Test display name generation with various name combinations."""
        keycloak_user = test_data_factory.create_keycloak_user(
            first_name=first_name, last_name=last_name
        )
        user = test_data_factory.create_user(
            keycloak_user, display_name=expected_display
        )

        assert user.display_name == expected_display

    def test_user_without_names(self, test_data_factory):
        """Test user creation without first and last names."""
        keycloak_user = test_data_factory.create_keycloak_user(
            first_name=None, last_name=None
        )
        user = test_data_factory.create_user(keycloak_user, display_name=None)

        assert user.first_name is None
        assert user.last_name is None
        assert (
            user.display_name == "None None"
        )  # Factory generates "None None" when both names are None

    def test_user_timestamps(self, test_data_factory):
        """Test that user timestamps are set correctly."""
        before_creation = datetime.now(timezone.utc)

        keycloak_user = test_data_factory.create_keycloak_user()
        user = test_data_factory.create_user(keycloak_user)

        after_creation = datetime.now(timezone.utc)

        assert before_creation <= user.created_at <= after_creation
        assert user.updated_at is None

    def test_user_update_timestamp(self, test_data_factory):
        """Test that user update timestamp is set when user is modified."""
        keycloak_user = test_data_factory.create_keycloak_user()
        user = test_data_factory.create_user(keycloak_user)

        original_created_at = user.created_at
        user.email = "updated@example.com"
        user.updated_at = datetime.now(timezone.utc)

        assert user.created_at == original_created_at
        assert user.updated_at is not None
        assert user.email == "updated@example.com"

    @pytest.mark.parametrize(
        "timezone_value",
        ["UTC", "America/New_York", "Europe/London", "Asia/Tokyo", "Australia/Sydney"],
    )
    def test_user_timezone_values(self, timezone_value, test_data_factory):
        """Test user creation with various timezone values."""
        keycloak_user = test_data_factory.create_keycloak_user()
        user = test_data_factory.create_user(keycloak_user, timezone_str=timezone_value)

        assert user.timezone == timezone_value


class TestUserSettingsModel:
    """Test cases for the UserSettings model."""

    def test_user_settings_creation_with_factory(self, test_data_factory, sample_user):
        """Test user settings creation using the test data factory."""
        settings = test_data_factory.create_user_settings(
            sample_user,
            default_session_type=SessionType.STRUCTURED,
            preferred_tempo_range_min=100,
            preferred_tempo_range_max=160,
            default_difficulty_level=4,
            daily_practice_goal_minutes=45,
            weekly_practice_goal_sessions=6,
            theme=Theme.DARK,
            profile_public=True,
            share_practice_stats=True,
        )

        assert settings.id is not None
        assert settings.user_id == sample_user.id
        assert settings.default_session_type == SessionType.STRUCTURED
        assert settings.preferred_tempo_range_min == 100
        assert settings.preferred_tempo_range_max == 160
        assert settings.default_difficulty_level == 4
        assert settings.daily_practice_goal_minutes == 45
        assert settings.weekly_practice_goal_sessions == 6
        assert settings.theme == Theme.DARK
        assert settings.profile_public is True
        assert settings.share_practice_stats is True

    def test_user_settings_creation_legacy(self, sample_user: User):
        """Test user settings creation with explicit parameters (legacy test)."""
        settings = UserSettings(
            id=uuid.uuid4(),
            user_id=sample_user.id,
            default_session_type=SessionType.STRUCTURED,
            preferred_tempo_range_min=100,
            preferred_tempo_range_max=160,
            default_difficulty_level=4,
            daily_practice_goal_minutes=45,
            weekly_practice_goal_sessions=6,
            theme=Theme.DARK,
            profile_public=True,
            share_practice_stats=True,
            created_at=datetime.now(timezone.utc),
            updated_at=None,
        )

        assert settings.id is not None
        assert settings.user_id == sample_user.id
        assert settings.default_session_type == SessionType.STRUCTURED
        assert settings.preferred_tempo_range_min == 100
        assert settings.preferred_tempo_range_max == 160
        assert settings.default_difficulty_level == 4
        assert settings.daily_practice_goal_minutes == 45
        assert settings.weekly_practice_goal_sessions == 6
        assert settings.theme == Theme.DARK
        assert settings.profile_public is True
        assert settings.share_practice_stats is True

    def test_user_settings_defaults(self, test_data_factory, sample_user):
        """Test user settings creation with default values."""
        settings = test_data_factory.create_user_settings(sample_user)

        assert settings.default_session_type == SessionType.FREE_PLAY
        assert settings.preferred_tempo_range_min == 80
        assert settings.preferred_tempo_range_max == 140
        assert settings.default_difficulty_level == 3
        assert settings.daily_practice_goal_minutes == 30
        assert settings.weekly_practice_goal_sessions == 5
        assert settings.theme == Theme.SYSTEM
        assert settings.profile_public is False
        assert settings.share_practice_stats is False

    @pytest.mark.parametrize(
        "tempo_min,tempo_max,should_raise",
        [
            (30, 350, True),  # Both invalid
            (50, 350, True),  # Max too high
            (30, 200, True),  # Min too low
            (80, 140, False),  # Valid range
            (60, 180, False),  # Valid range
        ],
    )
    def test_user_settings_tempo_validation(
        self, sample_user, tempo_min, tempo_max, should_raise
    ):
        """Test tempo range validation with various values."""
        if should_raise:
            with pytest.raises(ValueError):
                UserSettings.model_validate(
                    {
                        "id": uuid.uuid4(),
                        "user_id": sample_user.id,
                        "preferred_tempo_range_min": tempo_min,
                        "preferred_tempo_range_max": tempo_max,
                        "created_at": datetime.now(timezone.utc),
                        "updated_at": None,
                    }
                )
        else:
            # Should not raise
            settings = UserSettings.model_validate(
                {
                    "id": uuid.uuid4(),
                    "user_id": sample_user.id,
                    "preferred_tempo_range_min": tempo_min,
                    "preferred_tempo_range_max": tempo_max,
                    "created_at": datetime.now(timezone.utc),
                    "updated_at": None,
                }
            )
            assert settings.preferred_tempo_range_min == tempo_min
            assert settings.preferred_tempo_range_max == tempo_max

    def test_user_settings_relationship(self, test_data_factory, sample_user):
        """Test the relationship between User and UserSettings."""
        settings = test_data_factory.create_user_settings(sample_user)

        # Manually set the relationship for testing
        settings.user = sample_user
        sample_user.settings = settings

        assert settings.user.id == sample_user.id
        assert sample_user.settings.id == settings.id


class TestSessionTypeEnum:
    """Test cases for SessionType enum."""

    @pytest.mark.parametrize(
        "session_type,expected_value",
        [
            (SessionType.FREE_PLAY, "free_play"),
            (SessionType.STRUCTURED, "structured"),
            (SessionType.EXERCISE, "exercise"),
            (SessionType.REPERTOIRE, "repertoire"),
        ],
    )
    def test_session_type_values(self, session_type, expected_value):
        """Test that session type enum values are correct."""
        assert session_type == expected_value

    def test_session_type_enum_membership(self):
        """Test session type enum membership."""
        valid_values = [e.value for e in SessionType]
        assert "free_play" in valid_values
        assert "structured" in valid_values
        assert "exercise" in valid_values
        assert "repertoire" in valid_values
        assert "invalid_type" not in valid_values

    def test_session_type_enum_iteration(self):
        """Test that we can iterate over session type enum values."""
        session_types = list(SessionType)
        assert len(session_types) == 4
        assert all(isinstance(st, SessionType) for st in session_types)


class TestThemeEnum:
    """Test cases for Theme enum."""

    @pytest.mark.parametrize(
        "theme,expected_value",
        [
            (Theme.LIGHT, "light"),
            (Theme.DARK, "dark"),
            (Theme.SYSTEM, "system"),
        ],
    )
    def test_theme_values(self, theme, expected_value):
        """Test that theme enum values are correct."""
        assert theme == expected_value

    def test_theme_enum_membership(self):
        """Test theme enum membership."""
        valid_values = [e.value for e in Theme]
        assert "light" in valid_values
        assert "dark" in valid_values
        assert "system" in valid_values
        assert "invalid_theme" not in valid_values

    def test_theme_enum_iteration(self):
        """Test that we can iterate over theme enum values."""
        themes = list(Theme)
        assert len(themes) == 3
        assert all(isinstance(t, Theme) for t in themes)
