"""Main module

Imports:
    argparse
    server.FileService
"""

import argparse
import logging
import logging.config
import os
import sys

import yaml
from aiohttp import web

from config import Config
from server.FileService import FileService
from server.WebHandler import WebHandler


def set_logger(log_config: str, logfile: str, loglevel: str):
    """Set logger parameters.

    Args:
        logfile: log filename
        loglevel: logging level`
    """

    loglevel = loglevel.upper()

    # Let's create a directory for logs
    log_dir = os.path.dirname(logfile)
    if not os.path.exists(log_dir) and FileService.is_pathname_valid(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    conf_dict = dict()
    with open(log_config, "r") as f:
        conf_dict = yaml.load(f, Loader=yaml.Loader)

    if logfile == "-":
        # Set log output to console only.
        conf_dict["root"]["handlers"] = ["console"]
        del conf_dict["handlers"]["file"]
    else:
        conf_dict["handlers"]["file"]["filename"] = logfile
        conf_dict["handlers"]["file"]["level"] = loglevel

    conf_dict["handlers"]["console"]["level"] = loglevel
    conf_dict["root"]["level"] = loglevel

    logging.config.dictConfig(conf_dict)


#!/usr/bin/env python3
def main(args: argparse.Namespace):
    """Main function."""

    config = Config(args.config_file)
    config.env_override()
    config.cli_override(args)

    server_config = config.config
    set_logger(server_config["log_config"], server_config["log_file"], server_config["log_level"])

    logging.info("Server started")

    handler = WebHandler()
    app = web.Application()
    app.add_routes([
        web.get('/', handler.handle),
        # TODO: add more routes
    ])
    web.run_app(app, port=server_config["port"])

    logging.info("Server stopped")


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-d", "--data-directory", dest="data_directory", help="Data directory.")
        parser.add_argument(
            "-l",
            "--log-file",
            dest="log_file",
            #default=DEFAULT_CONFIG["log_file"],
            help=f"Log filename. Default: {Config.DEFAULT_CONFIG['log_file']}.",
        )
        parser.add_argument(
            "-L",
            "--log-level",
            dest="log_level",
            choices=STANDARD_LOG_LEVELS,
            #default=DEFAULT_CONFIG["log_level"],
            help=f"Log level. Default: {Config.DEFAULT_CONFIG['log_level']}.",
            type=str.upper,
        )
        parser.add_argument(
            "-c",
            "--config-file",
            dest="config_file",
            default=Config.DEFAULT_CONFIG_FILE,
            help=f"Configuration file. Default: {Config.DEFAULT_CONFIG_FILE}.",
        )

        args = parser.parse_args()
        main(args)
    except SystemExit as e:
        if e.code:
            print(f"Run error!")
        sys.exit(e.code)
