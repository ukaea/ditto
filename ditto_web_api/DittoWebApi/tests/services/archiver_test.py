# pylint: disable=W0201
import logging
import unittest
import pytest
import mock

from DittoWebApi.src.utils.file_system.files_system_helpers import FileSystemHelper
from DittoWebApi.src.models.file_storage_summary import FilesStorageSummary
from DittoWebApi.src.models.file_information import FileInformation
from DittoWebApi.src.services.internal.archiver import Archiver


class TestArchive(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup(self):
        self._file_system_helper = mock.create_autospec(FileSystemHelper)
        self._logger = mock.create_autospec(logging.Logger)
        self.mock_file_1 = mock.create_autospec(FileInformation)
        self.mock_file_2 = mock.create_autospec(FileInformation)
        self.test_archiver = Archiver(self._file_system_helper, self._logger)
        self.mock_open_file = mock.Mock()
        self._file_system_helper.create_file.return_value = self.mock_open_file
        self._file_system_helper.open_file.return_value = self.mock_open_file
        self.mock_file_summary = mock.create_autospec(FilesStorageSummary)
        self.mock_file_summary.new_files = [self.mock_file_1]
        self.mock_file_summary.updated_files = [self.mock_file_2]
        self._file_system_helper.file_size.side_effect = [100, 50]

    @mock.patch('DittoWebApi.src.utils.system_helper.time.time', return_value=12345)
    def test_write_archive_creates_archive_file(self, time):
        # Act
        self.test_archiver.write_archive("some_file_path", self.mock_file_summary)
        # Assert
        self._logger.debug.assert_called_with("Archive file created: some_file_path")
        self._file_system_helper.write_to_file.assert_called_once_with(
            self.mock_open_file, {self.mock_file_1.file_name: {
                'file': self.mock_file_1.file_name,
                'size': 100,
                'latest update': '12345',
                'type of transfer': 'new upload'},
                                  self.mock_file_2.file_name: {
                                      'file': self.mock_file_2.file_name,
                                      'size': 50,
                                      'latest update': '12345',
                                      'type of transfer': 'file_update'}}
        )

    @mock.patch('DittoWebApi.src.utils.system_helper.time.time', return_value=12345)
    def test_update_archive_updates_an_archive_file(self, time):
        # Arrange
        self._file_system_helper.read_file_as_json.return_value = {
            self.mock_file_2.file_name: {
                'file': self.mock_file_2.file_name,
                'size': 50,
                'latest update': '12345',
                'type of transfer': 'file_update'}
        }
        # Act
        self.test_archiver.update_archive("some_file_path", self.mock_file_summary)
        # Assert
        self._logger.debug.assert_called_with("Archive file updated: some_file_path")
        self._file_system_helper.write_to_file.assert_called_once_with(
            self.mock_open_file, {
                self.mock_file_2.file_name: {
                    'file': self.mock_file_2.file_name,
                    'size': 50,
                    'latest update': '12345',
                    'type of transfer': 'file_update'},
                self.mock_file_1.file_name: {
                    'file': self.mock_file_1.file_name,
                    'size': 100,
                    'latest update': '12345',
                    'type of transfer': 'new upload'}
            })
