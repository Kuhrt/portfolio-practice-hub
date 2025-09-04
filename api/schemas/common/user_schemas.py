import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict


class UserProfileResponse(BaseModel):
    """API response model for user profile data"""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    display_name: Optional[str]
    timezone: str
    last_login: Optional[datetime]
    created_at: datetime


class UserSettingsResponse(BaseModel):
    """API response model for user settings data"""

    model_config = ConfigDict(from_attributes=True)

    default_session_type: Optional[str]
    preferred_tempo_range_min: Optional[int]
    preferred_tempo_range_max: Optional[int]
    default_difficulty_level: Optional[int]
    daily_practice_goal_minutes: int
    weekly_practice_goal_sessions: int
    theme: str
    dashboard_layout: Dict[str, Any]
    notification_preferences: Dict[str, bool]
    spotify_connected: bool
    spotify_auto_import: bool
    profile_public: bool
    share_practice_stats: bool
    updated_at: Optional[datetime]


class UserSettingsUpdate(BaseModel):
    """API request model for updating user settings"""

    default_session_type: Optional[str] = None
    preferred_tempo_range_min: Optional[int] = None
    preferred_tempo_range_max: Optional[int] = None
    default_difficulty_level: Optional[int] = None
    daily_practice_goal_minutes: Optional[int] = None
    weekly_practice_goal_sessions: Optional[int] = None
    theme: Optional[str] = None
    dashboard_layout: Optional[Dict[str, Any]] = None
    notification_preferences: Optional[Dict[str, bool]] = None
    spotify_auto_import: Optional[bool] = None
    profile_public: Optional[bool] = None
    share_practice_stats: Optional[bool] = None


class UserProfileUpdate(BaseModel):
    """API request model for updating user profile"""

    display_name: Optional[str] = None
    timezone: Optional[str] = None


class UserWithSettingsResponse(BaseModel):
    """Combined API response model for user profile + settings"""

    model_config = ConfigDict(from_attributes=True)

    profile: UserProfileResponse
    settings: UserSettingsResponse
