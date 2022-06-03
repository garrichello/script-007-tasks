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

from server import FileService

DEFAULT_LOG_FILE = "server.log"
STANDARD_LOG_LEVELS = list(logging._nameToLevel.keys())
DEFAULT_LOG_LEVEL = "INFO"
LOG_CONFIG_FILE = "log_conf.yaml"

def set_logger(logfile: str, loglevel: str):
    """Set logger parameters

    Args:
        logfile: log filename
        loglevel: logging level`
    """

    # Let's create a directory for logs
    log_dir = os.path.dirname(logfile)
    if not os.path.exists(log_dir) and FileService.is_pathname_valid(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    with open(LOG_CONFIG_FILE, "r") as f:
        conf_dict = yaml.load(f, Loader=yaml.Loader)

    conf_dict["handlers"]["file"]["filename"] = logfile
    conf_dict["handlers"]["file"]["level"] = loglevel
    conf_dict["handlers"]["console"]["level"] = loglevel
    conf_dict["root"]["level"] = loglevel

    if args.logfile == "-":
        conf_dict["root"]["handlers"] = ["console"]

    logging.config.dictConfig(conf_dict)


#!/usr/bin/env python3
def main(args: argparse.Namespace):
    """Main function."""

    set_logger(args.logfile, args.loglevel)

    logging.info("Server started")

    # Set data directory
    try:
        FileService.change_dir(args.datadir, autocreate=True)
    except ValueError:
        logging.error(f"Bad data directory: {args.datadir}")
    finally:
        logging.info("Server stopped")


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-d", "--data-directory", dest="datadir", required=True, help="Data directory (reqired).")
        parser.add_argument(
            "-l",
            "--log-file",
            dest="logfile",
            default=DEFAULT_LOG_FILE,
            help="Log filename. Default: {DEFAULT_LOG_FILE}.",
        )
        parser.add_argument(
            "-L",
            "--log-level",
            dest="loglevel",
            choices=STANDARD_LOG_LEVELS,
            default=DEFAULT_LOG_LEVEL,
            help="Log level. Default: INFO.",
        )

        args = parser.parse_args()
        main(args)
    except SystemExit as e:
        if e.code:
            print(f"Run error!")
        sys.exit(e.code)
