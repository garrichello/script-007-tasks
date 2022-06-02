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

    def test_bad_file_name(self, os_system, bad_file_name_win, bad_file_name_lnx):
        """Bad file name raises ValueError"""
        with pytest.raises(ValueError):
            if os_system == "Windows":
                _ = create_file(bad_file_name_win, b"")
            elif os_system == "Linux":
                _ = create_file(bad_file_name_lnx, b"")
            else:
                raise NotImplementedError

    def test_create_new_binary_file(self, new_binary_file_info, tmp_path, sample_binary_data_1):
        """Test if get_files returns a list with metadata of a file."""
        target_filename = os.path.join(tmp_path, sample_binary_data_1["name"])
        file_full_info = create_file(target_filename, sample_binary_data_1["data"])
        assert file_full_info == new_binary_file_info
