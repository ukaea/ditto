import json
import mock
import pytest
import tornado.web
from DittoWebApi.src.services.data_replication.data_replication_service import DataReplicationService
from DittoWebApi.src.handlers.copy_dir import CopyDirHandler
from DittoWebApi.src.utils.return_helper import return_transfer_summary


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
    MOCK_DATA_REPLICATION_SERVICE.copy_dir.return_value = {"message": "Transfer successful",
                                                           "new files uploaded": 1,
                                                           "files updated": 0,
                                                           "files skipped": 0,
                                                           "data transferred (bytes)": 100}
    # Act
    url = base_url + "/copydir/"
    body = json.dumps({'bucket': "bucket_1", 'directory': "some_directory/some_sub_dir"})
    response = yield http_client.fetch(url, method="POST", body=body)
    # Assert
    response_body = json.loads(response.body, encoding='utf-8')
    assert response_body["status"] == "success"
    assert response_body["data"] == {'message': 'Transfer successful',
                                     'new files uploaded': 1,
                                     'files updated': 0,
                                     'files skipped': 0,
                                     'data transferred (bytes)': 100}


@pytest.mark.gen_test
def test_post_has_coupling_with_return_handler(http_client, base_url):
    # Arrange
    MOCK_DATA_REPLICATION_SERVICE.copy_dir.return_value = return_transfer_summary(1, 0, 0, 100, "Transfer successful")
    # Act
    url = base_url + "/copydir/"
    body = json.dumps({'bucket': "bucket_1", 'directory': "some_directory/some_sub_dir"})
    response = yield http_client.fetch(url, method="POST", body=body)
    # Assert
    response_body = json.loads(response.body, encoding='utf-8')
    assert response_body["status"] == "success"
    assert response_body["data"] == {'message': 'Transfer successful',
                                     'new files uploaded': 1,
                                     'files updated': 0,
                                     'files skipped': 0,
                                     'data transferred (bytes)': 100}


@pytest.mark.gen_test
def test_post_returns_summary_of_failed_transfer_as_json(http_client, base_url):
    # Arrange
    MOCK_DATA_REPLICATION_SERVICE.copy_dir.return_value = {"message": "Directory already exists, 5 files skipped",
                                                           "new files uploaded": 0,
                                                           "files updated": 0,
                                                           "files skipped": 5,
                                                           "data transferred (bytes)": 0}
    # Act
    url = base_url + "/copydir/"
    body = json.dumps({'bucket': "bucket_1", 'directory': "some_directory"})
    response = yield http_client.fetch(url, method="POST", body=body)
    # Assert
    response_body = json.loads(response.body, encoding='utf-8')
    assert response_body["status"] == "success"
    assert response_body["data"] == {'message': 'Directory already exists, 5 files skipped',
                                     'new files uploaded': 0,
                                     'files updated': 0,
                                     'files skipped': 5,
                                     'data transferred (bytes)': 0}


@pytest.mark.gen_test
def test_post_returns_summary_of_failed_transfer_as_json_with_return_helper_coupling(http_client, base_url):
    # Arrange
    MOCK_DATA_REPLICATION_SERVICE.copy_dir.return_value = return_transfer_summary(
        0, 0, 5, 0, "Directory already exists, 5 files skipped"
    )
    # Act
    url = base_url + "/copydir/"
    body = json.dumps({'bucket': "bucket_1", 'directory': "some_directory"})
    response = yield http_client.fetch(url, method="POST", body=body)
    # Assert
    response_body = json.loads(response.body, encoding='utf-8')
    assert response_body["status"] == "success"
    assert response_body["data"] == {'message': 'Directory already exists, 5 files skipped',
                                     'new files uploaded': 0,
                                     'files updated': 0,
                                     'files skipped': 5,
                                     'data transferred (bytes)': 0}
