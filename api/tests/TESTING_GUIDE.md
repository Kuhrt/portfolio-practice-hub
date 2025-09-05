# Testing Guide - Practice Hub API

This guide outlines the modern testing practices and patterns used in the Practice Hub API test suite, following 2025 best practices.

## Table of Contents

1. [Overview](#overview)
2. [Quick Reference - Common `uv` Commands](#quick-reference---common-uv-commands)
3. [Test Structure](#test-structure)
4. [Modern Patterns](#modern-patterns)
5. [Test Data Management](#test-data-management)
6. [Fixtures and Utilities](#fixtures-and-utilities)
7. [Assertion Patterns](#assertion-patterns)
8. [Running Tests](#running-tests)
9. [Best Practices](#best-practices)

## Quick Reference - Common `uv` Commands

```bash
# Most common commands
uv run pytest                                    # Run all tests
uv run pytest -v                                # Run all tests with verbose output
uv run pytest --cov=. --cov-report=html         # Run with coverage report
uv run pytest -m unit                           # Run only unit tests
uv run pytest -m "not slow"                     # Run fast tests only
uv run pytest tests/models/                     # Run model tests
uv run pytest -x                                # Stop on first failure
uv run pytest -k "test_user"                    # Run tests matching pattern
```

## Overview

The test suite follows modern Python testing practices with a focus on:

- **DRY Principles**: Eliminating code duplication through reusable components
- **Clean Code**: Readable, maintainable test code
- **Modern Pytest Features**: Leveraging latest pytest capabilities
- **Comprehensive Coverage**: Testing all critical paths and edge cases

All tests in this suite follow modern 2025 best practices by default.

## Test Structure

```
tests/
├── conftest.py                 # Global fixtures and test configuration
├── utils/
│   └── test_helpers.py        # Modern test utilities and patterns
├── models/                    # Model tests
├── services/                  # Service layer tests
├── routers/                   # API endpoint tests
├── middleware/                # Middleware tests
├── exceptions/                # Exception handling tests
├── schemas/                   # Schema validation tests
└── adapters/                  # Adapter tests
```

## Modern Patterns

### 1. Test Data Factories

Instead of hardcoded test data, we use factory patterns:

```python
# Old way (avoid)
user = User(
    id=uuid.uuid4(),
    keycloak_user_id="test-keycloak-id",
    email="test@example.com",
    # ... many more fields
)

# New way (preferred)
keycloak_user = test_data_factory.create_keycloak_user(
    user_id="test-keycloak-id",
    email="test@example.com"
)
user = test_data_factory.create_user(keycloak_user)
```

### 2. Parametrized Tests

Use `@pytest.mark.parametrize` for testing multiple scenarios:

```python
@pytest.mark.parametrize("first_name,last_name,expected_display", [
    ("John", "Doe", "John Doe"),
    ("Jane", "Smith", "Jane Smith"),
    (None, None, "None None"),
])
def test_display_name_generation(self, first_name, last_name, expected_display):
    # Test implementation
```

### 3. Fixture Organization

Organize fixtures by scope and purpose:

```python
# Session-scoped fixtures for expensive setup
@pytest.fixture(scope="session")
def event_loop():
    # Setup code

# Function-scoped fixtures for test isolation
@pytest.fixture(scope="function")
def mock_db_session():
    # Setup code

# Autouse fixtures for automatic setup
@pytest.fixture(autouse=True)
def setup_test_environment():
    # Automatic setup/cleanup
```

## Test Data Management

### TestDataFactory

The `TestDataFactory` class provides methods to create test objects with sensible defaults:

```python
# Create a KeycloakUser
keycloak_user = test_data_factory.create_keycloak_user(
    user_id="custom-id",
    email="custom@example.com"
)

# Create a User with custom settings
user = test_data_factory.create_user(
    keycloak_user,
    timezone="America/New_York",
    is_active=False
)

# Create UserSettings
settings = test_data_factory.create_user_settings(
    user,
    theme=Theme.DARK,
    daily_practice_goal_minutes=60
)
```

### Builder Pattern

For complex test data, use the builder pattern:

```python
data = (test_data_builder()
        .with_id("test-123")
        .with_field("name", "Test User")
        .with_timestamps()
        .build())
```

## Fixtures and Utilities

### Global Fixtures (conftest.py)

- `test_data_factory`: Access to the test data factory
- `mock_db_session`: Mock database session
- `mock_redis_client`: Mock Redis client
- `sample_user`: Pre-created user for testing
- `sample_user_with_settings`: User with settings attached
- `auth_headers`: Authorization headers for API tests

### Test Utilities

Custom assertion helpers and utilities are available in `tests/utils/test_helpers.py`:

```python
def test_with_custom_assertions(self, test_assertions):
    # Assert HTTP status
    test_assertions.assert_http_status(response, 200)

    # Assert response contains keys
    test_assertions.assert_response_contains(response, ["id", "email"])

    # Assert UUID validity
    test_assertions.assert_uuid_valid(user_id)

    # Assert timestamp is recent
    test_assertions.assert_timestamp_recent(created_at)
```

## Assertion Patterns

### Modern Assertions

Use descriptive assertions with custom messages:

```python
# Good
assert user.is_active is True, "User should be active after creation"
assert response.status_code == 200, f"Expected 200, got {response.status_code}"

# Better with custom assertions
test_assertions.assert_http_status(response, 200)
test_assertions.assert_response_contains(response, ["id", "email"])
```

### Exception Testing

Use context managers for exception testing:

```python
with pytest.raises(UserNotFoundError) as exc_info:
    user_service.get_user(nonexistent_id)

assert "User not found" in str(exc_info.value)
```

### Parametrized Exception Testing

```python
@pytest.mark.parametrize("user_id,email,expected_error", [
    ("", "test@example.com", "Keycloak user ID is required"),
    ("test-id", "", "Email is required"),
])
def test_validation_errors(self, user_id, email, expected_error):
    with pytest.raises(UserDataValidationError) as exc_info:
        # Test code
    assert expected_error in str(exc_info.value)
```

## Running Tests

### Basic Commands with `uv`

```bash
# Run all tests
uv run pytest

# Run all tests with coverage
uv run pytest --cov=. --cov-report=term-missing --cov-report=html:htmlcov

# Run specific test file
uv run pytest tests/models/test_user_models.py

# Run specific test class
uv run pytest tests/models/test_user_models.py::TestUserModel

# Run specific test method
uv run pytest tests/models/test_user_models.py::TestUserModel::test_user_creation

# Run with verbose output
uv run pytest -v

# Run with coverage and fail if below 80%
uv run pytest --cov=. --cov-fail-under=80 -v
```

### Test Categories with `uv`

```bash
# Run only unit tests
uv run pytest -m unit

# Run only integration tests
uv run pytest -m integration

# Run model tests
uv run pytest tests/models/

# Run service tests
uv run pytest tests/services/

# Run router tests
uv run pytest tests/routers/

# Run middleware tests
uv run pytest tests/middleware/

# Run exception tests
uv run pytest tests/exceptions/

# Run schema tests
uv run pytest tests/schemas/
```

### Specialized Test Runs with `uv`

```bash
# Run fast tests (exclude slow tests)
uv run pytest -m "not slow"

# Run factory pattern tests
uv run pytest -m factory

# Run parametrized tests
uv run pytest -m parametrize

# Run tests with specific markers
uv run pytest -m "unit and not slow"

# Run tests in parallel (if pytest-xdist is installed)
uv run pytest -n auto

# Run tests with detailed output
uv run pytest -v --tb=long

# Run tests and stop on first failure
uv run pytest -x

# Run tests and show local variables on failure
uv run pytest -l
```

### Using the Test Runner Script (Optional)

The `run_tests.py` script provides convenient wrapper commands:

```bash
# Run all tests with coverage
python run_tests.py all

# Run only unit tests
python run_tests.py unit

# Run only integration tests
python run_tests.py integration

# Run fast tests (exclude slow tests)
python run_tests.py fast

# Run factory pattern tests
python run_tests.py factory

# Run specific test category
python run_tests.py models
python run_tests.py services
python run_tests.py routers
```

### Pytest Markers with `uv`

Use markers to categorize and filter tests:

```python
@pytest.mark.unit
@pytest.mark.parametrize
@pytest.mark.factory
def test_user_creation():
    pass
```

**Running tests by markers with `uv`:**

```bash
# Run only unit tests
uv run pytest -m unit

# Run only integration tests
uv run pytest -m integration

# Run only parametrized tests
uv run pytest -m parametrize

# Run factory pattern tests
uv run pytest -m factory

# Run model tests
uv run pytest -m model

# Run service tests
uv run pytest -m service

# Run API tests
uv run pytest -m api

# Exclude slow tests
uv run pytest -m "not slow"

# Combine markers
uv run pytest -m "unit and factory"
uv run pytest -m "unit and not slow"
```

## Best Practices

### 1. Test Naming

Use descriptive test names that explain what is being tested:

```python
# Good
def test_user_creation_with_factory(self):
def test_display_name_generation_with_partial_names(self):
def test_validation_errors_for_missing_required_fields(self):

# Avoid
def test_user(self):
def test_validation(self):
def test_error(self):
```

### 2. Test Organization

Group related tests in classes and use docstrings:

```python
class TestUserService:
    """Test cases for the UserService class."""

    def test_get_or_create_user_existing_user(self):
        """Test getting an existing user and updating their information."""
        # Test implementation
```

### 3. Fixture Usage

Use fixtures to reduce duplication and improve maintainability:

```python
def test_user_creation(self, test_data_factory, user_service):
    # Use fixtures instead of creating objects manually
    keycloak_user = test_data_factory.create_keycloak_user()
    result = user_service.get_or_create_user(keycloak_user)
    # Assertions
```

### 4. Mock Usage

Use mocks appropriately and verify interactions:

```python
def test_user_service_calls_database(self, user_service, mock_db_session):
    # Setup
    mock_db_session.execute.return_value.scalar_one_or_none.return_value = None

    # Action
    user_service.get_or_create_user(keycloak_user)

    # Verify
    mock_db_session.execute.assert_called_once()
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
```

### 5. Test Isolation

Ensure tests are independent and can run in any order:

```python
@pytest.fixture(autouse=True)
def setup_test_environment():
    """Automatically set up test environment variables."""
    os.environ.setdefault("ENVIRONMENT", "testing")
    yield
    # Cleanup after test
    if "ENVIRONMENT" in os.environ:
        del os.environ["ENVIRONMENT"]
```

### 6. Error Testing

Test both success and failure scenarios:

```python
def test_success_case(self):
    # Test the happy path
    pass

def test_error_case(self):
    # Test error handling
    with pytest.raises(ExpectedException):
        # Code that should raise exception
        pass
```

### 7. Performance Testing

Use appropriate markers for different test types:

```python
@pytest.mark.slow
def test_large_dataset_processing(self):
    # Test that takes a long time
    pass

@pytest.mark.unit
def test_fast_unit_test(self):
    # Quick unit test
    pass
```

## Coverage Requirements

The test suite maintains a minimum coverage threshold of 80%. Coverage reports are generated in both terminal and HTML formats:

- Terminal: `pytest --cov=. --cov-report=term-missing`
- HTML: `pytest --cov=. --cov-report=html:htmlcov`

## Continuous Integration

Tests are designed to run in CI environments with:

- Automatic environment setup
- Parallel test execution support
- Clear failure reporting
- Coverage reporting

## Conclusion

This testing approach ensures:

- **Maintainability**: Easy to understand and modify tests
- **Reliability**: Tests catch regressions and bugs
- **Efficiency**: Fast test execution with good coverage
- **Clarity**: Clear test intent and results

Follow these patterns to maintain high-quality tests that support the development process effectively.
