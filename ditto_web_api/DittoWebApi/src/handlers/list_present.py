import tornado.web
import json


class ListPresentHandler(tornado.web.RequestHandler):
    def initialize(self, data_replication_service):
        self._data_replication_service = data_replication_service

    def get(self):
        object_dicts = self._data_replication_service.retrieve_object_dicts()
        self.write(json.dumps(object_dicts))
