# pylint: disable=W0201
import unittest
import mock
import pytest
from DittoWebApi.src.services.internal_data_service import InternalDataService
from DittoWebApi.src.utils.file_system.files_system_helpers import FileSystemHelper


class TestInternalDataServices(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_file_system_helper = mock.create_autospec(FileSystemHelper)
        mock_configuration = mock.Mock()
        mock_configuration.root_dir = "test_root_dir"
        self.mock_file_system_helper.join_paths.return_value = "test_root_dir/file_1"
        self.mock_file_system_helper.find_all_files_in_folder.return_value = ["test_root_dir/file_1.txt",
                                                                              "test_root_dir/file_2.txt"]
        self.mock_file_system_helper.relative_file_path.side_effect = ["file_1.txt",
                                                                       "file_2.txt"]
        self.mock_file_system_helper.absolute_file_path.side_effect = ["test_root_dir/file_1.txt",
                                                                       "test_root_dir/file_2.txt"]
        self.mock_file_system_helper.file_name.side_effect = ["file_1.txt",
                                                              "file_2.txt"]
        self.internal_data_services = InternalDataService(mock_configuration, self.mock_file_system_helper)

    def test_find_files_finds_files_in_a_directories(self):
        # Act
        file_information = self.internal_data_services.find_files("test_root_dir")
        # Assert
        self.mock_file_system_helper.find_all_files_in_folder.assert_called_with("test_root_dir/file_1")
        assert file_information[0].file_name == "file_1.txt"
        assert file_information[1].file_name == "file_2.txt"

        assert file_information[0].rel_path == "file_1.txt"
        assert file_information[1].rel_path == "file_2.txt"

        assert file_information[0].abs_path == "test_root_dir/file_1.txt"
        assert file_information[1].abs_path == "test_root_dir/file_2.txt"

    def test_find_files_finds_files_in_the_root_directory(self):
        # Act
        file_information = self.internal_data_services.find_files(None)
        # Assert
        self.mock_file_system_helper.find_all_files_in_folder.assert_called_with("test_root_dir")
        assert file_information[0].file_name == "file_1.txt"
        assert file_information[1].file_name == "file_2.txt"

        assert file_information[0].rel_path == "file_1.txt"
        assert file_information[1].rel_path == "file_2.txt"

        assert file_information[0].abs_path == "test_root_dir/file_1.txt"
        assert file_information[1].abs_path == "test_root_dir/file_2.txt"

    def test_file_builder_builds_a_file_information_object_with_correct_information(self):
        # Act
        file_information = self.internal_data_services.build_file_information("test_root_dir/file_1.txt")
        # Assert
        self.mock_file_system_helper.absolute_file_path.assert_called_with("test_root_dir/file_1.txt")
        self.mock_file_system_helper.relative_file_path.assert_called_with("test_root_dir/file_1.txt", "test_root_dir")
        self.mock_file_system_helper.file_name.assert_called_with("test_root_dir/file_1.txt")
        assert file_information.abs_path == "test_root_dir/file_1.txt"
        assert file_information.rel_path == "file_1.txt"
        assert file_information.file_name == "file_1.txt"
