import json
import mock
import pytest
import tornado.web
from DittoWebApi.src.services.data_replication.data_replication_service import DataReplicationService
from DittoWebApi.src.handlers.create_bucket import CreateBucketHandler


MOCK_DATA_REPLICATION_SERVICE = mock.create_autospec(DataReplicationService)


@pytest.fixture(autouse=True)
def app():
    application = tornado.web.Application([
        (r"/createbucket/", CreateBucketHandler, dict(data_replication_service=MOCK_DATA_REPLICATION_SERVICE))
    ])
    return application


@pytest.mark.gen_test
def test_create_bucket_returns_summary_of_new_bucket_when_successful(http_client, base_url):
    # Arrange
    MOCK_DATA_REPLICATION_SERVICE.create_bucket.return_value = {"message": "Bucket Created (some-bucket)",
                                                                "bucket": "some-bucket"}
    # Act
    url = base_url + "/createbucket/"
    body = json.dumps({'bucket': "bucket_1"})
    response = yield http_client.fetch(url, method="POST", body=body)
    # Assert
    response_body = json.loads(response.body, encoding='utf-8')
    assert response_body["status"] == "success"
    assert response_body["data"] == {'message': 'Bucket Created (some-bucket)',
                                     'bucket': 'some-bucket'}


@pytest.mark.gen_test
def test_create_bucket_returns_summary_of_failure_when_bucket_already_exists(http_client, base_url):
    # Arrange
    MOCK_DATA_REPLICATION_SERVICE.create_bucket.return_value = {"message": "Bucket already exists (some-bucket)",
                                                                "bucket": "some-bucket"}
    # Act
    url = base_url + "/createbucket/"
    body = json.dumps({'bucket': "bucket_1"})
    response = yield http_client.fetch(url, method="POST", body=body)
    # Assert
    response_body = json.loads(response.body, encoding='utf-8')
    assert response_body["status"] == "success"
    assert response_body["data"] == {'message': 'Bucket already exists (some-bucket)',
                                     'bucket': 'some-bucket'}
