"""Tests for server.FileService.get_files() function.

Imports:
    server.FileService.get_files()
"""

import os

from ..FileService import FileService


class TestGetFiles:
    """Test get_files function."""

    def test_if_list_is_returned(self):
        """Test if get_files returns a list."""

        assert isinstance(FileService().get_files(), list)

    def test_get_one_file_meta(self, tmp_dir, sample_binary_file_meta):
        """Test if get_files returns a list with metadata of a file."""

        os.chdir(tmp_dir)
        file_meta = FileService().get_files()
        assert file_meta == sample_binary_file_meta

    def test_get_two_files_meta(self, two_sample_binary_files_meta):
        """Test if get_files returns a list with metadata of two files."""

        two_files_meta = FileService().get_files()
        file_meta_is_present = list()

        # Since the order of info dicts in the list is unknown, check their presence in the loop.
        for file_meta in two_sample_binary_files_meta:
            file_meta_is_present.append(file_meta in two_files_meta)
        assert all(file_meta_is_present)
