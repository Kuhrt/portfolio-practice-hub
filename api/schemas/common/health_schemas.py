from pydantic import BaseModel, ConfigDict


class HealthCheckResponse(BaseModel):
    """API response model for health check endpoint"""

    model_config = ConfigDict(from_attributes=True)

    status: str
    version: str
