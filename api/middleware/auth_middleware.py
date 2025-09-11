from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, jwk as jose_jwk
from jose.exceptions import JWTError, ExpiredSignatureError

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

        # Convert JWK to key object for python-jose
        key = jose_jwk.construct(jwk)

        # Decode and validate token using python-jose
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=keycloak_config.client_id,
            issuer=keycloak_config.realm_url,
            options={"verify_exp": True,
                     "verify_aud": False, "verify_iss": True},
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

    except ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        ) from e
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {str(e)}"
        ) from e


def get_keycloak_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> KeycloakUser:
    """Dependency to extract and validate Keycloak user from JWT"""
    return validate_and_decode_jwt(credentials.credentials)
