"""Database migration service using Alembic"""

import logging
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


def run_migrations():
    """Run Alembic migrations to ensure database is up to date"""
    try:
        logger.info("Running database migrations...")

        # Run alembic upgrade head
        result = subprocess.run(
            [sys.executable, "-m", "alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,  # Project root
        )

        if result.returncode == 0:
            logger.info("Database migrations completed successfully")
            if result.stdout:
                logger.info(f"Migration output: {result.stdout}")
        else:
            logger.error(f"Migration failed: {result.stderr}")
            raise RuntimeError(f"Migration failed: {result.stderr}")

    except Exception as e:
        logger.error(f"Failed to run migrations: {e}")
        raise e


def check_migration_status():
    """Check if migrations are up to date"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "alembic", "current"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,  # Project root
        )

        if result.returncode == 0:
            logger.info(f"Current migration status: {result.stdout.strip()}")
            return True
        else:
            logger.warning(f"Could not check migration status: {result.stderr}")
            return False

    except Exception as e:
        logger.warning(f"Failed to check migration status: {e}")
        return False
