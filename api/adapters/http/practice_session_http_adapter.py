import logging
import uuid

from fastapi import Depends, HTTPException, status

from exceptions.practice import PracticeSessionNotFoundError
from schemas.practice import (
    PracticeSessionCreate,
    PracticeSessionResponse,
    PracticeSessionUpdate,
)

from services.practice import PracticeSessionService, get_practice_session_service

logger = logging.getLogger(__name__)


class PracticeSessionHTTPAdapter:
    """Adapts the practice session service to the HTTP layer"""

    def __init__(self, practice_session_service: PracticeSessionService):
        self._session_service = practice_session_service

    def get_session(self, session_id: uuid.UUID) -> PracticeSessionResponse:
        """Get a practice session by ID"""
        try:
            session = self._session_service.get_practice_session(session_id)
            return PracticeSessionResponse.model_validate(session)
        except PracticeSessionNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(
                    e)
            )

    def get_active_session(self, user_id: uuid.UUID) -> PracticeSessionResponse | None:
        """Get the active practice session for the user"""
        try:
            session = self._session_service.get_current_active_session(user_id)
            return PracticeSessionResponse.model_validate(session.model_dump()) if session else None
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def create_session(
        self, session_create: PracticeSessionCreate
    ) -> PracticeSessionResponse:
        """Create a practice session"""
        try:
            session = self._session_service.create_practice_session(
                session_create)
            return PracticeSessionResponse.model_validate(session.model_dump())
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(
                    e)
            )

    def update_session(
        self, session_id: uuid.UUID, session_update: PracticeSessionUpdate
    ) -> PracticeSessionResponse:
        """Update a practice session"""
        try:
            session = self._session_service.update_practice_session(
                session_id, session_update
            )
            return PracticeSessionResponse.model_validate(session.model_dump())
        except PracticeSessionNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(
                    e)
            )

    def delete_session(self, session_id: uuid.UUID) -> None:
        """Delete a practice session"""
        try:
            self._session_service.delete_practice_session(session_id)
        except PracticeSessionNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(
                    e)
            )

    def end_session(self, session_id: uuid.UUID) -> PracticeSessionResponse:
        """End a practice session"""
        try:
            session = self._session_service.end_practice_session(session_id)
            return PracticeSessionResponse.model_validate(session.model_dump())
        except PracticeSessionNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(
                    e)
            )


# FastAPI dependencies
def get_practice_session_http_adapter(
    practice_session_service: PracticeSessionService = Depends(
        get_practice_session_service
    ),
) -> PracticeSessionHTTPAdapter:
    return PracticeSessionHTTPAdapter(practice_session_service)
