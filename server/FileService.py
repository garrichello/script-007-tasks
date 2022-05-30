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
import glob
import os


def change_dir(path: str, autocreate: bool = True) -> None:
    """Change current directory of app.

    Args:
        path (str): Path to working directory with files.
        autocreate (bool): Create folder if it doesn't exist.

    Raises:
        RuntimeError: if directory does not exist and autocreate is False.
        ValueError: if path is invalid.
    """

    try:
        os.makedirs(path, exist_ok=autocreate)
    except (OSError, FileNotFoundError):
        raise ValueError

    os.chdir(path)


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
    for file_name in glob.glob(cur_dir):
        file_meta = get_file_metadata(file_name)
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

    result = dict()

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

    result = dict()

    return result


def delete_file(filename: str) -> None:
    """Delete file.

    Args:
        filename (str): filename

    Raises:
        RuntimeError: if file does not exist.
        ValueError: if filename is invalid.
    """

    pass
