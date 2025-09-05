"""
Modern test utilities and helpers for the Practice Hub API test suite.

This module provides advanced pytest patterns, custom assertions,
and reusable test components following 2025 best practices.
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Type, Union

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel


class TestAssertions:
    """Custom assertion helpers for more readable tests."""

    @staticmethod
    def assert_http_status(response, expected_status: int, message: str = None):
        """Assert HTTP status with a custom message."""
        if message is None:
            message = f"Expected status {expected_status}, got {response.status_code}"
        assert response.status_code == expected_status, message

    @staticmethod
    def assert_response_contains(response, expected_keys: List[str]):
        """Assert that response JSON contains all expected keys."""
        data = response.json()
        missing_keys = [key for key in expected_keys if key not in data]
        assert not missing_keys, f"Response missing keys: {missing_keys}"

    @staticmethod
    def assert_response_schema(response, schema_class: Type[BaseModel]):
        """Assert that response matches a Pydantic schema."""
        data = response.json()
        try:
            schema_class.model_validate(data)
        except Exception as e:
            pytest.fail(f"Response does not match schema {schema_class.__name__}: {e}")

    @staticmethod
    def assert_timestamp_recent(timestamp: datetime, max_age_seconds: int = 5):
        """Assert that a timestamp is recent (within max_age_seconds)."""
        now = datetime.now(timezone.utc)
        age = (now - timestamp).total_seconds()
        assert (
            age <= max_age_seconds
        ), f"Timestamp is {age:.2f}s old, max allowed is {max_age_seconds}s"

    @staticmethod
    def assert_uuid_valid(uuid_string: str):
        """Assert that a string is a valid UUID."""
        try:
            uuid.UUID(uuid_string)
        except ValueError:
            pytest.fail(f"'{uuid_string}' is not a valid UUID")


class DataBuilder:
    """Builder pattern for creating complex test data."""

    def __init__(self):
        self._data = {}

    def with_field(self, field: str, value: Any) -> "TestDataBuilder":
        """Add a field to the test data."""
        self._data[field] = value
        return self

    def with_id(self, id_value: str = None) -> "TestDataBuilder":
        """Add an ID field."""
        self._data["id"] = id_value or str(uuid.uuid4())
        return self

    def with_timestamps(
        self, created_at: datetime = None, updated_at: datetime = None
    ) -> "TestDataBuilder":
        """Add timestamp fields."""
        if created_at is None:
            created_at = datetime.now(timezone.utc)
        self._data["created_at"] = created_at
        if updated_at is not None:
            self._data["updated_at"] = updated_at
        return self

    def build(self) -> Dict[str, Any]:
        """Build the test data dictionary."""
        return self._data.copy()


class MockResponseBuilder:
    """Builder for creating mock HTTP responses."""

    def __init__(self):
        self._status_code = 200
        self._data = {}
        self._headers = {}

    def with_status(self, status_code: int) -> "MockResponseBuilder":
        """Set the response status code."""
        self._status_code = status_code
        return self

    def with_data(self, data: Dict[str, Any]) -> "MockResponseBuilder":
        """Set the response data."""
        self._data = data
        return self

    def with_header(self, key: str, value: str) -> "MockResponseBuilder":
        """Add a response header."""
        self._headers[key] = value
        return self

    def build(self):
        """Build the mock response."""
        from unittest.mock import Mock

        response = Mock()
        response.status_code = self._status_code
        response.json.return_value = self._data
        response.headers = self._headers
        return response


class Scenario:
    """Represents a test scenario with setup, action, and assertions."""

    def __init__(self, name: str):
        self.name = name
        self.setup_steps = []
        self.action_step = None
        self.assertion_steps = []
        self.cleanup_steps = []

    def setup(self, description: str, func):
        """Add a setup step."""
        self.setup_steps.append((description, func))
        return self

    def action(self, description: str, func):
        """Set the action step."""
        self.action_step = (description, func)
        return self

    def assert_that(self, description: str, func):
        """Add an assertion step."""
        self.assertion_steps.append((description, func))
        return self

    def cleanup(self, description: str, func):
        """Add a cleanup step."""
        self.cleanup_steps.append((description, func))
        return self

    def execute(self):
        """Execute the test scenario."""
        try:
            # Execute setup steps
            for description, func in self.setup_steps:
                func()

            # Execute action step
            if self.action_step:
                description, func = self.action_step
                result = func()
            else:
                result = None

            # Execute assertion steps
            for description, func in self.assertion_steps:
                func()

            return result
        finally:
            # Execute cleanup steps
            for description, func in self.cleanup_steps:
                try:
                    func()
                except Exception:
                    pass  # Ignore cleanup errors


# Pytest fixtures for modern testing patterns
@pytest.fixture
def test_assertions():
    """Provide access to custom test assertions."""
    return TestAssertions


@pytest.fixture
def test_data_builder():
    """Provide access to the test data builder."""
    return DataBuilder


@pytest.fixture
def mock_response_builder():
    """Provide access to the mock response builder."""
    return MockResponseBuilder


@pytest.fixture
def test_scenario():
    """Provide access to the test scenario builder."""
    return Scenario


# Pytest markers
pytestmark = [
    pytest.mark.unit,
]


class TestAdvancedPatterns:
    """Demonstration of advanced pytest patterns."""

    def test_builder_pattern(self, test_data_builder):
        """Test the builder pattern for creating test data."""
        data = (
            test_data_builder()
            .with_id("test-123")
            .with_field("name", "Test User")
            .with_field("email", "test@example.com")
            .with_timestamps()
            .build()
        )

        assert data["id"] == "test-123"
        assert data["name"] == "Test User"
        assert data["email"] == "test@example.com"
        assert "created_at" in data

    def test_scenario_pattern(self, test_scenario):
        """Test the scenario pattern for complex test flows."""
        result = (
            test_scenario("User creation flow")
            .setup("Initialize test data", lambda: None)
            .action("Create user", lambda: {"id": "user-123", "name": "Test"})
            .assert_that("User has ID", lambda: None)
            .assert_that("User has name", lambda: None)
            .cleanup("Clean up resources", lambda: None)
            .execute()
        )

        assert result["id"] == "user-123"
        assert result["name"] == "Test"

    def test_custom_assertions(self, test_assertions):
        """Test custom assertion helpers."""
        # Test UUID validation
        test_assertions.assert_uuid_valid(str(uuid.uuid4()))

        # Test timestamp validation
        recent_time = datetime.now(timezone.utc)
        test_assertions.assert_timestamp_recent(recent_time)

    @pytest.mark.parametrize(
        "status_code,expected",
        [
            (200, True),
            (201, True),
            (400, False),
            (500, False),
        ],
    )
    def test_http_status_assertions(self, test_assertions, status_code, expected):
        """Test HTTP status assertions."""
        from unittest.mock import Mock

        response = Mock()
        response.status_code = status_code

        if expected:
            test_assertions.assert_http_status(response, status_code)
        else:
            with pytest.raises(AssertionError):
                test_assertions.assert_http_status(response, 200)
