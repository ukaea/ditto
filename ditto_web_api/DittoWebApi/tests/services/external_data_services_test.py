# pylint: disable=W0201, W0212
from boto.s3.bucket import Bucket
import datetime
import logging
import mock
import pytest

from DittoWebApi.src.services.external.external_data_service import ExternalDataService
from DittoWebApi.src.utils.configurations import Configuration
from DittoWebApi.src.services.external.storage_adapters.is3_adapter import IS3Adapter
from DittoWebApi.src.models.s3_object_information import S3ObjectInformation


class TestExternalDataServices:
    @pytest.fixture(autouse=True)
    def setup(self):
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
        # Create mock buckets
        self.mock_bucket = mock.create_autospec(Bucket)
        # Create mock s3 objects
        self.mock_object_1 = S3ObjectInformation.create('mock_object_1',
                                                        'mock_bucket_1',
                                                        False,
                                                        100,
                                                        'test_etag',
                                                        datetime.datetime(2018, 10, 11))
        self.mock_object_2 = S3ObjectInformation.create('mock_object_2',
                                                        'mock_bucket_1',
                                                        False,
                                                        100,
                                                        'test_etag',
                                                        datetime.datetime(2018, 8, 10))

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
        mock_bucket = mock.create_autospec(Bucket)
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
        result = self.external_data_services.does_bucket_match_standard(bucket_name)
        assert result is True

    # does_dir_exist

    @pytest.mark.parametrize("dir_path", [None, "", " ", "  "])
    def test_does_dir_exist_returns_false_if_dir_path_empty(self, dir_path):
        # Act
        result = self.test_service.does_dir_exist("test-bucket", dir_path)
        # Assert
        assert result is False
        self.mock_logger.debug.assert_called_once_with(
            f'Tried to find empty directory path "{dir_path}"'
        )

    def test_does_dir_exist_returns_false_if_bucket_does_not_exist(self):
        # Arrange
        self.mock_s3_client.get_bucket.return_value = None
        # Act
        result = self.test_service.does_dir_exist("test-bucket", "testdir")
        # Assert
        self.mock_logger.debug.assert_called_once_with(
            'Tried to find directory "testdir" in non-existent bucket "test-bucket"'
        )
        assert result is False

    def test_does_dir_exist_returns_true_if_item_is_in_directory(self):
        # Arrange
        mock_bucket = mock.create_autospec(Bucket)
        mock_bucket.list.return_value = [self.mock_object_1]
        self.mock_s3_client.get_bucket.return_value = mock_bucket
        # Act
        result = self.test_service.does_dir_exist("test-bucket", "testdir")
        # Assert
        assert result is True

    def test_does_dir_exist_returns_false_if_directory_is_empty(self):
        # Arrange
        mock_bucket = mock.create_autospec(Bucket)
        mock_bucket.list.return_value = []
        self.mock_s3_client.get_bucket.return_value = mock_bucket
        # Act
        result = self.test_service.does_dir_exist("test-bucket", "testdir")
        # Assert
        assert result is False

    # get_objects

    @pytest.mark.parametrize("dir_path", [None, "testdir"])
    def test_does_object_exist_returns_empty_array_if_bucket_does_not_exist(self, dir_path):
        # Arrange
        self.mock_s3_client.get_bucket.return_value = None
        # Act
        result = self.test_service.get_objects("test-bucket", None)
        # Assert
        self.mock_s3_client.get_bucket.assert_called_once_with("test-bucket")
        self.mock_logger.warning.assert_called_once_with(
            'Tried to get objects from non-existent bucket "test-bucket"'
        )
        assert len(result) == 0

    def test_get_objects_returns_correct_objects_when_they_exist(self):
        # Arrange
        mock_bucket = mock.create_autospec(Bucket)
        mock_bucket.list.return_value = [self.mock_object_1, self.mock_object_2]
        self.mock_s3_client.get_bucket.return_value = mock_bucket
        # Act
        result = self.test_service.get_objects("test-bucket", None)
        # Assert
        assert result[0].object_name == "mock_object_1"
        assert result[1].object_name == "mock_object_2"
        assert len(result) == 2

    def test_get_objects_returns_empty_array_when_no_objects_exist(self):
        # Arrange
        mock_bucket = mock.create_autospec(Bucket)
        mock_bucket.list.return_value = []
        self.mock_s3_client.get_bucket.return_value = mock_bucket
        # Act
        result = self.test_service.get_objects("test-bucket", None)
        # Assert
        assert len(result) == 0

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
        mock_bucket = mock.create_autospec(Bucket)
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
        mock_bucket = mock.create_autospec(Bucket)
        mock_bucket.get_key.return_value = None
        self.mock_s3_client.get_bucket.return_value = mock_bucket
        # Act
        result = self.test_service.does_object_exist("test-bucket", "test.txt")
        # Assert
        self.mock_s3_client.get_bucket.assert_called_once_with("test-bucket")
        mock_bucket.get_key.assert_called_once_with("test.txt")
        assert result is False


    @pytest.mark.parametrize("return_value", [True, False])
    def test_delete_file_wraps_the_s3_adapter_method(self, return_value):
        # Arrange
        self.test_service._s3_client.remove_object.return_value = return_value
        file_name = "some_file"
        bucket_name = "some_bucket"
        # Act
        response = self.external_data_services.delete_file(file_name, bucket_name)
        # Assert
        assert response is return_value
