import logging
import uuid
from datetime import datetime, timezone

import redis
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from exceptions.practice import (
    PracticeSessionNotFoundError,
    PracticeSessionServiceError,
)
from models.practice import PracticeSession
from schemas.practice import PracticeSessionCreate, PracticeSessionUpdate
from services import get_db, get_redis

logger = logging.getLogger(__name__)


class PracticeSessionService:
    def __init__(self, db_session: Session, redis_client: redis.Redis):
        self.db = db_session
        self.redis = redis_client

    def get_practice_session(self, session_id: uuid.UUID) -> PracticeSession:
        """Get a practice session by ID"""
        try:
            session = self.db.get(PracticeSession, session_id)
            if not session:
                raise PracticeSessionNotFoundError(str(session_id))
            return session
        except PracticeSessionNotFoundError:
            raise
        except SQLAlchemyError as e:
            logger.error("Database error in get_practice_session: %s", str(e))
            raise PracticeSessionServiceError(
                f"Failed to get practice session: {str(e)}"
            )
        except Exception as e:
            logger.error("Unexpected error in get_practice_session: %s", str(e))
            raise PracticeSessionServiceError(f"Unexpected error occurred: {str(e)}")

    def create_practice_session(
        self, session_create: PracticeSessionCreate
    ) -> PracticeSession:
        """Create a practice session"""
        try:
            session = PracticeSession(**session_create.model_dump())
            session.created_at = datetime.now(timezone.utc)
            session.updated_at = datetime.now(timezone.utc)

            self.db.add(session)
            self.db.commit()

            return session
        except SQLAlchemyError as e:
            logger.error("Database error in create_practice_session: %s", str(e))
            raise PracticeSessionServiceError(
                f"Failed to create practice session: {str(e)}"
            )
        except Exception as e:
            logger.error("Unexpected error in create_practice_session: %s", str(e))
            raise PracticeSessionServiceError(f"Unexpected error occurred: {str(e)}")

    def update_practice_session(
        self, session_id: uuid.UUID, session_update: PracticeSessionUpdate
    ) -> PracticeSession:
        """Update a practice session"""
        try:
            session = self.db.get(PracticeSession, session_id)
            if not session:
                raise PracticeSessionNotFoundError(str(session_id))

            update_dict = session_update.model_dump(exclude_unset=True)
            for field, value in update_dict.items():
                setattr(session, field, value)

            session.updated_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(session)

            return session
        except PracticeSessionNotFoundError:
            raise
        except SQLAlchemyError as e:
            logger.error("Database error in update_practice_session: %s", str(e))
            raise PracticeSessionServiceError(
                f"Failed to update practice session: {str(e)}"
            )
        except Exception as e:
            logger.error("Unexpected error in update_practice_session: %s", str(e))
            raise PracticeSessionServiceError(f"Unexpected error occurred: {str(e)}")

    def delete_practice_session(self, session_id: uuid.UUID) -> None:
        """Delete a practice session"""
        try:
            session = self.db.get(PracticeSession, session_id)
            if not session:
                raise PracticeSessionNotFoundError(str(session_id))
            session.is_active = False
            session.is_deleted = True
            session.updated_at = datetime.now(timezone.utc)
            self.db.commit()
        except PracticeSessionNotFoundError:
            raise
        except SQLAlchemyError as e:
            logger.error("Database error in delete_practice_session: %s", str(e))
            raise PracticeSessionServiceError(
                f"Failed to delete practice session: {str(e)}"
            )
        except Exception as e:
            logger.error("Unexpected error in delete_practice_session: %s", str(e))
            raise PracticeSessionServiceError(f"Unexpected error occurred: {str(e)}")


# FastAPI dependencies
def get_practice_session_service(
    db_session: Session = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis),
) -> PracticeSessionService:
    return PracticeSessionService(db_session, redis_client)
