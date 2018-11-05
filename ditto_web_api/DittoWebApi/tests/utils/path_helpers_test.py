from DittoWebApi.src.utils.path_helpers import to_posix
import unittest


class TestPathHelpers(unittest.TestCase):
    def test_windows_path_converted_to_unix(self):
        path = r"c\test\subdir\file.txt"
        assert to_posix(path) == r"c/test/subdir/file.txt"

    def test_linux_paths_remain_linux_paths(self):
        path = r"c/test/subdir/file.txt"
        assert to_posix(path) == r"c/test/subdir/file.txt"

    def test_blank_string_remains_empty(self):
        path = r" "
        assert to_posix(path) == r" "

    def test_empty_string_return(self):
        path = r""
        assert to_posix(path) == r"."
