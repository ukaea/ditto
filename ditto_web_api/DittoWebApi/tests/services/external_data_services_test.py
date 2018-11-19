# pylint: disable=W0201, W0212
import logging
import mock
import pytest

from DittoWebApi.src.services.external.external_data_service import ExternalDataService
from DittoWebApi.src.services.external.storage_adapters.boto_bucket import BotoBucket
from DittoWebApi.src.services.external.storage_adapters.boto_bucket import BotoKey
from DittoWebApi.src.services.external.storage_adapters.is3_adapter import IS3Adapter
from DittoWebApi.src.models.s3_object_information import S3ObjectInformation
from DittoWebApi.src.utils.configurations import Configuration


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
        self.test_service = ExternalDataService(
            mock_configuration,
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
    def test_does_dir_exist_returns_false_if_dir_path_empty(self, dir_path):
        # Act
        result = self.test_service.does_dir_exist("test-bucket", dir_path)
        # Assert
        assert result is False
        self.mock_logger.warning.assert_called_once_with(
            f'Tried to find empty directory path "{dir_path}"'
        )

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
