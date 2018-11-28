from DittoWebApi.src.utils.system_helper import current_time


class Archiver:
    def __init__(self, logger, file_system_helper):
        self._logger = logger
        self._file_system_helper = file_system_helper

    def archive_transfer(self, file_summary, old_content):
        content = {} if old_content is None else old_content
        time_of_transfer = current_time()
        for file in file_summary.new_files:
            self._archive_new_file(content, file, time_of_transfer)
        for file in file_summary.updated_files:
            self._update_archive(content, file, time_of_transfer)
        return content

    def _archive_new_file(self, content, file, time_of_transfer):
        size = self._file_system_helper.file_size(file.abs_path)
        content[file.rel_path] = {"file": file.rel_path,
                                  "size": size,
                                  "first transferred": time_of_transfer,
                                  "latest update": time_of_transfer,
                                  "type of transfer": "new upload"}

    def _update_archive(self, content, file, time_of_transfer):
        size = self._file_system_helper.file_size(file.abs_path)
        content[file.rel_path]["latest update"] = time_of_transfer
        content[file.rel_path]["type of transfer"] = "update"
        content[file.rel_path]["size"] = size

    def _archive_file_deletion(self, content, file, time_of_transfer):
        content[file.rel_path]["latest update"] = time_of_transfer
        content[file.rel_path]["type of transfer"] = "delete"
        content[file.rel_path]["size"] = 0
