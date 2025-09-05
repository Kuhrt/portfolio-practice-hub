from unittest.mock import Mock, patch

import jwt
import pytest
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from middleware.auth_middleware import get_keycloak_user, validate_and_decode_jwt
from models.auth import KeycloakUser


class TestValidateAndDecodeJwt:
    def test_validate_and_decode_jwt_success(self, mock_jwt_payload):
        with patch(
            "middleware.auth_middleware.get_keycloak_public_keys"
        ) as mock_get_keys:
            mock_jwks = {
                "keys": [
                    {
                        "kid": "test-key-id",
                        "kty": "RSA",
                        "use": "sig",
                        "n": "test-n",
                        "e": "AQAB",
                    }
                ]
            }
            mock_get_keys.return_value = mock_jwks

            with patch("jwt.decode") as mock_decode:
                mock_decode.return_value = mock_jwt_payload

                token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRlc3Qta2V5LWlkIn0.eyJzdWIiOiJ0ZXN0LWtleWNsb2FrLWlkLTEyMyIsImVtYWlsIjoidGVzdEBleGFtcGxlLmNvbSIsInByZWZlcnJlZF91c2VybmFtZSI6InRlc3R1c2VyIiwiZ2l2ZW5fbmFtZSI6IlRlc3QiLCJmYW1pbHlfbmFtZSI6IlVzZXIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbInVzZXIiXX0sImF1ZCI6InRlc3QtY2xpZW50IiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwL3JlYWxtcy90ZXN0IiwiZXhwIjoxNjAwMDAwMDAwfQ.test-signature"
                result = validate_and_decode_jwt(token)

                assert isinstance(result, KeycloakUser)
                assert result.user_id == mock_jwt_payload["sub"]
                assert result.email == mock_jwt_payload["email"]
                assert result.username == mock_jwt_payload["preferred_username"]
                assert result.first_name == mock_jwt_payload["given_name"]
                assert result.last_name == mock_jwt_payload["family_name"]
                assert (
                    result.preferred_username == mock_jwt_payload["preferred_username"]
                )
                assert result.email_verified == mock_jwt_payload["email_verified"]
                assert result.roles == mock_jwt_payload["realm_access"]["roles"]

    def test_validate_and_decode_jwt_missing_key_id(self):
        with patch(
            "middleware.auth_middleware.get_keycloak_public_keys"
        ) as mock_get_keys:
            mock_jwks = {"keys": []}
            mock_get_keys.return_value = mock_jwks

            with patch("jwt.get_unverified_header") as mock_header:
                mock_header.return_value = {}  # No 'kid' field

                token = "test-jwt-token"

                with pytest.raises(HTTPException) as exc_info:
                    validate_and_decode_jwt(token)

                assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
                assert "missing key ID" in exc_info.value.detail

    def test_validate_and_decode_jwt_key_not_found(self):
        with patch(
            "middleware.auth_middleware.get_keycloak_public_keys"
        ) as mock_get_keys:
            mock_jwks = {"keys": [{"kid": "different-key-id", "kty": "RSA"}]}
            mock_get_keys.return_value = mock_jwks

            with patch("jwt.get_unverified_header") as mock_header:
                mock_header.return_value = {"kid": "test-key-id"}

                token = "test-jwt-token"

                with pytest.raises(HTTPException) as exc_info:
                    validate_and_decode_jwt(token)

                assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
                assert "key not found" in exc_info.value.detail

    def test_validate_and_decode_jwt_expired_token(self):
        with patch(
            "middleware.auth_middleware.get_keycloak_public_keys"
        ) as mock_get_keys:
            mock_jwks = {"keys": [{"kid": "test-key-id", "kty": "RSA"}]}
            mock_get_keys.return_value = mock_jwks

            with patch("jwt.get_unverified_header") as mock_header:
                mock_header.return_value = {"kid": "test-key-id"}

                with patch("jwt.decode") as mock_decode:
                    mock_decode.side_effect = jwt.ExpiredSignatureError(
                        "Token has expired"
                    )

                    token = "test-jwt-token"

                    with pytest.raises(HTTPException) as exc_info:
                        validate_and_decode_jwt(token)

                    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
                    assert "Token has expired" in exc_info.value.detail

    def test_validate_and_decode_jwt_invalid_token(self):
        with patch(
            "middleware.auth_middleware.get_keycloak_public_keys"
        ) as mock_get_keys:
            mock_jwks = {"keys": [{"kid": "test-key-id", "kty": "RSA"}]}
            mock_get_keys.return_value = mock_jwks

            with patch("jwt.get_unverified_header") as mock_header:
                mock_header.return_value = {"kid": "test-key-id"}

                with patch("jwt.decode") as mock_decode:
                    mock_decode.side_effect = jwt.InvalidTokenError("Invalid token")

                    token = "test-jwt-token"

                    with pytest.raises(HTTPException) as exc_info:
                        validate_and_decode_jwt(token)

                    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
                    assert "Invalid token" in exc_info.value.detail

    def test_validate_and_decode_jwt_missing_required_fields(self, mock_jwt_payload):
        with patch(
            "middleware.auth_middleware.get_keycloak_public_keys"
        ) as mock_get_keys:
            mock_jwks = {"keys": [{"kid": "test-key-id", "kty": "RSA"}]}
            mock_get_keys.return_value = mock_jwks

            with patch("jwt.get_unverified_header") as mock_header:
                mock_header.return_value = {"kid": "test-key-id"}

                with patch("jwt.decode") as mock_decode:
                    incomplete_payload = {"sub": "test-user-id"}
                    mock_decode.return_value = incomplete_payload

                    token = "test-jwt-token"
                    result = validate_and_decode_jwt(token)

                    assert result.user_id == "test-user-id"
                    assert result.email == ""
                    assert result.username == ""
                    assert result.first_name is None
                    assert result.last_name is None
                    assert result.preferred_username is None
                    assert result.email_verified is False
                    assert result.roles == []

    def test_validate_and_decode_jwt_jwt_decode_parameters(self, mock_jwt_payload):
        with patch(
            "middleware.auth_middleware.get_keycloak_public_keys"
        ) as mock_get_keys:
            mock_jwks = {
                "keys": [
                    {
                        "kid": "test-key-id",
                        "kty": "RSA",
                        "use": "sig",
                        "n": "test-n",
                        "e": "AQAB",
                    }
                ]
            }
            mock_get_keys.return_value = mock_jwks

            with patch("jwt.get_unverified_header") as mock_header:
                mock_header.return_value = {"kid": "test-key-id"}

                with patch("jwt.decode") as mock_decode:
                    mock_decode.return_value = mock_jwt_payload

                    token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRlc3Qta2V5LWlkIn0.eyJzdWIiOiJ0ZXN0LWtleWNsb2FrLWlkLTEyMyIsImVtYWlsIjoidGVzdEBleGFtcGxlLmNvbSIsInByZWZlcnJlZF91c2VybmFtZSI6InRlc3R1c2VyIiwiZ2l2ZW5fbmFtZSI6IlRlc3QiLCJmYW1pbHlfbmFtZSI6IlVzZXIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbInVzZXIiXX0sImF1ZCI6InRlc3QtY2xpZW50IiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwL3JlYWxtcy90ZXN0IiwiZXhwIjoxNjAwMDAwMDAwfQ.test-signature"
                    validate_and_decode_jwt(token)

                    mock_decode.assert_called_once()
                    call_args = mock_decode.call_args
                    assert call_args[0][0] == token
                    assert call_args[1]["algorithms"] == ["RS256"]
                    assert call_args[1]["audience"] == "app-public"
                    assert (
                        call_args[1]["issuer"]
                        == "http://localhost:8080/realms/practice-hub"
                    )
                    assert call_args[1]["options"]["verify_exp"] is True
                    assert call_args[1]["options"]["verify_aud"] is True
                    assert call_args[1]["options"]["verify_iss"] is True


