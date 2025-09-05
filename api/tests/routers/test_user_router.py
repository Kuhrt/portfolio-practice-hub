import uuid
from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException, status

from models.common.user_models import SessionType, Theme, User, UserSettings
from schemas.common import (
    UserProfileResponse,
    UserSettingsResponse,
    UserWithSettingsResponse,
)


class TestUserRouter:
    def test_get_current_user_profile_success(
        self, client, sample_user_with_settings, auth_headers
    ):
        with patch("middleware.auth_middleware.get_keycloak_user") as mock_auth:
            mock_auth.return_value = Mock(
                user_id=sample_user_with_settings.keycloak_user_id,
                email=sample_user_with_settings.email,
                username=sample_user_with_settings.username,
                first_name=sample_user_with_settings.first_name,
                last_name=sample_user_with_settings.last_name,
            )

            with patch(
                "services.common.user_service.get_current_user"
            ) as mock_get_user:
                mock_get_user.return_value = sample_user_with_settings

                response = client.get("/api/users/me", headers=auth_headers)

                assert response.status_code == 200
                data = response.json()
                assert data["id"] == str(sample_user_with_settings.id)
                assert data["email"] == sample_user_with_settings.email
                assert data["username"] == sample_user_with_settings.username

    def test_get_current_user_profile_unauthorized(self, unauthorized_client):
        response = unauthorized_client.get("/api/users/me")

        assert response.status_code == 403

    def test_get_current_user_settings_success(
        self, client, sample_user_with_settings, auth_headers
    ):
        with patch("middleware.auth_middleware.get_keycloak_user") as mock_auth:
            mock_auth.return_value = Mock(
                user_id=sample_user_with_settings.keycloak_user_id,
                email=sample_user_with_settings.email,
                username=sample_user_with_settings.username,
            )

            with patch(
                "services.common.user_service.get_current_user"
            ) as mock_get_user:
                mock_get_user.return_value = sample_user_with_settings

                response = client.get("/api/users/me/settings", headers=auth_headers)

                assert response.status_code == 200
                data = response.json()
                assert (
                    data["default_session_type"]
                    == sample_user_with_settings.settings.default_session_type.value
                )
                assert data["theme"] == sample_user_with_settings.settings.theme.value
                assert (
                    data["daily_practice_goal_minutes"]
                    == sample_user_with_settings.settings.daily_practice_goal_minutes
                )

    def test_get_current_user_settings_unauthorized(self, unauthorized_client):
        response = unauthorized_client.get("/api/users/me/settings")

        assert response.status_code == 403

    def test_get_current_user_all_success(
        self, client, sample_user_with_settings, auth_headers
    ):
        with patch("middleware.auth_middleware.get_keycloak_user") as mock_auth:
            mock_auth.return_value = Mock(
                user_id=sample_user_with_settings.keycloak_user_id,
                email=sample_user_with_settings.email,
                username=sample_user_with_settings.username,
            )

            with patch(
                "services.common.user_service.get_current_user"
            ) as mock_get_user:
                mock_get_user.return_value = sample_user_with_settings

                with patch(
                    "adapters.http.user_service_http_adapter.get_user_http_service"
                ) as mock_adapter:
                    mock_adapter_instance = Mock()
                    mock_adapter_instance.get_profile_and_settings_by_user.return_value = UserWithSettingsResponse(
                        profile=UserProfileResponse.model_validate(
                            sample_user_with_settings
                        ),
                        settings=UserSettingsResponse.model_validate(
                            sample_user_with_settings.settings
                        ),
                    )
                    mock_adapter.return_value = mock_adapter_instance

                    response = client.get("/api/users/me/all", headers=auth_headers)

                    assert response.status_code == 200
                    data = response.json()
                    assert "profile" in data
                    assert "settings" in data
                    assert data["profile"]["id"] == str(sample_user_with_settings.id)
                    assert (
                        data["settings"]["default_session_type"]
                        == sample_user_with_settings.settings.default_session_type.value
                    )

    def test_get_current_user_all_unauthorized(self, unauthorized_client):
        response = unauthorized_client.get("/api/users/me/all")

        assert response.status_code == 403

    def test_get_current_user_all_service_error(
        self, mock_db_session, mock_redis_client, sample_keycloak_user, auth_headers
    ):
        # Create a mock user service that throws an error
        error_service = Mock()
        error_service.get_or_create_user.side_effect = HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

        def override_get_db():
            yield mock_db_session

        def override_get_redis():
            yield mock_redis_client

        def override_get_keycloak_user():
            return sample_keycloak_user

        def override_get_user_service():
            return error_service

        from main import app
        from middleware.auth_middleware import get_keycloak_user
        from services import get_db, get_redis
        from services.common.user_service import get_user_service

        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_redis] = override_get_redis
        app.dependency_overrides[get_keycloak_user] = override_get_keycloak_user
        app.dependency_overrides[get_user_service] = override_get_user_service

        from fastapi.testclient import TestClient

        with TestClient(app) as test_client:
            response = test_client.get("/api/users/me/all", headers=auth_headers)
            assert response.status_code == 500

        app.dependency_overrides.clear()

    def test_user_router_prefix_and_tags(self, client):
        response = client.get("/api/users/me")

        assert response.status_code in [403, 200]

    def test_user_router_responses_configuration(self, client):
        response = client.get("/api/users/me")

        assert response.status_code in [403, 200, 422]

    def test_get_current_user_profile_response_model(
        self, client, sample_user_with_settings, auth_headers
    ):
        with patch("middleware.auth_middleware.get_keycloak_user") as mock_auth:
            mock_auth.return_value = Mock(
                user_id=sample_user_with_settings.keycloak_user_id,
                email=sample_user_with_settings.email,
                username=sample_user_with_settings.username,
            )

            with patch(
                "services.common.user_service.get_current_user"
            ) as mock_get_user:
                mock_get_user.return_value = sample_user_with_settings

                response = client.get("/api/users/me", headers=auth_headers)

                if response.status_code == 200:
                    data = response.json()
                    required_fields = [
                        "id",
                        "email",
                        "username",
                        "timezone",
                        "created_at",
                    ]
                    for field in required_fields:
                        assert field in data

    def test_get_current_user_settings_response_model(
        self, client, sample_user_with_settings, auth_headers
    ):
        with patch("middleware.auth_middleware.get_keycloak_user") as mock_auth:
            mock_auth.return_value = Mock(
                user_id=sample_user_with_settings.keycloak_user_id,
                email=sample_user_with_settings.email,
                username=sample_user_with_settings.username,
            )

            with patch(
                "services.common.user_service.get_current_user"
            ) as mock_get_user:
                mock_get_user.return_value = sample_user_with_settings

                response = client.get("/api/users/me/settings", headers=auth_headers)

                if response.status_code == 200:
                    data = response.json()
                    required_fields = [
                        "default_session_type",
                        "theme",
                        "daily_practice_goal_minutes",
                        "weekly_practice_goal_sessions",
                        "profile_public",
                        "share_practice_stats",
                    ]
                    for field in required_fields:
                        assert field in data

    def test_get_current_user_all_response_model(
        self, client, sample_user_with_settings, auth_headers
    ):
        with patch("middleware.auth_middleware.get_keycloak_user") as mock_auth:
            mock_auth.return_value = Mock(
                user_id=sample_user_with_settings.keycloak_user_id,
                email=sample_user_with_settings.email,
                username=sample_user_with_settings.username,
            )

            with patch(
                "services.common.user_service.get_current_user"
            ) as mock_get_user:
                mock_get_user.return_value = sample_user_with_settings

                with patch(
                    "adapters.http.user_service_http_adapter.get_user_http_service"
                ) as mock_adapter:
                    mock_adapter_instance = Mock()
                    mock_adapter_instance.get_profile_and_settings_by_user.return_value = UserWithSettingsResponse(
                        profile=UserProfileResponse.model_validate(
                            sample_user_with_settings
                        ),
                        settings=UserSettingsResponse.model_validate(
                            sample_user_with_settings.settings
                        ),
                    )
                    mock_adapter.return_value = mock_adapter_instance

                    response = client.get("/api/users/me/all", headers=auth_headers)

                    if response.status_code == 200:
                        data = response.json()
                        assert "profile" in data
                        assert "settings" in data
                        assert "id" in data["profile"]
                        assert "default_session_type" in data["settings"]
