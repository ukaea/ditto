from DittoWebApi.src.utils.system_helper import current_time


class Archiver:
    def __init__(self, logger, file_system_helper):
        self._logger = logger
        self._file_system_helper = file_system_helper

    def update_content(self, file_summary, old_content):
        content = {} if old_content is None else old_content
        time_of_transfer = current_time()
        for file in file_summary.new_files:
            name = file.rel_path
            size = self._file_system_helper.file_size(file.abs_path)
            type_of_transfer = "new"
            content[file.rel_path] = {"file": name,
                                      "size": size,
                                      "time_transferred": time_of_transfer,
                                      "type_of_transfer": type_of_transfer}
        for file in file_summary.updated_files:
            name = file.rel_path
            size = self._file_system_helper.file_size(file.abs_path)
            type_of_transfer = "update"
            content[file.rel_path] = {"file": name,
                                      "size": size,
                                      "time_transferred": time_of_transfer,
                                      "type_of_transfer": type_of_transfer}
        return content
