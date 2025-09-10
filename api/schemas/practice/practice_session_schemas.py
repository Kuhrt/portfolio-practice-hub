import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from models.common import SessionType


class PracticeSessionCreate(BaseModel):
    started_at: Optional[datetime] = None
    session_type: SessionType
    tempo: Optional[int] = None
    difficulty_level: Optional[int] = None
    notes: Optional[str] = None
    instrument: Optional[str] = None
    rating: Optional[int] = None


class PracticeSessionUpdate(BaseModel):
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    session_type: Optional[SessionType] = None
    tempo: Optional[int] = None
    difficulty_level: Optional[int] = None
    notes: Optional[str] = None
    instrument: Optional[str] = None
    rating: Optional[int] = None


class PracticeSessionResponse(BaseModel):
    id: uuid.UUID
    started_at: datetime
    ended_at: datetime
    session_type: SessionType
    tempo: Optional[int] = None
    difficulty_level: Optional[int] = None
    notes: Optional[str] = None
    instrument: Optional[str] = None
    rating: Optional[int] = None
