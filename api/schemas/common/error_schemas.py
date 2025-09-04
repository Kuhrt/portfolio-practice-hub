from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict


class ErrorDetail(BaseModel):
    """Detailed error information"""

    model_config = ConfigDict(from_attributes=True)

    field: Optional[str] = None
    message: str
    code: Optional[str] = None


class ErrorResponse(BaseModel):
    """Standard error response format"""

    model_config = ConfigDict(from_attributes=True)

    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None
    path: Optional[str] = None
