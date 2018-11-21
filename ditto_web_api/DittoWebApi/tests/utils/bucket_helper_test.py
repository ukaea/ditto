import pytest
from DittoWebApi.src.utils.bucket_helper import is_valid_bucket


class TestBucketHelpers:
    @pytest.mark.parametrize("bucket_name", ["test-1234",
                                             "test-1234",
                                             "tes",
                                             "test123--12",
                                             "test.test",
                                             "123test",
                                             "a-test-that-is-just-as-long-as-is-allowed-here-with-the-limit63"])
    def test_is_valid_returns_true_for_s3_bucket_names_that_are_valid(self, bucket_name):
        # Arrange
        name_to_test = bucket_name
        # Act
        output = is_valid_bucket(name_to_test)
        # Assert
        assert output is True

    @pytest.mark.parametrize("bucket_name", ["Test-1234",
                                             "test-a-really-long-name-that-is-too-long-to-be-valid-with-the-s3-servers",
                                             "ts",
                                             "test123_12",
                                             "test!!",
                                             "",
                                             "test-",
                                             "tests-..bucketname"])
    def test_is_valid_returns_false_for_s3_bucket_names_that_are_invalid(self, bucket_name):
        # Arrange
        name_to_test = bucket_name
        # Act
        output = is_valid_bucket(name_to_test)
        # Assert
        assert output is False
