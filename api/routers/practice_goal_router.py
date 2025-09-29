import logging
import uuid

from fastapi import APIRouter, Depends

from adapters.http import PracticeGoalHTTPAdapter, get_practice_goal_http_adapter
from schemas.common.error_responses import COMMON_ERROR_RESPONSES
from schemas.practice import (
    PracticeGoalCreate,
    PracticeGoalResponse,
    PracticeGoalUpdate,
)
from services import get_current_user

logger = logging.getLogger(__name__)

practice_goal_router = APIRouter(
    prefix="/goals/practice",
    tags=["Practice Goals"],
    responses=COMMON_ERROR_RESPONSES,
    dependencies=[Depends(get_current_user)],
)


@practice_goal_router.post("", response_model=PracticeGoalResponse)
def create_practice_goal(
    practice_goal_create: PracticeGoalCreate,
    service: PracticeGoalHTTPAdapter = Depends(get_practice_goal_http_adapter),
):
    return service.create_goal(practice_goal_create)


@practice_goal_router.get("/{goal_id}", response_model=PracticeGoalResponse)
def get_practice_goal(
    goal_id: uuid.UUID,
    service: PracticeGoalHTTPAdapter = Depends(get_practice_goal_http_adapter),
):
    return service.get_goal(goal_id)


@practice_goal_router.put("/{goal_id}", response_model=PracticeGoalResponse)
def update_practice_goal(
    goal_id: uuid.UUID,
    practice_goal_update: PracticeGoalUpdate,
    service: PracticeGoalHTTPAdapter = Depends(get_practice_goal_http_adapter),
):
    return service.update_goal(goal_id, practice_goal_update)


@practice_goal_router.delete("/{goal_id}", response_model=None)
def delete_practice_goal(
    goal_id: uuid.UUID,
    service: PracticeGoalHTTPAdapter = Depends(get_practice_goal_http_adapter),
):
    return service.delete_goal(goal_id)
