from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class TimestampMixin(SQLModel):
    """
    Mixin that provides created_at and updated_at timestamp fields.
    """

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default=None)