class TestGetKeycloakUser:
    def test_get_keycloak_user_success(self, mock_jwt_payload):
        with patch(
            "middleware.auth_middleware.validate_and_decode_jwt"
        ) as mock_validate:
            mock_validate.return_value = KeycloakUser(
                user_id=mock_jwt_payload["sub"],
                email=mock_jwt_payload["email"],
                username=mock_jwt_payload["preferred_username"],
                first_name=mock_jwt_payload["given_name"],
                last_name=mock_jwt_payload["family_name"],
                preferred_username=mock_jwt_payload["preferred_username"],
                email_verified=mock_jwt_payload["email_verified"],
                roles=mock_jwt_payload["realm_access"]["roles"],
            )

            credentials = HTTPAuthorizationCredentials(
                scheme="Bearer", credentials="test-token"
            )
            result = get_keycloak_user(credentials)

            assert isinstance(result, KeycloakUser)
            mock_validate.assert_called_once_with("test-token")

    def test_get_keycloak_user_validation_error(self):
        with patch(
            "middleware.auth_middleware.validate_and_decode_jwt"
        ) as mock_validate:
            mock_validate.side_effect = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

            credentials = HTTPAuthorizationCredentials(
                scheme="Bearer", credentials="invalid-token"
            )

            with pytest.raises(HTTPException) as exc_info:
                get_keycloak_user(credentials)

            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert "Invalid token" in exc_info.value.detail

    def test_get_keycloak_user_credentials_extraction(self, mock_jwt_payload):
        with patch(
            "middleware.auth_middleware.validate_and_decode_jwt"
        ) as mock_validate:
            mock_validate.return_value = KeycloakUser(
                user_id=mock_jwt_payload["sub"],
                email=mock_jwt_payload["email"],
                username=mock_jwt_payload["preferred_username"],
            )

            credentials = HTTPAuthorizationCredentials(
                scheme="Bearer", credentials="test-jwt-token"
            )
            get_keycloak_user(credentials)

            mock_validate.assert_called_once_with("test-jwt-token")
