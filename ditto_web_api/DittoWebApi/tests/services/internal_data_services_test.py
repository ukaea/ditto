# pylint: disable=W0201
import logging
import unittest
import mock
import pytest
from DittoWebApi.src.services.internal.internal_data_service import InternalDataService
from DittoWebApi.src.services.internal.archiver import Archiver
from DittoWebApi.src.utils.file_system.files_system_helpers import FileSystemHelper
from DittoWebApi.src.models.file_storage_summary import FilesStorageSummary
from DittoWebApi.src.utils.configurations import Configuration
from DittoWebApi.src.models.file_information import FileInformation


class TestInternalDataServices(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_archiver = mock.create_autospec(Archiver)
        mock_configuration = mock.Mock(Configuration)
        self.mock_file_system_helper = mock.create_autospec(FileSystemHelper)
        self.mock_logger = mock.create_autospec(logging.RootLogger, spec_set=False)

        mock_configuration.archive_file_name = ".ditto_archived"

        self.internal_data_services = InternalDataService(self.mock_archiver,
                                                          mock_configuration,
                                                          self.mock_file_system_helper,
                                                          self.mock_logger)
        self.mock_file_summary = mock.create_autospec(FilesStorageSummary)
        self.mock_file_1 = mock.create_autospec(FileInformation)
        self.mock_file_1.rel_path = 'root/test.txt'
        self.mock_file_1.file_name = 'test.txt'
        self.mock_file_2 = mock.create_autospec(FileInformation)
        self.mock_file_2.rel_path = 'root/sub_dir_1/test_1.txt'
        self.mock_file_2.file_name = 'test_1.txt'

    def test_find_files_finds_files_in_the_root_directory(self):
        # Arrange
        root_dir = "/usr/tmp/data"
        dir_path = None
        self.mock_file_system_helper.join_paths.return_value = "/usr/tmp/data"
        self.mock_file_system_helper.find_all_files_in_folder.return_value = [
            "/usr/tmp/data/file_1.txt",
            "/usr/tmp/data/file_2.txt"
        ]
        self.mock_file_system_helper.relative_file_path.side_effect = [
            "file_1.txt",
            "file_2.txt"
        ]
        self.mock_file_system_helper.absolute_file_path.side_effect = [
            "/usr/tmp/data/file_1.txt",
            "/usr/tmp/data/file_2.txt"
        ]
        self.mock_file_system_helper.file_name.side_effect = [
            "file_1.txt",
            "file_2.txt"
        ]
        # Act
        file_information = self.internal_data_services.find_files(root_dir, dir_path)
        # Assert
        self.mock_file_system_helper.find_all_files_in_folder.assert_called_once_with("/usr/tmp/data")
        assert len(file_information) == 2

        assert file_information[0].file_name == "file_1.txt"
        assert file_information[1].file_name == "file_2.txt"

        assert file_information[0].rel_path == "file_1.txt"
        assert file_information[1].rel_path == "file_2.txt"

        assert file_information[0].abs_path == "/usr/tmp/data/file_1.txt"
        assert file_information[1].abs_path == "/usr/tmp/data/file_2.txt"

    def test_find_files_finds_files_in_a_subdirectory(self):
        # Arrange
        root_dir = "/usr/tmp/data"
        dir_path = "test_dir"
        self.mock_file_system_helper.join_paths.return_value = "/usr/tmp/data/test_dir"
        self.mock_file_system_helper.find_all_files_in_folder.return_value = [
            "/usr/tmp/data/test_dir/file_1.txt",
            "/usr/tmp/data/test_dir/file_2.txt"
        ]
        self.mock_file_system_helper.relative_file_path.side_effect = [
            "test_dir/file_1.txt",
            "test_dir/file_2.txt"
        ]
        self.mock_file_system_helper.absolute_file_path.side_effect = [
            "/usr/tmp/data/test_dir/file_1.txt",
            "/usr/tmp/data/test_dir/file_2.txt"
        ]
        self.mock_file_system_helper.file_name.side_effect = [
            "file_1.txt",
            "file_2.txt"
        ]
        # Act
        file_information = self.internal_data_services.find_files(root_dir, dir_path)
        # Assert
        self.mock_file_system_helper.find_all_files_in_folder.assert_called_once_with("/usr/tmp/data/test_dir")
        assert len(file_information) == 2

        assert file_information[0].file_name == "file_1.txt"
        assert file_information[1].file_name == "file_2.txt"

        assert file_information[0].rel_path == "test_dir/file_1.txt"
        assert file_information[1].rel_path == "test_dir/file_2.txt"

        assert file_information[0].abs_path == "/usr/tmp/data/test_dir/file_1.txt"
        assert file_information[1].abs_path == "/usr/tmp/data/test_dir/file_2.txt"

    def test_find_files_skips_archive_file_in_root_directory(self):
        # Arrange
        root_dir = "/usr/tmp/data"
        dir_path = None
        self.mock_file_system_helper.join_paths.return_value = "/usr/tmp/data"
        self.mock_file_system_helper.find_all_files_in_folder.return_value = [
            "/usr/tmp/data/file_1.txt",
            "/usr/tmp/data/file_2.txt",
            "/usr/tmp/data/.ditto_archived"
        ]
        self.mock_file_system_helper.relative_file_path.side_effect = [
            "file_1.txt",
            "file_2.txt"
        ]
        self.mock_file_system_helper.absolute_file_path.side_effect = [
            "/usr/tmp/data/file_1.txt",
            "/usr/tmp/data/file_2.txt"
        ]
        self.mock_file_system_helper.file_name.side_effect = [
            "file_1.txt",
            "file_2.txt"
        ]
        # Act
        file_information = self.internal_data_services.find_files(root_dir, dir_path)
        # Assert
        self.mock_file_system_helper.find_all_files_in_folder.assert_called_once_with("/usr/tmp/data")
        assert len(file_information) == 2

        assert file_information[0].file_name == "file_1.txt"
        assert file_information[1].file_name == "file_2.txt"

        assert file_information[0].rel_path == "file_1.txt"
        assert file_information[1].rel_path == "file_2.txt"

        assert file_information[0].abs_path == "/usr/tmp/data/file_1.txt"
        assert file_information[1].abs_path == "/usr/tmp/data/file_2.txt"

    def test_find_files_skips_archive_file_in_subdirectory(self):
        # Arrange
        root_dir = "/usr/tmp/data"
        dir_path = "test_dir"
        self.mock_file_system_helper.join_paths.return_value = "/usr/tmp/data/test_dir"
        self.mock_file_system_helper.find_all_files_in_folder.return_value = [
            "/usr/tmp/data/test_dir/file_1.txt",
            "/usr/tmp/data/test_dir/file_2.txt",
            "/usr/tmp/data/test_dir/.ditto_archived"
        ]
        self.mock_file_system_helper.relative_file_path.side_effect = [
            "test_dir/file_1.txt",
            "test_dir/file_2.txt"
        ]
        self.mock_file_system_helper.absolute_file_path.side_effect = [
            "/usr/tmp/data/test_dir/file_1.txt",
            "/usr/tmp/data/test_dir/file_2.txt"
        ]
        self.mock_file_system_helper.file_name.side_effect = [
            "file_1.txt",
            "file_2.txt"
        ]
        # Act
        file_information = self.internal_data_services.find_files(root_dir, dir_path)
        # Assert
        self.mock_file_system_helper.find_all_files_in_folder.assert_called_once_with("/usr/tmp/data/test_dir")
        assert len(file_information) == 2

        assert file_information[0].file_name == "file_1.txt"
        assert file_information[1].file_name == "file_2.txt"

        assert file_information[0].rel_path == "test_dir/file_1.txt"
        assert file_information[1].rel_path == "test_dir/file_2.txt"

        assert file_information[0].abs_path == "/usr/tmp/data/test_dir/file_1.txt"
        assert file_information[1].abs_path == "/usr/tmp/data/test_dir/file_2.txt"

    def test_logger_is_called_when_find_files_is_run(self):
        # Arrange
        self.mock_file_system_helper.join_paths.return_value = "/usr/tmp/data/test_dir"
        self.mock_file_system_helper.find_all_files_in_folder.return_value = [
            "/usr/tmp/data/test_dir/file_1.txt",
            "/usr/tmp/data/test_dir/file_2.txt"
        ]
        self.mock_file_system_helper.relative_file_path.side_effect = [
            "test_dir/file_1.txt",
            "test_dir/file_2.txt"
        ]
        self.mock_file_system_helper.absolute_file_path.side_effect = [
            "/usr/tmp/data/test_dir/file_1.txt",
            "/usr/tmp/data/test_dir/file_2.txt"
        ]
        self.mock_file_system_helper.file_name.side_effect = [
            "file_1.txt",
            "file_2.txt"
        ]
        # Act
        self.internal_data_services.find_files("/usr/tmp/data", "test_dir")
        # Assert
        assert self.mock_logger.debug.call_count == 2
        self.mock_logger.debug.assert_any_call("Finding files in directory /usr/tmp/data/test_dir")
        self.mock_logger.debug.assert_any_call("Found 2 files, converting to file information objects")

    def test_create_archive_file_called_for_each_subdir_for_files_transferred_when_archive_file_does_not_exist(self):
        # Arrange
        self.mock_file_system_helper.does_file_exist.return_value = False
        self.mock_file_system_helper.join_paths.return_value = "/usr/tmp/data/.ditto_archived"
        self.mock_file_summary.new_files = [self.mock_file_1, self.mock_file_2]
        self.mock_file_summary.updated_files = []
        # Act
        self.internal_data_services.archive_file_transfer(self.mock_file_summary, "/usr/tmp/data")
        # Assert
        assert self.mock_archiver.write_archive.call_count == 1
        assert self.mock_archiver.update_archive.call_count == 0

    def test_create_archive_file_calls_archiver_with_updated_content_when_archive_file_exists(self):
        # Arrange
        self.mock_file_system_helper.does_file_exist.return_value = True
        self.mock_file_system_helper.join_paths.return_value = "/usr/tmp/data/.ditto_archived"
        self.mock_file_summary.new_files = []
        self.mock_file_summary.updated_files = [self.mock_file_1, self.mock_file_2]
        # Act
        self.internal_data_services.archive_file_transfer(self.mock_file_summary, "/usr/tmp/data")
        # Assert
        assert self.mock_archiver.write_archive.call_count == 0
        assert self.mock_archiver.update_archive.call_count == 1

    def test_create_archive_file_calls_archiver_with_updated_content_when_archive_file_exist(self):
        # Arrange
        self.mock_file_system_helper.does_file_exist.return_value = True
        self.mock_file_system_helper.join_paths.return_value = "/usr/tmp/data/.ditto_archived"
        self.mock_archiver.update_archive.return_value = "Some old content test_content"
        self.mock_file_summary.new_files = []
        self.mock_file_summary.updated_files = [self.mock_file_1, self.mock_file_2]
        # Act
        self.internal_data_services.archive_file_transfer(self.mock_file_summary, "/usr/tmp/data")
        # Assert
        assert self.mock_archiver.write_archive.call_count == 0
        assert self.mock_archiver.update_archive.call_count == 1

    def test_create_archive_file_updates_archive_when_exists_and_creates_new_when_not(self):
        # Arrange
        self.mock_file_system_helper.does_file_exist.side_effect = [False, True]
        self.mock_file_system_helper.join_paths.return_value = "/usr/tmp/data/.ditto_archived"
        self.mock_file_system_helper.file_directory.side_effect = ["path_1", "path_2"]
        self.mock_archiver.update_archive.return_value = "Some old content test_content"
        self.mock_file_summary.new_files = [self.mock_file_2]
        self.mock_file_summary.updated_files = [self.mock_file_1]
        # Act
        self.internal_data_services.archive_file_transfer(self.mock_file_summary, "/usr/tmp/data")
        # Assert
        assert self.mock_archiver.write_archive.call_count == 1
        assert self.mock_archiver.update_archive.call_count == 1

    def test_create_archive_file_updates_archive_when_exists_even_when_all_files_are_new(self):
        # Arrange
        self.mock_file_system_helper.does_file_exist.side_effect = [True, True]
        self.mock_file_system_helper.join_paths.return_value = "/usr/tmp/data/.ditto_archived"
        self.mock_archiver.update_archive.return_value = "Some old content test_content"
        self.mock_file_summary.new_files = [self.mock_file_1, self.mock_file_2]
        self.mock_file_summary.updated_files = []
        # Act
        self.internal_data_services.archive_file_transfer(self.mock_file_summary, "/usr/tmp/data")
        # Assert
        assert self.mock_archiver.write_archive.call_count == 0
        assert self.mock_archiver.update_archive.call_count == 1

    def test_create_archive_file_creates_archive_that_do_not_exist_even_when_all_files_are_updating_files_on_s3(self):
        # Arrange
        self.mock_file_system_helper.does_file_exist.side_effect = [False, False]
        self.mock_file_system_helper.join_paths.return_value = "/usr/tmp/data/.ditto_archived"
        self.mock_archiver.update_archive.return_value = "Some old content test_content"
        self.mock_file_summary.new_files = []
        self.mock_file_summary.updated_files = [self.mock_file_1, self.mock_file_2]
        # Act
        self.internal_data_services.archive_file_transfer(self.mock_file_summary, "/usr/tmp/data")
        # Assert
        assert self.mock_archiver.write_archive.call_count == 1
        assert self.mock_archiver.update_archive.call_count == 0
