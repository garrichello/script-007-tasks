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

from aiohttp import web

from auth import BasicAuthMiddleware
from config import ServerConfig
from db import UserDB
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
    os.makedirs(server_config["data_directory"], exist_ok=True)
    os.chdir(server_config["data_directory"])

    # Database config
    db_user = server_config["db_user"]
    db_pw = server_config["db_pw"]
    db_host = server_config["db_host"]
    db_port = server_config["db_port"]
    db_name = server_config["db_name"]

    user_db = UserDB(db_user, db_pw, db_host, db_port, db_name)
    if args.init_db:
        user_db.init_db()
        return

    logging.info("Server started")

    auth_middleware = BasicAuthMiddleware(force=False)
    handler = WebHandler()
    app = web.Application(middlewares=[auth_middleware])
    app.add_routes(
        [
            web.get("/", handler.handle),
            web.get("/current_dir", handler.current_dir),
            web.post("/change_dir", handler.change_dir),
            web.post("/delete_dir", handler.delete_dir),

            web.get("/files", handler.get_files),
            web.get("/files/{filename}", handler.get_file_data),
            web.post("/files", handler.create_file),
            web.delete("/files/{filename}", handler.delete_file),

            web.post("/register", handler.register),
            web.post("/login", handler.login),
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
            #default=default_dict["host"],
            help=f"Web server port. Default: {default_dict['host']}.",
        )
        parser.add_argument(
            "-p",
            "--port",
            dest="port",
            type=int,
            #default=default_dict["port"],
            help=f"Web server port. Default: {default_dict['port']}.",
        )
        parser.add_argument(
            "-c",
            "--config-file",
            dest="config_file",
            default=ServerConfig.DEFAULT_CONFIG_FILE,
            help=f"Configuration file. Default: {ServerConfig.DEFAULT_CONFIG_FILE}.",
        )
        parser.add_argument(
            "--init-db",
            dest="init_db",
            action="store_true",
            help=f"Initialize DB.",
        )

        args = parser.parse_args()
        main(args)
    except SystemExit as e:
        if e.code:
            print(f"Run error!")
        sys.exit(e.code)
