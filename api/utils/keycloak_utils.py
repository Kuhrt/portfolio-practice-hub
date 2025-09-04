from functools import lru_cache

import requests
from fastapi import HTTPException, status

from config import keycloak_config


@lru_cache()
def get_keycloak_public_keys():
    """Get and cache Keycloak public keys for JWT validation"""
    try:
        response = requests.get(keycloak_config.certs_url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Unable to fetch Keycloak public keys: {str(e)}",
        )
