from DittoWebApi.src.utils.system_helper import current_time


class Archiver:
    def __init__(self, logger, file_system_helper):
        self._logger = logger
        self._file_system_helper = file_system_helper

    def archive_content(self, file_summary, old_content):
        content = {} if old_content is None else old_content
        time_of_transfer = current_time()
        for file in file_summary.new_files:
            name = file.rel_path
            size = self._file_system_helper.file_size(file.abs_path)
            content[file.rel_path] = {"file": name,
                                      "size": size,
                                      "first transferred": time_of_transfer,
                                      "last updated": time_of_transfer,
                                      "type of transfer": "new upload"}
        for file in file_summary.updated_files:
            self.update_details(content, file)
        return content

    def update_details(self, content, file):
        size = self._file_system_helper.file_size(file.abs_path)
        content[file.rel_path]["last updated"] = current_time()
        content[file.rel_path]["type of transfer"] = "update"
        content[file.rel_path]["size"] = size
