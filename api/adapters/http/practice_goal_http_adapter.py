import logging
import uuid
from typing import List

from fastapi import Depends, HTTPException, status

from exceptions.practice import GoalNotFoundError
from schemas.practice import (
    PracticeGoalCreate,
    PracticeGoalResponse,
    PracticeGoalUpdate,
)
from services.practice import PracticeGoalService, get_practice_goal_service

logger = logging.getLogger(__name__)


class PracticeGoalHTTPAdapter:
    """Adapts the practice goal service to the HTTP layer"""

    def __init__(self, practice_goal_service: PracticeGoalService):
        self._goal_service = practice_goal_service

    def get_goal(self, goal_id: uuid.UUID) -> PracticeGoalResponse:
        """Get a practice goal by ID"""
        try:
            goal = self._goal_service.get_goal(goal_id)
            return PracticeGoalResponse.model_validate(goal)
        except GoalNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def get_goals_for_user(self, user_id: uuid.UUID) -> List[PracticeGoalResponse]:
        """Get all practice goals for a user"""
        try:
            goals = self._goal_service.get_goals_for_user(user_id)
            return [PracticeGoalResponse.model_validate(goal) for goal in goals]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def create_goal(self, goal_create: PracticeGoalCreate) -> PracticeGoalResponse:
        """Create a practice goal"""
        try:
            goal = self._goal_service.create_goal(goal_create)
            return PracticeGoalResponse.model_validate(goal)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def update_goal(
        self, goal_id: uuid.UUID, goal_update: PracticeGoalUpdate
    ) -> PracticeGoalResponse:
        """Update a practice goal"""
        try:
            goal = self._goal_service.update_goal(goal_id, goal_update)
            return PracticeGoalResponse.model_validate(goal)
        except GoalNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def delete_goal(self, goal_id: uuid.UUID) -> None:
        """Delete a practice goal"""
        try:
            self._goal_service.delete_goal(goal_id)
            return None
        except GoalNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )


# FastAPI Dependencies
def get_practice_goal_http_adapter(
    practice_goal_service: PracticeGoalService = Depends(get_practice_goal_service),
) -> PracticeGoalHTTPAdapter:
    """Get the practice goal HTTP adapter"""
    return PracticeGoalHTTPAdapter(practice_goal_service)
