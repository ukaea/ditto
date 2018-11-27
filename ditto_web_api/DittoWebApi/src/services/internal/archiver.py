from DittoWebApi.src.utils.system_helper import current_time


class Archiver:
    def __init__(self, logger, file_system_helper):
        self._logger = logger
        self._file_system_helper = file_system_helper

    # Current placeholder for processing contents of the archive files
    def update_content(self, old_content, new_content):
        return old_content + new_content

    def to_json(self, file_summary):
        for file in file_summary.new_files:
            name = file.rel_path
            size = self._file_system_helper.file_size(file.abs_path)
            time_of_transfer = current_time()
            type_of_transfer = "new"
        for file in file_summary.updated_files:
            name = file.rel_path
            size = self._file_system_helper.file_size(file.abs_path)
            time_of_transfer = current_time()
            type_of_transfer = "update"
            

