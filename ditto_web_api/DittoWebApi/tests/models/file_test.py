import unittest
import os
import pytest
from DittoWebApi.src.models.file import File


class TestFiles(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup(self):
        os.mkdir('temp_test_dir')
        file = open(os.path.join("temp_test_dir", "temp_test_file.txt"), 'w+')
        file.write("Testing,Testing,1,2,3!!!")
        file.close()
        yield
        os.remove(os.path.join("temp_test_dir", "temp_test_file.txt"))
        os.removedirs('temp_test_dir')

    def test_file_is_read_and_processed_correctly(self):
        file = File(os.path.join("temp_test_dir", "temp_test_file.txt"), os.path.dirname(__file__))
        self.assertEqual(file.file_name, "temp_test_file.txt")
        self.assertEqual(file.rel_path, os.path.join("temp_test_dir", "temp_test_file.txt"))
        self.assertEqual(file.abs_path, os.path.join(os.path.dirname(__file__), os.path.join("temp_test_dir",
                                                                                             "temp_test_file.txt")))

    def test_error_returned_when_root_dir_not_in_file_path(self):
        with pytest.raises(NameError):
            File(os.path.join("temp_test_dir", "temp_test_file.txt"), "some_unknown_dir")
