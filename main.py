"""Main module

Imports:
    argparse
    server.FileService
"""

import argparse
import logging
import logging.config
import sys

from aiohttp import web

from config import ServerConfig
from server.WebHandler import WebHandler

STANDARD_LOG_LEVELS = list(logging._nameToLevel.keys())


#!/usr/bin/env python3
def main(args: argparse.Namespace):
    """Main function."""

    config = ServerConfig()
    config.read_config_file(args.config_file)

    config.env_override()
    config.cli_override(args)
    config.set_logger()

    server_config = config.config

    logging.info("Server started")

    handler = WebHandler()
    app = web.Application()
    app.add_routes(
        [
            web.get("/", handler.handle),
            # TODO: add more routes
        ]
    )
    web.run_app(app, port=server_config["port"], host=server_config["host"])

    logging.info("Server stopped")


if __name__ == "__main__":
    default_dict = ServerConfig.extract_dict("default")
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-d", "--data-directory", dest="data_directory", help="Data directory.")
        parser.add_argument(
            "-l",
            "--log-file",
            dest="log_file",
            # default=DEFAULT_CONFIG["log_file"],
            help=f"Log filename. Default: {default_dict['log_file']}.",
        )
        parser.add_argument(
            "-L",
            "--log-level",
            dest="log_level",
            choices=STANDARD_LOG_LEVELS,
            # default=DEFAULT_CONFIG["log_level"],
            help=f"Log level. Default: {default_dict['log_level']}.",
            type=str.upper,
        )
        parser.add_argument(
            "-H",
            "--host",
            dest="host",
            default=default_dict["host"],
            help=f"Web server port. Default: {default_dict['host']}.",
        )
        parser.add_argument(
            "-p",
            "--port",
            dest="port",
            type=int,
            default=default_dict["port"],
            help=f"Web server port. Default: {default_dict['port']}.",
        )
        parser.add_argument(
            "-c",
            "--config-file",
            dest="config_file",
            default=ServerConfig.DEFAULT_CONFIG_FILE,
            help=f"Configuration file. Default: {ServerConfig.DEFAULT_CONFIG_FILE}.",
        )

        args = parser.parse_args()
        main(args)
    except SystemExit as e:
        if e.code:
            print(f"Run error!")
        sys.exit(e.code)
