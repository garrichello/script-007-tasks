"""Common fixtures for FileService functions testing

Imports:
    copy
    datetime
    os
    pytest
    random
"""

import base64
import copy
import os
import platform
import random
import time
import uuid
from datetime import datetime

import pytest

from config import ServerConfig

MIN_TEST_FILE_LEN = 16
MAX_TEST_FILE_LEN = 1024


@pytest.fixture
def os_system():
    return platform.system()


@pytest.fixture()
def tmp_dir():
    datadir = ServerConfig().config["data_directory"]
    data_tmp_dir = os.path.join(datadir, str(uuid.uuid4()))
    os.makedirs(data_tmp_dir, exist_ok=True)
    return data_tmp_dir

@pytest.fixture(autouse=True)
def chdir_to_tmp_path(tmp_path):
    os.chdir(str(tmp_path))
    ServerConfig().config['data_directory'] = tmp_path


@pytest.fixture
def test_file_len():
    return random.randint(MIN_TEST_FILE_LEN, MAX_TEST_FILE_LEN)


@pytest.fixture(params=["aNewDir", os.path.join("complex", "dir")])
def good_dir(request):
    """Return a good name of a directory."""
    return request.param


@pytest.fixture(params=[":a", "///:*this_is_a_bad_dir*:///", "another*bad*dir", ".." + os.path.sep])
def bad_dir_win(request):
    """Return a bad name of a directory."""
    return request.param


@pytest.fixture(params=["\0", "a" * 300])
def bad_dir_lnx(request):
    """Return a bad name of a directory."""
    return request.param


@pytest.fixture
def sample_binary_data_1(test_file_len):
    """Sample binary content for a file."""
    filename = str(uuid.uuid4()) + ".bin"
    return dict(name=filename, data=random.randbytes(test_file_len))


@pytest.fixture
def sample_binary_data_2(test_file_len):
    """Sample data for another file."""
    filename1 = str(uuid.uuid4()) + ".bin"
    filename2 = str(uuid.uuid4()) + ".bin"
    return [
        dict(name=filename1, data=random.randbytes(test_file_len)),
        dict(name=filename2, data=random.randbytes(test_file_len)),
    ]


@pytest.fixture(params=["", "*bad*file*name*", os.path.join("..", "file")])
def bad_file_name_win(request):
    """Return a bad name of a file."""
    return request.param


@pytest.fixture(params=["\0", "a" * 300])
def bad_file_name_lnx(request):
    """Return a bad name of a file."""
    return request.param

def set_file_info(filename: str, filesize: int) -> dict:
    """Set modification time of a file to a random value. Returns file information.

    Args:
        filename (str): Filename
        filesize (int): File size (in bytes)

    Returns:
        File information as a dictionary with keys:
        - name (str): Filename
        - create_date (datetime): File xreate date and time
        - edit_date (datetime): File modification date and time (randomly generated)
        - size (int): File length in bytes
    """
    m_time = int(random.random() * time.time())
    os.utime(filename, (m_time, m_time))

    rel_filename = filename.replace(str(ServerConfig().config["data_directory"]), ".")
    info = dict(
        name=rel_filename,
        create_date=datetime.fromtimestamp(os.path.getctime(filename)),
        edit_date=datetime.fromtimestamp(m_time),
        size=filesize,
    )
    return info


@pytest.fixture
def sample_binary_file_meta(tmp_dir, sample_binary_data_1, test_file_len):
    """Metadata for a binary file."""

    # Create a file and get its info.
    test_file_name = os.path.join(tmp_dir, sample_binary_data_1["name"])
    with open(test_file_name, "wb") as file:
        file.write(sample_binary_data_1["data"])

    file_info = set_file_info(test_file_name, test_file_len)

    # Return the info dict in a list.
    return [file_info]


@pytest.fixture
def two_sample_binary_files_meta(tmp_path, sample_binary_data_2, test_file_len):
    """Metadata for two binary files."""

    result = []

    for sample_data in sample_binary_data_2:
        test_file_name = os.path.join(tmp_path, sample_data["name"])
        with open(test_file_name, "wb") as file:
            file.write(sample_data["data"])
        file_info = set_file_info(test_file_name, test_file_len)
        result.append(file_info)

    # Return a list of both info dicts.
    return result


@pytest.fixture
def sample_binary_file_full_info(sample_binary_file_meta, sample_binary_data_1):
    """Return full info and contents of a sample binary file."""

    result = copy.copy(sample_binary_file_meta[0])
    result["content"] = sample_binary_data_1["data"]
    return result


@pytest.fixture
def new_binary_file_info(sample_binary_file_meta):
    """Return full info and contents of a new binary file."""

    result = copy.copy(sample_binary_file_meta[0])
    # result["content"] = sample_binary_data_1["data"]  # type: ignore
    del result["edit_date"]
    return result
