# pylint: disable=W0201
import logging
import unittest
import mock
import pytest
from DittoWebApi.src.services.internal.internal_data_service import InternalDataService
from DittoWebApi.src.services.internal.archiver import Archiver
from DittoWebApi.src.utils.file_system.files_system_helpers import FileSystemHelper


class TestInternalDataServices(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_file_system_helper = mock.create_autospec(FileSystemHelper)
        mock_configuration = mock.Mock()
        self.mock_logger = mock.create_autospec(logging.RootLogger, spec_set=False)
        self.mock_archiver = mock.create_autospec(Archiver)
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
        self.internal_data_services = InternalDataService(mock_configuration,
                                                          self.mock_file_system_helper,
                                                          self.mock_archiver,
                                                          self.mock_logger)

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

    def test_logger_is_called_when_find_files_is_run(self):
        self.internal_data_services.find_files("test_root_dir/file_1")
        assert self.mock_logger.debug.call_count == 2
        self.mock_logger.debug.assert_any_call("Finding files in directory test_root_dir/file_1")
        self.mock_logger.debug.assert_any_call("Found 2 files, converting to file information objects")

    def test_create_archive_file_calls_archiver_with_given_content_when_archive_file_does_not_exist(self):
        # Arrange
        self.mock_file_system_helper.does_file_exist.return_value = False
        self.mock_file_system_helper.join_paths.return_value = "root/.ditto_archived"
        # Act
        self.internal_data_services.create_archive_file(None, "test_content")
        # Assert
        self.mock_file_system_helper.create_file.assert_called_once_with("root/.ditto_archived", "test_content")

    def test_create_archive_file_calls_archiver_with_updated_content_when_archive_filet_exist(self):
        # Arrange
        self.mock_file_system_helper.does_file_exist.return_value = True
        self.mock_file_system_helper.join_paths.return_value = "root/.ditto_archived"
        self.mock_file_system_helper.load_content.return_value = "Some old content "
        self.mock_archiver.update_content.return_value = "Some old content test_content"
        # Act
        self.internal_data_services.create_archive_file(None, "test_content")
        # Assert
        self.mock_archiver.update_content.assert_called_once_with("Some old content ", "test_content")
        self.mock_file_system_helper.create_file.assert_called_once_with("root/.ditto_archived",
                                                                         "Some old content test_content")

