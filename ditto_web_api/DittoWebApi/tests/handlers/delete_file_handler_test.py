import json
import mock
import pytest
import tornado.web
from DittoWebApi.src.services.data_replication_service import DataReplicationService
from DittoWebApi.src.handlers.delete_file import DeleteFileHandler


MOCK_DATA_REPLICATION_SERVICE = mock.create_autospec(DataReplicationService)


@pytest.fixture(autouse=True)
def app():
    application = tornado.web.Application([
        (r"/deletefile/", DeleteFileHandler, dict(data_replication_service=MOCK_DATA_REPLICATION_SERVICE),)
    ])
    return application


@pytest.mark.gen_test
def test_delete_returns_summary_of_deleted_files_as_json_when_successful(http_client, base_url):
    # Arrange
    MOCK_DATA_REPLICATION_SERVICE.try_delete_file.return_value = {"Message": "File some_file.txt, successfully deleted"
                                                                             " from bucket bucket_1",
                                                                  "File": "some_file.txt",
                                                                  "Bucket": "bucket_1"}
    # Act
    url = base_url + "/deletefile/"
    body = json.dumps({'bucket': "bucket_1", 'file': "some_file.txt"})
    response = yield http_client.fetch(url, method="DELETE", body=body, allow_nonstandard_methods=True)
    # Assert
    response_body = json.loads(response.body, encoding='utf-8')
    assert response_body["status"] == "success"
    assert response_body["data"] == {'Message': 'File some_file.txt, successfully deleted from bucket bucket_1',
                                     'File': 'some_file.txt',
                                     'Bucket': 'bucket_1'}


@pytest.mark.gen_test
def test_delete_returns_summary_of_failed_delete_as_json_when_unsuccessful(http_client, base_url):
    # Arrange
    MOCK_DATA_REPLICATION_SERVICE.try_delete_file.return_value = {"Message": "File some_file.txt does not exist in "
                                                                             "bucket bucket_1",
                                                                  "File": "some_file.txt",
                                                                  "Bucket": "bucket_1"}
    # Act
    url = base_url + "/deletefile/"
    body = json.dumps({'bucket': "bucket_1", 'file': "some_file.txt"})
    response = yield http_client.fetch(url, method="DELETE", body=body, allow_nonstandard_methods=True)
    # Assert
    response_body = json.loads(response.body, encoding='utf-8')
    assert response_body["status"] == "success"
    assert response_body["data"] == {'Message': 'File some_file.txt does not exist in bucket bucket_1',
                                     'File': 'some_file.txt',
                                     'Bucket': 'bucket_1'}
