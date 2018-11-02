import tornado.web

class CopyDir(tornado.web.RequestHandler):
    def initialize(self, data_replication_service):
        self._data_replication_service = data_replication_service

    def get(self):
        files_to_copy = self._data_replication_service.retrieve_list_of_files()
        for file in files_to_copy:
            processed_file = self._data_replication_service.process_file(file)
            self._data_replication_service.upload_at_external(processed_file)
