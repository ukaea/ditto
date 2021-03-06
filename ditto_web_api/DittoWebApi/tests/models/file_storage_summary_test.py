# pylint: disable=W0201
import pytest
import mock
from DittoWebApi.src.models.file_information import FileInformation
from DittoWebApi.src.models.file_storage_summary import FilesStorageSummary


class TestFileStorageSummary:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_file_information_1 = mock.create_autospec(FileInformation)
        self.mock_file_information_2 = mock.create_autospec(FileInformation)
        self.mock_file_information_3 = mock.create_autospec(FileInformation)
        self.mock_file_information_4 = mock.create_autospec(FileInformation)
        self.file_summary = FilesStorageSummary([self.mock_file_information_1,
                                                 self.mock_file_information_2,
                                                 self.mock_file_information_3,
                                                 self.mock_file_information_4])

    def test_files_to_be_skipped_excludes_new_files(self):
        # Arrange
        self.file_summary.new_files = [self.mock_file_information_1, self.mock_file_information_2]
        # Act
        files_to_skip = self.file_summary.files_to_be_skipped()
        # Assert
        assert files_to_skip == [self.mock_file_information_3, self.mock_file_information_4]

    def test_files_to_be_skipped_excludes_updated_files(self):
        # Arrange
        self.file_summary.updated_files = [self.mock_file_information_3, self.mock_file_information_2]
        # Act
        files_to_skip = self.file_summary.files_to_be_skipped()
        # Assert
        assert files_to_skip == [self.mock_file_information_1, self.mock_file_information_4]

    def test_files_to_be_skipped_excludes_new_and_updated_files(self):
        # Arrange
        self.file_summary.new_files = [self.mock_file_information_2]
        self.file_summary.updated_files = [self.mock_file_information_1, self.mock_file_information_4]
        # Act
        files_to_skip = self.file_summary.files_to_be_skipped()
        # Assert
        assert files_to_skip == [self.mock_file_information_3]

    def test_files_to_be_skipped_excludes_all_when_none_new_or_updated(self):
        # Act
        files_to_skip = self.file_summary.files_to_be_skipped()
        # Assert
        assert files_to_skip == [self.mock_file_information_1,
                                 self.mock_file_information_2,
                                 self.mock_file_information_3,
                                 self.mock_file_information_4]

    def test_files_to_be_skipped_excludes_none_when_all_new_or_updated(self):
        # Arrange
        self.file_summary.new_files = [self.mock_file_information_2, self.mock_file_information_4]
        self.file_summary.updated_files = [self.mock_file_information_1, self.mock_file_information_3]
        # Act
        files_to_skip = self.file_summary.files_to_be_skipped()
        # Assert
        assert files_to_skip == []
