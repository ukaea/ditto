import json
import mock
import pytest
import tornado.web
from DittoWebApi.src.services.data_replication.data_replication_service import DataReplicationService
from DittoWebApi.src.handlers.create_bucket import CreateBucketHandler
from DittoWebApi.src.utils.return_helper import return_bucket_message
from DittoWebApi.src.utils.route_helper import format_route_specification


MOCK_DATA_REPLICATION_SERVICE = mock.create_autospec(DataReplicationService)


@pytest.fixture(autouse=True)
def app():
    application = tornado.web.Application([
        (
            format_route_specification("createbucket"),
            CreateBucketHandler,
            dict(data_replication_service=MOCK_DATA_REPLICATION_SERVICE)
        )
    ])
    return application


@pytest.mark.gen_test
@pytest.mark.parametrize("route", ["/createbucket/", "/createbucket"])
def test_create_bucket_returns_summary_of_new_bucket_when_successful(http_client, base_url, route):
    # Arrange
    MOCK_DATA_REPLICATION_SERVICE.create_bucket.return_value = return_bucket_message("Bucket Created (some-bucket)",
                                                                                     "some-bucket")
    # Act
    url = base_url + route
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
    MOCK_DATA_REPLICATION_SERVICE.create_bucket.return_value = return_bucket_message(
        "Bucket already exists (some-bucket)", "some-bucket"
    )
    # Act
    url = base_url + "/createbucket/"
    body = json.dumps({'bucket': "bucket_1"})
    response = yield http_client.fetch(url, method="POST", body=body)
    # Assert
    response_body = json.loads(response.body, encoding='utf-8')
    assert response_body["status"] == "success"
    assert response_body["data"] == {'message': 'Bucket already exists (some-bucket)',
                                     'bucket': 'some-bucket'}
