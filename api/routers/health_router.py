import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends

from models.common import User
from schemas.common import ErrorResponse, HealthCheckResponse
from services import get_current_user
from services.api import get_health_api_service

logger = logging.getLogger(__name__)

health_router = APIRouter(prefix="/health", tags=["Health Checks"])


@health_router.get(
    "/ping",
    response_model=HealthCheckResponse,
    status_code=200,
    responses={
        503: {"model": ErrorResponse, "description": "Service unavailable"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
        200: {"description": "Health check successful"},
    },
)
def health_check(service=Depends(get_health_api_service)) -> HealthCheckResponse:
    """
    Health check for the API.
    """
    logger.debug("Health check requested")
    response = service.ping()
    logger.info("Health check completed successfully")
    return response


# Protected health check that requires authentication
@health_router.get("/authenticated")
async def authenticated_health_check(current_user: User = Depends(get_current_user)):
    """Protected health check that verifies JWT validation"""
    return {
        "status": "OK",
        "user_id": str(current_user.id),
        "username": current_user.username,
        "timestamp": datetime.now(timezone.utc),
    }
