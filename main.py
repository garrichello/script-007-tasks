"""Main module

Imports:
    argparse
    server.FileService
"""

import argparse

from server import FileService


#!/usr/bin/env python3
def main(args: argparse.Namespace):
    """Main function."""

    # Set data directory
    FileService.change_dir(args.data_directory, autocreate=True)


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-d", "--data-directory", required=True, help="Data directory")
        args = parser.parse_args()
        main(args)
    except SystemExit as e:
        print(f"Run error!")
