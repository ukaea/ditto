# pylint: disable=W0201, W0212
import logging
import mock
import pytest

from DittoWebApi.src.services.external.external_data_service import ExternalDataService
from DittoWebApi.src.services.external.storage_adapters.boto_bucket import BotoBucket
from DittoWebApi.src.services.external.storage_adapters.boto_bucket import BotoKey
from DittoWebApi.src.services.external.storage_adapters.is3_adapter import IS3Adapter
from DittoWebApi.src.models.s3_object_information import S3ObjectInformation
from DittoWebApi.src.models.file_information import FileInformation
from DittoWebApi.src.models.file_storage_summary import FilesStorageSummary
from DittoWebApi.src.utils.configurations import Configuration
from DittoWebApi.src.utils.file_system.files_system_helpers import FileSystemHelper
from DittoWebApi.src.utils.return_status import StatusCodes


class TestExternalDataServices:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_logger = mock.create_autospec(logging.RootLogger, spec_set=False)
        mock_configuration = mock.create_autospec(Configuration)
        mock_configuration.bucket_standard = "test"
        mock_configuration.s3_url = "example"
        mock_configuration.s3_access_key = "example"
        mock_configuration.s3_secret_key = "example"
        mock_configuration.s3_use_secure = "example"
        self.mock_s3_client = mock.create_autospec(IS3Adapter)
        self.mock_logger = mock.create_autospec(logging.Logger)
        self.mock_file_system_helper = mock.create_autospec(FileSystemHelper)
        self.test_service = ExternalDataService(
            mock_configuration,
            self.mock_file_system_helper,
            self.mock_logger,
            self.mock_s3_client
        )

    @staticmethod
    def get_mock_key(name, bucket, etag, size, last_modified):
        mock_key = mock.create_autospec(BotoKey)
        mock_key.name = name
        mock_key.bucket = bucket
        mock_key.etag = etag
        mock_key.size = size
        mock_key.last_modified = last_modified
        return mock_key

    # create_bucket

    def test_create_bucket_reports_s3_client_success(self):
        # Arrange
        self.mock_s3_client.make_bucket.return_value = True
        # Act
        output = self.test_service.create_bucket("test-bucket")
        # Assert
        assert output is True
        self.mock_logger.debug.assert_called_once_with('Created bucket "test-bucket"')

    def test_create_bucket_reports_s3_client_failure(self):
        # Arrange
        self.mock_s3_client.make_bucket.return_value = False
        # Act
        output = self.test_service.create_bucket("test-bucket")
        # Assert
        assert output is False
        self.mock_logger.debug.assert_called_once_with('Could not create bucket "test-bucket"')

    # does_bucket_exist

    def test_does_bucket_exist_returns_true_when_bucket_retrieved(self):
        # Arrange
        mock_bucket = mock.create_autospec(BotoBucket)
        self.mock_s3_client.get_bucket.return_value = mock_bucket
        # Act
        output = self.test_service.does_bucket_exist("test-bucket")
        # Assert
        assert output is True
        self.mock_logger.debug.assert_called_once_with('Bucket "test-bucket" does exist')

    def test_does_bucket_exist_returns_true_when_s3_returns_none(self):
        # Arrange
        self.mock_s3_client.get_bucket.return_value = None
        # Act
        output = self.test_service.does_bucket_exist("test-bucket")
        # Assert
        assert output is False
        self.mock_logger.debug.assert_called_once_with('Bucket "test-bucket" does not exist')

    # does_bucket_match_standard

    @pytest.mark.parametrize("bucket_name", ["test1234", "TEST-1234", "tes", ""])
    def test_does_bucket_match_standard_catches_invalid_bucket_name(self, bucket_name):
        result = self.test_service.does_bucket_match_standard(bucket_name)
        assert result is False

    def test_does_bucket_match_standard_allows_valid_bucket_name(self):
        bucket_name = "test-1234"
        result = self.test_service.does_bucket_match_standard(bucket_name)
        assert result is True

    # does_dir_exist

    @pytest.mark.parametrize("dir_path", [None, "", " ", "  "])
    def test_does_dir_exist_returns_false_if_dir_path_empty_and_bucket_exists_and_is_empty(self, dir_path):
        # Act
        result = self.test_service.does_dir_exist("test-bucket", dir_path)
        # Assert
        assert result is False

    @pytest.mark.parametrize("dir_path", [None, "", " ", "  "])
    def test_does_dir_exist_returns_true_if_dir_path_empty_and_bucket_exists_and_contains_dir(self, dir_path):
        # Arrange
        mock_bucket = mock.create_autospec(BotoBucket)
        mock_key_1 = TestExternalDataServices.get_mock_key(
            'mock_object_1',
            mock_bucket,
            'test_etag_1',
            42,
            '2018-11-16T17:07:08.851Z'
        )
        mock_bucket.list.return_value = [mock_key_1]
        self.mock_s3_client.get_bucket.return_value = mock_bucket
        # Act
        result = self.test_service.does_dir_exist("test-bucket", dir_path)
        # Assert
        assert result is True

    def test_does_dir_exist_returns_false_if_bucket_does_not_exist(self):
        # Arrange
        self.mock_s3_client.get_bucket.return_value = None
        # Act
        result = self.test_service.does_dir_exist("test-bucket", "testdir")
        # Assert
        self.mock_logger.warning.assert_called_once_with(
            'Tried to find directory "testdir" in non-existent bucket "test-bucket"'
        )
        assert result is False

    def test_does_dir_exist_returns_true_if_item_is_in_directory(self):
        # Arrange
        mock_bucket = mock.create_autospec(BotoBucket)
        mock_key_1 = TestExternalDataServices.get_mock_key(
            'mock_object_1',
            mock_bucket,
            'test_etag_1',
            42,
            '2018-11-16T17:07:08.851Z'
        )
        mock_bucket.list.return_value = [mock_key_1]
        self.mock_s3_client.get_bucket.return_value = mock_bucket
        # Act
        result = self.test_service.does_dir_exist("test-bucket", "testdir")
        # Assert
        assert result is True

    def test_does_dir_exist_returns_false_if_directory_is_empty(self):
        # Arrange
        mock_bucket = mock.create_autospec(BotoBucket)
        mock_bucket.list.return_value = []
        self.mock_s3_client.get_bucket.return_value = mock_bucket
        # Act
        result = self.test_service.does_dir_exist("test-bucket", "testdir")
        # Assert
        assert result is False

    # get_objects

    def test_does_object_exist_returns_empty_array_if_bucket_does_not_exist(self):
        # Arrange
        self.mock_s3_client.get_bucket.return_value = None
        # Act
        result = self.test_service.get_objects("test-bucket", "testdir")
        # Assert
        self.mock_s3_client.get_bucket.assert_called_once_with("test-bucket")
        self.mock_logger.warning.assert_called_once_with(
            'Tried to get objects from non-existent bucket "test-bucket"'
        )
        assert isinstance(result, list)
        assert not result

    def test_get_objects_returns_correct_object_when_one_exists(self):
        # Arrange
        mock_bucket = mock.create_autospec(BotoBucket)
        mock_bucket.name = 'test-bucket'
        mock_key_1 = TestExternalDataServices.get_mock_key(
            'mock_object_1',
            mock_bucket,
            'test_etag_1',
            42,
            '2018-11-16T17:07:08.851Z'
        )
        mock_bucket.list.return_value = [mock_key_1]
        self.mock_s3_client.get_bucket.return_value = mock_bucket
        # Act
        result = self.test_service.get_objects('test-bucket', None)
        # Assert
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], S3ObjectInformation)
        assert result[0].object_name == 'mock_object_1'
        assert result[0].bucket_name == 'test-bucket'
        assert result[0].size == 42
        assert result[0].etag == 'test_etag_1'
        assert result[0].last_modified == 1542388028.851

    def test_get_objects_returns_correct_objects_when_they_exist(self):
        # Arrange
        mock_bucket = mock.create_autospec(BotoBucket)
        mock_bucket.name = 'test-bucket'
        mock_key_1 = TestExternalDataServices.get_mock_key(
            'mock_object_1',
            mock_bucket,
            'test_etag_1',
            42,
            '2018-11-16T17:07:08.851Z'
        )
        mock_key_2 = TestExternalDataServices.get_mock_key(
            'mock_object_2',
            mock_bucket,
            'test_etag_2',
            33,
            '2016-05-07T10:30:00.000Z'
        )
        mock_bucket.list.return_value = [mock_key_1, mock_key_2]
        self.mock_s3_client.get_bucket.return_value = mock_bucket
        # Act
        result = self.test_service.get_objects('test-bucket', None)
        # Assert
        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], S3ObjectInformation)
        assert result[0].object_name == 'mock_object_1'
        assert isinstance(result[1], S3ObjectInformation)
        assert result[1].object_name == 'mock_object_2'

    def test_get_objects_returns_empty_array_when_no_objects_exist(self):
        # Arrange
        mock_bucket = mock.create_autospec(BotoBucket)
        mock_bucket.list.return_value = []
        self.mock_s3_client.get_bucket.return_value = mock_bucket
        # Act
        result = self.test_service.get_objects("test-bucket", None)
        # Assert
        assert isinstance(result, list)
        assert not result

    # does_object_exist

    def test_does_object_exist_returns_false_if_bucket_does_not_exist(self):
        # Arrange
        self.mock_s3_client.get_bucket.return_value = None
        # Act
        result = self.test_service.does_object_exist("test-bucket", "test.txt")
        # Assert
        self.mock_s3_client.get_bucket.assert_called_once_with("test-bucket")
        self.mock_logger.warning.assert_called_once_with(
            'Tried to find object "test.txt" in non-existent bucket "test-bucket"'
        )
        assert result is False

    def test_does_object_exist_returns_true_when_it_exists(self):
        # Arrange
        mock_bucket = mock.create_autospec(BotoBucket)
        mock_bucket.get_key.return_value = "Object"
        self.mock_s3_client.get_bucket.return_value = mock_bucket
        # Act
        result = self.test_service.does_object_exist("test-bucket", "test.txt")
        # Assert
        self.mock_s3_client.get_bucket.assert_called_once_with("test-bucket")
        mock_bucket.get_key.assert_called_once_with("test.txt")
        assert result is True

    def test_does_object_exist_returns_false_when_no_object(self):
        # Arrange
        mock_bucket = mock.create_autospec(BotoBucket)
        mock_bucket.get_key.return_value = None
        self.mock_s3_client.get_bucket.return_value = mock_bucket
        # Act
        result = self.test_service.does_object_exist("test-bucket", "test.txt")
        # Assert
        self.mock_s3_client.get_bucket.assert_called_once_with("test-bucket")
        mock_bucket.get_key.assert_called_once_with("test.txt")
        assert result is False

    # delete_file

    def test_delete_file_returns_false_if_bucket_does_not_exist(self):
        # Arrange
        self.mock_s3_client.get_bucket.return_value = None
        file_rel_path = "test.txt"
        # Act
        result = self.test_service.delete_file("test-bucket", file_rel_path)
        # Assert
        self.mock_s3_client.get_bucket.assert_called_once_with("test-bucket")
        self.mock_logger.warning.assert_called_once_with(
            'Tried to delete object "test.txt" from non-existent bucket "test-bucket"'
        )
        assert result is False

    def test_delete_file_returns_false_if_object_does_not_exist(self):
        # Arrange
        mock_bucket = mock.create_autospec(BotoBucket)
        mock_bucket.get_key.return_value = None
        self.mock_s3_client.get_bucket.return_value = mock_bucket
        file_rel_path = "test.txt"
        # Act
        result = self.test_service.delete_file("test-bucket", file_rel_path)
        # Assert
        self.mock_s3_client.get_bucket.assert_called_once_with("test-bucket")
        mock_bucket.get_key.assert_called_once_with("test.txt")
        self.mock_logger.warning.assert_called_once_with(
            'Tried to delete non-existent object "test.txt" from bucket "test-bucket"'
        )
        assert result is False

    def test_delete_file_returns_true_if_object_does_exist(self):
        # Arrange
        mock_bucket = mock.create_autospec(BotoBucket)
        mock_key = TestExternalDataServices.get_mock_key(
            'test.txt',
            mock_bucket,
            'test_etag_1',
            42,
            '2018-11-16T17:07:08.851Z'
        )
        mock_bucket.get_key.return_value = mock_key
        self.mock_s3_client.get_bucket.return_value = mock_bucket
        file_rel_path = "test.txt"
        # Act
        result = self.test_service.delete_file("test-bucket", file_rel_path)
        # Assert
        self.mock_s3_client.get_bucket.assert_called_once_with("test-bucket")
        mock_bucket.get_key.assert_called_once_with("test.txt")
        mock_key.delete.assert_called_once()
        self.mock_logger.debug.assert_called_once_with('Deleted object "test.txt" from bucket "test-bucket"')
        assert result is True

    def test_upload_creates_correct_logging_and_returns_file_size_with_bucket_name(self):
        # Arrange
        bucket_name = "bucket"
        mock_file_1 = mock.create_autospec(FileInformation)
        mock_file_1.rel_path = "test_file_1.txt"
        mock_file_1.abs_path = "C:/root/test_file_1.txt"
        mock_boto_bucket = mock.create_autospec(BotoBucket)
        mock_boto_key = mock.create_autospec(BotoKey)
        mock_boto_bucket.get_key.return_value = mock_boto_key
        self.mock_s3_client.get_bucket.return_value = mock_boto_bucket
        self.mock_file_system_helper.file_size.return_value = 12
        # Act
        output = self.test_service.upload_file(bucket_name, mock_file_1)
        # Assert
        self.mock_logger.debug.assert_any_call('File "test_file_1.txt" uploaded, 12 bytes transferred')
        mock_boto_key.set_contents_from_filename.assert_called_once_with("C:/root/test_file_1.txt")
        assert output == 12

    def test_upload_creates_returns_false_when_bucket_does_not_exist(self):
        # Arrange
        bucket_name = "bucket"
        self.mock_s3_client.get_bucket.return_value = None
        # Act
        output = self.test_service.upload_file(bucket_name, "file_1")
        # Assert
        assert output is False

    def test_perform_transfer_return_correct_summary_of_files(self):
        # Arrange
        bucket_name = "bucket"
        file_summary = mock.create_autospec(FilesStorageSummary)
        mock_file_1 = mock.create_autospec(FileInformation)
        mock_file_1.rel_path = "test_file_1.txt"
        mock_file_2 = mock.create_autospec(FileInformation)
        mock_file_2.rel_path = "test_file_2.txt"
        mock_file_3 = mock.create_autospec(FileInformation)
        mock_file_3.rel_path = "test_file_3.txt"
        file_summary.new_files = [mock_file_1]
        file_summary.updated_files = [mock_file_2]
        file_summary.files_to_be_skipped.return_value = [mock_file_3]
        self.test_service.upload_file = mock.Mock()
        self.test_service.upload_file.side_effect = [12, 14]
        # Act
        output = self.test_service.perform_transfer(bucket_name, file_summary)
        # Assert
        assert output == {"message": "Transfer successful",
                          "new_files_uploaded": 1,
                          "files_updated": 1,
                          "files_skipped": 1,
                          "data_transferred": 26,
                          "status": StatusCodes.Okay}
        self.mock_logger.debug.assert_any_call("New files transferred: ['test_file_1.txt']")
        self.mock_logger.debug.assert_any_call("Files updated: ['test_file_2.txt']")
        self.mock_logger.debug.assert_any_call("Files not uploaded or updated: ['test_file_3.txt']")
