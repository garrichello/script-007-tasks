"""Files and directories manipulations.

Imports:
    glob
    os

Provides functions:
    change_dir()
    get_files()
    get_file_data()
    create_file()
    delete_file()
"""
from datetime import datetime
import errno
import glob
import os

# Windows-specific error code indicating an invalid pathname.
ERROR_INVALID_NAME = 123


def is_pathname_valid(pathname: str) -> bool:
    """
    Check if pathname is valid.

    Return:
        True - if the passed pathname is a valid pathname for the current OS;
        False - otherwise.

    Borrowed here: https://stackoverflow.com/questions/9532499/check-whether-a-path-is-valid-in-python-without-creating-a-file-at-the-paths-ta
    And slightly modified.
    """

    # If this pathname is either not a string or is but is empty, this pathname is invalid.
    try:
        if not isinstance(pathname, str) or ".." in pathname or not pathname.strip():
            return False

        # Strip this pathname's Windows-specific drive specifier (e.g., `C:\`) if any.
        _, pathname = os.path.splitdrive(pathname)

        # Directory guaranteed to exist.
        root_dirname = os.path.dirname(__file__)

        # Test whether each path component split from this pathname is valid or
        # not, ignoring non-existent and non-readable path components.
        for pathname_part in pathname.split(os.path.sep):
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


def get_file_metadata(filename: str):
    """Get file metadata.

    Args:
        filename (str): file name
    """
    file_meta = dict(
        name=filename,
        create_date=datetime.fromtimestamp(os.path.getctime(filename)),
        edit_date=datetime.fromtimestamp(os.path.getmtime(filename)),
        size=os.path.getsize(filename),
    )
    return file_meta


def change_dir(path: str, autocreate: bool = True) -> None:
    """Change current directory of app.

    Args:
        path (str): Path to working directory with files.
        autocreate (bool): Create folder if it doesn't exist.

    Raises:
        RuntimeError: if directory does not exist and autocreate is False.
        ValueError: if path is invalid.
    """

    if not is_pathname_valid(path):
        raise ValueError(f"Bad path: {path}")
    if not os.path.exists(path) and not autocreate:
        raise RuntimeError(f"Path does not exist: {path}")

    os.makedirs(path, exist_ok=autocreate)
    os.chdir(path)


def get_files() -> list:
    """Get info about all files in working directory.

    Returns:
        List of dicts, which contains info about each file. Keys:
        - name (str): filename
        - create_date (datetime): date of file creation.
        - edit_date (datetime): date of last file modification.
        - size (int): size of file in bytes.
    """

    result = list()
    cur_dir = os.path.join(os.getcwd(), "*")
    for filename in glob.glob(cur_dir):
        file_meta = get_file_metadata(filename)
        result.append(file_meta)
    return result


def get_file_data(filename: str) -> dict:
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

    if not is_pathname_valid(filename):
        raise ValueError(f"Bad filename: {filename}")
    if not os.path.exists(filename):
        raise RuntimeError(f"File does not exist: {filename}")

    result = dict()

    result = get_file_metadata(filename)
    with open(filename, "r") as f:
        content = f.read()
    result["content"] = content

    return result


def create_file(filename: str, content: str = "") -> dict:
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

    if not is_pathname_valid(filename):
        raise ValueError(f"Bad filename: {filename}")
        
    with open(filename, "w") as f:
        f.write(content)

    file_meta = get_file_metadata(filename)
    file_meta["content"] = content
    del file_meta["edit_date"]

    return file_meta


def delete_file(filename: str) -> None:
    """Delete file.

    Args:
        filename (str): filename

    Raises:
        RuntimeError: if file does not exist.
        ValueError: if filename is invalid.
    """

    pass
