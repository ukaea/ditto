import tornado.web
import json

class ListPresentHandler(tornado.web.RequestHandler):
    def initialize(self, data_replication_service):
        self.data_replication_service = data_replication_service

    def get(self):
        objects = self.data_replication_service.retrieve_objects()
        self.write(json.dumps(objects))

