import uuid

from sqlmodel import Field, SQLModel

from constants import SCHEMA_PRACTICE, TABLE_SESSIONS_GOALS


class PracticeSessionsGoals(SQLModel, table=True):
    """Many-to-many relationship between PracticeSession and PracticeGoal"""

    __tablename__ = TABLE_SESSIONS_GOALS  # type: ignore
    __table_args__ = {"schema": SCHEMA_PRACTICE}

    session_id: uuid.UUID = Field(
        foreign_key=f"{SCHEMA_PRACTICE}.sessions.id", primary_key=True
    )
    goal_id: uuid.UUID = Field(
        foreign_key=f"{SCHEMA_PRACTICE}.goals.id", primary_key=True
    )
