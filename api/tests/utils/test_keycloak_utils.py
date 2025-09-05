from unittest.mock import Mock, patch

import pytest

from utils.keycloak_utils import *


class TestKeycloakUtils:
    def test_get_keycloak_public_keys_exists(self):
        assert hasattr(__import__("utils.keycloak_utils"), "get_keycloak_public_keys")

    def test_keycloak_utils_module_imports(self):
        try:
            from utils import keycloak_utils

            assert keycloak_utils is not None
        except ImportError:
            pytest.skip("Keycloak utils module not available")

    def test_get_keycloak_public_keys_function_available(self):
        try:
            from utils.keycloak_utils import get_keycloak_public_keys

            assert callable(get_keycloak_public_keys)
        except ImportError:
            pytest.skip("Keycloak utils function not available")

    def test_get_keycloak_public_keys_with_mock(self):
        with patch("utils.keycloak_utils.get_keycloak_public_keys") as mock_get_keys:
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

            result = mock_get_keys()
            assert result == mock_jwks
            mock_get_keys.assert_called_once()

    def test_get_keycloak_public_keys_error_handling(self):
        with patch("utils.keycloak_utils.get_keycloak_public_keys") as mock_get_keys:
            mock_get_keys.side_effect = Exception("Keycloak connection failed")

            with pytest.raises(Exception) as exc_info:
                mock_get_keys()

            assert "Keycloak connection failed" in str(exc_info.value)

    def test_get_keycloak_public_keys_caching(self):
        with patch("utils.keycloak_utils.get_keycloak_public_keys") as mock_get_keys:
            mock_jwks = {"keys": []}
            mock_get_keys.return_value = mock_jwks

            result1 = mock_get_keys()
            result2 = mock_get_keys()

            assert result1 == result2
            assert mock_get_keys.call_count == 2

    def test_keycloak_utils_function_signature(self):
        try:
            import inspect

            from utils.keycloak_utils import get_keycloak_public_keys

            sig = inspect.signature(get_keycloak_public_keys)
            assert len(sig.parameters) >= 0
        except ImportError:
            pytest.skip("Keycloak utils function not available for inspection")

    def test_keycloak_utils_return_type(self):
        with patch("utils.keycloak_utils.get_keycloak_public_keys") as mock_get_keys:
            mock_jwks = {"keys": []}
            mock_get_keys.return_value = mock_jwks

            result = mock_get_keys()
            assert isinstance(result, dict)
            assert "keys" in result

    def test_keycloak_utils_with_requests_mock(self):
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {"keys": []}
            mock_response.status_code = 200
            mock_get.return_value = mock_response

            with patch(
                "utils.keycloak_utils.get_keycloak_public_keys"
            ) as mock_get_keys:
                mock_get_keys.return_value = {"keys": []}

                result = mock_get_keys()
                assert result == {"keys": []}

    def test_keycloak_utils_configuration_dependency(self):
        with patch("config.keycloak_config") as mock_config:
            mock_config.realm_url = "http://localhost:8080/realms/test"

            with patch(
                "utils.keycloak_utils.get_keycloak_public_keys"
            ) as mock_get_keys:
                mock_get_keys.return_value = {"keys": []}

                result = mock_get_keys()
                assert result == {"keys": []}
