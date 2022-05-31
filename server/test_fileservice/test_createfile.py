"""Tests for server.FileService.create_file() function.

Imports:
    os
    pytest
    server.FileService.create_file()
"""

import os

import pytest

from ..FileService import create_file


class TestCreateFile:
    """Test create_file function."""

    def test_bad_file_name(self, bad_file_name):
        """Bad file name raises ValueError"""
        with pytest.raises(ValueError):
            _ = create_file(bad_file_name, "")

    def test_create_new_file(self, new_file_info, tmp_path, sample_data_1):
        """Test if get_files returns a list with metadata of a file."""
        target_filename = os.path.join(tmp_path, sample_data_1["name"])
        file_full_info = create_file(target_filename, sample_data_1["data"])
        assert file_full_info == new_file_info

    def test_create_new_binary_file(self, new_binary_file_info, tmp_path, sample_binary_data_1):
        """Test if get_files returns a list with metadata of a file."""
        target_filename = os.path.join(tmp_path, sample_binary_data_1["name"])
        file_full_info = create_file(target_filename, sample_binary_data_1["data"])
        print(file_full_info)
        assert file_full_info == new_binary_file_info
