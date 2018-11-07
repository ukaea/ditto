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
        bucket_name_1 = "test-123esj"
        bucket_name_2 = "test--.123esjs"
        # Act
        valid_1 = external_data_services.valid_bucket(bucket_name_1)
        valid_2 = external_data_services.valid_bucket(bucket_name_2)
        # Assert
        self.assertTrue(valid_1)
        self.assertTrue(valid_2)

    def test_invalid_bucket_names_are_rejected(self):
        mock_configuration = mock.Mock()
        mock_configuration.bucket_standard = "test"
        mock_configuration.s3_url = "example"
        mock_configuration.s3_access_key = "example"
        mock_configuration.s3_secret_key = "example"
        mock_configuration.s3_use_secure = "example"
        external_data_services = ExternalDataService(mock_configuration)
        bucket_name_1 = "test123esj--in-wrong-place"
        bucket_name_2 = "badstart-112e2"
        bucket_name_3 = ""
        bucket_name_4 = "test-include-CAPITALs"
        bucket_name_5 = "test-invalid-last-character-"
        bucket_name_6 = "test-including..ohd-ear"
        bucket_name_7 = "test-a-bucket-name-that-is-way-too-long-to-be-accepted-but-otherwise-would-be-fine"
        # Act
        valid_1 = external_data_services.valid_bucket(bucket_name_1)
        valid_2 = external_data_services.valid_bucket(bucket_name_2)
        valid_3 = external_data_services.valid_bucket(bucket_name_3)
        valid_4 = external_data_services.valid_bucket(bucket_name_4)
        valid_5 = external_data_services.valid_bucket(bucket_name_5)
        valid_6 = external_data_services.valid_bucket(bucket_name_6)
        valid_7 = external_data_services.valid_bucket(bucket_name_7)
        self.assertFalse(valid_1)
        self.assertFalse(valid_2)
        self.assertFalse(valid_3)
        self.assertFalse(valid_4)
        self.assertFalse(valid_5)
        self.assertFalse(valid_6)
        self.assertFalse(valid_7)
