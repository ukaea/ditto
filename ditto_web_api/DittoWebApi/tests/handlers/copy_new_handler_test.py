import json
import mock
import pytest
import tornado.web
from DittoWebApi.src.services.data_replication.data_replication_service import DataReplicationService
from DittoWebApi.src.handlers.copy_new import CopyNewHandler
from DittoWebApi.src.utils.return_helper import return_transfer_summary
from DittoWebApi.src.utils.route_helper import format_route_specification


MOCK_DATA_REPLICATION_SERVICE = mock.create_autospec(DataReplicationService)


@pytest.fixture(autouse=True)
def app():
    application = tornado.web.Application([
        (
            format_route_specification("copynew"),
            CopyNewHandler,
            dict(data_replication_service=MOCK_DATA_REPLICATION_SERVICE))
    ])
    return application


@pytest.mark.gen_test
@pytest.mark.parametrize("route", ["/copynew/", "/copynew"])
def test_post_returns_summary_of_transfer_as_json_when_successful(http_client, base_url, route):
    # Arrange
    MOCK_DATA_REPLICATION_SERVICE.copy_new.return_value = {'message': 'Transfer successful',
                                                           'new files transferred': 1,
                                                           'files updated': 0,
                                                           'files skipped': 3,
                                                           'data transferred (bytes)': 100}
    # Act
    url = base_url + route
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
def test_post_returns_summary_of_transfer_as_json_when_successful_with_return_handler_coupling(http_client, base_url):
    # Arrange
    MOCK_DATA_REPLICATION_SERVICE.copy_new.return_value = return_transfer_summary(
        message='Transfer successful',
        new_files_uploaded=1,
        files_updated=0,
        files_skipped=3,
        data_transferred=100
    )
    # Act
    url = base_url + "/copynew/"
    body = json.dumps({'bucket': "bucket_1", 'directory': "some_directory"})
    response = yield http_client.fetch(url, method="POST", body=body)
    # Assert
    response_body = json.loads(response.body, encoding='utf-8')
    assert response_body["status"] == "success"
    assert response_body["data"] == {'message': 'Transfer successful',
                                     'new files uploaded': 1,
                                     'files updated': 0,
                                     'files skipped': 3,
                                     'data transferred (bytes)': 100}


@pytest.mark.gen_test
def test_post_returns_summary_of_failed_transfer_as_json(http_client, base_url):
    # Arrange
    MOCK_DATA_REPLICATION_SERVICE.copy_new.return_value = {'message': "Directory already exists, 5 files skipped",
                                                           'new files transferred': 0,
                                                           'files updated': 0,
                                                           'files skipped': 5,
                                                           'data transferred (bytes)': 0}
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


@pytest.mark.gen_test
def test_post_returns_summary_of_failed_transfer_as_json_with_coupling_return_handler(http_client, base_url):
    # Arrange
    MOCK_DATA_REPLICATION_SERVICE.copy_new.return_value = return_transfer_summary(
        message="Directory already exists, 5 files skipped",
        new_files_uploaded=0,
        files_updated=0,
        files_skipped=5,
        data_transferred=0
    )
    # Act
    url = base_url + "/copynew/"
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
