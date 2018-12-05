# pylint: disable=W0201, W0212
import logging
import unittest

import mock
import pytest

from DittoWebApi.src.models.s3_object_information import S3ObjectInformation
from DittoWebApi.src.services.external.external_data_service import ExternalDataService
from DittoWebApi.src.services.data_replication.data_replication_service import DataReplicationService
from DittoWebApi.src.services.data_replication.storage_difference_processor import StorageDifferenceProcessor
from DittoWebApi.src.services.internal.internal_data_service import InternalDataService
from DittoWebApi.src.models.file_information import FileInformation
from DittoWebApi.src.models.file_storage_summary import FilesStorageSummary
from DittoWebApi.src.utils.return_helper import return_transfer_summary
from DittoWebApi.src.utils.return_helper import return_delete_file_helper
from DittoWebApi.tests.helpers_for_tests import build_mock_file_information
from DittoWebApi.tests.helpers_for_tests import build_mock_file_summary
from DittoWebApi.tests.helpers_for_tests import build_transfer_return


class DataReplicationServiceTest(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_external_data_service = mock.create_autospec(ExternalDataService)
        self.mock_internal_data_service = mock.create_autospec(InternalDataService)
        self.mock_storage_difference_processor = mock.create_autospec(StorageDifferenceProcessor)
        self.mock_s3_object_file_comparison = mock.create_autospec(FilesStorageSummary)
        self.mock_storage_difference_processor.return_difference_comparison.return_value = \
            self.mock_s3_object_file_comparison
        self.mock_logger = mock.create_autospec(logging.Logger)
        self.test_service = DataReplicationService(self.mock_external_data_service,
                                                   self.mock_internal_data_service,
                                                   self.mock_storage_difference_processor,
                                                   self.mock_logger)
        # Mock_objects
        self.mock_object_1 = mock.create_autospec(S3ObjectInformation)
        self.mock_object_1.to_dict.return_value = {"object_name": "test",
                                                   "bucket_name": "test_bucket",
                                                   "is_dir": False,
                                                   "size": 100,
                                                   "etag": "test_etag",
                                                   "last_modified": 2132142421.123123}
        self.mock_object_2 = mock.create_autospec(S3ObjectInformation)
        self.mock_object_2.to_dict.return_value = {"object_name": "test_2",
                                                   "bucket_name": "test_bucket",
                                                   "is_dir": False,
                                                   "size": 100,
                                                   "etag": "test_etag_2",
                                                   "last_modified": 1124557444.128364}
        self.mock_object_3 = mock.create_autospec(S3ObjectInformation)
        self.mock_object_3.to_dict.return_value = {"object_name": "test_dir/test",
                                                   "bucket_name": "test_bucket",
                                                   "is_dir": False,
                                                   "size": 100,
                                                   "etag": "test_etag",
                                                   "last_modified": 4132242586.159111}
        # mock file information
        self.mock_file_information_1 = build_mock_file_information("test", "test", "test")
        self.mock_file_information_2 = build_mock_file_information("test_2", "test_2", "test_2")
        self.mock_file_information_3 = build_mock_file_information("test", "test_dir/test", "test_dir/test")

    def _set_up_system(self, does_bucket_exists=True, objects_in_bucket=None, files_in_system=None):
        self.mock_external_data_service.does_bucket_exist.return_value = does_bucket_exists
        self.mock_external_data_service.get_objects.return_value = objects_in_bucket if objects_in_bucket else []
        self.mock_internal_data_service.find_files.return_value = files_in_system if files_in_system else []

    def test_retrieve_objects_dicts_returns_warning_when_bucket_does_not_exist(self):
        # Arrange
        self.mock_external_data_service.does_bucket_exist.return_value = False
        # Act
        output = self.test_service.retrieve_object_dicts("test-bucket", None)
        # Assert
        self.mock_external_data_service.get_objects.assert_not_called()
        self.mock_logger.warning.assert_called_with("Warning, bucket does not exist (test-bucket)")
        assert output == {"message": "Warning, bucket does not exist (test-bucket)", "objects": []}

    def test_retrieve_objects_dicts_returns_all_correct_dictionaries_of_objects(self):
        # Arrange
        self._set_up_system(does_bucket_exists=True, objects_in_bucket=[self.mock_object_1, self.mock_object_2])
        # Act
        output = self.test_service.retrieve_object_dicts("test-bucket", None)
        # Assert
        self.mock_external_data_service.get_objects.assert_called_once_with("test-bucket", None)
        assert output["objects"][0] == {"object_name": "test",
                                        "bucket_name": "test_bucket",
                                        "is_dir": False,
                                        "size": 100,
                                        "etag": "test_etag",
                                        "last_modified": 2132142421.123123}
        assert output["objects"][1] == {"object_name": "test_2",
                                        "bucket_name": "test_bucket",
                                        "is_dir": False, "size": 100,
                                        "etag": "test_etag_2",
                                        "last_modified": 1124557444.128364}
        assert len(output["objects"]) == 2

    def test_retrieve_objects_dicts_empty_array_when_no_objects_present(self):
        self._set_up_system(True, [], [])
        # Act
        output = self.test_service.retrieve_object_dicts("test-bucket", None)
        # Assert
        self.mock_external_data_service.get_objects.assert_called_once_with("test-bucket", None)
        assert output["objects"] == []

    def test_retrieve_objects_dicts_returns_all_correct_dictionaries_of_objects_from_sub_dir(self):
        # Arrange
        self._set_up_system(does_bucket_exists=True, objects_in_bucket=[self.mock_object_3])
        # Act
        output = self.test_service.retrieve_object_dicts("test-bucket", "test_dir")
        # Assert
        self.mock_external_data_service.get_objects.assert_called_once_with("test-bucket", "test_dir")
        assert output["objects"][0] == {"object_name": "test_dir/test",
                                        "bucket_name": "test_bucket",
                                        "is_dir": False,
                                        "size": 100,
                                        "etag": "test_etag",
                                        "last_modified": 4132242586.159111}
        assert len(output["objects"]) == 1

    def test_create_bucket_message_correct_when_bucket_name_invalid(self):
        # Arrange
        self.mock_external_data_service.does_bucket_match_standard.return_value = False
        bucket_name = "test-1234-"
        # Act
        response = self.test_service.create_bucket(bucket_name)
        # Assert
        self.mock_external_data_service.create_bucket.assert_not_called()
        self.assertEqual(response, {"message": "Bucket breaks local naming standard (test-1234-)",
                                    "bucket": "test-1234-"})

    def test_create_bucket_return_correct_when_bucket_not_given(self):
        # Arrange
        bucket_name = None
        # Act
        response = self.test_service.create_bucket(bucket_name)
        # Assert
        self.mock_external_data_service.create_bucket.assert_not_called()
        self.assertEqual(response, {"message": "No bucket name provided",
                                    "bucket": ""})

    def test_create_bucket_return_correct_when_bucket_already_exists(self):
        # Arrange
        bucket_name = 'test-12345'
        self.mock_external_data_service.does_bucket_match_standard.return_value = True
        self.mock_external_data_service.does_bucket_exist.return_value = True
        # Act
        response = self.test_service.create_bucket(bucket_name)
        # Assert
        self.mock_external_data_service.create_bucket.assert_not_called()
        self.assertEqual(response, {"message": "Warning, bucket already exists (test-12345)",
                                    "bucket": "test-12345"})

    def test_create_bucket_returns_correctly_when_successful(self):
        # Arrange
        bucket_name = 'test-12345'
        self.mock_external_data_service.does_bucket_match_standard.return_value = True
        self.mock_external_data_service.does_bucket_exist.return_value = False
        # Act
        response = self.test_service.create_bucket(bucket_name)
        # Assert
        self.mock_external_data_service.create_bucket.assert_called_once_with(bucket_name)
        self.assertEqual(response, {"message": "Bucket Created (test-12345)",
                                    "bucket": "test-12345"})

    def test_copy_dir_returns_warning_if_bucket_does_not_exist(self):
        # Arrange
        bucket_name = 'test-12345'
        dir_path = 'testdir/testsubdir/'
        self.mock_external_data_service.does_bucket_exist.return_value = False
        # Act
        response = self.test_service.copy_dir(bucket_name, dir_path)
        # Assert
        self.mock_logger.warning.assert_called_with("Warning, bucket does not exist (test-12345)")
        self.mock_external_data_service.perform_transfer.assert_not_called()
        self.mock_storage_difference_processor.return_difference_comparison.assert_not_called()
        assert response == return_transfer_summary(
            message='Warning, bucket does not exist (test-12345)'
        )

    def test_copy_dir_does_not_upload_if_no_local_files_found(self):
        # Arrange
        bucket_name = 'test-12345'
        dir_path = 'testdir/testsubdir/'
        self._set_up_system(does_bucket_exists=True)
        # Act
        response = self.test_service.copy_dir(bucket_name, dir_path)
        # Assert
        self.mock_external_data_service.perform_transfer.assert_not_called()
        self.mock_storage_difference_processor.return_difference_comparison.assert_not_called()
        self.mock_logger.warning.assert_called_with("No files found in directory or directory"
                                                    " does not exist (testdir/testsubdir/)")
        assert response == return_transfer_summary(
            message='No files found in directory or directory does not exist (testdir/testsubdir/)'
        )

    def test_copy_dir_does_not_upload_if_s3_dir_already_exists(self):
        # Arrange
        bucket_name = 'test-12345'
        dir_path = 'testdir/testsubdir/'
        file_1 = FileInformation("/home/test/test1.txt", "test1.txt", "test1.txt")
        self._set_up_system(True, [], [file_1])
        self.mock_external_data_service.does_dir_exist.return_value = True
        # Act
        self.test_service.copy_dir(bucket_name, dir_path)
        # Assert
        self.mock_external_data_service.upload_file.assert_not_called()
        self.mock_storage_difference_processor.return_difference_comparison.assert_not_called()
        self.mock_logger.warning.assert_called_with("Directory testdir/testsubdir/ "
                                                    "already exists on S3, 1 files skipped")

    def test_copy_dir_uploads_single_file_in_new_dir(self):
        # Arrange
        bucket_name = 'test-12345'
        dir_path = 'testdir/testsubdir/'
        file_1 = FileInformation("/home/test/test1.txt", "test1.txt", "test1.txt")
        self._set_up_system(does_bucket_exists=True, files_in_system=[file_1])
        self.mock_external_data_service.does_dir_exist.return_value = False
        self.mock_external_data_service.perform_transfer.return_value = build_transfer_return(1, 0, 0, 42)
        # Act
        response = self.test_service.copy_dir(bucket_name, dir_path)
        # Assert
        self.mock_storage_difference_processor.return_difference_comparison.assert_called_with(
            [],
            [file_1]
        )
        assert response["new files uploaded"] == 1
        assert response["data transferred (bytes)"] == 42

    def test_copy_dir_uploads_files_from_sub_dir_in_new_dir(self):
        # Arrange
        bucket_name = 'test-12345'
        dir_path = 'testdir/testsubdir/'
        file_1 = FileInformation("/home/test/test1.txt", "test1.txt", "test1.txt")
        file_2 = FileInformation("/home/test/sub_1/test2.txt", "sub_1/test2.txt", "test2.txt")
        self.mock_external_data_service.does_dir_exist.return_value = False
        self._set_up_system(does_bucket_exists=True, files_in_system=[file_1, file_2])
        self.mock_external_data_service.perform_transfer.return_value = build_transfer_return(2, 0, 0, 32)
        # Act
        response = self.test_service.copy_dir(bucket_name, dir_path)
        # Assert
        self.mock_storage_difference_processor.return_difference_comparison.assert_called_with(
            [],
            [file_1, file_2]
        )
        assert response["new files uploaded"] == 2
        assert response["data transferred (bytes)"] == 32

    def test_try_delete_file_returns_warning_message_when_bucket_doesnt_exist(self):
        # Arrange
        bucket_name = "test-bucket"
        file_rel_path = "test.txt"
        self.mock_external_data_service.does_bucket_exist.return_value = False
        # Act
        response = self.test_service.try_delete_file(bucket_name, file_rel_path)
        # Assert
        self.mock_logger.warning.assert_called_with("Warning, bucket does not exist (test-bucket)")
        assert response == return_delete_file_helper(
            bucket_name=bucket_name,
            file_rel_path=file_rel_path,
            message='Warning, bucket does not exist (test-bucket)'
        )

    def test_try_delete_file_returns_error_message_when_file_doesnt_exist(self):
        # Arrange
        self.mock_external_data_service.does_bucket_exist.return_value = True
        self.mock_external_data_service.does_object_exist.return_value = False
        # Act
        response = self.test_service.try_delete_file("some-bucket", "unknown_file")
        # Assert
        self.mock_logger.warning.assert_called_with('File unknown_file does not exist in bucket some-bucket')
        assert response == {'bucket': 'some-bucket',
                            'file': 'unknown_file',
                            'message': 'File unknown_file does not exist in bucket some-bucket'}

    def test_try_delete_file_returns_confirmation_message_when_file_does_exist(self):
        # Arrange
        self.mock_external_data_service.does_bucket_exist.return_value = True
        self.mock_external_data_service.does_object_exist.return_value = True
        # Act
        response = self.test_service.try_delete_file("some-bucket", "known_file")
        # Assert
        assert response == {'bucket': 'some-bucket',
                            'file': 'known_file',
                            'message': 'File known_file successfully deleted from bucket some-bucket'}

    def test_copy_new_return_warning_when_bucket_not_found(self):
        # Arrange
        self.mock_external_data_service.does_bucket_exist.return_value = False
        # Act
        response = self.test_service.copy_new("bucket", None)
        # Assert
        self.mock_external_data_service.perform_transfer.assert_not_called()
        self.mock_logger.warning.assert_called_with('Warning, bucket does not exist (bucket)')
        assert response == {'message': 'Warning, bucket does not exist (bucket)',
                            'new files uploaded': 0,
                            'files updated': 0,
                            'files skipped': 0,
                            'data transferred (bytes)': 0}

    def test_copy_new_return_message_when_no_new_files_to_transfer(self):
        # Arrange
        self._set_up_system(does_bucket_exists=True,
                            objects_in_bucket=[self.mock_object_1],
                            files_in_system=[self.mock_file_information_1])
        mock_file_summary = build_mock_file_summary(files_in_dir=[self.mock_file_information_1],
                                                    files_to_be_skipped=[self.mock_file_information_1])
        self.mock_storage_difference_processor.return_difference_comparison.return_value = mock_file_summary
        # Act
        response = self.test_service.copy_new("bucket", None)
        # Assert
        self.mock_external_data_service.perform_transfer.assert_not_called()
        self.mock_storage_difference_processor.return_difference_comparison.assert_called_with(
            [self.mock_object_1],
            [self.mock_file_information_1],
        )
        self.mock_logger.info.assert_called_with('No new files found in directory (root)')
        assert response == {'message': 'No new files found in directory (root)',
                            'new files uploaded': 0,
                            'files updated': 0,
                            'files skipped': 1,
                            'data transferred (bytes)': 0}

    def test_copy_new_return_message_directory_does_not_exist(self):
        # Arrange
        self._set_up_system(does_bucket_exists=True, objects_in_bucket=[self.mock_object_1])
        # Act
        response = self.test_service.copy_new("bucket", None)
        # Assert
        self.mock_external_data_service.perform_transfer.assert_not_called()
        self.mock_logger.warning.assert_called_with('No files found in directory or directory does not exist (root)')
        assert response == {'message': 'No files found in directory or directory does not exist (root)',
                            'new files uploaded': 0,
                            'files updated': 0,
                            'files skipped': 0,
                            'data transferred (bytes)': 0}

    def test_copy_new_transfers_all_files_when_no_objects_in_s3(self):
        # Arrange
        self._set_up_system(does_bucket_exists=True, files_in_system=[self.mock_file_information_2, self.mock_file_information_3])
        mock_file_summary = build_mock_file_summary(files_in_dir=[self.mock_file_information_2,
                                                                  self.mock_file_information_3],
                                                    new_files=[self.mock_file_information_2,
                                                               self.mock_file_information_3])
        self.mock_storage_difference_processor.return_difference_comparison.return_value = mock_file_summary
        self.mock_external_data_service.perform_transfer.return_value = build_transfer_return(2, 0, 0, 52)
        # Act
        response = self.test_service.copy_new("bucket", None)
        # Assert
        self.mock_storage_difference_processor.return_difference_comparison.assert_called_with(
            [],
            [self.mock_file_information_2, self.mock_file_information_3],
        )
        self.mock_external_data_service.perform_transfer.assert_called_once_with("bucket", mock_file_summary)
        assert response == {'message': 'Transfer successful',
                            'new files uploaded': 2,
                            'files updated': 0,
                            'files skipped': 0,
                            'data transferred (bytes)': 52}

    def test_copy_new_return_message_when_new_files_transferred(self):
        # Arrange
        self._set_up_system(does_bucket_exists=True,
                            objects_in_bucket=[self.mock_object_1],
                            files_in_system=[self.mock_file_information_1,
                                             self.mock_file_information_2,
                                             self.mock_file_information_3])
        mock_file_summary = build_mock_file_summary(files_in_dir=[self.mock_file_information_1,
                                                                  self.mock_file_information_2,
                                                                  self.mock_file_information_3],
                                                    new_files=[self.mock_file_information_2,
                                                               self.mock_file_information_3])
        self.mock_storage_difference_processor.return_difference_comparison.return_value = mock_file_summary
        self.mock_external_data_service.perform_transfer.return_value = build_transfer_return(2, 0, 1, 46)
        # Act
        response = self.test_service.copy_new("bucket", "some_dir")
        # Assert
        self.mock_storage_difference_processor.return_difference_comparison.assert_called_with(
            [self.mock_object_1],
            [self.mock_file_information_1, self.mock_file_information_2, self.mock_file_information_3],
        )
        self.mock_external_data_service.perform_transfer.assert_called_once_with("bucket", mock_file_summary)
        assert response == {'message': 'Transfer successful',
                            'new files uploaded': 2,
                            'files updated': 0,
                            'files skipped': 1,
                            'data transferred (bytes)': 46}

    def test_copy_new_and_update_return_warning_when_bucket_not_found(self):
        # Arrange
        self.mock_external_data_service.does_bucket_exist.return_value = False
        # Act
        response = self.test_service.copy_new_and_update("bucket", None)
        # Assert
        self.mock_external_data_service.perform_transfer.assert_not_called()
        self.mock_logger.warning.assert_called_with('Warning, bucket does not exist (bucket)')
        assert response == {'message': 'Warning, bucket does not exist (bucket)',
                            'new files uploaded': 0,
                            'files updated': 0,
                            'files skipped': 0,
                            'data transferred (bytes)': 0}

    def test_copy_new_and_update_return_message_when_no_new_files_to_transfer_or_update(self):
        # Arrange
        self._set_up_system(does_bucket_exists=True,
                            objects_in_bucket=[self.mock_object_1],
                            files_in_system=[self.mock_file_information_1])
        mock_file_summary = build_mock_file_summary(files_in_dir=[self.mock_file_information_1],
                                                    files_to_be_skipped=[self.mock_file_information_1])
        self.mock_storage_difference_processor.return_difference_comparison.return_value = mock_file_summary
        # Act
        response = self.test_service.copy_new_and_update("bucket", None)
        # Assert
        self.mock_external_data_service.perform_transfer.assert_not_called()
        self.mock_storage_difference_processor.return_difference_comparison.assert_called_with(
            [self.mock_object_1],
            [self.mock_file_information_1],
            check_for_updates=True
        )
        self.mock_logger.info.assert_called_with('No new or updated files found in directory (root)')
        assert response == {'message': 'No new or updated files found in directory (root)',
                            'new files uploaded': 0,
                            'files updated': 0,
                            'files skipped': 1,
                            'data transferred (bytes)': 0}

    def test_copy_new_and_update_return_message_directory_does_not_exist(self):
        # Arrange
        self._set_up_system(does_bucket_exists=True, objects_in_bucket=self.mock_object_1)
        # Act
        response = self.test_service.copy_new_and_update("bucket", None)
        # Assert
        self.mock_external_data_service.perform_transfer.assert_not_called()
        self.mock_logger.warning.assert_called_with('No files found in directory or directory does not exist (root)')
        assert response == {'message': 'No files found in directory or directory does not exist (root)',
                            'new files uploaded': 0,
                            'files updated': 0,
                            'files skipped': 0,
                            'data transferred (bytes)': 0}

    def test_copy_new_and_update_return_message_when_new_files_transferred_and_files_updated(self):
        # Arrange
        self._set_up_system(does_bucket_exists=True,
                            objects_in_bucket=[self.mock_object_1, self.mock_object_3],
                            files_in_system=[self.mock_file_information_1,
                                             self.mock_file_information_2,
                                             self.mock_file_information_3])
        mock_file_summary = build_mock_file_summary(files_in_dir=[self.mock_file_information_1,
                                                                  self.mock_file_information_2,
                                                                  self.mock_file_information_3],
                                                    new_files=[self.mock_file_information_2],
                                                    updated_files=[self.mock_file_information_3],
                                                    files_to_be_skipped=[self.mock_file_information_1])
        self.mock_storage_difference_processor.return_difference_comparison.return_value = mock_file_summary
        self.mock_external_data_service.perform_transfer.return_value = build_transfer_return(1, 1, 1, 46)
        # Act
        response = self.test_service.copy_new_and_update("bucket", "some_dir")
        # Assert
        self.mock_external_data_service.perform_transfer.assert_called_once_with("bucket", mock_file_summary)
        self.mock_storage_difference_processor.return_difference_comparison.assert_called_with(
            [self.mock_object_1, self.mock_object_3],
            [self.mock_file_information_1, self.mock_file_information_2, self.mock_file_information_3],
            check_for_updates=True
        )
        assert response == {'message': 'Transfer successful',
                            'new files uploaded': 1,
                            'files updated': 1,
                            'files skipped': 1,
                            'data transferred (bytes)': 46}

    def test_copy_new_and_update_transfers_all_files_when_no_objects_already_in_bucket(self):
        # Arrange
        self._set_up_system(does_bucket_exists=True,
                            files_in_system=[self.mock_file_information_1, self.mock_file_information_2])
        mock_file_summary = build_mock_file_summary()
        mock_file_summary.new_files = [self.mock_file_information_1, self.mock_file_information_2]
        self.mock_storage_difference_processor.return_difference_comparison.return_value = mock_file_summary
        self.mock_external_data_service.perform_transfer.return_value = build_transfer_return(2, 0, 0, 46)
        # Act
        response = self.test_service.copy_new_and_update("bucket", None)
        # Assert
        self.mock_external_data_service.perform_transfer.assert_called_once_with("bucket", mock_file_summary)
        self.mock_storage_difference_processor.return_difference_comparison.assert_called_with(
            [],
            [self.mock_file_information_1,
             self.mock_file_information_2],
            check_for_updates=True
        )
        assert response == {'message': 'Transfer successful',
                            'new files uploaded': 2,
                            'files updated': 0,
                            'files skipped': 0,
                            'data transferred (bytes)': 46}

    def test_check_bucket_warning_returns_waning_when_bucket_name_is_not_valid(self):
        # Act
        response = self.test_service._check_bucket_warning("bu")
        # Assert
        self.mock_logger.warning.assert_called_with("Bucket name breaks S3 naming convention (bu)")
        assert response == "Bucket name breaks S3 naming convention (bu)"

    def test_check_bucket_warning_returns_waning_when_bucket_does_not_match_configuration(self):
        # Arrange
        self.mock_external_data_service.does_bucket_match_standard.return_value = False
        # Act
        response = self.test_service._check_bucket_warning("bucket")
        # Assert
        self.mock_logger.warning.assert_called_with("Bucket breaks local naming standard (bucket)")
        assert response == "Bucket breaks local naming standard (bucket)"

    def test_check_bucket_warning_returns_waning_when_bucket_does_not_exist(self):
        # Arrange
        self.mock_external_data_service.does_bucket_match_standard.return_value = True
        self.mock_external_data_service.does_bucket_exist.return_value = False
        # Act
        response = self.test_service._check_bucket_warning("bucket")
        # Assert
        self.mock_logger.warning.assert_called_with("Warning, bucket does not exist (bucket)")
        assert response == "Warning, bucket does not exist (bucket)"

    def test_check_bucket_warning_returns_none_when_no_warnings(self):
        # Arrange
        self.mock_external_data_service.does_bucket_match_standard.return_value = True
        self.mock_external_data_service.does_bucket_exist.return_value = True
        # Act
        response = self.test_service._check_bucket_warning("bucket")
        # Assert
        self.mock_logger.debug.assert_called_with("No bucket related warnings found")
        self.mock_logger.warning.assert_not_called()
        assert response is None
