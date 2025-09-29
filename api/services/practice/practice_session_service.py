import logging
import uuid
from datetime import datetime, timezone

import redis
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, desc, select

from exceptions.practice import (
    PracticeSessionNotFoundError,
    PracticeSessionServiceError,
)
from models.practice import PracticeSession
from schemas.practice import PracticeSessionCreate, PracticeSessionUpdate, PracticeSessionStart
from services import get_db, get_redis, get_current_user

logger = logging.getLogger(__name__)


class PracticeSessionService:
    def __init__(self, db_session: Session, redis_client: redis.Redis):
        self.db = db_session
        self.redis = redis_client

    def get_all_practice_sessions(self, user_id: uuid.UUID) -> list[PracticeSession]:
        """Get all practice sessions for a user"""
        try:
            sessions = self.db.exec(select(PracticeSession).where(
                PracticeSession.user_id == user_id).order_by(desc(PracticeSession.started_at))).all()
            return list(sessions)
        except SQLAlchemyError as e:
            logger.error(
                "Database error in get_all_practice_sessions: %s", str(e))
            raise PracticeSessionServiceError(
                f"Failed to get all practice sessions: {str(e)}")

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
            logger.error(
                "Unexpected error in get_practice_session: %s", str(e))
            raise PracticeSessionServiceError(
                f"Unexpected error occurred: {str(e)}")

    def get_current_active_session(self, user_id: uuid.UUID) -> PracticeSession | None:
        """Get the current active session for a user"""
        try:
            session = self.db.exec(select(PracticeSession).where(
                PracticeSession.user_id == user_id, PracticeSession.stopped_at == None)).one_or_none()
            return session
        except SQLAlchemyError as e:
            logger.error(
                "Database error in get_current_active_session: %s", str(e))
            raise PracticeSessionServiceError(
                f"Failed to get current active session: {str(e)}"
            )
        except Exception as e:
            logger.error(
                "Unexpected error in get_current_active_session: %s", str(e))
            raise PracticeSessionServiceError(
                f"Unexpected error occurred: {str(e)}")

    def create_practice_session(
        self, session_create: PracticeSessionCreate
    ) -> PracticeSession:
        """Create a practice session"""
        try:
            self.__stop_users_active_sessions(session_create.user_id)

            session = PracticeSession(**session_create.model_dump())
            now = datetime.now(timezone.utc)
            session.started_at = now
            session.created_at = now
            session.updated_at = now

            self.db.add(session)
            self.db.commit()
            self.db.refresh(session)

            return session
        except SQLAlchemyError as e:
            logger.error(
                "Database error in create_practice_session: %s", str(e))
            raise PracticeSessionServiceError(
                f"Failed to create practice session: {str(e)}"
            )
        except Exception as e:
            logger.error(
                "Unexpected error in create_practice_session: %s", str(e))
            raise PracticeSessionServiceError(
                f"Unexpected error occurred: {str(e)}")

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

            if session.started_at and session.stopped_at:
                session.duration = (session.stopped_at -
                                    session.started_at).total_seconds()

            session.updated_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(session)

            return session
        except PracticeSessionNotFoundError:
            raise
        except SQLAlchemyError as e:
            logger.error(
                "Database error in update_practice_session: %s", str(e))
            raise PracticeSessionServiceError(
                f"Failed to update practice session: {str(e)}"
            )
        except Exception as e:
            logger.error(
                "Unexpected error in update_practice_session: %s", str(e))
            raise PracticeSessionServiceError(
                f"Unexpected error occurred: {str(e)}")

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
            logger.error(
                "Database error in delete_practice_session: %s", str(e))
            raise PracticeSessionServiceError(
                f"Failed to delete practice session: {str(e)}"
            )
        except Exception as e:
            logger.error(
                "Unexpected error in delete_practice_session: %s", str(e))
            raise PracticeSessionServiceError(
                f"Unexpected error occurred: {str(e)}")

    def end_practice_session(self, session_id: uuid.UUID) -> PracticeSession:
        """End a practice session"""
        try:
            session = self.db.get(PracticeSession, session_id)
            if not session:
                raise PracticeSessionNotFoundError(str(session_id))
            session.stopped_at = datetime.now(timezone.utc)
            session.duration = self.__calculate_session_duration(session)
            session.updated_at = session.stopped_at
            self.db.commit()
            self.db.refresh(session)
            return session
        except PracticeSessionNotFoundError:
            raise
        except SQLAlchemyError as e:
            logger.error("Database error in end_practice_session: %s", str(e))
            raise PracticeSessionServiceError(
                f"Failed to end practice session: {str(e)}")
        except Exception as e:
            logger.error(
                "Unexpected error in end_practice_session: %s", str(e))
            raise PracticeSessionServiceError(
                f"Unexpected error occurred: {str(e)}")

    def __stop_users_active_sessions(self, user_id: uuid.UUID):
        """Stop all active sessions for a user"""
        try:
            logger.info("Stopping all active sessions")
            sessions = self.db.exec(select(PracticeSession).where(
                PracticeSession.user_id == user_id, PracticeSession.stopped_at == None)).all()
            stopped_at = datetime.now(timezone.utc)
            for session in sessions:
                session.stopped_at = stopped_at
                session.duration = self.__calculate_session_duration(session)
                session.updated_at = stopped_at
            self.db.commit()
        except SQLAlchemyError as e:
            logger.error(
                "Database error in __stop_user_active_sessions: %s", str(e))
            raise PracticeSessionServiceError(
                f"Failed to stop user active sessions: {str(e)}")
        except Exception as e:
            logger.error(
                "Unexpected error in __stop_user_active_sessions: %s", str(e))
            raise PracticeSessionServiceError(
                f"Unexpected error occurred: {str(e)}")

    def __calculate_session_duration(self, session: PracticeSession):
        """Calculate the duration of a practice session"""
        # Return 0 if session hasn't started
        if not session.started_at:
            return 0

        # Ensure started_at is timezone-aware
        aware_started_at = self.__ensure_utc(session.started_at)

        # Use stopped_at if available, otherwise use current time
        if session.stopped_at:
            aware_stopped_at = self.__ensure_utc(session.stopped_at)
        else:
            aware_stopped_at = datetime.now(timezone.utc)

        # Calculate duration in seconds
        duration_seconds = (aware_stopped_at -
                            aware_started_at).total_seconds()

        # Return 0 if duration is negative (shouldn't happen, but safety check)
        return max(0, int(duration_seconds))

    def __ensure_utc(self, dt: datetime) -> datetime:
        """Ensure a datetime is timezone-aware"""
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)

# FastAPI dependencies


def get_practice_session_service(
    db_session: Session = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis),
) -> PracticeSessionService:
    return PracticeSessionService(db_session, redis_client)
