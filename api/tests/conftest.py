import asyncio
import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Generator, List, Optional
from unittest.mock import MagicMock, Mock

import pytest
from fastapi.testclient import TestClient

from main import app
from middleware.auth_middleware import get_keycloak_user
from models.auth import KeycloakUser
from models.common.user_models import SessionType, Theme, User, UserSettings
from services import get_db, get_redis
from services.api.health_api_service import HealthApiService, get_health_api_service
from services.common.user_service import UserService, get_user_service


# Test data factories for better DRY principles
class TestDataFactory:
    """Factory class for creating test data with sensible defaults."""

    @staticmethod
    def create_keycloak_user(
        user_id: str = "test-keycloak-id-123",
        email: str = "test@example.com",
        username: str = "testuser",
        first_name: str = "Test",
        last_name: str = "User",
        preferred_username: str = "testuser",
        email_verified: bool = True,
        roles: List[str] = None,
    ) -> KeycloakUser:
        """Create a KeycloakUser with sensible defaults."""
        if roles is None:
            roles = ["user"]
        return KeycloakUser(
            user_id=user_id,
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            preferred_username=preferred_username,
            email_verified=email_verified,
            roles=roles,
        )

    @staticmethod
    def create_user(
        keycloak_user: KeycloakUser,
        user_id: Optional[uuid.UUID] = None,
        display_name: Optional[str] = None,
        timezone_str: str = "UTC",
        is_active: bool = True,
        last_login: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> User:
        """Create a User with sensible defaults."""
        if user_id is None:
            user_id = uuid.uuid4()
        if last_login is None:
            last_login = datetime.now(timezone.utc)
        if created_at is None:
            created_at = datetime.now(timezone.utc)
        if display_name is None:
            display_name = f"{keycloak_user.first_name} {keycloak_user.last_name}"

        return User(
            id=user_id,
            keycloak_user_id=keycloak_user.user_id,
            email=keycloak_user.email,
            username=keycloak_user.username,
            first_name=keycloak_user.first_name,
            last_name=keycloak_user.last_name,
            display_name=display_name,
            timezone=timezone_str,
            is_active=is_active,
            last_login=last_login,
            created_at=created_at,
            updated_at=updated_at,
        )

    @staticmethod
    def create_user_settings(
        user: User,
        settings_id: Optional[uuid.UUID] = None,
        default_session_type: SessionType = SessionType.FREE_PLAY,
        preferred_tempo_range_min: int = 80,
        preferred_tempo_range_max: int = 140,
        default_difficulty_level: int = 3,
        daily_practice_goal_minutes: int = 30,
        weekly_practice_goal_sessions: int = 5,
        theme: Theme = Theme.SYSTEM,
        profile_public: bool = False,
        share_practice_stats: bool = False,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> UserSettings:
        """Create UserSettings with sensible defaults."""
        if settings_id is None:
            settings_id = uuid.uuid4()
        if created_at is None:
            created_at = datetime.now(timezone.utc)

        return UserSettings(
            id=settings_id,
            user_id=user.id,
            default_session_type=default_session_type,
            preferred_tempo_range_min=preferred_tempo_range_min,
            preferred_tempo_range_max=preferred_tempo_range_max,
            default_difficulty_level=default_difficulty_level,
            daily_practice_goal_minutes=daily_practice_goal_minutes,
            weekly_practice_goal_sessions=weekly_practice_goal_sessions,
            theme=theme,
            profile_public=profile_public,
            share_practice_stats=share_practice_stats,
            created_at=created_at,
            updated_at=updated_at,
        )


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_data_factory():
    """Provide access to the test data factory."""
    return TestDataFactory


@pytest.fixture(scope="function")
def mock_db_session():
    """Mock database session for testing with comprehensive interface."""
    session = MagicMock()
    session.add = Mock()
    session.commit = Mock()
    session.refresh = Mock()
    session.execute = Mock()
    session.get = Mock()
    session.close = Mock()
    session.flush = Mock()
    session.rollback = Mock()
    session.begin = Mock()
    session.begin_nested = Mock()
    return session


@pytest.fixture(scope="function")
def mock_redis_client():
    """Mock Redis client for testing with comprehensive interface."""
    redis_client = MagicMock()
    redis_client.get = Mock(return_value=None)
    redis_client.set = Mock()
    redis_client.delete = Mock()
    redis_client.flushdb = Mock()
    redis_client.close = Mock()
    redis_client.exists = Mock(return_value=False)
    redis_client.expire = Mock()
    redis_client.keys = Mock(return_value=[])
    redis_client.ping = Mock(return_value=True)
    return redis_client


@pytest.fixture
def mock_user_service(sample_user_with_settings):
    """Mock user service for testing"""
    service = Mock(spec=UserService)
    service.get_or_create_user.return_value = sample_user_with_settings
    service.get_user_and_settings.return_value = sample_user_with_settings
    return service


@pytest.fixture
def mock_health_service():
    """Mock health service for testing"""
    from schemas.common import HealthCheckResponse

    service = Mock(spec=HealthApiService)
    service.ping.return_value = HealthCheckResponse(status="OK", version="1.0.0")
    return service


@pytest.fixture
def client(
    mock_db_session,
    mock_redis_client,
    sample_keycloak_user,
    mock_user_service,
    mock_health_service,
):
    def override_get_db():
        yield mock_db_session

    def override_get_redis():
        yield mock_redis_client

    def override_get_keycloak_user():
        return sample_keycloak_user

    def override_get_user_service():
        return mock_user_service

    def override_get_health_api_service():
        return mock_health_service

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = override_get_redis
    app.dependency_overrides[get_keycloak_user] = override_get_keycloak_user
    app.dependency_overrides[get_user_service] = override_get_user_service
    app.dependency_overrides[get_health_api_service] = override_get_health_api_service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def unauthorized_client(
    mock_db_session, mock_redis_client, mock_user_service, mock_health_service
):
    """Client fixture for testing unauthorized access - no auth override"""

    def override_get_db():
        yield mock_db_session

    def override_get_redis():
        yield mock_redis_client

    def override_get_user_service():
        return mock_user_service

    def override_get_health_api_service():
        return mock_health_service

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = override_get_redis
    app.dependency_overrides[get_user_service] = override_get_user_service
    app.dependency_overrides[get_health_api_service] = override_get_health_api_service
    # Note: No get_keycloak_user override - this will cause 401/403

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_keycloak_user(test_data_factory):
    """Create a sample KeycloakUser using the factory."""
    return test_data_factory.create_keycloak_user()


@pytest.fixture
def sample_user(test_data_factory, sample_keycloak_user):
    """Create a sample User using the factory."""
    return test_data_factory.create_user(sample_keycloak_user)


@pytest.fixture
def sample_user_settings(test_data_factory, sample_user):
    """Create sample UserSettings using the factory."""
    return test_data_factory.create_user_settings(sample_user)


@pytest.fixture
def sample_user_with_settings(sample_user, sample_user_settings):
    """Create a user with settings attached."""
    sample_user.settings = sample_user_settings
    return sample_user


# Additional test data fixtures for different scenarios
@pytest.fixture
def admin_keycloak_user(test_data_factory):
    """Create an admin KeycloakUser."""
    return test_data_factory.create_keycloak_user(
        user_id="admin-keycloak-id",
        email="admin@example.com",
        username="admin",
        first_name="Admin",
        last_name="User",
        roles=["admin", "user"],
    )


@pytest.fixture
def inactive_user(test_data_factory, sample_keycloak_user):
    """Create an inactive user."""
    return test_data_factory.create_user(
        sample_keycloak_user, is_active=False, display_name="Inactive User"
    )


@pytest.fixture
def user_with_custom_settings(test_data_factory, sample_user):
    """Create a user with custom settings."""
    return test_data_factory.create_user_settings(
        sample_user,
        default_session_type=SessionType.STRUCTURED,
        theme=Theme.DARK,
        daily_practice_goal_minutes=60,
        profile_public=True,
    )


@pytest.fixture
def auth_headers(sample_keycloak_user):
    """Create authorization headers for testing."""
    return {"Authorization": f"Bearer mock-jwt-token-{sample_keycloak_user.user_id}"}


@pytest.fixture
def mock_jwt_payload(sample_keycloak_user):
    """Create a mock JWT payload for testing."""
    return {
        "sub": sample_keycloak_user.user_id,
        "email": sample_keycloak_user.email,
        "preferred_username": sample_keycloak_user.username,
        "given_name": sample_keycloak_user.first_name,
        "family_name": sample_keycloak_user.last_name,
        "email_verified": sample_keycloak_user.email_verified,
        "realm_access": {"roles": sample_keycloak_user.roles},
        "aud": "test-client",
        "iss": "http://localhost:8080/realms/test",
        "exp": int((datetime.now(timezone.utc).timestamp()) + 3600),
    }


# Modern pytest utilities
@pytest.fixture
def assert_raises():
    """Provide a more readable way to assert exceptions."""

    def _assert_raises(exception_class, *args, **kwargs):
        return pytest.raises(exception_class, *args, **kwargs)

    return _assert_raises


@pytest.fixture
def assert_warns():
    """Provide a more readable way to assert warnings."""

    def _assert_warns(warning_class, *args, **kwargs):
        return pytest.warns(warning_class, *args, **kwargs)

    return _assert_warns


# Parametrized test data
@pytest.fixture(
    params=[
        ("free_play", SessionType.FREE_PLAY),
        ("structured", SessionType.STRUCTURED),
        ("exercise", SessionType.EXERCISE),
        ("repertoire", SessionType.REPERTOIRE),
    ]
)
def session_type_data(request):
    """Provide session type test data for parametrized tests."""
    return request.param


@pytest.fixture(
    params=[
        ("light", Theme.LIGHT),
        ("dark", Theme.DARK),
        ("system", Theme.SYSTEM),
    ]
)
def theme_data(request):
    """Provide theme test data for parametrized tests."""
    return request.param


# Test environment setup
@pytest.fixture(autouse=True)
def setup_test_environment():
    """Automatically set up test environment variables."""
    os.environ.setdefault("TEST_DATABASE_URL", "sqlite:///./test.db")
    os.environ.setdefault("TEST_REDIS_URL", "redis://localhost:6379/1")
    os.environ.setdefault("ENVIRONMENT", "testing")
    yield
    # Cleanup after test
    for key in ["TEST_DATABASE_URL", "TEST_REDIS_URL", "ENVIRONMENT"]:
        if key in os.environ:
            del os.environ[key]
