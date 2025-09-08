import logging
import uuid
from datetime import datetime, timezone

import redis
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from exceptions.common import (
    UserSettingsServiceError,
    UserSettingsValidationError,
)
from models.common import UserSettings
from schemas.common import UserSettingsUpdate
from services import get_db, get_redis

logger = logging.getLogger(__name__)


class UserSettingsService:
    """Service for user settings"""

    def __init__(self, db_session: Session, redis_client: redis.Redis):
        self.db = db_session
        self.redis = redis_client

    def get_user_settings(self, user_id: uuid.UUID) -> UserSettings:
        """Get user settings"""
        try:
            return self.__get_or_create_user_settings(user_id)

        except UserSettingsValidationError:
            raise
        except SQLAlchemyError as e:
            logger.error(
                f"Database error in get_user_settings for user {user_id}: {str(e)}"
            )
            raise UserSettingsServiceError(f"Failed to get user settings: {str(e)}")
        except Exception as e:
            logger.error(
                f"Unexpected error in get_user_settings for user {user_id}: {str(e)}"
            )
            raise UserSettingsServiceError(f"Unexpected error occurred: {str(e)}")

    def update_user_settings(
        self, user_id: uuid.UUID, settings_update: UserSettingsUpdate
    ) -> UserSettings:
        """Update user settings"""
        try:
            settings = self.__get_or_create_user_settings(user_id)

            update_dict = settings_update.model_dump(exclude_unset=True)
            for field, value in update_dict.items():
                setattr(settings, field, value)

            settings.updated_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(settings)

            return settings

        except UserSettingsValidationError:
            raise
        except SQLAlchemyError as e:
            logger.error(
                f"Database error in update_user_settings for user {user_id}: {str(e)}"
            )
            raise UserSettingsServiceError(f"Failed to update user settings: {str(e)}")
        except Exception as e:
            logger.error(
                f"Unexpected error in update_user_settings for user {user_id}: {str(e)}"
            )
            raise UserSettingsServiceError(f"Unexpected error occurred: {str(e)}")

    def __get_or_create_user_settings(self, user_id: uuid.UUID) -> UserSettings:
        """Ensures user settings are created if they don't exist"""
        try:
            settings = self.db.exec(
                select(UserSettings).where(UserSettings.user_id == user_id)
            ).one_or_none()
            if not settings:
                settings = UserSettings(user_id=user_id)
                self.db.add(settings)
                self.db.commit()
                self.db.refresh(settings)
            return settings

        except SQLAlchemyError as e:
            logger.error(
                f"Database error in __get_or_create_user_settings for user {user_id}: {str(e)}"
            )
            raise UserSettingsServiceError(
                f"Failed to get or create user settings: {str(e)}"
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in __get_or_create_user_settings for user {user_id}: {str(e)}"
            )
            raise UserSettingsServiceError(f"Unexpected error occurred: {str(e)}")


# FastAPI Dependencies
def get_user_settings_service(
    db_session: Session = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis),
) -> UserSettingsService:
    """Dependency to get the user settings service"""
    return UserSettingsService(db_session, redis_client)
