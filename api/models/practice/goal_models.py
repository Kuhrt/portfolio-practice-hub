import uuid
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from constants import SCHEMA_COMMON, SCHEMA_PRACTICE, TABLE_PRACTICE_GOALS
from models.common import TimestampMixin

if TYPE_CHECKING:
    from models.common import User


class GoalType(str, Enum):
    """Available goal types"""

    PRACTICE = "practice"


class GoalStatus(str, Enum):
    """Goal status options"""

    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class PracticeTargetType(str, Enum):
    """Available practice target types"""

    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"
    WEEKS = "weeks"
    MONTHS = "months"
    SESSIONS = "sessions"


class PracticeInterval(str, Enum):
    """Available practice intervals"""

    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


class Goal(TimestampMixin, table=False):
    """Base class for all goals - provides common fields and behavior"""

    # Meta
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key=f"{SCHEMA_COMMON}.users.id")

    # Goal identification
    goal_type: GoalType = Field(description="Type of goal")
    title: str = Field(max_length=255, description="Goal title")
    description: str = Field(max_length=1000, description="Goal description")

    # Status and flags
    status: GoalStatus = Field(
        default=GoalStatus.ACTIVE, description="Current goal status"
    )
    is_active: bool = Field(default=True, description="Whether goal is active")
    is_deleted: bool = Field(default=False, description="Soft delete flag")

    # Optional common fields
    target_date: Optional[str] = Field(
        default=None, description="Target completion date (ISO format)"
    )
    priority: Optional[int] = Field(
        default=1, ge=1, le=5, description="Priority level 1-5"
    )


class PracticeGoal(Goal, table=True):
    """Practice-specific goal with music practice fields"""

    __tablename__ = TABLE_PRACTICE_GOALS  # type: ignore
    __table_args__ = {"schema": SCHEMA_PRACTICE}

    target: int = Field(default=0, description="Targe value for the goal")
    target_type: PracticeTargetType = Field(
        default=PracticeTargetType.MINUTES, description="Type of target for the goal"
    )
    target_interval: PracticeInterval = Field(
        default=PracticeInterval.DAY, description="Interval for the goal"
    )
    instrument: Optional[str] = Field(
        default=None, max_length=100, description="Instrument to practice"
    )

    # Relationships
    user: "User" = Relationship(back_populates="practice_goals")
