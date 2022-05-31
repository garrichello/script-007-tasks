"""Common fixtures for FileService functions testing

Imports:
    copy
    datetime
    os
    pytest
"""

import copy
from datetime import datetime
import os

import pytest

@pytest.fixture(autouse=True)
def chdir_to_tmp_path(tmp_path):
    os.chdir(str(tmp_path))

@pytest.fixture
def sample_data_1():
    """Sample data for a file."""

    return dict(name="letters.txt", data="abcdefghijklmnopqrstuvwxyz")


@pytest.fixture
def sample_data_2():
    """Sample data for another file."""

    return [dict(name="letters.txt", data="abcdefghijklmnopqrstuvwxyz"), dict(name="digits.txt", data="1234567890")]


@pytest.fixture
def sample_binary_data_1():
    """Sample binary content for a file."""

    return dict(name="binary.bin", data=b"abcdefghijklmnopqrstuvwxyz")


@pytest.fixture(params=["", "*bad*file*name*", os.path.join("..", "file")])
def bad_file_name(request):
    """Return a bad name of a file."""
    return request.param


def get_file_info(file_name: str):
    return dict(
        name=file_name,
        create_date=datetime.fromtimestamp(os.path.getctime(file_name)),
        edit_date=datetime.fromtimestamp(os.path.getmtime(file_name)),
        size=os.path.getsize(file_name),
    )


@pytest.fixture
def sample_file_meta(tmp_path, sample_data_1):
    """Metadata for a file."""

    # Create a file and get its info.
    test_file_name = os.path.join(tmp_path, sample_data_1["name"])
    with open(test_file_name, "w") as file:
        file.write(sample_data_1["data"])

    # Return the info dict in a list.
    return [get_file_info(test_file_name)]

@pytest.fixture
def sample_binary_file_meta(tmp_path, sample_binary_data_1):
    """Metadata for a binary file."""

    # Create a file and get its info.
    test_file_name = os.path.join(tmp_path, sample_binary_data_1["name"])
    with open(test_file_name, "wb") as file:
        file.write(sample_binary_data_1["data"])

    # Return the info dict in a list.
    return [get_file_info(test_file_name)]


@pytest.fixture
def two_sample_files_meta(tmp_path, sample_data_2):
    """Metadata for two files."""

    result = []

    for sample_data in sample_data_2:
        test_file_name = os.path.join(tmp_path, sample_data["name"])
        with open(test_file_name, "w") as file:
            file.write(sample_data["data"])
        file_meta = get_file_info(test_file_name)
        result.append(file_meta)

    # Return a list of both info dicts.
    return result


@pytest.fixture
def sample_file_full_info(sample_file_meta, sample_data_1):
    """Return full info and contents of a sample file."""

    result = copy.copy(sample_file_meta[0])
    result["content"] = sample_data_1["data"]
    return result


@pytest.fixture
def new_file_info(sample_file_meta, sample_data_1):
    """Return full info and contents of a new file."""

    result = copy.copy(sample_file_meta[0])
    result["content"] = sample_data_1["data"]
    del result["edit_date"]
    return result

@pytest.fixture
def new_binary_file_info(sample_binary_file_meta, sample_binary_data_1):
    """Return full info and contents of a new binary file."""

    result = copy.copy(sample_binary_file_meta[0])
    result["content"] = sample_binary_data_1["data"]  # type: ignore
    del result["edit_date"]
    return result
