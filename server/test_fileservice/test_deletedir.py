"""Tests for server.FileService.delete_dir() function.

Imports:
    os
    pytest
    server.FileService.delete_dir()
"""

import os

import pytest

from ..FileService import delete_dir


class TestDeleteDir:
    """Test delete_dir function."""



    def test_delete_existing_good_dir_with_a_child_with_recursion(self, tmp_path, good_dir):
        """Delete an existing directory with a child directory recursively."""
        target_dir = os.path.join(str(tmp_path), good_dir)
        os.makedirs(target_dir, exist_ok=True)
        os.chdir(target_dir)
        os.mkdir("child_folder")
        delete_dir(target_dir, recursive=True)
        assert not os.path.exists(target_dir)

    def test_delete_existing_good_dir_with_a_child_no_recursion(self, tmp_path, good_dir):
        """Delete an existing directory with a child directory non recursively."""
        target_dir = os.path.join(str(tmp_path), good_dir)
        child_dir = os.path.join(str(tmp_path), good_dir, "child_folder")
        os.makedirs(child_dir, exist_ok=True)
        with pytest.raises(RuntimeError):
            delete_dir(target_dir, recursive=False)

    def test_delete_nonexisting_dir(self, tmp_path, good_dir):
        """Raise RuntimeError if directory does not exist."""
        target_dir = os.path.join(str(tmp_path), good_dir)
        with pytest.raises(FileNotFoundError):
            delete_dir(target_dir)

    def test_delete_invalid_dir(self, os_system, bad_dir_win, bad_dir_lnx):
        """Raise ValueError if path is invalid."""
        with pytest.raises(ValueError):
            if os_system == "Windows":
                delete_dir(bad_dir_win)
            elif os_system == "Linux":
                delete_dir(bad_dir_lnx)
            else:
                raise NotImplementedError
