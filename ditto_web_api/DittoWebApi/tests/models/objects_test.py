import pytest
import unittest
import mock
import datetime
from DittoWebApi.src.models.object import Object


class TestObjects(unittest.TestCase):


    def test_minio_object_is_correctly_converted_to_dictionary(self):
        # Arrange
        mock_minio_object = mock.Mock()
        mock_minio_object.object_name = "test_1.txt"
        mock_minio_object.bucket_name = "bucket_1_test"
        mock_minio_object.is_dir = False
        mock_minio_object.size = 100
        mock_minio_object.etag = "test_etag"
        mock_minio_object.last_modified = datetime.datetime(2018, 11, 15)
        test_object = Object(mock_minio_object)
        # Act
        output = test_object.to_dict()
        # Assert
        assert output == {'object_name': 'test_1.txt', 'bucket_name': 'bucket_1_test', 'is_dir': False, 'size': 100,
                          'etag': 'test_etag', 'last modified': "15/11/2018"}
        self.assertIsInstance(output, dict)
