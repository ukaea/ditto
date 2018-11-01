import mock
import datetime
import pytest
import logging
import unittest
import tornado.web



from DittoWebApi.src.services.data_replication_service import DataReplicationService
from DittoWebApi.src.models.object import Object

from DittoWebApi.src.handlers.list_present import ListPresentHandler

mock_data_replication_service = None
application = None
mock_data_replication_service = mock.create_autospec(DataReplicationService)

@pytest.fixture(autouse=True)
def app():

    application = tornado.web.Application([
        (r"/", ListPresentHandler, dict(data_replication_service=mock_data_replication_service))
    ])
    return application

@pytest.mark.gen_test
def test_get_returns_objects_from_server_as_json(http_client, base_url):
    # Arrange
    mock_object_1 = mock.create_autospec(Object)
    mock_object_1.object_name = "file_1.txt"
    mock_object_1.bucket_name = "bucket_1"
    mock_data_replication_service.retrieve_objects.return_value = [{"object_name": "file_1.txt", "bucket_name": "bucket_1"}]
    # Act
    response = yield http_client.fetch(base_url)
    # Assert
    assert response.body == b'[{"object_name": "file_1.txt", "bucket_name": "bucket_1"}]'

