# Tests

This directory contains the comprehensive test suite for the Practice Hub API, following modern 2025 best practices.

## Quick Start

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=. --cov-report=html

# Run specific test category
uv run pytest tests/models/
uv run pytest tests/services/
uv run pytest tests/routers/

# Run with markers
uv run pytest -m unit
uv run pytest -m "not slow"
uv run pytest -m factory
```

## Test Categories

- **`tests/models/`** - Model tests (User, UserSettings, etc.)
- **`tests/services/`** - Service layer tests
- **`tests/routers/`** - API endpoint tests
- **`tests/middleware/`** - Middleware tests
- **`tests/exceptions/`** - Exception handling tests
- **`tests/schemas/`** - Schema validation tests
- **`tests/adapters/`** - Adapter tests
- **`tests/utils/`** - Test utilities and helpers

## Running Tests

### Basic Commands

```bash
# All tests
uv run pytest

# With verbose output
uv run pytest -v

# With coverage
uv run pytest --cov=. --cov-report=html

# Stop on first failure
uv run pytest -x

# Run specific test file
uv run pytest tests/models/test_user_models.py

# Run specific test method
uv run pytest tests/models/test_user_models.py::TestUserModel::test_user_creation
```

### By Markers

```bash
# Unit tests only
uv run pytest -m unit

# Integration tests only
uv run pytest -m integration

# Fast tests (exclude slow)
uv run pytest -m "not slow"

# Factory pattern tests
uv run pytest -m factory

# Parametrized tests
uv run pytest -m parametrize
```

### By Directory

```bash
uv run pytest tests/models/
uv run pytest tests/services/
uv run pytest tests/routers/
uv run pytest tests/middleware/
uv run pytest tests/exceptions/
uv run pytest tests/schemas/
uv run pytest tests/adapters/
```

## Test Runner Script

For convenience, you can also use the test runner script:

```bash
python run_tests.py all          # All tests with coverage
python run_tests.py unit         # Unit tests only
python run_tests.py models       # Model tests only
python run_tests.py fast         # Fast tests only
python run_tests.py factory      # Factory pattern tests
python run_tests.py lint         # Code linting
python run_tests.py format       # Code formatting
```

## Documentation

For detailed information about testing patterns, fixtures, and best practices, see [TESTING_GUIDE.md](./TESTING_GUIDE.md).

## Coverage

The test suite maintains a minimum coverage threshold of 80%. Coverage reports are generated in both terminal and HTML formats:

- Terminal: `uv run pytest --cov=. --cov-report=term-missing`
- HTML: `uv run pytest --cov=. --cov-report=html:htmlcov`

## Modern Features

This test suite includes:

- **Test Data Factories** for DRY test data creation
- **Parametrized Tests** for testing multiple scenarios
- **Custom Assertions** for better test readability
- **Builder Patterns** for complex test data
- **Comprehensive Fixtures** for test isolation
- **Modern Pytest Features** throughout
