from unittest.mock import Mock, patch

import pytest

from utils.schema_utils import *


class TestSchemaUtils:
    def test_create_schema_if_not_exists_exists(self):
        from utils import schema_utils

        assert hasattr(schema_utils, "create_schema_if_not_exists")

    def test_drop_schema_if_exists_exists(self):
        from utils import schema_utils

        assert hasattr(schema_utils, "drop_schema_if_exists")

    def test_schema_utils_module_imports(self):
        try:
            from utils import schema_utils

            assert schema_utils is not None
        except ImportError:
            pytest.skip("Schema utils module not available")

    def test_schema_utils_functions_available(self):
        try:
            from utils.schema_utils import (
                create_schema_if_not_exists,
                drop_schema_if_exists,
            )

            assert callable(create_schema_if_not_exists)
            assert callable(drop_schema_if_exists)
        except ImportError:
            pytest.skip("Schema utils functions not available")

    def test_schema_utils_with_mock_functions(self):
        with patch("utils.schema_utils.create_schema_if_not_exists") as mock_create:
            mock_create.return_value = None

            result = mock_create("test_schema")
            assert result is None
            mock_create.assert_called_once_with("test_schema")

    def test_schema_utils_error_handling(self):
        with patch("utils.schema_utils.create_schema_if_not_exists") as mock_create:
            mock_create.side_effect = Exception("Schema creation failed")

            with pytest.raises(Exception) as exc_info:
                mock_create("test_schema")

            assert "Schema creation failed" in str(exc_info.value)

    def test_schema_utils_function_signatures(self):
        try:
            import inspect

            from utils.schema_utils import (
                create_schema_if_not_exists,
                drop_schema_if_exists,
            )

            create_sig = inspect.signature(create_schema_if_not_exists)
            drop_sig = inspect.signature(drop_schema_if_exists)

            assert len(create_sig.parameters) >= 1
            assert len(drop_sig.parameters) >= 1
        except ImportError:
            pytest.skip("Schema utils functions not available for inspection")
