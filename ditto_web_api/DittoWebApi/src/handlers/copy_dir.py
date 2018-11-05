import tornado.web


class CopyDirHandler(tornado.web.RequestHandler):
    def initialize(self, data_replication_service):
        self._data_replication_service = data_replication_service

    def get(self, dir_path=None):
        self._data_replication_service.copy_dir(dir_path)
