import unittest
import mock
import pytest
import datetime
from DittoWebApi.src.services.external.external_data_service import ExternalDataService
from DittoWebApi.src.utils.configurations import Configuration
from DittoWebApi.src.services.external.storage_adapters.minio_adaptor import MinioAdapter
from DittoWebApi.src.models.bucket_information import Bucket
from DittoWebApi.src.models.object_information import Object
from minio.error import NoSuchKey

class TestExternalDataServices(unittest.TestCase):
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
        self.mock_bucket_1 = mock.create_autospec(Bucket)
        self.mock_bucket_2 = mock.create_autospec(Bucket)
        self.mock_bucket_1.name = "Bucket_1"
        self.mock_bucket_1.creation_date = "17/11/18"
        self.mock_bucket_2.name = "Bucket_2"
        self.mock_bucket_2.creation_date = "10/10/18"
        self.mock_object_1 = mock.create_autospec(Object)
        self.mock_object_1.is_dir = False
        self.mock_object_1.object_name = 'mock_object_1'
        self.mock_object_1.bucket_name = 'mock_bucket_1'
        self.mock_object_1.size = 100
        self.mock_object_1.etag = 'test_etag'
        self.mock_object_1.last_modified = datetime.datetime(2018, 10, 11)
        self.mock_object_2 = mock.create_autospec(Object)
        self.mock_object_2.is_dir = False
        self.mock_object_2.object_name = 'mock_object_2'
        self.mock_object_2.bucket_name = 'mock_bucket_1'
        self.mock_object_2.size = 100
        self.mock_object_2.etag = 'test_etag'
        self.mock_object_2.last_modified = datetime.datetime(2018, 8, 10)

    def test_valid_bucket_names_are_accepted_by_is_valid_bucket(self):
        # Arrange
        bucket_name_1 = "test-123esj"
        bucket_name_2 = "test--.123esjs"
        # Act
        valid_1 = self.external_data_services.is_valid_bucket(bucket_name_1)
        valid_2 = self.external_data_services.is_valid_bucket(bucket_name_2)
        # Assert
        assert valid_1
        assert valid_2

    def test_invalid_bucket_names_are_rejected_by_is_valid_bucket(self):
        # Arrange
        bucket_name_1 = "test123esj--in-wrong-place"
        bucket_name_2 = "badstart-112e2"
        bucket_name_3 = ""
        # Act
        valid_1 = self.external_data_services.is_valid_bucket(bucket_name_1)
        valid_2 = self.external_data_services.is_valid_bucket(bucket_name_2)
        valid_3 = self.external_data_services.is_valid_bucket(bucket_name_3)
        # Assert
        assert not valid_1
        assert not valid_2
        assert not valid_3

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

    def test_get_buckets_returns_empty_list_when_none_exist(self):
        # Act
        self.external_data_services._s3_client.list_buckets.return_value = []
        # Assert
        assert not self.external_data_services.get_buckets()

    def test_get_objects_returns_no_objects_when_none_exist(self):
        # Arrange
        self.external_data_services._s3_client.list_objects.return_value = []
        buckets = [self.mock_bucket_1, self.mock_bucket_2]
        # Assert
        assert not self.external_data_services.get_objects(buckets, None)

    def test_get_objects_returns_correct_objects_when_they_exist(self):
        # Arrange
        self.external_data_services._s3_client.list_objects.return_value = [self.mock_object_1, self.mock_object_2]
        buckets = [self.mock_bucket_1, self.mock_bucket_2]
        # Assert
        assert self.external_data_services.get_objects(buckets, None)[0].object_name == "mock_object_1"
        assert self.external_data_services.get_objects(buckets, None)[1].object_name == "mock_object_2"

    def test_does_dir_exist_returns_true_if_item_is_in_directory(self):
        # Arrange
        bucket = self.mock_bucket_1
        # Act
        self.external_data_services._s3_client.list_objects.return_value = [self.mock_object_1]
        # Assert
        assert self.external_data_services.does_dir_exist(None, bucket)

    def test_does_dir_exist_returns_false_if_directory_is_empty(self):
        # Arrange
        bucket = self.mock_bucket_1
        # Act
        self.external_data_services._s3_client.list_objects.return_value = []
        # Assert
        assert not self.external_data_services.does_dir_exist(None, bucket)

    def test_valid_bucket_returns_true_if_bucket_name_agrees_with_local_standards(self):
        assert self.external_data_services.is_valid_bucket("test-1234")
        assert not self.external_data_services.is_valid_bucket("test1234")
        assert not self.external_data_services.is_valid_bucket("TEST-1234")
        assert not self.external_data_services.is_valid_bucket("")
        assert not self.external_data_services.is_valid_bucket("tes")

    def test_does_object_exist_returns_true_when_object_exists(self):
        self.external_data_services._s3_client.stat_object.return_value = ["Okay"]
        assert self.external_data_services.does_object_exist(self.mock_object_1, self.mock_bucket_1)

    def test_does_object_exist_returns_false_when_object_does_not_exist(self):
        self.external_data_services._s3_client.stat_object.side_effect = NoSuchKey(1212)
        assert not self.external_data_services.does_object_exist(self.mock_object_1, self.mock_bucket_1)
