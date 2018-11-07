import unittest
import mock
from DittoWebApi.src.services.external_data_service import ExternalDataService


class TestExternalDataServices(unittest.TestCase):
    def test_valid_bucket_names_are_accepted(self):
        # Arrange
        mock_configuration = mock.Mock()
        mock_configuration.bucket_standard = "test"
        mock_configuration.s3_url = "example"
        mock_configuration.s3_access_key = "example"
        mock_configuration.s3_secret_key = "example"
        mock_configuration.s3_use_secure = "example"
        external_data_services = ExternalDataService(mock_configuration)
        bucket_name = "test-123esj"
        # Act
        valid = external_data_services.valid_bucket(bucket_name)
        # Assert
        self.assertTrue(valid)

    def test_invalid_bucket_names_are_rejected(self):
        mock_configuration = mock.Mock()
        mock_configuration.bucket_standard = "test"
        mock_configuration.s3_url = "example"
        mock_configuration.s3_access_key = "example"
        mock_configuration.s3_secret_key = "example"
        mock_configuration.s3_use_secure = "example"
        external_data_services = ExternalDataService(mock_configuration)
        bucket_name_1 = "test123esj"
        bucket_name_2 = "badstart-112e2"
        bucket_name_3 = ""
        # Act
        valid_1 = external_data_services.valid_bucket(bucket_name_1)
        valid_2 = external_data_services.valid_bucket(bucket_name_2)
        valid_3 = external_data_services.valid_bucket(bucket_name_3)
        self.assertFalse(valid_1)
        self.assertFalse(valid_2)
        self.assertFalse(valid_3)
