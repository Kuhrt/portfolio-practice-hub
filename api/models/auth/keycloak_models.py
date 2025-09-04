from typing import Optional

from pydantic import BaseModel


class KeycloakUser(BaseModel):
    """Keycloak user information extracted from JWT"""

    user_id: str  # Keycloak user UUID
    email: str
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    preferred_username: Optional[str] = None
    email_verified: bool = False
    roles: list[str] = []
