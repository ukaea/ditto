# pylint: disable=W0201,
import pytest
import mock
from DittoWebApi.src.models.file_information import FileInformation
from DittoWebApi.src.models.s3_object_information import S3ObjectInformation
from DittoWebApi.src.services.data_replication.storage_difference_processor import StorageDifferenceProcessor


class TestSorageDifferenceProcessor:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.processor = StorageDifferenceProcessor()
        # Mock file information objects
        self.file_1 = mock.create_autospec(FileInformation)
        self.file_2 = mock.create_autospec(FileInformation)
        self.file_3 = mock.create_autospec(FileInformation)
        self.file_4 = mock.create_autospec(FileInformation)
        self.file_1.rel_path = "file_1.txt"
        self.file_2.rel_path = "file_2.txt"
        self.file_3.rel_path = "file_3.txt"
        self.file_4.rel_path = "file_4.txt"
        # Mock s3 objects
        self.s3_object_1 = mock.create_autospec(S3ObjectInformation)
        self.s3_object_2 = mock.create_autospec(S3ObjectInformation)
        self.s3_object_3 = mock.create_autospec(S3ObjectInformation)
        self.s3_object_4 = mock.create_autospec(S3ObjectInformation)
        self.s3_object_1.object_name = "file_1.txt"
        self.s3_object_2.object_name = "file_2.txt"
        self.s3_object_3.object_name = "file_3.txt"
        self.s3_object_4.object_name = "file_4.txt"

    def test_new_files_returns_all_files_when_only_new_files_are_present(self):
        # Arrange
        objects_in_bucket = []
        files_in_directory = [self.file_1, self.file_2]
        # Act
        result = self.processor.new_files(objects_in_bucket, files_in_directory)
        # Assert
        assert len(result) == 2
        assert result[0].rel_path == "file_1.txt"
        assert result[1].rel_path == "file_2.txt"

    def test_new_files_returns_empty_array_when_all_files_are_already_present(self):
        # Arrange
        objects_in_bucket = [self.s3_object_1, self.s3_object_2]
        files_in_directory = [self.file_1, self.file_2]
        # Act
        result = self.processor.new_files(objects_in_bucket, files_in_directory)
        # Assert
        assert result == []

    def test_new_files_returns_only_new_files_when_some_are_new_and_some_are_already_present(self):
        # Arrange
        objects_in_bucket = [self.s3_object_2]
        files_in_directory = [self.file_1, self.file_2, self.file_3]
        # Act
        result = self.processor.new_files(objects_in_bucket, files_in_directory)
        # Assert
        assert len(result) == 2
        assert result[0].rel_path == "file_1.txt"
        assert result[1].rel_path == "file_3.txt"

    def test_new_files_returns_only_new_files_when_there_is_extra_file_in_bucket_but_not_in_dir(self):
        # Arrange
        objects_in_bucket = [self.s3_object_2, self.s3_object_4]
        files_in_directory = [self.file_1, self.file_2, self.file_3]
        # Act
        result = self.processor.new_files(objects_in_bucket, files_in_directory)
        # Assert
        assert len(result) == 2
        assert result[0].rel_path == "file_1.txt"
        assert result[1].rel_path == "file_3.txt"

    def test_are_the_same_returns_true_when_objects_represent_the_same_file(self):
        # Arrange
        s3_object = self.s3_object_2
        file_information = self.file_2
        # Act
        result = self.processor.are_the_same(s3_object, file_information)
        # Assert
        assert result is True

    def test_are_the_same_returns_false_when_objects_represent_different_files(self):
        # Arrange
        s3_object = self.s3_object_3
        file_information = self.file_1
        # Act
        result = self.processor.are_the_same(s3_object, file_information)
        # Assert
        assert result is False
