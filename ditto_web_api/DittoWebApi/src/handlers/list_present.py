# pylint: disable=W0221,W0223
import json
import tornado.web
from DittoWebApi.src.utils.parse_args import extract_primary_arg


class ListPresentHandler(tornado.web.RequestHandler):
    def initialize(self, data_replication_service):
        self._data_replication_service = data_replication_service

    def get(self, *args, **kwargs):
        dir_path = extract_primary_arg(args)
        object_dicts = self._data_replication_service.retrieve_object_dicts(dir_path)
        self.write(json.dumps(object_dicts))
