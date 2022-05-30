"""Tests for server.FileService.change_dir() function.

Imports:
    server.FileService.change_dir()

"""
import os

import pytest

from server.FileService import change_dir


class TestChangeDir:
    """Test change_dir function."""

    @pytest.fixture(params=["aNewDir", os.path.join("complex", "dir")])
    def good_dir(self, request):
        """Return a good name of a directory."""
        return request.param

    @pytest.fixture(params=["///:this_is_a_bad_dir:///", "another*bad*dir"])
    def bad_dir(self, request):
        """Return a bad name of a directory."""
        return request.param

    def test_change_to_existing_dir(self, tmp_path):
        """Test if change_dir can change to an existing directory."""
        target_dir = str(tmp_path)
        change_dir(target_dir)
        assert os.getcwd() == target_dir

    def test_change_to_nonexisting_dir_with_autocreate(self, tmp_path, good_dir):
        """Test if change_dir can autocreate a nonexistent directory and change to it."""
        target_dir = os.path.join(str(tmp_path), good_dir)
        change_dir(target_dir, autocreate=True)
        assert os.getcwd() == target_dir

    @pytest.mark.xfail(raises=RuntimeError)
    def test_change_to_nonexisting_dir_no_autocreate(self, tmp_path, good_dir):
        """Test if change_dir fails changing to a nonexistent directory."""
        target_dir = os.path.join(str(tmp_path), good_dir)
        change_dir(target_dir, autocreate=False)

    @pytest.mark.xfail(raises=ValueError)
    def test_change_to_invalid_dir(self, tmp_path, bad_dir):
        """Test if change_dir fails changing to an invalid directory."""
        target_dir = os.path.join(str(tmp_path), bad_dir)
        change_dir(target_dir, autocreate=True)
