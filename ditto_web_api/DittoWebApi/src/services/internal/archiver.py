from DittoWebApi.src.utils.system_helper import current_time


class Archiver:
    def __init__(self, file_system_helper, logger):
        self._logger = logger
        self._file_system_helper = file_system_helper

    def write_archive(self, file_path, file_summary):
        content = {}
        time_of_transfer = current_time()
        for file in file_summary.new_files:
            self._archive_new_file(content, file, time_of_transfer)
        for file in file_summary.updated_files:
            self._archive_file_update(content, file, time_of_transfer)
        self._file_system_helper.create_file(file_path, content)
        self._logger.debug(f"Archive file created: {file_path}")


    def update_archive(self, file_path, file_summary):
        content = "test test"
        try:
            archived_file = self._file_system_helper.open_file(file_path)
            archived_file.write(content)

        except Exception as exception:
            self._logger.error(f"Exception found: {exception}")
            raise
        finally:
            self._file_system_helper.close_file(archived_file)
        self._logger.debug(f"Archive file updated: {file_path}")

    def _archive_new_file(self, content, file, time_of_transfer):
        size = self._file_system_helper.file_size(file.abs_path)
        content[file.rel_path] = {"file": file.rel_path,
                                  "size": size,
                                  "first transferred": time_of_transfer,
                                  "latest update": time_of_transfer,
                                  "type of transfer": "new upload"}

    def _archive_file_update(self, content, file, time_of_transfer):
        size = self._file_system_helper.file_size(file.abs_path)
        content[file.rel_path] = {"file": file.rel_path,
                                  "size": size,
                                  "first transferred": time_of_transfer,
                                  "latest update": time_of_transfer,
                                  "type of transfer": "file_update"}

    def _update_archive(self, content, file, time_of_transfer):
        size = self._file_system_helper.file_size(file.abs_path)
        content[file.rel_path]["latest update"] = time_of_transfer
        content[file.rel_path]["type of transfer"] = "update"
        content[file.rel_path]["size"] = size

    def _archive_file_deletion(self, content, file, time_of_transfer):
        content[file.rel_path]["latest update"] = time_of_transfer
        content[file.rel_path]["type of transfer"] = "delete"
        content[file.rel_path]["size"] = 0
        
    def archive_transfer(self, file_summary, old_content):
        content = {} if old_content is None else old_content
        time_of_transfer = current_time()
        for file in file_summary.new_files:
            self._archive_new_file(content, file, time_of_transfer)
        for file in file_summary.updated_files:
            self._update_archive(content, file, time_of_transfer)
        return content
