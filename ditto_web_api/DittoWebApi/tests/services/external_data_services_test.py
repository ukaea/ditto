# pylint: disable=W0201, W0212
import datetime
import mock
import pytest

from DittoWebApi.src.services.external.external_data_service import ExternalDataService
from DittoWebApi.src.utils.configurations import Configuration
from DittoWebApi.src.services.external.storage_adapters.minio_adaptor import MinioAdapter
from DittoWebApi.src.models.bucket_information import BucketInformation
from DittoWebApi.src.models.s3_object_information import S3ObjectInformation
from minio.error import NoSuchKey


class TestExternalDataServices:
    @pytest.fixture(autouse=True)
    def setup(self):
        mock_configuration = mock.create_autospec(Configuration)
        mock_configuration.bucket_standard = "test"
        mock_configuration.s3_url = "example"
        mock_configuration.s3_access_key = "example"
        mock_configuration.s3_secret_key = "example"
        mock_configuration.s3_use_secure = "example"
        self.external_data_services = ExternalDataService(mock_configuration)
        mock_s3_client = mock.create_autospec(MinioAdapter)
        self.external_data_services._s3_client = mock_s3_client
        # Create mock buckets
        self.mock_bucket_1 = mock.create_autospec(BucketInformation)
        self.mock_bucket_2 = mock.create_autospec(BucketInformation)
        self.mock_bucket_1.name = "bucket1"
        self.mock_bucket_1.creation_date = "17/11/18"
        self.mock_bucket_2.name = "bucket2"
        self.mock_bucket_2.creation_date = "10/10/18"
        # Create mock s3 objects
        self.mock_object_1 = mock.create_autospec(S3ObjectInformation)
        self.mock_object_1.is_dir = False
        self.mock_object_1.object_name = 'mock_object_1'
        self.mock_object_1.bucket_name = 'mock_bucket_1'
        self.mock_object_1.size = 100
        self.mock_object_1.etag = 'test_etag'
        self.mock_object_1.last_modified = datetime.datetime(2018, 10, 11)
        self.mock_object_2 = mock.create_autospec(S3ObjectInformation)
        self.mock_object_2.is_dir = False
        self.mock_object_2.object_name = 'mock_object_2'
        self.mock_object_2.bucket_name = 'mock_bucket_1'
        self.mock_object_2.size = 100
        self.mock_object_2.etag = 'test_etag'
        self.mock_object_2.last_modified = datetime.datetime(2018, 8, 10)

    def test_get_buckets_returns_list_of_buckets_when_they_exist(self):
        # Arrange
        self.external_data_services._s3_client.list_buckets.return_value = [self.mock_bucket_1, self.mock_bucket_2]
        # Act
        results = self.external_data_services.get_buckets()
        # Assert
        assert results[0].name == self.mock_bucket_1.name
        assert results[0].creation_date == self.mock_bucket_1.creation_date

        assert results[1].name == self.mock_bucket_2.name
        assert results[1].creation_date == self.mock_bucket_2.creation_date

        assert len(results) == 2

    def test_get_buckets_returns_empty_list_when_none_exist(self):
        # Arrange
        self.external_data_services._s3_client.list_buckets.return_value = []
        # Act
        result = self.external_data_services.get_buckets()
        # Assert
        assert result == []

    def test_get_objects_returns_no_objects_when_none_exist(self):
        # Arrange
        self.external_data_services._s3_client.list_objects.return_value = []
        buckets = [self.mock_bucket_1, self.mock_bucket_2]
        # Act
        result = self.external_data_services.get_objects(buckets, None)
        # Assert
        assert result == []

    def test_get_objects_returns_correct_objects_when_they_exist(self):
        # Arrange
        self.external_data_services._s3_client.list_objects.return_value = [self.mock_object_1, self.mock_object_2]
        buckets = [self.mock_bucket_1]
        # Act
        result = self.external_data_services.get_objects(buckets, None)
        # Assert
        assert result[0].object_name == "mock_object_1"
        assert result[1].object_name == "mock_object_2"
        assert len(result) == 2

    def test_does_dir_exist_returns_true_if_item_is_in_directory(self):
        # Arrange
        bucket = self.mock_bucket_1
        self.external_data_services._s3_client.list_objects.return_value = [self.mock_object_1]
        # Act
        result = self.external_data_services.does_dir_exist(None, bucket)
        # Assert
        assert result is True

    def test_does_dir_exist_returns_false_if_directory_is_empty(self):
        # Arrange
        bucket = self.mock_bucket_1
        self.external_data_services._s3_client.list_objects.return_value = []
        # Act
        result = self.external_data_services.does_dir_exist(None, bucket)
        # Assert
        assert result is False

    @pytest.mark.parametrize("valid_bucket_name", ["test1234", "TEST-1234", "tes", ""])
    def test_is_bucket_valid_locally_returns_false_if_bucket_name_does_not_agree_with_local_standards(self, valid_bucket_name):
        assert self.external_data_services.is_bucket_valid_locally(valid_bucket_name) is False

    def test_is_bucket_valid_locally_returns_true_if_bucket_name_does_agree_with_local_standards(self):
        assert self.external_data_services.is_bucket_valid_locally("test-1234") is True

    def test_does_object_exist_returns_true_when_object_exists(self):
        # Arrange
        self.external_data_services._s3_client.stat_object.return_value = ["Okay"]
        # Act
        result = self.external_data_services.does_object_exist(self.mock_object_1, self.mock_bucket_1)
        # Assert
        assert result is True

    def test_does_object_exist_returns_false_when_object_does_not_exist(self):
        # Arrange
        self.external_data_services._s3_client.stat_object.side_effect = NoSuchKey(1212)
        # Act
        result = self.external_data_services.does_object_exist(self.mock_object_1, self.mock_bucket_1)
        # Assert
        assert result is False
