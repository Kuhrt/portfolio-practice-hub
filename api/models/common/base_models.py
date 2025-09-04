from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class TimestampMixin(SQLModel):
    """
    Mixin that provides created_at and updated_at timestamp fields.
    """

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default=None)


class BaseModel(SQLModel):
    """
    Base model class for all database models.
    This ensures all models share the same metadata and configuration.
    """

    class Config:
        # Enable SQLModel to work with SQLAlchemy
        arbitrary_types_allowed = True
