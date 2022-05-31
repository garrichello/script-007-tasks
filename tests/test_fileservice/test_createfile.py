"""Tests for server.FileService.create_file() function.

Imports:
    server.FileService.create_file()

"""

import pytest
import os

from server.FileService import create_file


class TestCreateFile:
    """Test create_file function."""

    def test_bad_file_name(self, bad_file_name):
        """Bad file name raises ValueError"""
        with pytest.raises(ValueError):
            _ = create_file(bad_file_name)


    def test_create_new_file(self, new_file_info, tmp_path, sample_data_1):
        """Test if get_files returns a list with metadata of a file."""
        target_filename = os.path.join(tmp_path, sample_data_1["name"])
        file_full_info = create_file(target_filename, sample_data_1["data"])
        assert file_full_info == new_file_info
        