import pytest
from pydantic import ValidationError

from models.auth import KeycloakUser


class TestKeycloakUser:
    def test_keycloak_user_creation(self):
        user = KeycloakUser(
            user_id="test-user-id",
            email="test@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            preferred_username="testuser",
            email_verified=True,
            roles=["user", "admin"],
        )

        assert user.user_id == "test-user-id"
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.preferred_username == "testuser"
        assert user.email_verified is True
        assert user.roles == ["user", "admin"]

    def test_keycloak_user_minimal_data(self):
        user = KeycloakUser(
            user_id="test-user-id", email="test@example.com", username="testuser"
        )

        assert user.user_id == "test-user-id"
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.first_name is None
        assert user.last_name is None
        assert user.preferred_username is None
        assert user.email_verified is False
        assert user.roles == []

    def test_keycloak_user_required_fields(self):
        with pytest.raises(ValidationError) as exc_info:
            KeycloakUser()

        errors = exc_info.value.errors()
        required_fields = {
            error["loc"][0] for error in errors if error["type"] == "missing"
        }
        assert "user_id" in required_fields
        assert "email" in required_fields
        assert "username" in required_fields

    def test_keycloak_user_empty_roles(self):
        user = KeycloakUser(
            user_id="test-user-id",
            email="test@example.com",
            username="testuser",
            roles=[],
        )

        assert user.roles == []

    def test_keycloak_user_boolean_defaults(self):
        user = KeycloakUser(
            user_id="test-user-id", email="test@example.com", username="testuser"
        )

        assert user.email_verified is False

    def test_keycloak_user_serialization(self):
        user = KeycloakUser(
            user_id="test-user-id",
            email="test@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            roles=["user"],
        )

        data = user.model_dump()

        assert data["user_id"] == "test-user-id"
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"
        assert data["first_name"] == "Test"
        assert data["last_name"] == "User"
        assert data["email_verified"] is False
        assert data["roles"] == ["user"]

    def test_keycloak_user_from_dict(self):
        data = {
            "user_id": "test-user-id",
            "email": "test@example.com",
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "preferred_username": "testuser",
            "email_verified": True,
            "roles": ["user", "admin"],
        }

        user = KeycloakUser(**data)

        assert user.user_id == "test-user-id"
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.preferred_username == "testuser"
        assert user.email_verified is True
        assert user.roles == ["user", "admin"]
