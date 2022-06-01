"""Tests for server.FileService.delete_file() function.

Imports:
    os
    pytest
    server.FileService.delete_file()
"""

import os
import uuid

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

    def test_delete_file(self, tmp_path):
        """Test if get_files returns a list with metadata of a file."""
        target_filename = os.path.join(tmp_path, str(uuid.uuid4()))

        with open(target_filename, "wb") as f:
            f.write(b"")

        delete_file(target_filename)
        assert not os.path.exists(target_filename)