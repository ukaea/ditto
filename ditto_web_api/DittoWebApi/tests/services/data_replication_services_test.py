import mock
import datetime
import pytest
import logging
import unittest
from DittoWebApi.src.services.external_data_service import ExternalDataService
from DittoWebApi.src.services.data_replication_service import DataReplicationService
from DittoWebApi.src.services.internal_data_service import InternalDataService


class DataReplicationServiceTest(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_external_data_service = mock.create_autospec(ExternalDataService)
        self.mock_internal_data_service = mock.create_autospec(InternalDataService)
        self.mock_logger = mock.create_autospec(logging.Logger)
        self.test_service = DataReplicationService(self.mock_external_data_service, self.mock_internal_data_service,
                                                   self.mock_logger)

    def test_retrieve_objects_returns_all_json_objects(self):
        # Arrange
        self.mock_external_data_service.get_objects.return_value = [{"object_name": "test",
                                                                     "bucket_name": "test_bucket", "is_dir": False,
                                                                     "size": 100, "etag": "test_etag",
                                                                     "last_modified": datetime.datetime(2018, 11, 1)}]
        # Act
        output = self.test_service.retrieve_objects()
        # Assert
        assert output[0] == {"object_name": "test", "bucket_name": "test_bucket", "is_dir": False, "size": 100,
                             "etag": "test_etag", "last_modified": datetime.datetime(2018, 11, 1)}
