"""Tests for server.FileService.change_dir() function.

Imports:
    os
    pytest
    server.FileService.change_dir()
"""

import os

import pytest

from ..FileService import change_dir


class TestChangeDir:
    """Test change_dir function."""

    @pytest.fixture(params=["aNewDir", os.path.join("complex", "dir")])
    def good_dir(self, request):
        """Return a good name of a directory."""
        return request.param

    @pytest.fixture(params=[":a", "///:*this_is_a_bad_dir*:///", "another*bad*dir", ".." + os.path.sep])
    def bad_dir_win(self, request):
        """Return a bad name of a directory."""
        return request.param

    @pytest.fixture(params=["\0", "a" * 300])
    def bad_dir_lnx(self, request):
        """Return a bad name of a directory."""
        return request.param

    def test_change_to_existing_dir(self, tmp_path):
        """CWD to an existing directory."""
        target_dir = str(tmp_path)
        change_dir(target_dir)
        assert os.getcwd() == target_dir

    def test_change_to_nonexisting_dir_with_autocreate(self, tmp_path, good_dir):
        """Autocreate a nonexistent directory and CWD to it."""
        target_dir = os.path.join(str(tmp_path), good_dir)
        change_dir(target_dir, autocreate=True)
        assert os.getcwd() == target_dir

    def test_change_to_nonexisting_dir_no_autocreate_2(self, good_dir):
        """Raise RuntimeError if directory does not exist and autocreate is False."""
        with pytest.raises(RuntimeError):
            change_dir(good_dir, autocreate=False)

    def test_change_to_invalid_dir(self, os_system, bad_dir_win, bad_dir_lnx):
        """Raise ValueError if path is invalid."""
        with pytest.raises(ValueError):
            if os_system == "Windows":
                change_dir(bad_dir_win, autocreate=True)
            elif os_system == "Linux":
                change_dir(bad_dir_lnx, autocreate=True)
            else:
                raise NotImplementedError
