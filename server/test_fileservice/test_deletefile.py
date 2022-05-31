"""Tests for server.FileService.delete_file() function.

Imports:
    os
    pytest
    server.FileService.delete_file()
"""

import os

import pytest

from ..FileService import delete_file


class TestDeleteFile:
    """Test delete_file function."""

    def test_bad_file_name(self, bad_file_name):
        """Bad file name raises ValueError"""
        with pytest.raises(ValueError):
            _ = delete_file(bad_file_name)

    def test_file_not_exists(self):
        """Test file does not exists raises RuntimeError"""
        with pytest.raises(RuntimeError):
            _ = delete_file("non_existing_file")

    def test_delete_file(self, new_file_info, tmp_path):
        """Test if get_files returns a list with metadata of a file."""
        target_filename = os.path.join(tmp_path, "delete_me")

        with open(target_filename, "w") as f:
            f.write("delete me!")

        delete_file(target_filename)
        assert not os.path.exists(target_filename)
