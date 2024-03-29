"""Tests for server.FileService.change_dir() function.

Imports:
    os
    pytest
    server.FileService.change_dir()
"""

import os
import uuid

import pytest

from ..FileService import FileService


class TestChangeDir:
    """Test change_dir function."""

    def test_change_to_existing_dir(self, tmp_dir):
        """CWD to an existing directory."""
        FileService().change_dir(tmp_dir)
        assert os.getcwd() == tmp_dir

    def test_change_to_nonexisting_dir_with_autocreate(self, tmp_dir, good_dir):
        """Autocreate a nonexistent directory and CWD to it."""
        target_dir = os.path.join(str(tmp_dir), good_dir)
        FileService().change_dir(target_dir, autocreate=True)
        assert os.getcwd() == target_dir

    def test_change_to_nonexisting_dir_no_autocreate_2(self, good_dir):
        """Raise RuntimeError if directory does not exist and autocreate is False."""
        with pytest.raises(RuntimeError):
            FileService().change_dir(good_dir, autocreate=False)

    def test_change_to_invalid_dir(self, os_system, bad_dir_win, bad_dir_lnx):
        """Raise ValueError if path is invalid."""
        with pytest.raises(ValueError):
            if os_system == "Windows":
                FileService().change_dir(bad_dir_win, autocreate=True)
            elif os_system == "Linux":
                FileService().change_dir(bad_dir_lnx, autocreate=True)
            else:
                raise NotImplementedError
