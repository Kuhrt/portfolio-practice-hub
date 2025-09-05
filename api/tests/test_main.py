import pytest
from fastapi.testclient import TestClient

from main import app


class TestMainApp:
    def test_app_creation(self):
        assert app is not None
        assert app.title == "Practice Hub API"
        assert app.description == "API for tracking music practice sessions"
        assert app.version == "1.0.0"

    def test_app_routes_registration(self):
        routes = [route.path for route in app.routes]

        assert "/api/health/ping" in routes
        assert "/api/health/authenticated" in routes
        assert "/api/users/me" in routes
        assert "/api/users/me/settings" in routes
        assert "/api/users/me/all" in routes

    def test_app_openapi_docs(self, client):
        response = client.get("/docs")
        assert response.status_code == 200

    def test_app_openapi_json(self, client):
        response = client.get("/openapi.json")
        assert response.status_code == 200

        data = response.json()
        assert data["info"]["title"] == "Practice Hub API"
        assert data["info"]["version"] == "1.0.0"

    def test_app_cors_middleware(self, client):
        response = client.options("/api/health/ping")
        assert response.status_code in [200, 405]

    def test_app_exception_handlers_registration(self):
        exception_handlers = app.exception_handlers

        from fastapi import HTTPException
        from fastapi.exceptions import RequestValidationError

        from exceptions.common.user_exceptions import UserServiceError

        assert HTTPException in exception_handlers
        assert RequestValidationError in exception_handlers
        assert Exception in exception_handlers

    def test_app_lifespan_events(self):
        assert hasattr(app, "router")
        assert hasattr(app, "middleware")

    def test_app_include_routers(self):
        # Check that the router paths are included in the app routes
        routes = [route.path for route in app.routes if hasattr(route, "path")]

        # Check for health router paths
        assert any("/api/health" in route for route in routes)

        # Check for user router paths
        assert any("/api/users" in route for route in routes)

    def test_app_cors_configuration(self):
        cors_middleware = None
        for middleware in app.user_middleware:
            if hasattr(middleware, "cls") and "CORSMiddleware" in str(middleware.cls):
                cors_middleware = middleware
                break

        assert cors_middleware is not None

    def test_app_health_check_endpoint(self, client):
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "services.api.health_api_service.get_health_api_service",
                lambda: type(
                    "MockService",
                    (),
                    {
                        "ping": lambda: type(
                            "Response", (), {"status": "OK", "version": "1.0.0"}
                        )()
                    },
                )(),
            )

            response = client.get("/api/health/ping")
            assert response.status_code == 200

    def test_app_unauthorized_access(self, unauthorized_client):
        response = unauthorized_client.get("/api/users/me")
        assert response.status_code == 403

    def test_app_root_endpoint(self, client):
        response = client.get("/")
        assert response.status_code == 404

    def test_app_nonexistent_endpoint(self, client):
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
