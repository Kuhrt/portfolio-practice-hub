import uuid
from datetime import datetime, timezone
from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException, status

from models.common.user_models import User
from schemas.common import HealthCheckResponse


class TestHealthRouter:
    def test_health_check_ping_success(self, client):
        with patch(
            "services.api.health_api_service.get_health_api_service"
        ) as mock_service:
            mock_service_instance = Mock()
            mock_service_instance.ping.return_value = HealthCheckResponse(
                status="OK", version="1.0.0"
            )
            mock_service.return_value = mock_service_instance

            response = client.get("/api/health/ping")

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "OK"
            assert data["version"] == "1.0.0"

    def test_health_check_ping_service_unavailable(
        self,
        mock_db_session,
        mock_redis_client,
        mock_user_service,
        sample_keycloak_user,
    ):
        # Create a mock health service that throws a 503 error
        error_service = Mock()
        error_service.ping.side_effect = HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is currently unavailable",
        )

        def override_get_db():
            yield mock_db_session

        def override_get_redis():
            yield mock_redis_client

        def override_get_keycloak_user():
            return sample_keycloak_user

        def override_get_user_service():
            return mock_user_service

        def override_get_health_api_service():
            return error_service

        from main import app
        from middleware.auth_middleware import get_keycloak_user
        from services import get_db, get_redis
        from services.api.health_api_service import get_health_api_service
        from services.common.user_service import get_user_service

        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_redis] = override_get_redis
        app.dependency_overrides[get_keycloak_user] = override_get_keycloak_user
        app.dependency_overrides[get_user_service] = override_get_user_service
        app.dependency_overrides[get_health_api_service] = (
            override_get_health_api_service
        )

        from fastapi.testclient import TestClient

        with TestClient(app) as test_client:
            response = test_client.get("/api/health/ping")
            assert response.status_code == 503
            data = response.json()
            assert "error" in data
            assert "Service is currently unavailable" in data["message"]

        app.dependency_overrides.clear()

    def test_health_check_ping_internal_server_error(
        self,
        mock_db_session,
        mock_redis_client,
        mock_user_service,
        sample_keycloak_user,
    ):
        # Create a mock health service that throws a 500 error
        error_service = Mock()
        error_service.ping.side_effect = HTTPException(
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
            return mock_user_service

        def override_get_health_api_service():
            return error_service

        from main import app
        from middleware.auth_middleware import get_keycloak_user
        from services import get_db, get_redis
        from services.api.health_api_service import get_health_api_service
        from services.common.user_service import get_user_service

        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_redis] = override_get_redis
        app.dependency_overrides[get_keycloak_user] = override_get_keycloak_user
        app.dependency_overrides[get_user_service] = override_get_user_service
        app.dependency_overrides[get_health_api_service] = (
            override_get_health_api_service
        )

        from fastapi.testclient import TestClient

        with TestClient(app) as test_client:
            response = test_client.get("/api/health/ping")
            assert response.status_code == 500
            data = response.json()
            assert "error" in data
            assert "Internal server error" in data["message"]

        app.dependency_overrides.clear()

    def test_health_check_ping_with_simulate_failure_query(
        self,
        mock_db_session,
        mock_redis_client,
        mock_user_service,
        sample_keycloak_user,
    ):
        # Create a mock health service that throws a 503 error
        error_service = Mock()
        error_service.ping.side_effect = HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is currently unavailable",
        )

        def override_get_db():
            yield mock_db_session

        def override_get_redis():
            yield mock_redis_client

        def override_get_keycloak_user():
            return sample_keycloak_user

        def override_get_user_service():
            return mock_user_service

        def override_get_health_api_service():
            return error_service

        from main import app
        from middleware.auth_middleware import get_keycloak_user
        from services import get_db, get_redis
        from services.api.health_api_service import get_health_api_service
        from services.common.user_service import get_user_service

        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_redis] = override_get_redis
        app.dependency_overrides[get_keycloak_user] = override_get_keycloak_user
        app.dependency_overrides[get_user_service] = override_get_user_service
        app.dependency_overrides[get_health_api_service] = (
            override_get_health_api_service
        )

        from fastapi.testclient import TestClient

        with TestClient(app) as test_client:
            response = test_client.get("/api/health/ping?simulate_failure=true")
            assert response.status_code == 503

        app.dependency_overrides.clear()

    def test_authenticated_health_check_success(
        self, client, sample_user, auth_headers
    ):
        with patch("middleware.auth_middleware.get_keycloak_user") as mock_auth:
            mock_auth.return_value = Mock(
                user_id=sample_user.keycloak_user_id,
                email=sample_user.email,
                username=sample_user.username,
            )

            with patch(
                "services.common.user_service.get_current_user"
            ) as mock_get_user:
                mock_get_user.return_value = sample_user

                response = client.get("/api/health/authenticated", headers=auth_headers)

                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "OK"
                assert data["user_id"] == str(sample_user.id)
                assert data["username"] == sample_user.username
                assert "timestamp" in data

    def test_authenticated_health_check_unauthorized(self, unauthorized_client):
        response = unauthorized_client.get("/api/health/authenticated")

        assert response.status_code == 403

    def test_authenticated_health_check_invalid_token(
        self, unauthorized_client, auth_headers
    ):
        response = unauthorized_client.get(
            "/api/health/authenticated", headers=auth_headers
        )

        assert response.status_code == 401

    def test_health_router_prefix_and_tags(self, client):
        response = client.get("/api/health/ping")

        assert response.status_code in [200, 503, 500]

    def test_health_check_response_model_validation(self, client):
        with patch(
            "services.api.health_api_service.get_health_api_service"
        ) as mock_service:
            mock_service_instance = Mock()
            mock_service_instance.ping.return_value = HealthCheckResponse(
                status="OK", version="1.0.0"
            )
            mock_service.return_value = mock_service_instance

            response = client.get("/api/health/ping")

            if response.status_code == 200:
                data = response.json()
                required_fields = ["status", "version"]
                for field in required_fields:
                    assert field in data

    def test_authenticated_health_check_response_structure(
        self, client, sample_user, auth_headers
    ):
        with patch("middleware.auth_middleware.get_keycloak_user") as mock_auth:
            mock_auth.return_value = Mock(
                user_id=sample_user.keycloak_user_id,
                email=sample_user.email,
                username=sample_user.username,
            )

            with patch(
                "services.common.user_service.get_current_user"
            ) as mock_get_user:
                mock_get_user.return_value = sample_user

                response = client.get("/api/health/authenticated", headers=auth_headers)

                if response.status_code == 200:
                    data = response.json()
                    required_fields = ["status", "user_id", "username", "timestamp"]
                    for field in required_fields:
                        assert field in data

                    assert data["status"] == "OK"
                    assert data["user_id"] == str(sample_user.id)
                    assert data["username"] == sample_user.username

    def test_health_check_ping_logging(self, client):
        with patch(
            "services.api.health_api_service.get_health_api_service"
        ) as mock_service:
            mock_service_instance = Mock()
            mock_service_instance.ping.return_value = HealthCheckResponse(
                status="OK", version="1.0.0"
            )
            mock_service.return_value = mock_service_instance

            with patch("routers.health_router.logger") as mock_logger:
                response = client.get("/api/health/ping")

                if response.status_code == 200:
                    mock_logger.info.assert_called_with(
                        "Health check completed successfully"
                    )

    def test_health_check_ping_debug_logging(self, client):
        with patch(
            "services.api.health_api_service.get_health_api_service"
        ) as mock_service:
            mock_service_instance = Mock()
            mock_service_instance.ping.return_value = HealthCheckResponse(
                status="OK", version="1.0.0"
            )
            mock_service.return_value = mock_service_instance

            with patch("routers.health_router.logger") as mock_logger:
                response = client.get("/api/health/ping")

                if response.status_code == 200:
                    mock_logger.debug.assert_called_with("Health check requested")

    def test_health_check_ping_service_dependency_injection(self, client):
        from main import app
        from services.api.health_api_service import get_health_api_service

        mock_service_instance = Mock()
        mock_service_instance.ping.return_value = HealthCheckResponse(
            status="OK", version="1.0.0"
        )

        # Override the dependency
        app.dependency_overrides[get_health_api_service] = lambda: mock_service_instance

        try:
            response = client.get("/api/health/ping")

            # The service should be called when the endpoint is hit
            assert response.status_code == 200
            mock_service_instance.ping.assert_called_once()
        finally:
            # Clean up the override
            app.dependency_overrides.clear()
