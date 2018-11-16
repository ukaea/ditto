# pylint: disable=W0201, W0212
import datetime
import mock
import pytest

from DittoWebApi.src.services.external.external_data_service import ExternalDataService
from DittoWebApi.src.utils.configurations import Configuration
from DittoWebApi.src.services.external.storage_adapters.is3_adapter import IS3Adapter
from DittoWebApi.src.models.bucket_information import BucketInformation
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
        mock_s3_client = mock.create_autospec(IS3Adapter)
        self.external_data_services = ExternalDataService(mock_configuration, mock_s3_client)
        # Create mock buckets
        self.mock_bucket_1 = BucketInformation.create("bucket1", "17/11/18")
        self.mock_bucket_2 = BucketInformation.create("bucket2", "10/10/18")
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
    def test_does_bucket_match_standard_catches_invalid_bucket_name(self, valid_bucket_name):
        assert self.external_data_services.does_bucket_match_standard(valid_bucket_name) is False

    def test_does_bucket_match_standard_returns_true_if_bucket_name_does_agree_with_local_standards(self):
        assert self.external_data_services.does_bucket_match_standard("test-1234") is True

    @pytest.mark.parametrize("object_exists", [True, False])
    def test_does_object_exist_passes_s3_client_response(self, object_exists):
        # Arrange
        self.external_data_services._s3_client.object_exists.return_value = object_exists
        # Act
        result = self.external_data_services.does_object_exist(self.mock_object_1, self.mock_bucket_1)
        # Assert
        assert result is object_exists

    @pytest.mark.parametrize("return_value", [True, False])
    def test_delete_file_wraps_the_s3_adapter_method(self, return_value):
        # Arrange
        self.external_data_services._s3_client.remove_object.return_value = return_value
        file_name = "some_file"
        bucket_name = "some_bucket"
        # Act
        response = self.external_data_services.delete_file(file_name, bucket_name)
        # Assert
        assert response is return_value
