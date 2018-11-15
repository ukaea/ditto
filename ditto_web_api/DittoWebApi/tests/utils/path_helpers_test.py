import unittest
from DittoWebApi.src.utils.file_system.path_helpers import to_posix


class TestPathHelpers(unittest.TestCase):
    def test_windows_path_converted_to_posix(self):
        path = r'c\test\subdir\file.txt'
        self.assertEqual(to_posix(path), r"c/test/subdir/file.txt")

    def test_mixed_path_converted_to_posix(self):
        path = r"c/test\subdir/file.txt"
        self.assertEqual(to_posix(path), r"c/test/subdir/file.txt")

    def test_posix_path_remain_posix(self):
        path = r"c/test/subdir/file.txt"
        self.assertEqual(to_posix(path), r"c/test/subdir/file.txt")

    def test_windows_directory_converts_to_posix_final_slash_removed(self):
        path = r"C:\\test\\subdir\\"
        self.assertEqual(to_posix(path), r"C:/test/subdir")

    def test_posix_directory_remain_posix_final_slash_removed(self):
        path = r"C:/test/subdir/"
        self.assertEqual(to_posix(path), r"C:/test/subdir")

    def test_blank_string_remains_empty(self):
        path = r" "
        self.assertEqual(to_posix(path), r" ")

    def test_empty_string_returns_dot(self):
        path = r""
        self.assertEqual(to_posix(path), r".")
