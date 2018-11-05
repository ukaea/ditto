import unittest
import os
import pytest
import mock
import shutil
from DittoWebApi.src.services.internal_data_service import InternalDataService


class TestInternalDataServices(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup(self):
        current_dir = os.getcwd()
        new_dir = os.path.join(current_dir, 'temp_test_dir')
        os.mkdir(new_dir)
        yield
        shutil.rmtree(new_dir)

    def test_files_are_found_in_directories(self):
        current_dir = os.getcwd()
        new_dir = os.path.join(current_dir, 'temp_test_dir')
        with open(os.path.join(new_dir, "temp_test_file.txt"), 'w+') as f1:
            f1.write("Testing,Testing,1,2,3!!!")
        with open(os.path.join(new_dir, "temp2.txt"), "w+") as f2:
            f2.write("safdgvafdjvhjsdvksdvhjsdvkhxjchsdkjfhksadvksdncncjafdsdnkcjxankjcjsacxbnacbdsdajddafjklfjksadl")
        os.mkdir(os.path.join(new_dir, "sub_dir"))
        with open(os.path.join(new_dir, "sub_dir", "sub_file.txt"), "w+") as f3:
            f3.write("sffavbabhdb")
        mock_configuration = mock.Mock()
        mock_configuration.root_dir = os.path.join(os.getcwd(), 'temp_test_dir')
        internal_data_services = InternalDataService(mock_configuration)
        files = internal_data_services.find_files()
        assert files[1].file_name == "temp_test_file.txt"
        assert files[0].file_name == "temp2.txt"
        assert files[2].file_name == "sub_file.txt"

