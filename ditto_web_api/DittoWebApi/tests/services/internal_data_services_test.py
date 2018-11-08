import unittest
import mock
import pytest
from DittoWebApi.src.services.internal_data_service import InternalDataService
from DittoWebApi.src.utils.file_system.files_system_helpers import FileSystemHelpers


class TestInternalDataServices(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_file_system_helper = mock.create_autospec(FileSystemHelpers)
        mock_configuration = mock.Mock()
        mock_configuration.root_dir = "test_root_dir"
        self.mock_file_system_helper.join_paths.return_value = "test_root_dir/file_1"
        self.mock_file_system_helper.find_all_files_in_folder.return_value = ["test_root_dir/file_1.txt",
                                                                              "test_root_dir/file_2.txt"]
        self.internal_data_services = InternalDataService(mock_configuration, self.mock_file_system_helper)

    def test_files_are_found_in_directories(self):
        # Act
        file_information = self.internal_data_services.find_files("test_root_dir")
        # Assert
        self.mock_file_system_helper.find_all_files_in_folder.assert_called_with("test_root_dir/file_1")
        assert file_information[0].file_name == "file_1.txt"
        assert file_information[1].file_name == "file_2.txt"

        assert file_information[0].rel_path == "file_1.txt"
        assert file_information[1].rel_path == "file_2.txt"

    def test_files_are_found_in_root_directory(self):
        # Act
        file_information = self.internal_data_services.find_files(None)
        # Assert
        self.mock_file_system_helper.find_all_files_in_folder.assert_called_with("test_root_dir")
        assert file_information[0].file_name == "file_1.txt"
        assert file_information[1].file_name == "file_2.txt"

        assert file_information[0].rel_path == "file_1.txt"
        assert file_information[1].rel_path == "file_2.txt"
