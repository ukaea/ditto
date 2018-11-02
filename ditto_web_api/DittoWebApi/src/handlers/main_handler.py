import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, data_replication_service):
        self.data_replication_service = data_replication_service
