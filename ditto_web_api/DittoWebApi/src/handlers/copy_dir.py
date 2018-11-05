import tornado.web

class CopyDir(tornado.web.RequestHandler):
    def initialize(self, data_replication_service):
        self._data_replication_service = data_replication_service

    def get(self):
        self._data_replication_service.copy_dir()
