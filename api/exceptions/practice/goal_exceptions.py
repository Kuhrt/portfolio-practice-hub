class PracticeGoalServiceError(Exception):
    """Base exception for practice goal service errors"""

    def __init__(self, message: str, goal_id: str | None = None):
        self.message = message
        self.goal_id = goal_id
        super().__init__(message)


class GoalNotFoundError(PracticeGoalServiceError):
    """Raised when a goal is not found"""

    def __init__(self, goal_id: str):
        self.goal_id = goal_id
        super().__init__(f"Goal with ID {goal_id} not found", goal_id)
