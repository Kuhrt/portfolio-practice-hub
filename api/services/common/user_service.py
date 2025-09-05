import logging
import uuid
from datetime import datetime, timezone

import redis
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from sqlmodel import Session, select

from exceptions.common import (
    UserDataValidationError,
    UserNotFoundError,
    UserServiceError,
)
from middleware.auth_middleware import get_keycloak_user
from models.auth import KeycloakUser
from models.common import User, UserSettings
from schemas.common import UserProfileUpdate, UserSettingsUpdate
from services import get_db, get_redis

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, db_session: Session, redis_client: redis.Redis):
        self.cache_ttl = 3600  # 1 hour
        self.db = db_session
        self.redis = redis_client

    def get_or_create_user(self, keycloak_user: KeycloakUser) -> User:
        """
        Get existing user or create new one from Keycloak user.
        This is called on every authenticated request (JIT user provisioning).
        """
        try:
            if not keycloak_user.user_id:
                raise UserDataValidationError("Keycloak user ID is required", "user_id")
            if not keycloak_user.email:
                raise UserDataValidationError("Email is required", "email")

            user = self.db.exec(
                select(User).where(User.keycloak_user_id == keycloak_user.user_id)
            ).first()

            if user:
                updated = False

                if user.email != keycloak_user.email:
                    user.email = keycloak_user.email
                    updated = True

                if user.username != keycloak_user.username:
                    user.username = keycloak_user.username
                    updated = True

                if user.first_name != keycloak_user.first_name:
                    user.first_name = keycloak_user.first_name
                    updated = True

                if user.last_name != keycloak_user.last_name:
                    user.last_name = keycloak_user.last_name
                    updated = True

                user.last_login = datetime.now(timezone.utc)
                user.updated_at = datetime.now(timezone.utc)

                if updated:
                    self.db.commit()
                    self.db.refresh(user)

                return user

            new_user = User(
                keycloak_user_id=keycloak_user.user_id,
                email=keycloak_user.email,
                username=keycloak_user.username,
                first_name=keycloak_user.first_name,
                last_name=keycloak_user.last_name,
                display_name=f"{keycloak_user.first_name} {keycloak_user.last_name}".strip()
                or keycloak_user.username,
                last_login=datetime.now(timezone.utc),
            )

            self.db.add(new_user)
            self.db.flush()

            default_settings = UserSettings(user_id=new_user.id)
            self.db.add(default_settings)

            self.db.commit()
            self.db.refresh(new_user)

            return new_user

        except UserDataValidationError:
            raise
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_or_create_user: {str(e)}")
            raise UserServiceError(f"Failed to get or create user: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in get_or_create_user: {str(e)}")
            raise UserServiceError(f"Unexpected error occurred: {str(e)}")

    def get_user_and_settings(self, user_id: uuid.UUID) -> User | None:
        try:
            settings_relationship = getattr(User, "settings")

            user = self.db.exec(
                select(User)
                .where(User.id == user_id)
                .options(joinedload(settings_relationship))
            ).first()

            return user

        except UserDataValidationError:
            raise
        except SQLAlchemyError as e:
            logger.error(
                f"Database error in get_user_and_settings for user {user_id}: {str(e)}"
            )
            raise UserServiceError(f"Failed to get user and settings: {str(e)}")
        except Exception as e:
            logger.error(
                f"Unexpected error in get_user_and_settings for user {user_id}: {str(e)}"
            )
            raise UserServiceError(f"Unexpected error occurred: {str(e)}")

    def update_user_profile(
        self, user_id: uuid.UUID, profile_update: UserProfileUpdate
    ) -> User | None:
        """Update user information"""
        try:
            user = self.db.get(User, user_id)
            if not user:
                raise UserNotFoundError(str(user_id))

            update_dict = profile_update.model_dump(exclude_unset=True)
            for field, value in update_dict.items():
                setattr(user, field, value)

            user.updated_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(user)

            self.invalidate_user_cache(user.keycloak_user_id)

            return user

        except (UserDataValidationError, UserNotFoundError):
            raise
        except SQLAlchemyError as e:
            logger.error(
                f"Database error in update_user_profile for user {user_id}: {str(e)}"
            )
            raise UserServiceError(f"Failed to update user profile: {str(e)}")
        except Exception as e:
            logger.error(
                f"Unexpected error in update_user_profile for user {user_id}: {str(e)}"
            )
            raise UserServiceError(f"Unexpected error occurred: {str(e)}")

    def get_user_cache_key(self, keycloak_user_id: str) -> str:
        """
        Get cache key for user.
        Ensure the id used is the keycloak_user_id, not the user_id.
        """
        return f"user:keycloak:{keycloak_user_id}"

    def cache_user(self, user: User):
        """Cache user data"""
        try:
            if not user or not user.keycloak_user_id:
                raise UserDataValidationError(
                    "User and keycloak_user_id are required for caching"
                )

            cache_key = self.get_user_cache_key(user.keycloak_user_id)
            self.redis.set(cache_key, user.model_dump_json(), ex=self.cache_ttl)

        except UserDataValidationError:
            raise
        except Exception as e:
            logger.warning(f"Failed to cache user data: {str(e)}")

    def invalidate_user_cache(self, keycloak_user_id: str):
        """Invalidate user cache"""
        try:
            if not keycloak_user_id:
                raise UserDataValidationError(
                    "Keycloak user ID is required for cache invalidation"
                )

            cache_key = self.get_user_cache_key(keycloak_user_id)
            self.redis.delete(cache_key)

        except UserDataValidationError:
            raise
        except Exception as e:
            logger.warning(f"Failed to invalidate user cache: {str(e)}")


# FastAPI Dependencies
def get_user_service(
    db: Session = Depends(get_db), redis_client: redis.Redis = Depends(get_redis)
) -> UserService:
    """Dependency to get user service"""
    return UserService(db, redis_client)


def get_current_user(
    keycloak_user: KeycloakUser = Depends(get_keycloak_user),
    user_service: UserService = Depends(get_user_service),
) -> User:
    """
    Main dependency to get current authenticated user.
    This handles the JIT user provisioning automatically.
    """
    return user_service.get_or_create_user(keycloak_user)
