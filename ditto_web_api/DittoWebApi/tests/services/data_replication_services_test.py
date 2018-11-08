# pylint: disable=W0201
import logging
import unittest

import mock
import pytest

from DittoWebApi.src.services.external_data_service import ExternalDataService
from DittoWebApi.src.services.data_replication_service import DataReplicationService
from DittoWebApi.src.services.internal_data_service import InternalDataService
from DittoWebApi.src.models.object import Object


class DataReplicationServiceTest(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_external_data_service = mock.create_autospec(ExternalDataService)
        self.mock_internal_data_service = mock.create_autospec(InternalDataService)
        self.mock_logger = mock.create_autospec(logging.Logger)
        self.test_service = DataReplicationService(self.mock_external_data_service, self.mock_internal_data_service,
                                                   self.mock_logger)

    def test_retrieve_objects_dicts_returns_all_correct_dictionaries_of_objects(self):
        # Arrange
        mock_object_1 = mock.create_autospec(Object)
        mock_object_1.to_dict.return_value = {"object_name": "test",
                                              "bucket_name": "test_bucket",
                                              "is_dir": False,
                                              "size": 100,
                                              "etag": "test_etag",
                                              "last_modified": 2132142421.123123}
        mock_object_2 = mock.create_autospec(Object)
        mock_object_2.to_dict.return_value = {"object_name": "test_2",
                                              "bucket_name": "test_bucket_2",
                                              "is_dir": False, "size": 100,
                                              "etag": "test_etag_2",
                                              "last_modified": 2132142421.123123}
        self.mock_external_data_service.get_objects.return_value = [mock_object_1, mock_object_2]
        # Act
        output = self.test_service.retrieve_object_dicts(None)
        # Assert
        assert output[0] == {"object_name": "test",
                             "bucket_name": "test_bucket",
                             "is_dir": False,
                             "size": 100,
                             "etag": "test_etag",
                             "last_modified": 2132142421.123123}
        assert output[1] == {"object_name": "test_2",
                             "bucket_name": "test_bucket_2",
                             "is_dir": False, "size": 100,
                             "etag": "test_etag_2",
                             "last_modified": 2132142421.123123}

    def test_retrieve_objects_dicts_empty_array_when_no_objects_present(self):
        self.mock_external_data_service.get_objects.return_value = []
        # Act
        output = self.test_service.retrieve_object_dicts(None)
        # Assert
        assert output == []

    def test_retrieve_objects_dicts_returns_all_correct_dictionaries_of_objects_from_sub_dir(self):
        # Arrange
        mock_object_1 = mock.create_autospec(Object)
        mock_object_1.to_dict.return_value = {"object_name": "test_dir/test",
                                              "bucket_name": "test_bucket",
                                              "is_dir": False,
                                              "size": 100,
                                              "etag": "test_etag",
                                              "last_modified": 2132142421.123123}
        mock_object_2 = mock.create_autospec(Object)
        mock_object_2.to_dict.return_value = {"object_name": "test_2",
                                              "bucket_name": "test_bucket_2",
                                              "is_dir": False, "size": 100,
                                              "etag": "test_etag_2",
                                              "last_modified": 2132142421.123123}
        self.mock_external_data_service.get_objects.return_value = [mock_object_1]
        # Act
        output = self.test_service.retrieve_object_dicts("test_dir")
        # Assert
        assert output[0] == {"object_name": "test_dir/test",
                             "bucket_name": "test_bucket",
                             "is_dir": False,
                             "size": 100,
                             "etag": "test_etag",
                             "last_modified": 2132142421.123123}

    def test_return_bucket_message_correct_when_bucket_name_invalid(self):
        self.mock_external_data_service.is_valid_bucket.return_value = False
        bucket_name = "test-1234-"
        response = self.test_service.create_bucket(bucket_name)
        self.assertEqual(response, {"Message": "Bucket name breaks S3 or local naming standard (test-1234-)",
                                    "Name of bucket attempted": "test-1234-"})

    def test_create_bucket_return_correct_when_bucket_not_given(self):
        bucket_name = None
        response = self.test_service.create_bucket(bucket_name)
        self.assertEqual(response, {"Message": "No bucket name provided",
                                    "Name of bucket attempted": ""})

    def test_create_bucket_return_correct_when_bucket_already_exists(self):
        bucket_name = 'test-12345'
        self.mock_external_data_service.is_valid_bucket.return_value = True
        self.mock_external_data_service.does_bucket_exist.return_value = True
        response = self.test_service.create_bucket(bucket_name)
        self.assertEqual(response, {"Message": "Bucket already exists (test-12345)",
                                    "Name of bucket attempted": "test-12345"})

    def test_create_bucket_returns_correctly_when_successful(self):
        bucket_name = 'test-12345'
        self.mock_external_data_service.is_valid_bucket.return_value = True
        self.mock_external_data_service.does_bucket_exist.return_value = False
        response = self.test_service.create_bucket(bucket_name)
        self.assertEqual(response, {"Message": "Bucket Created (test-12345)",
                                    "Name of bucket attempted": "test-12345"})
