import tornado.web


class ListPresentHandler(tornado.web.RequestHandler):
    def initialize(self, data_replication_service):
        self.data_replication_service = data_replication_service

    def get(self):
        return self.data_replication_service.retrieve_objects()


