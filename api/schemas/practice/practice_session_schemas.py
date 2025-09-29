import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from models.common import SessionType


class PracticeSessionCreate(BaseModel):
    user_id: Optional[uuid.UUID] = None
    description: Optional[str] = None
    session_type: Optional[SessionType] = None
    tempo: Optional[int] = None
    difficulty_level: Optional[int] = None
    notes: Optional[str] = None
    instrument: Optional[str] = None
    rating: Optional[int] = None


class PracticeSessionUpdate(BaseModel):
    description: Optional[str] = None
    started_at: Optional[datetime] = None
    stopped_at: Optional[datetime] = None
    session_type: Optional[SessionType] = None
    tempo: Optional[int] = None
    difficulty_level: Optional[int] = None
    notes: Optional[str] = None
    instrument: Optional[str] = None
    rating: Optional[int] = None


class PracticeSessionResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    description: Optional[str] = None
    started_at: Optional[datetime] = None
    stopped_at: Optional[datetime] = None
    duration: Optional[int] = None
    session_type: SessionType
    tempo: Optional[int] = None
    difficulty_level: Optional[int] = None
    notes: Optional[str] = None
    instrument: Optional[str] = None
    rating: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class PracticeSessionStart(BaseModel):
    description: Optional[str] = None
    session_type: Optional[SessionType] = None
    instrument: Optional[str] = None
