import unittest
from DittoWebApi.src.utils.file_system.path_helpers import to_posix
from DittoWebApi.src.utils.file_system.path_helpers import dir_path_as_prefix


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

    def test_dir_path_as_prefix_returns_none_for_none(self):
        dir_path = None
        prefix = dir_path_as_prefix(dir_path)
        self.assertEqual(prefix, None)

    def test_dir_path_as_prefix_returns_none_for_empty_string(self):
        dir_path = ""
        prefix = dir_path_as_prefix(dir_path)
        self.assertEqual(prefix, None)

    def test_dir_path_as_prefix_returns_none_for_whitespace(self):
        dir_path = " "
        prefix = dir_path_as_prefix(dir_path)
        self.assertEqual(prefix, None)

    def test_dir_path_as_prefix_returns_posix_path_with_end_slash(self):
        dir_path = "testdir/testsubdir/"
        prefix = dir_path_as_prefix(dir_path)
        self.assertEqual(prefix, "testdir/testsubdir/")

    def test_dir_path_as_prefix_adds_end_slash_to_posix_path_without(self):
        dir_path = "testdir/testsubdir"
        prefix = dir_path_as_prefix(dir_path)
        self.assertEqual(prefix, "testdir/testsubdir/")

    def test_dir_path_as_prefix_converts_windows_path_with_end_slash(self):
        dir_path = "testdir\\testsubdir\\"
        prefix = dir_path_as_prefix(dir_path)
        self.assertEqual(prefix, "testdir/testsubdir/")

    def test_dir_path_as_prefix_adds_end_slash_to_windows_path_without(self):
        dir_path = "testdir\\testsubdir"
        prefix = dir_path_as_prefix(dir_path)
        self.assertEqual(prefix, "testdir/testsubdir/")
