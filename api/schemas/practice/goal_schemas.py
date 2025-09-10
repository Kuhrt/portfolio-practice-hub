import uuid
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel

from models.practice import GoalStatus, PracticeInterval, PracticeTargetType
from schemas.practice.practice_session_schemas import PracticeSessionResponse


class PracticeGoalCreate(BaseModel):
    title: str
    description: str
    target_date: Optional[str] = None
    priority: Optional[int] = 1

    target: int
    target_type: PracticeTargetType
    target_interval: PracticeInterval
    instrument: Optional[str] = None


class PracticeGoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[GoalStatus] = None
    is_active: Optional[bool] = None
    target_date: Optional[str] = None
    priority: Optional[int] = None

    target: Optional[int] = None
    target_type: Optional[PracticeTargetType] = None
    target_interval: Optional[PracticeInterval] = None
    instrument: Optional[str] = None


class PracticeGoalResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    status: GoalStatus
    is_active: bool
    target_date: Optional[str] = None
    priority: int
    target: int
    target_type: PracticeTargetType
    target_interval: PracticeInterval
    instrument: Optional[str] = None
    sessions: Optional[List["PracticeSessionResponse"]] = None
