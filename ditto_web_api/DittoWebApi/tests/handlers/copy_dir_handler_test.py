import json
import mock
import pytest
import tornado.web
from DittoWebApi.src.services.data_replication_service import DataReplicationService
from DittoWebApi.src.handlers.copy_dir import CopyDirHandler


MOCK_DATA_REPLICATION_SERVICE = mock.create_autospec(DataReplicationService)


@pytest.fixture(autouse=True)
def app():
    application = tornado.web.Application([
        (r"/copydir/", CopyDirHandler, dict(data_replication_service=MOCK_DATA_REPLICATION_SERVICE))
    ])
    return application


@pytest.mark.gen_test
def test_post_returns_summary_of_transfer_as_json_when_successful(http_client, base_url):
    # Arrange
    MOCK_DATA_REPLICATION_SERVICE.copy_dir.return_value = {"Message": "Transfer successful",
                                                           "Files transferred": 1,
                                                           "Files updated": 0,
                                                           "Files skipped": 0,
                                                           "Data transferred (bytes)": 100}
    # Act
    url = base_url + "/copydir/"
    body = json.dumps({'bucket': "bucket_1", 'directory': "some_directory"})
    response = yield http_client.fetch(url, method="POST", body=body)
    # Assert
    response_body = json.loads(response.body, encoding='utf-8')
    assert response_body["status"] == "success"
    assert response_body["data"] == {'Message': 'Transfer successful',
                                     'Files transferred': 1,
                                     'Files updated': 0,
                                     'Files skipped': 0,
                                     'Data transferred (bytes)': 100}


@pytest.mark.gen_test
def test_post_returns_summary_of_failed_transfer_as_json(http_client, base_url):
    # Arrange
    MOCK_DATA_REPLICATION_SERVICE.copy_dir.return_value = {"Message": "Directory already exists, 5 files skipped",
                                                           "Files transferred": 0,
                                                           "Files updated": 0,
                                                           "Files skipped": 5,
                                                           "Data transferred (bytes)": 0}
    # Act
    url = base_url + "/copydir/"
    body = json.dumps({'bucket': "bucket_1", 'directory': "some_directory"})
    response = yield http_client.fetch(url, method="POST", body=body)
    # Assert
    response_body = json.loads(response.body, encoding='utf-8')
    assert response_body["status"] == "success"
    assert response_body["data"] == {'Message': 'Directory already exists, 5 files skipped',
                                     'Files transferred': 0,
                                     'Files updated': 0,
                                     'Files skipped': 5,
                                     'Data transferred (bytes)': 0}
