"""Configuration module for the application.

Imports:
    yaml
"""

import argparse
import logging
import logging.config
import os

import yaml

from server.FileService import FileService


class ServerConfig:
    """Stores and manages configuratin of the app"""

    DEFAULT_CONFIG_FILE = "server.conf"
    ENV_PREFIX = "MCWS_"
    _CONFIG_INFO = {
        "data_directory": {"dest": "data_directory", "env": "DATA_DIR", "default": "data"},
        "log_config": {"dest": "log_config", "env": "LOG_CONFIG", "default": "log.conf"},
        "log_file": {"dest": "log_file", "env": "LOG_FILE", "default": "server.log"},
        "log_level": {"dest": "log_level", "env": "LOG_LEVEL", "default": "INFO"},
        "host": {"dest": "host", "env": "HOST", "default": "127.0.0.1"},
        "port": {"dest": "port", "env": "PORT", "default": "8081"},
    }

    @classmethod
    def extract_dict(cls, dict_name: str) -> dict:
        """Extract dictionary from a common info metadictionary.

        Args:
            config_info - metadictionary containing values for different dctionaries.
            dict_name - name of a dictionary stored in a metadictionary.

        Returns:
            dictioanry: contains values of dict_name dictionary.
        """
        result_dict = dict()
        for key in cls._CONFIG_INFO:
            result_dict[key] = cls._CONFIG_INFO[key][dict_name]
        return result_dict

    # This makes me a singleton!
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(ServerConfig, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        """Simple initialization"""

        logging.basicConfig(encoding="utf-8", level=logging.INFO)

        # Initialize config with default values if it doesn't exist
        self._default_dict = self.extract_dict("default")
        if not hasattr(self, "config"):
            self.config = self._default_dict

    def read_config_file(self, config_file: str):
        """Read config file into a dictionary

        Args:
            config_file: path to a configuration YAML-file
        """

        # Always initialize the config with the default values
        self.config = self._default_dict

        if not FileService.is_pathname_valid(config_file):
            raise ValueError(f"Invalid name of configuration file: {config_file}")

        if not os.path.exists(config_file):
            logging.info(f"Configuration file {config_file} not found. Creating with default values.")
            with open(config_file, "w") as f:
                f.write(yaml.dump(self._default_dict))
            self.config = self._default_dict
        else:
            logging.info(f"Using configuration file: {config_file}")
            with open(config_file, "r") as f:
                file_config = yaml.load(f, Loader=yaml.Loader)
                self._file_override(file_config)

    def _file_override(self, file_config: dict):
        """Overrides default values with values from the config file"""
        for key in file_config:
            if key in self.config:
                self.config[key] = file_config[key]

    def env_override(self):
        """Overrides config with environmental variables."""
        env_dict = self.extract_dict("env")
        for env_var, config_opt in env_dict.items():
            env_var_name = self.ENV_PREFIX + env_var
            if env_var_name in os.environ:
                self.config[config_opt] = os.environ[env_var_name]

    def cli_override(self, cli_args: argparse.Namespace):
        """Overrides config with values from CLI."""
        dest_dict = self.extract_dict("dest")
        cli_dict = vars(cli_args)
        for config_opt in dest_dict:
            if config_opt in cli_dict and cli_dict[config_opt]:
                self.config[config_opt] = cli_dict[config_opt]

    def set_logger(self):
        """Set logger parameters.

        Args:
            logfile: log filename
            loglevel: logging level`
        """

        loglevel = self.config['log_level'].upper()

        # Let's create a directory for logs
        log_dir = os.path.dirname(os.path.abspath(self.config['log_file']))
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        conf_dict = dict()
        with open(self.config['log_config'], "r") as f:
            conf_dict = yaml.load(f, Loader=yaml.Loader)

        if self.config['log_file'] == "-":
            # Set log output to console only.
            conf_dict["root"]["handlers"] = ["console"]
            del conf_dict["handlers"]["file"]
        else:
            conf_dict["handlers"]["file"]["filename"] = self.config['log_file']
            conf_dict["handlers"]["file"]["level"] = loglevel

        conf_dict["handlers"]["console"]["level"] = loglevel
        conf_dict["root"]["level"] = loglevel

        logging.config.dictConfig(conf_dict)
