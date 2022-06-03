"""Tests for server.FileService.get_file_data() function.

Imports:
    os
    pytest
    server.FileService.get_file_data()
"""

import os

import pytest

from ..FileService import FileService


class TestGetFileData:
    """Test get_file_data function."""

    def test_bad_file_name(self, os_system, bad_file_name_win, bad_file_name_lnx):
        """Test bad name raises ValueError"""
        with pytest.raises(ValueError):
            if os_system == "Windows":
                _ = FileService().get_file_data(bad_file_name_win)
            elif os_system == "Linux":
                _ = FileService().get_file_data(bad_file_name_lnx)
            else:
                raise NotImplementedError

    def test_file_not_exists(self):
        """Test file does not exists raises RuntimeError"""
        with pytest.raises(RuntimeError):
            _ = FileService().get_file_data("non_existing_file")

    def test_get_one_file_meta(self, sample_binary_file_full_info, tmp_path, sample_binary_data_1):
        """Test if get_files returns a list with metadata of a file."""
        target_filename = os.path.join(tmp_path, sample_binary_data_1["name"])
        file_full_info = FileService().get_file_data(target_filename)
        assert file_full_info == sample_binary_file_full_info
