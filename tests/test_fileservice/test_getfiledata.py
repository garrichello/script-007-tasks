"""Tests for server.FileService.get_file_data() function.

Imports:
    os
    pytest
    server.FileService.get_file_data()
"""

import os

import pytest

from server.FileService import get_file_data


class TestGetFileData:
    """Test get_file_data function."""

    def test_bad_file_name(self, bad_file_name):
        """Test bad name raises ValueError"""
        with pytest.raises(ValueError):
            _ = get_file_data(bad_file_name)

    def test_file_not_exists(self):
        """Test file does not exists raises RuntimeError"""
        with pytest.raises(RuntimeError):
            _ = get_file_data("non_existing_file")

    def test_get_one_file_meta(self, sample_file_full_info, tmp_path, sample_data_1):
        """Test if get_files returns a list with metadata of a file."""
        target_filename = os.path.join(tmp_path, sample_data_1["name"])
        file_full_info = get_file_data(target_filename)
        assert file_full_info == sample_file_full_info
