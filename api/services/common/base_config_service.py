import logging
import os
import sys

from dotenv import dotenv_values
from pydantic import BaseModel, Field

# TODO: logger has not yet been configured here
logger = logging.getLogger(__name__)


class BaseConfigService(BaseModel):
    """
    Base class for application configuration.
    - Loads {Environment} from command line argument "ENV={Environment}"
      - If not set, loads {Environment} from environment variable "APP_ENVIRONMENT"
      - If not set, defaults to "none"
    - Loads config from
        .env,
        .env.local,           -- local overrides (highest priority)
        .env.secrets,
        .env.{Environment},          -- if environment != none
        .env.{Environment}.secrets,  -- if environment != none
        Environment Variables,
        and command line arguments
    - Converts values to the correct type, as long as type is int, bool, or str
    - If --conf-debug is set, prints the config to the console
    - If --conf-skip-env is set, skips loading OS environment variables
    """

    APP_ENVIRONMENT: str = Field(default="none")

    def __init__(self, **data):
        # Set up the raw config first
        app_environment = os.getenv("APP_ENVIRONMENT", "none")

        # Parse command line arguments into a dictionary
        cmd_args = {}
        for arg in sys.argv[1:]:
            if "=" in arg:
                key, value = arg.split("=", 1)
                cmd_args[key] = value
        verbose = "--conf-debug" in sys.argv[1:]
        skip_env = "--conf-skip-env" in sys.argv[1:]

        # Update app_environment if provided in command line arguments
        if "ENV" in cmd_args:
            app_environment = cmd_args["ENV"]

        env = {**dotenv_values(".env")}
        env_local = {**dotenv_values(".env.local")}
        env_secrets = {**dotenv_values(".env.secrets")}
        env_app = (
            {**dotenv_values(f".env.{app_environment}")}
            if app_environment != "none"
            else {}
        )
        env_app_secrets = (
            {**dotenv_values(f".env.{app_environment}.secrets")}
            if app_environment != "none"
            else {}
        )
        if skip_env:
            env_os = {}
        else:
            env_os = {**os.environ}
        env_cmd = {**cmd_args}

        if verbose:
            self.__pretty_print_dict(".env", env)
            self.__pretty_print_dict(".env.local", env_local)
            self.__pretty_print_dict(".env.secrets", env_secrets)
            self.__pretty_print_dict(f".env.{app_environment}", env_app)
            self.__pretty_print_dict(f".env.{app_environment}.secrets", env_app_secrets)
            self.__pretty_print_dict("Environment Variables", env_os)
            self.__pretty_print_dict("Command Line Arguments", env_cmd)

        config = {
            **env,
            **env_secrets,
            **env_app,
            **env_app_secrets,
            **env_os,
            **env_cmd,
            **env_local,
        }
        # Load values from config into data dict for Pydantic initialization
        self._prepare_data_from_config(config, data)

        # Initialize the Pydantic model with the prepared data
        super().__init__(**data)
        self.APP_ENVIRONMENT = app_environment or "none"

    def __pretty_print_dict(self, caption: str, d: dict) -> None:
        if len(d) == 0:
            print(f"{caption}: (empty)")
            return
        print(f"{caption}:")
        for k, v in d.items():
            print(f"    {k}={v}")

    def _prepare_data_from_config(
        self, config: dict, data: dict, verbose: bool = False
    ) -> None:
        """
        Prepares values from self.config dictionary and adds them to the data dict
        for Pydantic initialization.
        """
        # Get the field types from the model
        field_types = self.__annotations__

        for field_name, expected_type in field_types.items():
            if verbose:
                print(f"field_name: {field_name}, expected_type: {expected_type}")
            # Skip if the field is already provided in the initialization data
            if field_name in data:
                if verbose:
                    print(
                        f"field_name: {field_name} is already provided in the initialization data"
                    )
                continue

            if field_name in config:
                raw_value = config[field_name]
                if raw_value is None or raw_value == "":
                    print(f"WARNING: {field_name} is not set in config")
                    continue
                if verbose:
                    print(f"raw_value: {raw_value}")

                # Convert the value to the expected type
                converted_value = None

                if expected_type == int:
                    if field_name == "LOG_LEVEL":
                        converted_value = self.__get_log_level(str(raw_value))
                    else:
                        if self.__is_int(raw_value):
                            converted_value = int(raw_value)
                        else:
                            if verbose:
                                print(
                                    f"WARNING: {field_name} is not a valid integer value: {raw_value}"
                                )
                            continue
                elif expected_type == bool:
                    # Handle boolean conversion (supports "True", "true", "1", etc.)
                    converted_value = self.__get_bool(raw_value)
                    if converted_value is None:
                        if verbose:
                            print(
                                f"WARNING: {field_name} is not a valid boolean value: {raw_value}"
                            )
                        continue
                elif expected_type == str:
                    converted_value = str(raw_value)
                else:
                    # For other types, let pydantic handle conversion
                    converted_value = raw_value

                # Only add the converted value if it was successfully converted
                if converted_value is not None:
                    data[field_name] = converted_value

    def __is_int(self, raw_value: str) -> bool:
        try:
            int(raw_value)
            return True
        except ValueError:
            return False

    def __get_bool(self, raw_value: str) -> bool | None:
        is_true = raw_value.lower() in ("true", "t", "1", "yes", "y", "on")
        is_false = raw_value.lower() in ("false", "f", "0", "no", "n", "off")
        if not is_true and not is_false:
            return None
        return is_true

    def __get_log_level(self, raw_value: str) -> int:
        level = raw_value.upper()
        levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        return levels.get(level, logging.INFO)
