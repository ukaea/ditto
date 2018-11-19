import json
import mock
import pytest
import tornado.web
from DittoWebApi.src.services.data_replication.data_replication_service import DataReplicationService
from DittoWebApi.src.handlers.copy_update import CopyUpdateHandler
from DittoWebApi.src.utils.return_helper import return_transfer_summary


MOCK_DATA_REPLICATION_SERVICE = mock.create_autospec(DataReplicationService)


@pytest.fixture(autouse=True)
def app():
    application = tornado.web.Application([
        (r"/copyupdate/", CopyUpdateHandler, dict(data_replication_service=MOCK_DATA_REPLICATION_SERVICE))
    ])
    return application


@pytest.mark.gen_test
def test_post_returns_summary_of_transfer_as_json_when_successful(http_client, base_url):
    # Arrange
    MOCK_DATA_REPLICATION_SERVICE.copy_new_and_update.return_value = {'message': 'Transfer successful',
                                                                      'new files uploaded': 2,
                                                                      'files updated': 1,
                                                                      'files skipped': 3,
                                                                      'data transferred (bytes)': 100}
    # Act
    url = base_url + "/copyupdate/"
    body = json.dumps({'bucket': "bucket_1", 'directory': "some_directory"})
    response = yield http_client.fetch(url, method="POST", body=body)
    # Assert
    response_body = json.loads(response.body, encoding='utf-8')
    assert response_body["status"] == "success"
    assert response_body["data"] == {'message': 'Transfer successful',
                                     'new files uploaded': 2,
                                     'files updated': 1,
                                     'files skipped': 3,
                                     'data transferred (bytes)': 100}


@pytest.mark.gen_test
def test_post_returns_summary_of_transfer_as_json_when_successful_with_return_handler_coupling(http_client, base_url):
    # Arrange
    MOCK_DATA_REPLICATION_SERVICE.copy_new_and_update.return_value = return_transfer_summary(
        message='Transfer successful',
        files_transferred=3,
        files_updated=4,
        files_skipped=7,
        data_transferred=2560
    )
    # Act
    url = base_url + "/copyupdate/"
    body = json.dumps({'bucket': "bucket_1", 'directory': "some_directory"})
    response = yield http_client.fetch(url, method="POST", body=body)
    # Assert
    response_body = json.loads(response.body, encoding='utf-8')
    assert response_body["status"] == "success"
    assert response_body["data"] == {'message': 'Transfer successful',
                                     'new files uploaded': 3,
                                     'files updated': 4,
                                     'files skipped': 7,
                                     'data transferred (bytes)': 2560}


@pytest.mark.gen_test
def test_post_returns_summary_of_failed_transfer_as_json(http_client, base_url):
    # Arrange
    MOCK_DATA_REPLICATION_SERVICE.copy_new_and_update.return_value = \
        {'message': "No new or updated files found in directory some_directory",
         'new files transferred': 0,
         'files updated': 0,
         'files skipped': 5,
         'data transferred (bytes)': 0}
    # Act
    url = base_url + "/copyupdate/"
    body = json.dumps({'bucket': "bucket_1", 'directory': "some_directory"})
    response = yield http_client.fetch(url, method="POST", body=body)
    # Assert
    response_body = json.loads(response.body, encoding='utf-8')
    assert response_body["status"] == "success"
    assert response_body["data"] == {'message': 'No new or updated files found in directory some_directory',
                                     'new files transferred': 0,
                                     'files updated': 0,
                                     'files skipped': 5,
                                     'data transferred (bytes)': 0}


@pytest.mark.gen_test
def test_post_returns_summary_of_failed_transfer_as_json_with_coupling_return_handler(http_client, base_url):
    # Arrange
    MOCK_DATA_REPLICATION_SERVICE.copy_new_and_update.return_value = return_transfer_summary(
        message="No new or updated files found in directory some_directory",
        files_transferred=0,
        files_updated=0,
        files_skipped=5,
        data_transferred=0
    )
    # Act
    url = base_url + "/copyupdate/"
    body = json.dumps({'bucket': "bucket_1", 'directory': "some_directory"})
    response = yield http_client.fetch(url, method="POST", body=body)
    # Assert
    response_body = json.loads(response.body, encoding='utf-8')
    assert response_body["status"] == "success"
    assert response_body["data"] == {'message': 'No new or updated files found in directory some_directory',
                                     'new files uploaded': 0,
                                     'files updated': 0,
                                     'files skipped': 5,
                                     'data transferred (bytes)': 0}
