import json
import mock
import pytest
import tornado.web
from DittoWebApi.src.services.data_replication.data_replication_service import DataReplicationService
from DittoWebApi.src.handlers.copy_new import CopyNewHandler


MOCK_DATA_REPLICATION_SERVICE = mock.create_autospec(DataReplicationService)


@pytest.fixture(autouse=True)
def app():
    application = tornado.web.Application([
        (r"/copynew/", CopyNewHandler, dict(data_replication_service=MOCK_DATA_REPLICATION_SERVICE))
    ])
    return application


@pytest.mark.gen_test
def test_post_returns_summary_of_transfer_as_json_when_successful(http_client, base_url):
    # Arrange
    MOCK_DATA_REPLICATION_SERVICE.copy_new.return_value = {"message": "Transfer successful",
                                                           "new files transferred": 1,
                                                           "files updated": 0,
                                                           "files skipped": 3,
                                                           "data transferred (bytes)": 100}
    # Act
    url = base_url + "/copynew/"
    body = json.dumps({'bucket': "bucket_1", 'directory': "some_directory"})
    response = yield http_client.fetch(url, method="POST", body=body)
    # Assert
    response_body = json.loads(response.body, encoding='utf-8')
    assert response_body["status"] == "success"
    assert response_body["data"] == {'message': 'Transfer successful',
                                     'new files transferred': 1,
                                     'files updated': 0,
                                     'files skipped': 3,
                                     'data transferred (bytes)': 100}


@pytest.mark.gen_test
def test_post_returns_summary_of_failed_transfer_as_json(http_client, base_url):
    # Arrange
    MOCK_DATA_REPLICATION_SERVICE.copy_new.return_value = {"message": "Directory already exists, 5 files skipped",
                                                           "new files transferred": 0,
                                                           "files updated": 0,
                                                           "files skipped": 5,
                                                           "data transferred (bytes)": 0}
    # Act
    url = base_url + "/copynew/"
    body = json.dumps({'bucket': "bucket_1", 'directory': "some_directory"})
    response = yield http_client.fetch(url, method="POST", body=body)
    # Assert
    response_body = json.loads(response.body, encoding='utf-8')
    assert response_body["status"] == "success"
    assert response_body["data"] == {'message': 'Directory already exists, 5 files skipped',
                                     'new files transferred': 0,
                                     'files updated': 0,
                                     'files skipped': 5,
                                     'data transferred (bytes)': 0}
