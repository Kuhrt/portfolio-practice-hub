"""Utility functions for schema management in migrations"""

from alembic import op


def create_schema_if_not_exists(schema_name: str) -> None:
    """
    Create a schema if it doesn't exist.
    Use this in your Alembic migration files.

    Args:
        schema_name: Name of the schema to create
    """
    op.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")


def drop_schema_if_exists(schema_name: str) -> None:
    """
    Drop a schema if it exists.
    Use this in your Alembic migration downgrade functions.

    Args:
        schema_name: Name of the schema to drop
    """
    op.execute(f"DROP SCHEMA IF EXISTS {schema_name}")


# Example usage in a migration file:
"""
from utils.schema_utils import create_schema_if_not_exists, drop_schema_if_exists

def upgrade() -> None:
    create_schema_if_not_exists("analytics")
    # ... create tables in the schema

def downgrade() -> None:
    # ... drop tables first
    drop_schema_if_exists("analytics")
"""
