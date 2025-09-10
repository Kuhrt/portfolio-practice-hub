class PracticeSessionServiceError(Exception):
    """Base exception for practice session service errors"""

    def __init__(self, message: str, session_id: str | None = None):
        self.message = message
        self.session_id = session_id
        super().__init__(message)


class PracticeSessionNotFoundError(PracticeSessionServiceError):
    """Raised when a practice session is not found"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        super().__init__(f"Practice session with ID {session_id} not found", session_id)
