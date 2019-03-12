import json
from tornado.testing import AsyncHTTPTestCase
from tornado.testing import gen_test
from tornado.web import Application

from DittoWebApi.src.handlers.heartbeat import HeartbeatHandler


class HeartbeatHandlerTest(AsyncHTTPTestCase):
    def get_app(self):
        application = Application([
            ("/", HeartbeatHandler)
        ])
        return application

    @gen_test
    def test_heartbeat_returns_response(self):
        response = yield self.http_client.fetch(
            self.get_url("/"),
            method="GET"
        )
        response_body = json.loads(response.body, encoding='utf-8')
        assert response.code == 200
        assert "Server" not in response.headers
        assert response_body['status'] == 'success'
        assert response_body['data']['running'] == 'true'
