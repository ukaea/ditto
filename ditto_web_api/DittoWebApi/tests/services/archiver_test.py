# pylint: disable=W0201
import logging
import unittest
import pytest
import mock

from DittoWebApi.version import __version__ as version
from DittoWebApi.src.utils.file_system.files_system_helpers import FileSystemHelper
from DittoWebApi.src.models.file_storage_summary import FilesStorageSummary
from DittoWebApi.src.models.file_information import FileInformation
from DittoWebApi.src.services.internal.archiver import Archiver
from DittoWebApi.src.utils.file_read_write_helper import FileReadWriteHelper


class TestArchive(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup(self):
        self._file_system_helper = mock.create_autospec(FileSystemHelper)
        self._logger = mock.create_autospec(logging.Logger)
        self._file_read_write_helper = mock.create_autospec(FileReadWriteHelper)
        self.test_archiver = Archiver(self._file_read_write_helper, self._file_system_helper, self._logger)

        self.mock_open_file = mock.Mock()
        self._file_system_helper.create_and_open_file_for_writing.return_value = self.mock_open_file
        self._file_system_helper.open_file_for_reading_and_writing.return_value = self.mock_open_file

        self.mock_file_1 = mock.create_autospec(FileInformation)
        self.mock_file_2 = mock.create_autospec(FileInformation)
        self.mock_file_1.file_name = "file_1.txt"
        self.mock_file_2.file_name = "file_2.txt"

        self.mock_file_summary = mock.create_autospec(FilesStorageSummary)

        self._file_system_helper.file_size.side_effect = [100, 50]

    @mock.patch('DittoWebApi.src.utils.system_helper.time.time', return_value=12345)
    def test_write_archive_creates_archive_file(self, time):
        self.mock_file_summary.new_files = [self.mock_file_1]
        self.mock_file_summary.updated_files = [self.mock_file_2]
        # Act
        self.test_archiver.write_archive("some_file_path", "some_bucket", self.mock_file_summary)
        # Assert
        self._logger.debug.assert_called_with("Archive file created: some_file_path")
        self._file_read_write_helper.write_json_to_file.assert_called_once_with(
            self.mock_open_file, {self.mock_file_1.file_name: {
                'file': self.mock_file_1.file_name,
                'bucket': "some_bucket",
                'size': 100,
                'last archived': '1970-01-01 03:25:45',
                'type of transfer': 'new upload',
                'ditto version': version},
                                  self.mock_file_2.file_name: {
                                      'file': self.mock_file_2.file_name,
                                      'bucket': "some_bucket",
                                      'size': 50,
                                      'last archived': '1970-01-01 03:25:45',
                                      'type of transfer': 'file update',
                                      'ditto version': version}}
        )

    @mock.patch('DittoWebApi.src.utils.system_helper.time.time', return_value=12345)
    def test_update_archive_updates_an_archive_file(self, time):
        self.mock_file_summary.new_files = [self.mock_file_1]
        self.mock_file_summary.updated_files = [self.mock_file_2]
        # Arrange
        self._file_read_write_helper.read_file_as_json.return_value = {
            self.mock_file_2.file_name: {
                'file': self.mock_file_2.file_name,
                'bucket': "some_bucket",
                'size': 50,
                'last archived': '1970-01-01 03:25:45',
                'type of transfer': 'file update',
                'ditto version': version}
        }
        # Act
        self.test_archiver.update_archive("some_file_path", "some_bucket", self.mock_file_summary)
        # Assert
        self._logger.debug.assert_called_with("Archive file updated: some_file_path")
        self._file_read_write_helper.write_json_to_file.assert_called_once_with(
            self.mock_open_file, {
                self.mock_file_2.file_name: {
                    'file': self.mock_file_2.file_name,
                    'bucket': "some_bucket",
                    'size': 50,
                    'last archived': '1970-01-01 03:25:45',
                    'type of transfer': 'file update',
                    'ditto version': version},
                self.mock_file_1.file_name: {
                    'file': self.mock_file_1.file_name,
                    'bucket': "some_bucket",
                    'size': 100,
                    'last archived': '1970-01-01 03:25:45',
                    'type of transfer': 'new upload',
                    'ditto version': version}
            })

    @mock.patch('DittoWebApi.src.utils.system_helper.time.time', return_value=12345)
    def test_update_archive_updates_an_archive_file_when_no_new_files(self, time):
        self.mock_file_summary.new_files = []
        self.mock_file_summary.updated_files = [self.mock_file_1, self.mock_file_2]
        # Arrange
        self._file_read_write_helper.read_file_as_json.return_value = {
            self.mock_file_2.file_name: {
                'file': self.mock_file_2.file_name,
                'bucket': "some_bucket",
                'size': 50,
                'last archived': '1970-01-01 03:25:45',
                'type of transfer': 'new upload',
                'ditto version': version}
        }
        # Act
        self.test_archiver.update_archive("some_file_path", "some_bucket", self.mock_file_summary)
        # Assert
        self._logger.debug.assert_called_with("Archive file updated: some_file_path")
        self._file_read_write_helper.write_json_to_file.assert_called_once_with(
            self.mock_open_file, {
                self.mock_file_1.file_name: {
                    'file': self.mock_file_1.file_name,
                    'bucket': "some_bucket",
                    'size': 100,
                    'last archived': '1970-01-01 03:25:45',
                    'type of transfer': 'file update',
                    'ditto version': version},
                self.mock_file_2.file_name: {
                    'file': self.mock_file_2.file_name,
                    'bucket': "some_bucket",
                    'size': 50,
                    'last archived': '1970-01-01 03:25:45',
                    'type of transfer': 'file update',
                    'ditto version': version}
            })
