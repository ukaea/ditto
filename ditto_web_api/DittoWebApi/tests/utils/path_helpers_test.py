# pylint: disable=R0201
import pytest

from DittoWebApi.src.utils.file_system.path_helpers import to_posix
from DittoWebApi.src.utils.file_system.path_helpers import dir_path_as_prefix
from DittoWebApi.src.utils.file_system.path_helpers import is_sub_dir_of_root


class TestPathHelpers:
    def test_windows_path_converted_to_posix(self):
        path = r'c\test\subdir\file.txt'
        assert to_posix(path) == r"c/test/subdir/file.txt"

    def test_mixed_path_converted_to_posix(self):
        path = r"c/test\subdir/file.txt"
        assert to_posix(path) == r"c/test/subdir/file.txt"

    def test_posix_path_remain_posix(self):
        path = r"c/test/subdir/file.txt"
        assert to_posix(path) == r"c/test/subdir/file.txt"

    def test_windows_directory_converts_to_posix_final_slash_removed(self):
        path = r"C:\\test\\subdir\\"
        assert to_posix(path) == r"C:/test/subdir"

    def test_posix_directory_remain_posix_final_slash_removed(self):
        path = r"C:/test/subdir/"
        assert to_posix(path) == r"C:/test/subdir"

    def test_blank_string_remains_empty(self):
        path = r" "
        assert to_posix(path) == r" "

    def test_empty_string_returns_dot(self):
        path = r""
        assert to_posix(path) == r"."

    def test_dir_path_as_prefix_returns_none_for_none(self):
        dir_path = None
        prefix = dir_path_as_prefix(dir_path)
        assert prefix is None

    def test_dir_path_as_prefix_returns_none_for_empty_string(self):
        dir_path = ""
        prefix = dir_path_as_prefix(dir_path)
        assert prefix is None

    def test_dir_path_as_prefix_returns_none_for_whitespace(self):
        dir_path = " "
        prefix = dir_path_as_prefix(dir_path)
        assert prefix is None

    def test_dir_path_as_prefix_returns_posix_path_with_end_slash(self):
        dir_path = "testdir/testsubdir/"
        prefix = dir_path_as_prefix(dir_path)
        assert prefix == "testdir/testsubdir/"

    def test_dir_path_as_prefix_adds_end_slash_to_posix_path_without(self):
        dir_path = "testdir/testsubdir"
        prefix = dir_path_as_prefix(dir_path)
        assert prefix == "testdir/testsubdir/"

    def test_dir_path_as_prefix_converts_windows_path_with_end_slash(self):
        dir_path = "testdir\\testsubdir\\"
        prefix = dir_path_as_prefix(dir_path)
        assert prefix == "testdir/testsubdir/"

    def test_dir_path_as_prefix_adds_end_slash_to_windows_path_without(self):
        dir_path = "testdir\\testsubdir"
        prefix = dir_path_as_prefix(dir_path)
        assert prefix == "testdir/testsubdir/"

    @pytest.mark.parametrize('path', ['path/to/root/file',
                                      'path/to/root/',
                                      'path/to/root/dir/sub_dir/file'])
    def test_check_if_sub_dir_of_root_returns_true_when_path_is_in_root(self, path):
        root = "path/to/root/"
        assert is_sub_dir_of_root(path, root) is True

    @pytest.mark.parametrize('path', ['path/root/file',
                                      'path/to/file',
                                      'to/root/file',
                                      'path/to/newroot/',
                                      'path/to/root'])  # Note should always be called with canonical paths
    def test_check_if_sub_dir_of_root_returns_false_when_path_is_not_in_root(self, path):
        root = "path/to/root/"
        assert is_sub_dir_of_root(path, root) is False
