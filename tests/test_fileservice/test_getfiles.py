"""Tests for server.FileService.get_files() function.

Imports:
    server.FileService.get_files()
"""

from server.FileService import get_files


class TestGetFiles:
    """Test get_files function."""

    def test_if_list_is_returned(self):
        """Test if get_files returns a list."""

        assert isinstance(get_files(), list)

    def test_get_one_file_meta(self, sample_file_meta):
        """Test if get_files returns a list with metadata of a file."""

        file_meta = get_files()
        assert file_meta == sample_file_meta

    def test_get_two_files_meta(self, two_sample_files_meta):
        """Test if get_files returns a list with metadata of two files."""

        two_files_meta = get_files()
        file_meta_is_present = list()

        # Since the order of info dicts in the list is unknown, check their presence in the loop.
        for file_meta in two_sample_files_meta:
            if file_meta in two_files_meta:
                file_meta_is_present.append(True)
            else:
                file_meta_is_present.append(False)
        assert all(file_meta_is_present)
