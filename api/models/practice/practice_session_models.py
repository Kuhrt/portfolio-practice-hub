import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from constants import SCHEMA_COMMON, SCHEMA_PRACTICE, TABLE_PRACTICE_SESSIONS
from models.common import SessionType, TimestampMixin
from models.practice.link_models import PracticeSessionsGoals

if TYPE_CHECKING:
    from models.common import User
    from models.practice import PracticeGoal


class PracticeSession(TimestampMixin, table=True):
    """Practice session model"""

    __tablename__ = TABLE_PRACTICE_SESSIONS  # type: ignore
    __table_args__ = {"schema": SCHEMA_PRACTICE}

    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                          primary_key=True, index=True)
    user_id: uuid.UUID = Field(foreign_key=f"{SCHEMA_COMMON}.users.id")

    description: Optional[str] = Field(default=None)
    started_at: Optional[datetime] = Field(default=None)
    stopped_at: Optional[datetime] = Field(default=None)
    duration: Optional[int] = Field(default=0)
    session_type: SessionType = Field(default=SessionType.FREE_PLAY)
    tempo: Optional[int] = Field(default=None)
    difficulty_level: Optional[int] = Field(default=None, ge=1, le=10)
    notes: Optional[str] = Field(default=None)
    instrument: Optional[str] = Field(default=None)
    rating: Optional[int] = Field(default=None, ge=1, le=5)

    # Relationships
    user: "User" = Relationship(back_populates="practice_sessions")
    goals: Optional[list["PracticeGoal"]] = Relationship(
        back_populates="sessions", link_model=PracticeSessionsGoals
    )
