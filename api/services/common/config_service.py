import logging

from pydantic import Field

from .base_config_service import BaseConfigService


class ConfigService(BaseConfigService):
    """
    Configuration class for the application.
    """

    # App Defaults
    ENVIRONMENT: str = Field(default="development")
    LOG_LEVEL: int = Field(default=logging.INFO)
    PORT: int = Field(default=8000)
    WEB_APP_URL: str = Field(default="http://localhost:3000")

    # Data
    DATABASE_URL: str = Field(
        default="postgresql://postgres:password@localhost:5432/db"
    )
    REDIS_URL: str = Field(default="redis://localhost:6379")

    # Keycloak
    KEYCLOAK_CLIENT_ID: str = Field(default="")
    KEYCLOAK_CLIENT_SECRET: str = Field(default="")
    KEYCLOAK_REALM: str = Field(default="")
    KEYCLOAK_URL: str = Field(default="")

    # Spotify
    SPOTIFY_CLIENT_ID: str = Field(default="")
    SPOTIFY_CLIENT_SECRET: str = Field(default="")

    @property
    def LOG_LEVEL_STR(self) -> str:
        """Get the string representation of LOG_LEVEL for Uvicorn"""
        level_map = {
            logging.DEBUG: "debug",
            logging.INFO: "info",
            logging.WARNING: "warning",
            logging.ERROR: "error",
            logging.CRITICAL: "critical",
        }
        return level_map.get(self.LOG_LEVEL, "info")


config = ConfigService()
