import logging
import uuid
from datetime import datetime, timezone
from typing import List

import redis
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, desc, select

from exceptions.practice import GoalNotFoundError, PracticeGoalServiceError
from models.practice import PracticeGoal
from schemas.practice import PracticeGoalCreate, PracticeGoalUpdate
from services import get_db, get_redis

logger = logging.getLogger(__name__)


class PracticeGoalService:
    def __init__(self, db_session: Session, redis_client: redis.Redis):
        self.db = db_session
        self.redis = redis_client

    def get_goal(self, goal_id: uuid.UUID) -> PracticeGoal:
        """Get a practice goal by ID"""
        try:
            goal = self.db.get(PracticeGoal, goal_id)

            if not goal:
                raise GoalNotFoundError(str(goal_id))

            return goal

        except GoalNotFoundError:
            raise
        except SQLAlchemyError as e:
            logger.error("Database error in get_goal: %s", str(e))
            raise PracticeGoalServiceError(f"Failed to get practice goal: {str(e)}")
        except Exception as e:
            logger.error("Unexpected error in get_goal: %s", str(e))
            raise PracticeGoalServiceError(f"Unexpected error occurred: {str(e)}")

    def get_goals_for_user(self, user_id: uuid.UUID) -> List[PracticeGoal]:
        """Get all practice goals for a user"""
        try:
            goals = self.db.exec(
                select(PracticeGoal)
                .where(
                    PracticeGoal.user_id == user_id,
                    PracticeGoal.is_deleted == False,
                    PracticeGoal.is_active == True,
                )
                .order_by(desc(PracticeGoal.created_at))
            ).all()
            return list(goals)
        except SQLAlchemyError as e:
            logger.error("Database error in get_goals_for_user: %s", str(e))
            raise PracticeGoalServiceError(
                f"Failed to get practice goals for user: {str(e)}"
            )
        except Exception as e:
            logger.error("Unexpected error in get_goals_for_user: %s", str(e))
            raise PracticeGoalServiceError(f"Unexpected error occurred: {str(e)}")

    def create_goal(self, goal_create: PracticeGoalCreate) -> PracticeGoal:
        """Create a practice goal"""
        try:
            goal = PracticeGoal(**goal_create.model_dump())
            goal.created_at = datetime.now(timezone.utc)
            goal.updated_at = datetime.now(timezone.utc)
            self.db.add(goal)
            self.db.commit()
            return goal
        except SQLAlchemyError as e:
            logger.error("Database error in create_goal: %s", str(e))
            raise PracticeGoalServiceError(f"Failed to create practice goal: {str(e)}")
        except Exception as e:
            logger.error("Unexpected error in create_goal: %s", str(e))
            raise PracticeGoalServiceError(f"Unexpected error occurred: {str(e)}")

    def update_goal(
        self, goal_id: uuid.UUID, goal_update: PracticeGoalUpdate
    ) -> PracticeGoal:
        """Update a practice goal"""
        try:
            goal = self.db.get(PracticeGoal, goal_id)
            if not goal or goal.is_deleted:
                raise GoalNotFoundError(str(goal_id))

            update_dict = goal_update.model_dump(exclude_unset=True)
            for field, value in update_dict.items():
                setattr(goal, field, value)

            goal.updated_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(goal)

            return goal
        except SQLAlchemyError as e:
            logger.error("Database error in update_goal: %s", str(e))
            raise PracticeGoalServiceError(f"Failed to update practice goal: {str(e)}")
        except Exception as e:
            logger.error("Unexpected error in update_goal: %s", str(e))
            raise PracticeGoalServiceError(f"Unexpected error occurred: {str(e)}")

    def delete_goal(self, goal_id: uuid.UUID) -> None:
        """Delete a practice goal"""
        try:
            goal = self.db.get(PracticeGoal, goal_id)
            if not goal:
                raise GoalNotFoundError(str(goal_id))

            goal.is_active = False
            goal.is_deleted = True
            goal.updated_at = datetime.now(timezone.utc)

            self.db.add(goal)
            self.db.commit()
        except SQLAlchemyError as e:
            logger.error("Database error in delete_goal: %s", str(e))
            raise PracticeGoalServiceError(f"Failed to delete practice goal: {str(e)}")
        except Exception as e:
            logger.error("Unexpected error in delete_goal: %s", str(e))
            raise PracticeGoalServiceError(f"Unexpected error occurred: {str(e)}")


# FastAPI Dependencies
def get_practice_goal_service(
    db_session: Session = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis),
) -> PracticeGoalService:
    """Dependency to get the practice goal service"""
    return PracticeGoalService(db_session, redis_client)
