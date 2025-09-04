import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config import keycloak_config
from models.auth import KeycloakUser
from utils import get_keycloak_public_keys

security = HTTPBearer()


def validate_and_decode_jwt(token: str) -> KeycloakUser:
    """Validate JWT token and extract user information"""
    try:
        # Get public keys
        jwks = get_keycloak_public_keys()

        # Decode header to get key ID
        header = jwt.get_unverified_header(token)
        key_id = header.get("kid")

        if not key_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing key ID",
            )

        # Find the correct public key
        jwk = None
        for key in jwks.get("keys", []):
            if key.get("kid") == key_id:
                jwk = key
                break

        if not jwk:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: key not found",
            )

        # Decode and validate token
        payload = jwt.decode(
            token,
            jwk,
            algorithms=["RS256"],
            audience=keycloak_config.client_id,
            issuer=keycloak_config.realm_url,
            options={"verify_exp": True, "verify_aud": True, "verify_iss": True},
        )

        # Extract user information
        return KeycloakUser(
            user_id=payload.get("sub"),
            email=payload.get("email", ""),
            username=payload.get("preferred_username", ""),
            first_name=payload.get("given_name"),
            last_name=payload.get("family_name"),
            preferred_username=payload.get("preferred_username"),
            email_verified=payload.get("email_verified", False),
            roles=payload.get("realm_access", {}).get("roles", []),
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {str(e)}"
        )


def get_keycloak_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> KeycloakUser:
    """Dependency to extract and validate Keycloak user from JWT"""
    return validate_and_decode_jwt(credentials.credentials)
