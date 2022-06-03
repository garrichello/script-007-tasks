"""Configuration module for the application.

Imports:
    yaml
"""

import argparse
import os

import yaml

DEFAULT_CONFIG_FILE = "server.conf"
DEFAULT_CONFIG = {
    "data_directory": "data",
    "log_config": "log.conf",
    "log_file": "server.log",
    "log_level": "INFO",
}

ENV_PREFIX = "MCWS_"
ENV_VARIABLES = {
    "DATA_DIR": "data_directory",
    "LOG_CONFIG": "log_config",
    "LOG_FILE": "log_file",
    "LOG_LEVEL": "log_level",
}


class BadConfigError(Exception):
    pass


class Config:
    """Stores and manages configuratin of the app"""

    # This makes me a singleton!
    def __new__(cls, config_file):
        if not hasattr(cls, "instance"):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance

    def __init__(self, config_file: str):
        """Read config file into a dictionary

        Args:
            config_file: path to a configuration YAML-file
        """
        if not os.path.exists(config_file):
            print(
                f"Configuration file {config_file} not found. Creating with default values."
            )
            with open(config_file, "w") as f:
                f.write(yaml.dump(DEFAULT_CONFIG))
            self.config = DEFAULT_CONFIG
        else:
            print(f"Using configuration file: {config_file}")
            with open(config_file, "r") as f:
                self.config = yaml.load(f, Loader=yaml.Loader)

    def env_override(self):
        """Overrides config with environmental variables."""
        for env_var, config_opt in ENV_VARIABLES.items():
            env_var_name = ENV_PREFIX + env_var
            if env_var_name in os.environ:
                self.config[config_opt] = os.environ[env_var_name]

    def cli_override(self, cli_args: argparse.Namespace):
        """Overrides config with values from CLI."""
        cli_dict = vars(cli_args)
        for config_opt in DEFAULT_CONFIG:
            if config_opt in cli_dict:
                if cli_dict[config_opt]:
                    self.config[config_opt] = cli_dict[config_opt]
