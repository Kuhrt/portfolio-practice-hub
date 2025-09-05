import logging
import uuid

from fastapi import Depends, HTTPException, status

from exceptions.common import (
    UserDataValidationError,
    UserNotFoundError,
    UserServiceError,
    UserSettingsServiceError,
    UserSettingsValidationError,
)
from models.common.user_models import User
from schemas.common import (
    UserProfileResponse,
    UserProfileUpdate,
    UserSettingsResponse,
    UserWithSettingsResponse,
)
from services import (
    UserService,
    UserSettingsService,
    get_user_service,
    get_user_settings_service,
)

logger = logging.getLogger(__name__)


class UserServiceHttpAdapter:
    """Adapts the user service to the HTTP layer"""

    def __init__(
        self, user_service: UserService, user_settings_service: UserSettingsService
    ):
        self._user_service = user_service
        self._user_settings_service = user_settings_service

    def get_profile_and_settings(self, user_id: uuid.UUID) -> UserWithSettingsResponse:
        """Get user by ID"""
        try:
            user = self._user_service.get_user_and_settings(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
                )

            return self.__map_user_and_settings_to_response(user)

        except UserDataValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid user data: {e.message}",
            )
        except UserServiceError as e:
            logger.error(f"User service error in get_profile_and_settings: {e.message}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

    def get_profile_and_settings_by_user(self, user: User) -> UserWithSettingsResponse:
        """Get user by User object"""
        try:
            if not user.settings:
                user.settings = self._user_settings_service.get_user_settings(user.id)
            return self.__map_user_and_settings_to_response(user)

        except UserSettingsValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid user settings data: {e.message}",
            )
        except UserSettingsServiceError as e:
            logger.error(
                f"User settings service error in get_profile_and_settings_by_user: {e.message}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

    def update_user_profile(
        self, user_id: uuid.UUID, profile_update: UserProfileUpdate
    ) -> User:
        """Update user data in their profile"""
        try:
            user = self._user_service.update_user_profile(user_id, profile_update)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User not found: {user_id}",
                )
            return user

        except UserNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User not found: {e.user_id}",
            )
        except UserDataValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid user data: {e.message}",
            )
        except UserServiceError as e:
            logger.error(f"User service error in update_user_profile: {e.message}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

    def __map_user_and_settings_to_response(
        self, user: User
    ) -> UserWithSettingsResponse:
        settings = UserSettingsResponse.model_validate(user.settings)
        profile = UserProfileResponse.model_validate(user)
        return UserWithSettingsResponse(profile=profile, settings=settings)


# FastAPI Dependencies
def get_user_http_service(
    user_service: UserService = Depends(get_user_service),
    user_settings_service: UserSettingsService = Depends(get_user_settings_service),
) -> UserServiceHttpAdapter:
    """Get the user service HTTP adapter"""
    return UserServiceHttpAdapter(user_service, user_settings_service)
