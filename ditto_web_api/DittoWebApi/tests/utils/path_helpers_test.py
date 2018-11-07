import unittest
from DittoWebApi.src.utils.path_helpers import to_posix
from pathlib import PureWindowsPath
from pathlib import PurePosixPath

class TestPathHelpers(unittest.TestCase):
    def test_windows_path_converted_to_unix(self):
        path = PureWindowsPath(r'c\test\subdir\file.txt')
        self.assertEqual(to_posix(path), r"c/test/subdir/file.txt")

    def test_linux_paths_remain_linux_paths(self):
        path = PurePosixPath(r"c/test/subdir/file.txt")
        self.assertEqual(to_posix(path), r"c/test/subdir/file.txt")

    def test_blank_string_remains_empty(self):
        path = r" "
        self.assertEqual(to_posix(path), r" ")

    def test_empty_string_returns_dot(self):
        path = r""
        self.assertEqual(to_posix(path), r".")
