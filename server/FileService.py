"""Files and directories manipulations.

Imports:
    datetime
    glob
    errno
    os

Provides functions:
    change_dir()
    get_files()
    get_file_data()
    create_file()
    delete_file()
"""

import errno
import glob
import logging
import logging.config
import os
import shutil
from datetime import datetime

from config import ServerConfig


class FileService:
    """File service class"""

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._config = ServerConfig().config

    @staticmethod
    def is_pathname_valid(pathname: str) -> bool:
        """
        Check if pathname is valid.

        Return:
            True - if the passed pathname is a valid pathname for the current OS;
            False - otherwise.

        Borrowed here: https://stackoverflow.com/questions/9532499/check-whether-a-path-is-valid-in-python-without-creating-a-file-at-the-paths-ta
        And slightly modified.
        """
        # Windows-specific error code indicating an invalid pathname.
        ERROR_INVALID_NAME = 123

        # If this pathname is either not a string or is but is empty, this pathname is invalid.
        try:
            if not isinstance(pathname, str) or not pathname.strip():
                return False

            # Strip this pathname's Windows-specific drive specifier (e.g., `C:\`) if any.
            _, pathname = os.path.splitdrive(pathname)

            # Directory guaranteed to exist.
            root_dirname = os.path.dirname(__file__)

            # Test whether each path component split from this pathname is valid or
            # not, ignoring non-existent and non-readable path components.
            for pathname_part in pathname.split(os.path.sep):
                if pathname_part == ".." or ":" in pathname_part:
                    return False
                try:
                    os.lstat(root_dirname + pathname_part)
                # If an OS-specific exception is raised, its error code
                # indicates whether this pathname is valid or not. Unless this
                # is the case, this exception implies an ignorable kernel or
                # filesystem complaint (e.g., path not found or inaccessible).
                #
                # Only the following exceptions indicate invalid pathnames:
                #
                # * Instances of the Windows-specific "WindowsError" class
                #   defining the "winerror" attribute whose value is
                #   "ERROR_INVALID_NAME". Under Windows, "winerror" is more
                #   fine-grained and hence useful than the generic "errno"
                #   attribute. When a too-long pathname is passed, for example,
                #   "errno" is "ENOENT" (i.e., no such file or directory) rather
                #   than "ENAMETOOLONG" (i.e., file name too long).
                # * Instances of the cross-platform "OSError" class defining the
                #   generic "errno" attribute whose value is either:
                #   * Under most POSIX-compatible OSes, "ENAMETOOLONG".
                #   * Under some edge-case OSes (e.g., SunOS, *BSD), "ERANGE".
                except OSError as exc:
                    if hasattr(exc, "winerror"):
                        if exc.winerror == ERROR_INVALID_NAME:
                            return False
                    elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                        return False
        # If a "TypeError" exception was raised, it almost certainly has the
        # error message "embedded NUL character" indicating an invalid pathname.
        except TypeError as exc:
            return False
        # If no exception was raised, all path components and hence this
        # pathname itself are valid.
        else:
            return True
        # If any other exception was raised, this is an unrelated fatal issue
        # (e.g., a bug). Permit this exception to unwind the call stack.

    def _make_path_relative(self, path: str) -> str:
        return path.replace(self._config["data_directory"], ".")
    
    def get_file_metadata(self, filename: str):
        """Get file metadata.

        Args:
            filename (str): file name
        """
        file_meta = dict(
            name=self._make_path_relative(filename),
            create_date=datetime.fromtimestamp(os.path.getctime(filename)),
            edit_date=datetime.fromtimestamp(os.path.getmtime(filename)),
            size=os.path.getsize(filename),
        )
        return file_meta

    def current_dir(self) -> str:
        """Get current directory of app.

        Returns:
            Current working directory of tha app
        """

        path = self._make_path_relative(os.getcwd())
        self._logger.debug(f"Current directory is {path}")

        return path

    def change_dir(self, path: str, autocreate: bool = True) -> str:
        """Change current directory of app.

        Args:
            path (str): Path to working directory with files.
            autocreate (bool): Create folder if it doesn't exist.

        Raises:
            RuntimeError: if directory does not exist and autocreate is False.
            ValueError: if path is invalid.
        """

        autocreate_mode = "with" if autocreate else "withOUT"
        self._logger.debug(f'Changing current directory to "{path}" {autocreate_mode} autocreate')

        if not self.is_pathname_valid(path):
            raise ValueError(f"Bad path: {path}")
        if not os.path.exists(path) and not autocreate:
            raise RuntimeError(f"Path does not exist: {path}")

        os.chdir(self._config["data_directory"])
        try:
            os.makedirs(path, exist_ok=autocreate)
        except NotADirectoryError:
            raise ValueError(f"Bad path: {path}")
        os.chdir(path)

        new_path = self._make_path_relative(os.getcwd())

        self._logger.debug(f"Done")

        return new_path

    def delete_dir(self, path: str, recursive: bool = True) -> None:
        """Delete specified directory.
        If path is a current directory, change current directory to its parent before deletion.

        Args:
            path (str): Path to a directory to delete.
            recursive (bool): if True delete all files and child directories recursively before deletion.

        Raises:
            FileNotFoundError: if directory does not exist.
            RuntimeError: if directory contains files and recursive is False.
            ValueError: if path is invalid.
        """

        self._logger.debug(f'Removing directory "{path}"')
        dir_to_delete = os.path.join(self._config["data_directory"], path)

        if not self.is_pathname_valid(dir_to_delete):
            raise ValueError(f"Bad path: {path}")
        if not os.path.exists(dir_to_delete):
            raise FileNotFoundError(f"Directory does not exist: {path}")
        if os.listdir(dir_to_delete) and not recursive:
            raise RuntimeError(f"Directory is not empty: {path}")

        os.chdir(self._config["data_directory"])
        if recursive:
            shutil.rmtree(path)
        else:
            os.rmdir(path)
        self._logger.debug(f"Done")

    def get_files(self) -> list:
        """Get info about all files in working directory.

        Returns:
            List of dicts, which contains info about each file. Keys:
            - name (str): filename
            - create_date (datetime): date of file creation.
            - edit_date (datetime): date of last file modification.
            - size (int): size of file in bytes.
        """

        self._logger.debug("Getting files list")

        result = list()
        cur_dir = os.path.join(os.getcwd(), "*")
        files = glob.glob(cur_dir)
        for filename in files:
            if os.path.isfile(filename):
                file_meta = self.get_file_metadata(filename)
                result.append(file_meta)

        self._logger.debug(f"{len(files)} files found")

        return result

    def get_file_data(self, filename: str) -> dict:
        """Get full info about file.

        Args:
            filename (str): Filename.

        Returns:
            Dict, which contains full info about file. Keys:
            - name (str): filename
            - content (str): file content
            - create_date (datetime): date of file creation
            - edit_date (datetime): date of last file modification
            - size (int): size of file in bytes

        Raises:
            RuntimeError: if file does not exist.
            ValueError: if filename is invalid.
        """

        self._logger.debug(f'Reading file "{filename}"')

        if not self.is_pathname_valid(filename):
            raise ValueError(f"Bad filename: {filename}")
        if not os.path.exists(filename):
            raise RuntimeError(f"File does not exist: {filename}")

        result = dict()

        result = self.get_file_metadata(filename)
        content = bytes()
        with open(filename, "rb") as f:
            content = f.read()
        result["content"] = content  # type: ignore

        self._logger.debug(f"{len(content)} bytes read")

        return result

    def create_file(self, filename: str, content: bytes) -> dict:
        """Create a new file.

        Args:
            filename (str): Filename.
            content (str): String with file content.

        Returns:
            Dict, which contains name of created file. Keys:
            - name (str): filename
            - content (str): file content
            - create_date (datetime): date of file creation
            - size (int): size of file in bytes

        Raises:
            ValueError: if filename is invalid.
        """

        self._logger.debug(f'Creating file "{filename}"')

        if not self.is_pathname_valid(filename):
            raise ValueError(f"Bad filename: {filename}")

        with open(filename, "wb") as f:
            f.write(content)

        file_meta = self.get_file_metadata(filename)
        del file_meta["edit_date"]

        self._logger.debug(f"{len(content)} bytes written")

        return file_meta

    def delete_file(self, filename: str) -> None:
        """Delete file.

        Args:
            filename (str): filename

        Raises:
            RuntimeError: if file does not exist.
            ValueError: if filename is invalid.
        """

        self._logger.debug(f"Deleting file {filename}")

        if not self.is_pathname_valid(filename):
            raise ValueError(f"Bad filename: {filename}")
        if not os.path.exists(filename):
            raise RuntimeError(f"File does not exist: {filename}")

        os.remove(filename)

        self._logger.debug("Done")
