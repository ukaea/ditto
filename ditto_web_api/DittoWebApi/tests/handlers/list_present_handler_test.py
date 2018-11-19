import json
import mock
import pytest
import tornado.web
from DittoWebApi.src.services.data_replication.data_replication_service import DataReplicationService
from DittoWebApi.src.handlers.list_present import ListPresentHandler


MOCK_DATA_REPLICATION_SERVICE = mock.create_autospec(DataReplicationService)


@pytest.fixture(autouse=True)
def app():
    application = tornado.web.Application([
        (r"/listpresent/", ListPresentHandler, dict(data_replication_service=MOCK_DATA_REPLICATION_SERVICE))
    ])
    return application


@pytest.mark.gen_test
def test_post_returns_objects_from_server_as_json(http_client, base_url):
    # Arrange
    MOCK_DATA_REPLICATION_SERVICE.retrieve_object_dicts.return_value = {"message": "objects returned succesfully",
                                                                        "objects": [{"object_name": "file_1.txt",
                                                                                     "bucket_name": "bucket_1"}]}
    # Act
    url = base_url + "/listpresent/"
    body = json.dumps({'bucket': "bucket_1", })
    response = yield http_client.fetch(url, method="POST", body=body)
    # Assert
    response_body = json.loads(response.body, encoding='utf-8')
    assert response_body["status"] == "success"
    assert response_body["data"]["objects"] == [{"object_name": "file_1.txt", "bucket_name": "bucket_1"}]
    assert response_body["data"]["message"] == "objects returned succesfully"


@pytest.mark.gen_test
def test_post_returns_multiple_objects_as_a_json_array(http_client, base_url):
    # Arrange
    MOCK_DATA_REPLICATION_SERVICE.retrieve_object_dicts.return_value = {"message": "objects returned succesfully",
                                                                        "objects": [{"object_name": "file_1.txt",
                                                                                     "bucket_name": "bucket_1"},
                                                                                    {"object_name": "file_2.txt",
                                                                                     "bucket_name": "bucket_1"}]}
    # Act
    url = base_url + "/listpresent/"
    body = json.dumps({'bucket': "bucket_1", })
    response = yield http_client.fetch(url, method="POST", body=body)
    # Assert
    response_body = json.loads(response.body, encoding='utf-8')
    assert response_body["status"] == "success"
    assert response_body["data"]["objects"] == [{"object_name": "file_1.txt", "bucket_name": "bucket_1"},
                                                {"object_name": "file_2.txt", "bucket_name": "bucket_1"}]
    assert response_body["data"]["message"] == "objects returned succesfully"


@pytest.mark.gen_test
def test_post_returns_empty_array_when_no_objects(http_client, base_url):
    # Arrange
    MOCK_DATA_REPLICATION_SERVICE.retrieve_object_dicts.return_value = {"message": "no objects in s3 bucket",
                                                                        "objects": []}
    # Act
    url = base_url + "/listpresent/"
    body = json.dumps({'bucket': "bucket_1", })
    response = yield http_client.fetch(url, method="POST", body=body)
    # Assert
    response_body = json.loads(response.body, encoding='utf-8')
    assert response_body["status"] == "success"
    assert response_body["data"]["objects"] == []
    assert response_body["data"]["message"] == "no objects in s3 bucket"


@pytest.mark.gen_test
def test_post_returns_warning_when_invalid_bucket_name_provided(http_client, base_url):
    # Arrange
    MOCK_DATA_REPLICATION_SERVICE.retrieve_object_dicts.return_value = {"message": "bucket_1 does not exist in S3",
                                                                        "objects": []}
    # Act
    url = base_url + "/listpresent/"
    body = json.dumps({'bucket': "bucket_1", })
    response = yield http_client.fetch(url, method="POST", body=body)
    # Assert
    response_body = json.loads(response.body, encoding='utf-8')
    assert response_body["status"] == "success"
    assert response_body["data"]["objects"] == []
    assert response_body["data"]["message"] == "bucket_1 does not exist in S3"
