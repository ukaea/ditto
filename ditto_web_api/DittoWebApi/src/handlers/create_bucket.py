# pylint: disable=W0221,W0223
import tornado.web
from DittoWebApi.src.utils.parse_args import extract_bucket_name

class CreatBucketHandler(tornado.web.RequestHandler):
    def initialize(self, data_replication_service):
        self._data_replication_service = data_replication_service

    def post(self, *args, **kwargs):
        bucket_name = extract_bucket_name(args)
        self.write(self._data_replication_service.create_bucket(bucket_name))
