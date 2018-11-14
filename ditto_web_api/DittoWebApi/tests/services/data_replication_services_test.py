# pylint: disable=W0201
import logging
import unittest

import mock
import pytest

from DittoWebApi.src.models.file_information import FileInformation
from DittoWebApi.src.services.external.external_data_service import ExternalDataService
from DittoWebApi.src.services.data_replication.data_replication_service import DataReplicationService
from DittoWebApi.src.services.internal_data_service import InternalDataService
from DittoWebApi.src.models.s3_object_information import S3ObjectInformation
from DittoWebApi.src.models.bucket_information import BucketInformation
from DittoWebApi.src.services.data_replication.storage_difference_processor import StorageDifferenceProcessor


class DataReplicationServiceTest(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_external_data_service = mock.create_autospec(ExternalDataService)
        self.mock_internal_data_service = mock.create_autospec(InternalDataService)
        self.mock_storage_difference_processor = mock.create_autospec(StorageDifferenceProcessor)
        self.mock_logger = mock.create_autospec(logging.Logger)
        self.test_service = DataReplicationService(self.mock_external_data_service,
                                                   self.mock_internal_data_service,
                                                   self.mock_logger)
        # Mock_objects
        self.mock_object_1 = mock.create_autospec(S3ObjectInformation)
        self.mock_object_1.to_dict.return_value = {"object_name": "test",
                                                   "bucket_name": "test_bucket",
                                                   "is_dir": False,
                                                   "size": 100,
                                                   "etag": "test_etag",
                                                   "last_modified": 2132142421.123123}
        self.mock_object_1.object_name = "test"
        self.mock_object_2 = mock.create_autospec(S3ObjectInformation)
        self.mock_object_2.to_dict.return_value = {"object_name": "test_2",
                                                   "bucket_name": "test_bucket",
                                                   "is_dir": False, "size": 100,
                                                   "etag": "test_etag_2",
                                                   "last_modified": 2132142421.123123}
        self.mock_object_2.object_name = "test_2"
        self.mock_object_3 = mock.create_autospec(S3ObjectInformation)
        self.mock_object_3.to_dict.return_value = {"object_name": "test_dir/test",
                                                   "bucket_name": "test_bucket",
                                                   "is_dir": False,
                                                   "size": 100,
                                                   "etag": "test_etag",
                                                   "last_modified": 2132142421.123123}
        self.mock_object_3.object_name = "test_dir/test"
        # mock file information
        self.mock_file_information_1 = mock.create_autospec(FileInformation)
        self.mock_file_information_1.rel_path = "test"
        self.mock_file_information_2 = mock.create_autospec(FileInformation)
        self.mock_file_information_2.rel_path = "test_2"
        self.mock_file_information_3 = mock.create_autospec(FileInformation)
        self.mock_file_information_3.rel_path = "test_dir/test"

    def test_retrieve_objects_dicts_returns_all_correct_dictionaries_of_objects(self):
        # Arrange
        self.mock_external_data_service.get_objects.return_value = [self.mock_object_1, self.mock_object_2]
        # Act
        output = self.test_service.retrieve_object_dicts("test_bucket", None)
        # Assert
        self.mock_external_data_service.get_objects.assert_called_once_with("test_bucket", None)
        assert output[0] == {"object_name": "test",
                             "bucket_name": "test_bucket",
                             "is_dir": False,
                             "size": 100,
                             "etag": "test_etag",
                             "last_modified": 2132142421.123123}
        assert output[1] == {"object_name": "test_2",
                             "bucket_name": "test_bucket",
                             "is_dir": False, "size": 100,
                             "etag": "test_etag_2",
                             "last_modified": 2132142421.123123}
        assert len(output) == 2

    def test_retrieve_objects_dicts_empty_array_when_no_objects_present(self):
        self.mock_external_data_service.get_objects.return_value = []
        # Act
        output = self.test_service.retrieve_object_dicts("test_bucket", None)
        # Assert
        self.mock_external_data_service.get_objects.assert_called_once_with("test_bucket", None)
        assert output == []

    def test_retrieve_objects_dicts_returns_all_correct_dictionaries_of_objects_from_sub_dir(self):
        # Arrange
        self.mock_external_data_service.get_objects.return_value = [self.mock_object_3]
        # Act
        output = self.test_service.retrieve_object_dicts("test_bucket", "test_dir")
        # Assert
        self.mock_external_data_service.get_objects.assert_called_once_with("test_bucket", "test_dir")
        assert output[0] == {"object_name": "test_dir/test",
                             "bucket_name": "test_bucket",
                             "is_dir": False,
                             "size": 100,
                             "etag": "test_etag",
                             "last_modified": 2132142421.123123}
        assert len(output) == 1

    def test_return_bucket_message_correct_when_bucket_name_invalid(self):
        # Arrange
        self.mock_external_data_service.does_bucket_match_standard.return_value = False
        bucket_name = "test-1234-"
        # Act
        response = self.test_service.create_bucket(bucket_name)
        # Assert
        self.mock_external_data_service.create_bucket.assert_not_called()
        self.assertEqual(response, {"Message": "Bucket breaks local naming standard (test-1234-)",
                                    "Bucket": "test-1234-"})

    def test_create_bucket_return_correct_when_bucket_not_given(self):
        # Arrange
        bucket_name = None
        # Act
        response = self.test_service.create_bucket(bucket_name)
        # Assert
        self.mock_external_data_service.create_bucket.assert_not_called()
        self.assertEqual(response, {"Message": "No bucket name provided",
                                    "Bucket": ""})

    def test_create_bucket_return_correct_when_bucket_already_exists(self):
        # Arrange
        bucket_name = 'test-12345'
        self.mock_external_data_service.does_bucket_match_standard.return_value = True
        self.mock_external_data_service.does_bucket_exist.return_value = True
        # Act
        response = self.test_service.create_bucket(bucket_name)
        # Assert
        self.mock_external_data_service.create_bucket.assert_not_called()
        self.assertEqual(response, {"Message": "Bucket already exists (test-12345)",
                                    "Bucket": "test-12345"})

    def test_create_bucket_returns_correctly_when_successful(self):
        # Arrange
        bucket_name = 'test-12345'
        self.mock_external_data_service.does_bucket_match_standard.return_value = True
        self.mock_external_data_service.does_bucket_exist.return_value = False
        # Act
        response = self.test_service.create_bucket(bucket_name)
        # Assert
        self.mock_external_data_service.create_bucket.assert_called_once_with(bucket_name)
        self.assertEqual(response, {"Message": "Bucket Created (test-12345)",
                                    "Bucket": "test-12345"})

    def test_copy_dir_does_not_upload_if_no_local_files_found(self):
        # Arrange
        bucket_name = 'test-12345'
        dir_path = 'testdir/testsubdir/'
        self.mock_internal_data_service.find_files.return_value = []
        # Act
        self.test_service.copy_dir(bucket_name, dir_path)
        # Assert
        self.mock_external_data_service.upload_file.assert_not_called()

    def test_copy_dir_does_not_upload_if_s3_dir_already_exists(self):
        # Arrange
        bucket_name = 'test-12345'
        dir_path = 'testdir/testsubdir/'
        self.mock_internal_data_service.find_files.return_value = [
            FileInformation("/home/test/test1.txt", "test1.txt", "test1.txt")
        ]
        self.mock_external_data_service.does_dir_exist.return_value = True
        # Act
        self.test_service.copy_dir(bucket_name, dir_path)
        # Assert
        self.mock_external_data_service.upload_file.assert_not_called()

    def test_copy_dir_uploads_single_file_in_new_dir(self):
        # Arrange
        bucket_name = 'test-12345'
        dir_path = 'testdir/testsubdir/'
        self.mock_internal_data_service.find_files.return_value = [
            FileInformation("/home/test/test1.txt", "test1.txt", "test1.txt")
        ]
        self.mock_external_data_service.does_dir_exist.return_value = False
        self.mock_external_data_service.upload_file.return_value = 42
        # Act
        response = self.test_service.copy_dir(bucket_name, dir_path)
        # Assert
        self.mock_external_data_service.upload_file.assert_called_once()
        assert response["Files transferred"] == 1
        assert response["Data transferred (bytes)"] == 42

    def test_copy_dir_uploads_files_from_sub_dir_in_new_dir(self):
        # Arrange
        bucket_name = 'test-12345'
        dir_path = 'testdir/testsubdir/'
        file_1 = FileInformation("/home/test/test1.txt", "test1.txt", "test1.txt")
        file_2 = FileInformation("/home/test/sub_1/test2.txt", "sub_1/test2.txt", "test2.txt")
        self.mock_internal_data_service.find_files.return_value = [file_1, file_2]
        self.mock_external_data_service.does_dir_exist.return_value = False
        self.mock_external_data_service.upload_file.return_value = 44
        # Act
        response = self.test_service.copy_dir(bucket_name, dir_path)
        # Assert
        assert self.mock_external_data_service.upload_file.call_count == 2
        assert response["Files transferred"] == 2
        assert response["Data transferred (bytes)"] == 88

    def test_try_delete_file_returns_error_message_when_file_doesnt_exist(self):
        # Arrange
        file_name = "unknown_file"
        mock_bucket = mock.create_autospec(BucketInformation)
        mock_bucket.name = "some-bucket"
        self.mock_external_data_service.get_buckets.return_value = [mock_bucket]
        self.mock_external_data_service.does_object_exist.return_value = False
        # Act
        response = self.test_service.try_delete_file(mock_bucket.name, file_name)
        # Assert
        assert response == {'Bucket': 'some-bucket',
                            'File': 'unknown_file',
                            'Message': 'File unknown_file does not exist in bucket some-bucket'}

    def test_try_delete_file_returns_confirmation_message_when_file_does_exist(self):
        # Arrange
        file_name = "known_file"
        mock_bucket = mock.create_autospec(BucketInformation)
        mock_bucket.name = "some-bucket"
        self.mock_external_data_service.get_buckets.return_value = [mock_bucket]
        self.mock_external_data_service.does_object_exist.return_value = True
        # Act
        response = self.test_service.try_delete_file(mock_bucket.name, file_name)
        # Assert
        assert response == {'Bucket': 'some-bucket',
                            'File': 'known_file',
                            'Message': 'File known_file successfully deleted from bucket some-bucket'}

    def test_copy_new_return_message_when_no_new_files_to_transfer(self):
        # Arrange
        self.mock_external_data_service.get_objects.return_value = [self.mock_object_1]
        self.mock_internal_data_service.find_files.return_value = [self.mock_file_information_1]
        self.mock_storage_difference_processor.return_new_files.return_value = []
        # Act
        response = self.test_service.copy_new_with_optional_updates("bucket", None)
        assert self.mock_external_data_service.upload_file.call_count == 0
        # Assert
        assert response == {'Message': 'No new files found in directory or directory does not exist (root)',
                            'Files transferred': 0,
                            'Files updated': 0,
                            'Files skipped': 1,
                            'Data transferred (bytes)': 0}

    def test_copy_new_return_message_directory_does_not_exist(self):
        # Arrange
        self.mock_external_data_service.get_objects.return_value = [self.mock_object_1]
        self.mock_internal_data_service.find_files.return_value = []
        self.mock_storage_difference_processor.return_new_files.return_value = []
        # Act
        response = self.test_service.copy_new_with_optional_updates("bucket", None)
        # Assert
        assert self.mock_external_data_service.upload_file.call_count == 0
        assert response == {'Message': 'No new files found in directory or directory does not exist (root)',
                            'Files transferred': 0,
                            'Files updated': 0,
                            'Files skipped': 0,
                            'Data transferred (bytes)': 0}

    def test_copy_new_return_message_when_new_files_transferred(self):
        # Arrange
        self.mock_external_data_service.get_objects.return_value = [self.mock_object_1]
        self.mock_internal_data_service.find_files.return_value = [self.mock_file_information_1,
                                                                   self.mock_file_information_2,
                                                                   self.mock_file_information_3]
        self.mock_external_data_service.upload_file.side_effect = [12, 34]
        # Act
        response = self.test_service.copy_new_with_optional_updates("bucket", "some_dir")
        # Assert
        assert self.mock_external_data_service.upload_file.call_count == 2
        assert response == {'Message': 'Transfer successful, copied 2 new files from some_dir totalling 46 bytes',
                            'Files transferred': 2,
                            'Files updated': 0,
                            'Files skipped': 1,
                            'Data transferred (bytes)': 46}
