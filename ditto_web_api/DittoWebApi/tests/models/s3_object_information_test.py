import datetime
import unittest

from DittoWebApi.src.models.s3_object_information import S3ObjectInformation


class TestS3ObjectInformation(unittest.TestCase):
    def test_s3_object_information_is_correctly_converted_to_dictionary(self):
        # Arrange
        test_object = S3ObjectInformation.create(
            "test_1.txt",
            "bucket_1_test",
            100,
            "test_etag",
            datetime.datetime(2018, 11, 15)
        )
        # Act
        output = test_object.to_dict()
        # Assert
        assert output == {'object_name': 'test_1.txt',
                          'bucket_name': 'bucket_1_test',
                          'size': 100,
                          'etag': 'test_etag',
                          'last modified': 1542240000.0}
        self.assertIsInstance(output, dict)
