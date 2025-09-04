import logging

from fastapi import HTTPException, Query, status

from schemas.common import HealthCheckResponse

logger = logging.getLogger(__name__)


class HealthApiService:
    def __init__(self, simulate_failure: bool = False):
        self.simulate_failure = simulate_failure

    def ping(self) -> HealthCheckResponse:
        """
        Health check for the API.
        """
        logger.debug("Health check requested")

        if self.simulate_failure:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service is currently unavailable",
            )

        return HealthCheckResponse(status="OK", version="1.0.0")


def get_health_api_service(simulate_failure: bool = Query(False)) -> HealthApiService:
    return HealthApiService(simulate_failure=simulate_failure)
