"""Common fixtures for FileService functions testing

Imports:
    datetime
    os
    pytest
"""

import copy
from datetime import datetime
import os

import pytest


@pytest.fixture
def sample_data_1():
    """Sample data for a file."""

    return dict(name="letters.txt", data="abcdefghijklmnopqrstuvwxyz")


@pytest.fixture
def sample_data_2():
    """Sample data for another file."""

    return dict(name="digits.txt", data="1234567890")


@pytest.fixture
def sample_file_meta(tmp_path, sample_data_1):
    """Metadata for a file."""

    os.chdir(str(tmp_path))

    # Create a file and get its info.
    test_file_name = os.path.join(tmp_path, sample_data_1["name"])
    with open(test_file_name, "w") as file:
        file.write(sample_data_1["data"])

    # Return the info dict in a list.
    return [
        dict(
            name=test_file_name,
            create_date=datetime.fromtimestamp(os.path.getctime(test_file_name)),
            edit_date=datetime.fromtimestamp(os.path.getmtime(test_file_name)),
            size=os.path.getsize(test_file_name),
        )
    ]


@pytest.fixture
def two_sample_files_meta(tmp_path, sample_data_1, sample_data_2):
    """Metadata for two files."""
    
    os.chdir(str(tmp_path))

    # Create the first file and get its info.
    test_file_name = os.path.join(tmp_path, sample_data_1["name"])
    with open(test_file_name, "w") as file:
        file.write(sample_data_1["data"])
    file1_meta = dict(
        name=test_file_name,
        create_date=datetime.fromtimestamp(os.path.getctime(test_file_name)),
        edit_date=datetime.fromtimestamp(os.path.getmtime(test_file_name)),
        size=os.path.getsize(test_file_name),
    )

    # Create the second file and get its info.
    test_file_name = os.path.join(tmp_path, sample_data_2["name"])
    with open(test_file_name, "w") as file:
        file.write(sample_data_2["data"])
    file2_meta = dict(
        name=test_file_name,
        create_date=datetime.fromtimestamp(os.path.getctime(test_file_name)),
        edit_date=datetime.fromtimestamp(os.path.getmtime(test_file_name)),
        size=os.path.getsize(test_file_name),
    )

    # Return a list of both info dicts.
    return [file1_meta, file2_meta]


@pytest.fixture
def sample_file_full_info(tmp_path, sample_file_meta, sample_data_1):
    """Full info of a file."""

    os.chdir(str(tmp_path))

    # Return full info and contents of a file.
    result = copy.copy(sample_file_meta[0])
    result["content"] = sample_data_1["data"]
    return [result]