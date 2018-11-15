import unittest
from DittoWebApi.src.utils.file_system.path_helpers import to_posix


class TestPathHelpers(unittest.TestCase):
    def test_windows_path_converted_to_unix(self):
        path = r'c\test\subdir\file.txt'
        self.assertEqual(to_posix(path), r"c/test/subdir/file.txt")

    def test_mixed_paths_converted_to_linux_paths(self):
        path = r"c/test/subdir/file.txt"
        self.assertEqual(to_posix(path), r"c/test/subdir/file.txt")

    def test_linux_paths_remain_linux_paths(self):
        path = r"c/test/subdir/file.txt"
        self.assertEqual(to_posix(path), r"c/test/subdir/file.txt")

    def test_blank_string_remains_empty(self):
        path = r" "
        self.assertEqual(to_posix(path), r" ")

    def test_empty_string_returns_dot(self):
        path = r""
        self.assertEqual(to_posix(path), r".")
