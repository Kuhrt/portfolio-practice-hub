#!/usr/bin/env python3
"""
Test runner script for the Practice Hub API project.
This script provides convenient commands for running different types of tests.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=False)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False


def run_all_tests():
    """Run all tests with coverage."""
    command = (
        "uv run pytest --cov=. --cov-report=term-missing --cov-report=html:htmlcov -v"
    )
    return run_command(command, "All tests with coverage")


def run_unit_tests():
    """Run unit tests only."""
    command = "uv run pytest -m unit -v"
    return run_command(command, "Unit tests")


def run_integration_tests():
    """Run integration tests only."""
    command = "uv run pytest -m integration -v"
    return run_command(command, "Integration tests")


def run_model_tests():
    """Run model tests."""
    command = "uv run pytest tests/models/ -v"
    return run_command(command, "Model tests")


def run_service_tests():
    """Run service tests."""
    command = "uv run pytest tests/services/ -v"
    return run_command(command, "Service tests")


def run_router_tests():
    """Run router tests."""
    command = "uv run pytest tests/routers/ -v"
    return run_command(command, "Router tests")


def run_middleware_tests():
    """Run middleware tests."""
    command = "uv run pytest tests/middleware/ -v"
    return run_command(command, "Middleware tests")


def run_specific_test(test_path):
    """Run a specific test file or test method."""
    command = f"uv run pytest {test_path} -v"
    return run_command(command, f"Specific test: {test_path}")


def run_tests_with_coverage():
    """Run tests with detailed coverage report."""
    command = "uv run pytest --cov=. --cov-report=term-missing --cov-report=html:htmlcov --cov-fail-under=80 -v"
    return run_command(command, "Tests with coverage (80% minimum)")


def run_fast_tests():
    """Run fast tests only (exclude slow tests)."""
    command = "uv run pytest -m 'not slow' -v"
    return run_command(command, "Fast tests only")


def run_factory_tests():
    """Run tests using test data factories."""
    command = "uv run pytest -m factory -v"
    return run_command(command, "Factory pattern tests")


def lint_code():
    """Run code linting."""
    commands = [
        ("uv run black --check .", "Black formatting check"),
        ("uv run isort --check-only .", "Import sorting check"),
        ("uv run flake8 .", "Flake8 linting"),
        ("uv run mypy .", "Type checking"),
    ]

    all_passed = True
    for command, description in commands:
        if not run_command(command, description):
            all_passed = False

    return all_passed


def format_code():
    """Format code with black and isort."""
    commands = [
        ("uv run black .", "Black formatting"),
        ("uv run isort .", "Import sorting"),
    ]

    all_passed = True
    for command, description in commands:
        if not run_command(command, description):
            all_passed = False

    return all_passed


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description="Practice Hub API Test Runner")
    parser.add_argument(
        "command",
        choices=[
            "all",
            "unit",
            "integration",
            "models",
            "services",
            "routers",
            "middleware",
            "coverage",
            "fast",
            "factory",
            "lint",
            "format",
            "specific",
        ],
        help="Test command to run",
    )
    parser.add_argument("--path", help="Specific test path for 'specific' command")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    # Set environment variables for testing
    os.environ.setdefault("TEST_DATABASE_URL", "sqlite:///./test.db")
    os.environ.setdefault("TEST_REDIS_URL", "redis://localhost:6379/1")
    os.environ.setdefault("ENVIRONMENT", "testing")

    success = False

    if args.command == "all":
        success = run_all_tests()
    elif args.command == "unit":
        success = run_unit_tests()
    elif args.command == "integration":
        success = run_integration_tests()
    elif args.command == "models":
        success = run_model_tests()
    elif args.command == "services":
        success = run_service_tests()
    elif args.command == "routers":
        success = run_router_tests()
    elif args.command == "middleware":
        success = run_middleware_tests()
    elif args.command == "coverage":
        success = run_tests_with_coverage()
    elif args.command == "fast":
        success = run_fast_tests()
    elif args.command == "factory":
        success = run_factory_tests()
    elif args.command == "lint":
        success = lint_code()
    elif args.command == "format":
        success = format_code()
    elif args.command == "specific":
        if not args.path:
            print("❌ Error: --path is required for 'specific' command")
            sys.exit(1)
        success = run_specific_test(args.path)

    if success:
        print(f"\n🎉 {args.command.title()} completed successfully!")
        sys.exit(0)
    else:
        print(f"\n💥 {args.command.title()} failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
