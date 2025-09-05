import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, Relationship

from constants import SCHEMA_COMMON, TABLE_USER_SETTINGS, TABLE_USERS

from .base_models import TimestampMixin


class SessionType(str, Enum):
    """Available session types for music practice"""

    FREE_PLAY = "free_play"
    STRUCTURED = "structured"
    EXERCISE = "exercise"
    REPERTOIRE = "repertoire"


class Theme(str, Enum):
    """Available UI themes"""

    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


class User(TimestampMixin, table=True):
    """
    Application user table that links to Keycloak users.
    This stores application-specific user data.
    """

    __tablename__ = TABLE_USERS  # type: ignore
    __table_args__ = {"schema": SCHEMA_COMMON}

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    # Link to Keycloak user - this is the key connection
    keycloak_user_id: str = Field(
        unique=True, index=True, description="Keycloak user UUID"
    )

    # User profile data (synced from Keycloak on login)
    email: str = Field(index=True, description="User's email address")
    username: str = Field(index=True, description="Unique username")
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)

    # Application-specific user data
    display_name: Optional[str] = Field(
        default=None, max_length=200, description="User's preferred display name"
    )
    timezone: str = Field(default="UTC", description="User's timezone")
    is_active: bool = Field(
        default=True, description="Whether the user account is active"
    )
    last_login: Optional[datetime] = Field(
        default=None, description="Last login timestamp"
    )

    # Relationships
    settings: "UserSettings" = Relationship(back_populates="user")


class UserSettings(TimestampMixin, table=True):
    """
    User application settings - separate table for flexibility
    """

    __tablename__ = TABLE_USER_SETTINGS  # type: ignore
    __table_args__ = {"schema": SCHEMA_COMMON}

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(
        foreign_key=f"{SCHEMA_COMMON}.users.id", unique=True, index=True
    )

    # Music Practice Settings
    default_session_type: SessionType = Field(default=SessionType.FREE_PLAY)
    preferred_tempo_range_min: Optional[int] = Field(default=80, ge=40, le=300)
    preferred_tempo_range_max: Optional[int] = Field(default=140, ge=40, le=300)
    default_difficulty_level: Optional[int] = Field(default=3, ge=1, le=5)

    # Goal Settings
    daily_practice_goal_minutes: int = Field(
        default=30, ge=5, le=480, description="Daily practice goal in minutes"
    )
    weekly_practice_goal_sessions: int = Field(
        default=5, ge=1, le=14, description="Weekly practice goal sessions"
    )

    # UI/UX Preferences
    theme: Theme = Field(default=Theme.SYSTEM)

    # Privacy Settings
    profile_public: bool = Field(default=False)
    share_practice_stats: bool = Field(default=False)

    # Relationships
    user: User = Relationship(back_populates="settings")
