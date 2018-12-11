from logging import Logger
import pytest
import mock
from mock import call

from DittoWebApi.src.services.data_replication.bucket_validator import BucketValidator
from DittoWebApi.src.services.external.external_data_service import ExternalDataService


class TestBucketValidator:
    # pylint: disable=attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_external_data_service = mock.create_autospec(ExternalDataService)
        self.mock_logger = mock.create_autospec(Logger)

        self.test_validator = BucketValidator(self.mock_external_data_service, self.mock_logger)

    @pytest.mark.parametrize("bucket_name", ["Test-1234",
                                             "test-a-really-long-name-that-is-too-long-to-be-valid-with-the-s3-servers",
                                             "ts",
                                             "test123_12",
                                             "test!!",
                                             "",
                                             "test-",
                                             "tests-..bucketname",
                                             "test-bucket-.name",
                                             "test-bucket.-name"])
    def test_check_bucket_returns_warning_when_bucket_name_invalid(self, bucket_name):
        # Act
        bucket_warning = self.test_validator.check_bucket(bucket_name)
        # Assert
        self.mock_logger.debug.assert_called_once_with(
            f'About to check for warning to do with bucket name {bucket_name}')
        self.mock_logger.warning.assert_called_once_with(
            f'Bucket name breaks S3 naming convention ({bucket_name})')
        assert bucket_warning == f'Bucket name breaks S3 naming convention ({bucket_name})'

    def test_check_bucket_returns_warning_when_bucket_name_not_standard(self):
        # Arrange
        bucket_name = 'wrong-bucket'
        self.mock_external_data_service.does_bucket_match_standard.return_value = False
        # Act
        bucket_warning = self.test_validator.check_bucket(bucket_name)
        # Assert
        self.mock_logger.debug.assert_called_once_with('About to check for warning to do with bucket name wrong-bucket')
        self.mock_external_data_service.does_bucket_match_standard.assert_called_once_with('wrong-bucket')
        self.mock_logger.warning.assert_called_once_with('Bucket breaks local naming standard (wrong-bucket)')
        assert bucket_warning == 'Bucket breaks local naming standard (wrong-bucket)'

    def test_check_bucket_returns_warning_when_bucket_does_not_exist(self):
        # Arrange
        bucket_name = 'wrong-bucket'
        self.mock_external_data_service.does_bucket_match_standard.return_value = True
        self.mock_external_data_service.does_bucket_exist.return_value = False
        # Act
        bucket_warning = self.test_validator.check_bucket(bucket_name)
        # Assert
        self.mock_logger.debug.assert_called_once_with('About to check for warning to do with bucket name wrong-bucket')
        self.mock_external_data_service.does_bucket_match_standard.assert_called_once_with('wrong-bucket')
        self.mock_external_data_service.does_bucket_exist.assert_called_once_with('wrong-bucket')
        self.mock_logger.warning.assert_called_once_with('Warning, bucket does not exist (wrong-bucket)')
        assert bucket_warning == 'Warning, bucket does not exist (wrong-bucket)'

    def test_check_bucket_validator_returns_none_when_bucket_exists(self):
        # Arrange
        bucket_name = 'test-bucket'
        self.mock_external_data_service.does_bucket_match_standard.return_value = True
        self.mock_external_data_service.does_bucket_exist.return_value = True
        # Act
        bucket_warning = self.test_validator.check_bucket(bucket_name)
        # Assert
        self.mock_external_data_service.does_bucket_match_standard.assert_called_once_with('test-bucket')
        self.mock_external_data_service.does_bucket_exist.assert_called_once_with('test-bucket')
        self.mock_logger.debug.assert_has_calls([
            call('About to check for warning to do with bucket name test-bucket'),
            call('No bucket related warnings found')
        ])
        assert bucket_warning is None
