import uuid
from datetime import datetime, timezone

import redis
from fastapi import Depends
from sqlalchemy.orm import joinedload
from sqlmodel import Session, select

from middleware.auth_middleware import get_keycloak_user
from models.auth import KeycloakUser
from models.common import User, UserSettings
from services import get_db, get_redis


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
        user = self.db.exec(
            select(User).where(User.keycloak_user_id == keycloak_user.user_id)
        ).first()

        if user:
            # Update user info if it has changed
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

            # Update last login
            user.last_login = datetime.now(timezone.utc)
            user.updated_at = datetime.now(timezone.utc)

            if updated:
                self.db.commit()
                self.db.refresh(user)

            return user

        # Create new user
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
        self.db.flush()  # Get the ID without committing

        # Create default settings for new user
        default_settings = UserSettings(user_id=new_user.id)
        self.db.add(default_settings)

        self.db.commit()
        self.db.refresh(new_user)

        return new_user


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
