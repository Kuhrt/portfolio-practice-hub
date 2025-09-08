import logging
from typing import List

from fastapi import APIRouter, Depends

from adapters.http import (
    PracticeGoalHTTPAdapter,
    UserServiceHttpAdapter,
    get_practice_goal_http_adapter,
    get_user_http_service,
)
from models.common.user_models import User
from schemas.common import (
    UserGoalsResponse,
    UserProfileResponse,
    UserProfileUpdate,
    UserSettingsResponse,
    UserSettingsUpdate,
    UserWithSettingsResponse,
)
from schemas.common.error_responses import COMMON_ERROR_RESPONSES
from services import get_current_user

logger = logging.getLogger(__name__)

user_router = APIRouter(
    prefix="/users", tags=["Users"], responses=COMMON_ERROR_RESPONSES
)


@user_router.get("/me", response_model=UserProfileResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get the current user's profile"""
    return UserProfileResponse.model_validate(current_user)


@user_router.put("/me", response_model=UserProfileResponse)
def update_current_user_profile(
    profile_update: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    service: UserServiceHttpAdapter = Depends(get_user_http_service),
):
    """Update the current user's profile"""
    return service.update_user_profile(current_user.id, profile_update)


@user_router.get("/me/settings", response_model=UserSettingsResponse)
def get_current_user_settings(current_user: User = Depends(get_current_user)):
    """Get the current user's settings"""
    return UserSettingsResponse.model_validate(current_user.settings)


@user_router.put("/me/settings", response_model=UserSettingsResponse)
def update_current_user_settings(
    settings_update: UserSettingsUpdate,
    current_user: User = Depends(get_current_user),
    service: UserServiceHttpAdapter = Depends(get_user_http_service),
):
    """Update the current user's settings"""
    return service.update_user_settings(current_user.id, settings_update)


@user_router.get("/me/all", response_model=UserWithSettingsResponse)
def get_current_user_all(
    current_user: User = Depends(get_current_user),
    service: UserServiceHttpAdapter = Depends(get_user_http_service),
):
    """Get the current user's profile and settings"""
    return service.get_profile_and_settings_by_user(current_user)


@user_router.get("/me/goals", response_model=UserGoalsResponse)
def get_current_user_practice_goals(
    current_user: User = Depends(get_current_user),
    service: PracticeGoalHTTPAdapter = Depends(get_practice_goal_http_adapter),
):
    """Get the current user's practice goals"""
    return UserGoalsResponse(practice_goals=service.get_goals_for_user(current_user.id))
