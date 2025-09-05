import uuid
from datetime import datetime, timezone
from unittest.mock import Mock, patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from exceptions.common import (
    UserDataValidationError,
    UserNotFoundError,
    UserServiceError,
)
from models.auth import KeycloakUser
from models.common.user_models import SessionType, Theme, User, UserSettings
from schemas.common import UserProfileUpdate
from services.common.user_service import UserService


class TestUserService:
    """Test cases for the UserService class."""

    @pytest.fixture
    def user_service(self, mock_db_session, mock_redis_client):
        """Create a UserService instance for testing."""
        return UserService(mock_db_session, mock_redis_client)

    def test_get_or_create_user_existing_user(
        self, user_service, mock_db_session, sample_user, test_data_factory
    ):
        """Test getting an existing user and updating their information."""
        # Mock database query to return existing user
        mock_db_session.execute.return_value.scalar_one_or_none.return_value = (
            sample_user
        )

        keycloak_user = test_data_factory.create_keycloak_user(
            user_id=sample_user.keycloak_user_id,
            email="updated@example.com",
            username="updateduser",
            first_name="Updated",
            last_name="User",
        )

        result = user_service.get_or_create_user(keycloak_user)

        assert result.id == sample_user.id
        assert result.email == "updated@example.com"
        assert result.username == "updateduser"
        assert result.first_name == "Updated"
        assert result.last_name == "User"
        assert result.last_login is not None
        assert result.updated_at is not None

    def test_get_or_create_user_new_user(
        self, user_service, mock_db_session, sample_keycloak_user
    ):
        """Test creating a new user when none exists."""
        # Mock database query to return None (no existing user)
        mock_db_session.execute.return_value.scalar_one_or_none.return_value = None

        result = user_service.get_or_create_user(sample_keycloak_user)

        assert result.keycloak_user_id == sample_keycloak_user.user_id
        assert result.email == sample_keycloak_user.email
        assert result.username == sample_keycloak_user.username
        assert result.first_name == sample_keycloak_user.first_name
        assert result.last_name == sample_keycloak_user.last_name
        assert result.display_name == "Test User"
        assert result.last_login is not None
        assert result.is_active is True

    def test_get_or_create_user_creates_default_settings(
        self, mock_db_session, mock_redis_client, sample_keycloak_user
    ):
        # Mock database query to return None (no existing user)
        mock_db_session.execute.return_value.scalar_one_or_none.return_value = None

        # Create a mock user that will be returned after creation
        mock_user = User(
            id=uuid.uuid4(),
            keycloak_user_id=sample_keycloak_user.user_id,
            email=sample_keycloak_user.email,
            username=sample_keycloak_user.username,
            first_name=sample_keycloak_user.first_name,
            last_name=sample_keycloak_user.last_name,
            display_name="Test User",
            timezone="UTC",
            is_active=True,
            last_login=datetime.now(timezone.utc),
            created_at=datetime.now(timezone.utc),
            updated_at=None,
        )

        # Mock the refresh to return the user with settings
        def mock_refresh(user):
            # Create default settings and attach them
            settings = UserSettings(
                id=uuid.uuid4(),
                user_id=user.id,
                default_session_type=SessionType.FREE_PLAY,
                theme=Theme.SYSTEM,
                daily_practice_goal_minutes=30,
                created_at=datetime.now(timezone.utc),
                updated_at=None,
            )
            user.settings = settings
            return user

        mock_db_session.refresh.side_effect = mock_refresh

        service = UserService(mock_db_session, mock_redis_client)

        result = service.get_or_create_user(sample_keycloak_user)

        assert result.settings is not None
        assert result.settings.default_session_type == SessionType.FREE_PLAY
        assert result.settings.theme == Theme.SYSTEM
        assert result.settings.daily_practice_goal_minutes == 30

    @pytest.mark.parametrize(
        "user_id,email,expected_error",
        [
            ("", "test@example.com", "Keycloak user ID is required"),
            ("test-id", "", "Email is required"),
            (None, "test@example.com", "Keycloak user ID is required"),
            ("test-id", None, "Email is required"),
        ],
    )
    def test_get_or_create_user_validation_errors(
        self, user_service, user_id, email, expected_error, test_data_factory
    ):
        """Test validation errors for missing required fields."""
        keycloak_user = test_data_factory.create_keycloak_user(
            user_id=user_id or "", email=email or ""
        )

        with pytest.raises(UserDataValidationError) as exc_info:
            user_service.get_or_create_user(keycloak_user)

        assert expected_error in str(exc_info.value)

    def test_get_or_create_user_database_error(
        self, user_service, mock_db_session, sample_keycloak_user
    ):
        """Test handling of database errors during user creation."""
        with patch.object(
            mock_db_session, "execute", side_effect=SQLAlchemyError("Database error")
        ):
            with pytest.raises(UserServiceError) as exc_info:
                user_service.get_or_create_user(sample_keycloak_user)

            assert "Failed to get or create user" in str(exc_info.value)

    def test_get_user_and_settings_existing_user(
        self, user_service, mock_db_session, sample_user_with_settings
    ):
        """Test getting an existing user with their settings."""
        # Mock database query to return user with settings
        mock_db_session.execute.return_value.scalar_one_or_none.return_value = (
            sample_user_with_settings
        )

        result = user_service.get_user_and_settings(sample_user_with_settings.id)

        assert result is not None
        assert result.id == sample_user_with_settings.id
        assert result.settings is not None
        assert result.settings.user_id == sample_user_with_settings.id

    def test_get_user_and_settings_nonexistent_user(
        self, user_service, mock_db_session
    ):
        """Test getting a user that doesn't exist."""
        # Mock database query to return None
        mock_db_session.execute.return_value.scalar_one_or_none.return_value = None

        nonexistent_id = uuid.uuid4()
        result = user_service.get_user_and_settings(nonexistent_id)

        assert result is None

    def test_get_user_and_settings_database_error(
        self, mock_db_session, mock_redis_client
    ):
        service = UserService(mock_db_session, mock_redis_client)
        user_id = uuid.uuid4()

        with patch.object(
            mock_db_session, "execute", side_effect=SQLAlchemyError("Database error")
        ):
            with pytest.raises(UserServiceError) as exc_info:
                service.get_user_and_settings(user_id)

            assert "Failed to get user and settings" in str(exc_info.value)

    def test_update_user_profile_success(
        self, mock_db_session, mock_redis_client, sample_user
    ):
        # Mock database get to return user
        mock_db_session.get.return_value = sample_user

        service = UserService(mock_db_session, mock_redis_client)
        profile_update = UserProfileUpdate(
            display_name="New Display Name", timezone="America/New_York"
        )

        result = service.update_user_profile(sample_user.id, profile_update)

        assert result is not None
        assert result.display_name == "New Display Name"
        assert result.timezone == "America/New_York"
        assert result.updated_at is not None

    def test_update_user_profile_user_not_found(
        self, mock_db_session, mock_redis_client
    ):
        # Mock database get to return None
        mock_db_session.get.return_value = None

        service = UserService(mock_db_session, mock_redis_client)
        nonexistent_id = uuid.uuid4()
        profile_update = UserProfileUpdate(display_name="New Name")

        with pytest.raises(UserNotFoundError) as exc_info:
            service.update_user_profile(nonexistent_id, profile_update)

        assert str(nonexistent_id) in str(exc_info.value)

    def test_update_user_profile_database_error(
        self, mock_db_session, mock_redis_client, sample_user
    ):
        service = UserService(mock_db_session, mock_redis_client)
        profile_update = UserProfileUpdate(display_name="New Name")

        with patch.object(
            mock_db_session, "get", side_effect=SQLAlchemyError("Database error")
        ):
            with pytest.raises(UserServiceError) as exc_info:
                service.update_user_profile(sample_user.id, profile_update)

            assert "Failed to update user profile" in str(exc_info.value)

    def test_get_user_cache_key(self, mock_db_session, mock_redis_client):
        service = UserService(mock_db_session, mock_redis_client)
        keycloak_user_id = "test-keycloak-id"

        cache_key = service.get_user_cache_key(keycloak_user_id)

        assert cache_key == f"user:keycloak:{keycloak_user_id}"

    def test_cache_user_success(self, mock_db_session, mock_redis_client, sample_user):
        service = UserService(mock_db_session, mock_redis_client)

        service.cache_user(sample_user)

        # Verify that redis.set was called
        mock_redis_client.set.assert_called_once()

    def test_cache_user_missing_keycloak_id(self, mock_db_session, mock_redis_client):
        service = UserService(mock_db_session, mock_redis_client)
        user = User(
            id=uuid.uuid4(),
            keycloak_user_id="",
            email="test@example.com",
            username="testuser",
        )

        with pytest.raises(UserDataValidationError) as exc_info:
            service.cache_user(user)

        assert "keycloak_user_id" in str(exc_info.value)

    def test_invalidate_user_cache_success(
        self, mock_db_session, mock_redis_client, sample_user
    ):
        service = UserService(mock_db_session, mock_redis_client)

        service.cache_user(sample_user)
        service.invalidate_user_cache(sample_user.keycloak_user_id)

        # Verify that redis.delete was called
        mock_redis_client.delete.assert_called_once()

    def test_invalidate_user_cache_missing_keycloak_id(
        self, mock_db_session, mock_redis_client
    ):
        service = UserService(mock_db_session, mock_redis_client)

        with pytest.raises(UserDataValidationError) as exc_info:
            service.invalidate_user_cache("")

        assert "Keycloak user ID is required" in str(exc_info.value)

    @pytest.mark.parametrize(
        "first_name,last_name,expected_display",
        [
            ("John", "Doe", "John Doe"),
            ("Jane", "Smith", "Jane Smith"),
            (None, None, "None None"),
            ("John", None, "John None"),
            (None, "Doe", "None Doe"),
            ("", "", "testuser"),  # Service falls back to username when names are empty
        ],
    )
    def test_display_name_generation(
        self,
        user_service,
        mock_db_session,
        first_name,
        last_name,
        expected_display,
        test_data_factory,
    ):
        """Test display name generation with various name combinations."""
        # Mock database query to return None (no existing user)
        mock_db_session.execute.return_value.scalar_one_or_none.return_value = None

        keycloak_user = test_data_factory.create_keycloak_user(
            user_id="test-id",
            email="test@example.com",
            username="testuser",
            first_name=first_name,
            last_name=last_name,
        )

        result = user_service.get_or_create_user(keycloak_user)

        assert result.display_name == expected_display
