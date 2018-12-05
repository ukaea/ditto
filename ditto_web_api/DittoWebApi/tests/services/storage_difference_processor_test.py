# pylint: disable=W0201, W0212
import logging
import pytest
import mock

from DittoWebApi.src.models.file_information import FileInformation
from DittoWebApi.src.models.s3_object_information import S3ObjectInformation
from DittoWebApi.src.services.data_replication.storage_difference_processor import StorageDifferenceProcessor
from DittoWebApi.src.utils.file_system.files_system_helpers import FileSystemHelper


class TestStorageDifferenceProcessor:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_logger = mock.create_autospec(logging.Logger)
        self.mock_file_system_helper = mock.create_autospec(FileSystemHelper)
        self.processor = StorageDifferenceProcessor(self.mock_file_system_helper, self.mock_logger)
        # Mock file information objects
        self.file_1 = mock.create_autospec(FileInformation)
        self.file_2 = mock.create_autospec(FileInformation)
        self.file_3 = mock.create_autospec(FileInformation)
        self.file_4 = mock.create_autospec(FileInformation)
        self.file_1.rel_path = "file_1.txt"
        self.file_2.rel_path = "some_dir/file_2.txt"
        self.file_3.rel_path = r"some_win_dir\some_win_sub_dir\file_3.txt"
        self.file_4.rel_path = r"some/badly\formed/path\file_4.txt"
        self.file_1.abs_path = "root/file_1.txt"
        self.file_2.abs_path = "root/some_dir/file_2.txt"
        self.file_3.abs_path = r"root/some_win_dir\some_win_sub_dir\file_3.txt"
        self.file_4.abs_path = r"root/some/badly\formed/path\file_4.txt"
        # Mock s3 objects
        self.s3_object_1 = mock.create_autospec(S3ObjectInformation)
        self.s3_object_2 = mock.create_autospec(S3ObjectInformation)
        self.s3_object_3 = mock.create_autospec(S3ObjectInformation)
        self.s3_object_4 = mock.create_autospec(S3ObjectInformation)
        self.s3_object_1.object_name = "file_1.txt"
        self.s3_object_2.object_name = "some_dir/file_2.txt"
        self.s3_object_3.object_name = "some_win_dir/some_win_sub_dir/file_3.txt"
        self.s3_object_4.object_name = "some/badly/formed/path/file_4.txt"
        self.s3_object_1.last_modified = 123.123
        self.s3_object_2.last_modified = 234.234
        self.s3_object_3.last_modified = 345.345
        self.s3_object_4.last_modified = 456.456

    def test_return_difference_comparison_returns_all_files_when_only_new_files_are_present(self):
        # Arrange
        objects_in_bucket = []
        files_in_directory = [self.file_1, self.file_2]
        # Act
        result = self.processor.return_difference_comparison(objects_in_bucket, files_in_directory)
        # Assert
        assert len(result.new_files) == 2
        assert result.updated_files == []
        assert result.new_files[0] == self.file_1
        assert result.new_files[1] == self.file_2

    def test_return_difference_comparison_returns_empty_array_when_all_files_are_already_present(self):
        # Arrange
        objects_in_bucket = [self.s3_object_1, self.s3_object_2]
        files_in_directory = [self.file_1, self.file_2]
        # Act
        result = self.processor.return_difference_comparison(objects_in_bucket, files_in_directory)
        # Assert
        assert result.new_files == []
        assert result.updated_files == []

    def test_return_difference_comparison_returns_only_new_files_when_some_new_some_not_including_non_unix_paths(self):
        # Arrange
        objects_in_bucket = [self.s3_object_2]
        files_in_directory = [self.file_1, self.file_2, self.file_3]
        # Act
        result = self.processor.return_difference_comparison(objects_in_bucket, files_in_directory)
        # Assert
        assert len(result.new_files) == 2
        assert result.updated_files == []
        assert result.new_files[0] == self.file_1
        assert result.new_files[1] == self.file_3

    def test_return_difference_comparison_returns_only_new_files_when_extra_file_in_bucket_but_not_in_dir(self):
        # Arrange
        objects_in_bucket = [self.s3_object_2, self.s3_object_4]
        files_in_directory = [self.file_1, self.file_2, self.file_3]
        # Act
        result = self.processor.return_difference_comparison(objects_in_bucket, files_in_directory)
        # Assert
        assert len(result.new_files) == 2
        assert result.updated_files == []
        assert result.new_files[0] == self.file_1
        assert result.new_files[1] == self.file_3

    def test_are_the_same_returns_true_when_objects_represent_the_same_file(self):
        # Arrange
        s3_object = self.s3_object_2
        file_information = self.file_2
        # Act
        result = self.processor.are_the_same_file(s3_object, file_information)
        # Assert
        assert result is True

    def test_are_the_same_returns_false_when_objects_represent_different_files(self):
        # Arrange
        s3_object = self.s3_object_2
        file_information = self.file_1
        # Act
        result = self.processor.are_the_same_file(s3_object, file_information)
        # Assert
        assert result is False

    def test_are_the_same_returns_true_when_objects_represent_the_same_file_but_with_windows_path(self):
        # Arrange
        s3_object = self.s3_object_3
        file_information = self.file_3
        # Act
        result = self.processor.are_the_same_file(s3_object, file_information)
        # Assert
        assert result is True

    def test_are_the_same_returns_true_when_objects_represent_the_same_file_but_with_mixed_path(self):
        # Arrange
        s3_object = self.s3_object_4
        file_information = self.file_4
        # Act
        result = self.processor.are_the_same_file(s3_object, file_information)
        # Assert
        assert result is True

    def test_changes_in_file_returns_true_when_timestamp_for_file_information_is_more_recent(self):
        # Arrange
        s3_object = self.s3_object_1
        file_information = self.file_1
        s3_object.last_modified = 12345665.12345
        self.processor._file_system_helper.last_modified.return_value = 22234589.12345
        # Act
        result = self.processor.has_file_changed(s3_object, file_information)
        # Assert
        assert result is True

    def test_changes_in_file_returns_false_when_timestamp_for_s3_object_is_more_recent(self):
        # Arrange
        s3_object = self.s3_object_1
        file_information = self.file_1
        s3_object.last_modified = 9912345665.12345
        self.processor._file_system_helper.last_modified.return_value = 12234589.12345
        # Act
        result = self.processor.has_file_changed(s3_object, file_information)
        # Assert
        assert result is False

    def test_changes_in_file_returns_false_when_timestamps_are_equal_for_s3_object_and_file_information(self):
        # Arrange
        s3_object = self.s3_object_1
        file_information = self.file_1
        s3_object.last_modified = 12345.12345
        self.processor._file_system_helper.last_modified.return_value = 12345.12345
        # Act
        result = self.processor.has_file_changed(s3_object, file_information)
        # Assert
        assert result is False

    def test_return_difference_comparison_returns_only_new_files_when_new_files_and_none_to_update_but_some_copy(self):
        # Arrange
        objects_in_bucket = [self.s3_object_2, self.s3_object_4]
        files_in_directory = [self.file_1, self.file_2, self.file_3]
        self.processor._file_system_helper.last_modified.side_effect = [234.234]
        # Act
        result = self.processor.return_difference_comparison(objects_in_bucket,
                                                             files_in_directory,
                                                             check_for_updates=True)
        new_files = result.new_files
        files_to_update = result.updated_files
        # Assert
        assert len(new_files) == 2
        assert files_to_update == []
        assert new_files[0] == self.file_1
        assert new_files[1] == self.file_3

    def test_return_difference_comparison_returns_only_files_to_update_when_no_new_but_some_changed(self):
        # Arrange
        objects_in_bucket = [self.s3_object_1, self.s3_object_2, self.s3_object_3]
        files_in_directory = [self.file_1, self.file_2, self.file_3]
        self.processor._file_system_helper.last_modified.side_effect = [2222222.1, 234.234, 4442323.2232]
        # Act
        result = self.processor.return_difference_comparison(objects_in_bucket,
                                                             files_in_directory,
                                                             check_for_updates=True)
        new_files = result.new_files
        files_to_update = result.updated_files
        # Assert
        assert new_files == []
        assert len(files_to_update) == 2
        assert files_to_update[0] == self.file_1
        assert files_to_update[1] == self.file_3

    def test_return_difference_comparison_returns_both_new_and_updated_when_present(self):
        # Arrange
        objects_in_bucket = [self.s3_object_1, self.s3_object_2, self.s3_object_4]
        files_in_directory = [self.file_1, self.file_2, self.file_3, self.file_4]
        self.processor._file_system_helper.last_modified.side_effect = [123.123, 5234.234, 4442323.2232]
        # Act
        result = self.processor.return_difference_comparison(objects_in_bucket,
                                                             files_in_directory,
                                                             check_for_updates=True)
        new_files = result.new_files
        files_to_update = result.updated_files
        # Assert
        assert len(new_files) == 1
        assert len(files_to_update) == 2
        assert new_files[0] == self.file_3
        assert files_to_update[0] == self.file_2
        assert files_to_update[1] == self.file_4

    def test_difference_comparison_returns_none_when_neither_present(self):
        # Arrange
        objects_in_bucket = [self.s3_object_1, self.s3_object_2, self.s3_object_3, self.s3_object_4]
        files_in_directory = [self.file_1, self.file_2, self.file_3, self.file_4]
        self.processor._file_system_helper.last_modified.side_effect = [123.123, 234.234, 345.345, 456.456]
        # Act
        result = self.processor.return_difference_comparison(objects_in_bucket,
                                                             files_in_directory,
                                                             check_for_updates=True)
        new_files = result.new_files
        files_to_update = result.updated_files
        # Assert
        assert new_files == []
        assert files_to_update == []
