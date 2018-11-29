from DittoWebApi.src.utils.system_helper import current_time_in_utc


class Archiver:
    def __init__(self, file_system_helper, logger):
        self._logger = logger
        self._file_system_helper = file_system_helper

    def write_archive(self, archive_file_path, file_summary):
        time_of_transfer = current_time_in_utc()
        try:
            new_archive_file = self._file_system_helper.open_file(archive_file_path)
            for file in file_summary.new_files:
                new_content = self._archive_new_file(file, time_of_transfer)
                self._file_system_helper.write_to_file(new_archive_file, new_content)
            for file in file_summary.updated_files:
                new_content = self._archive_file_update(file, time_of_transfer)
                self._file_system_helper.write_to_file(new_archive_file, new_content)
        except Exception as exception:
            self._logger.error(f"Exception found: {exception}")
            raise
        finally:
            self._file_system_helper.close_file(new_archive_file)
        self._logger.debug(f"Archive file created: {archive_file_path}")


    def update_archive(self, archive_file_path, file_summary):
        content = "test test"
        try:
            archived_file = self._file_system_helper.open_file(archive_file_path)


        except Exception as exception:
            self._logger.error(f"Exception found: {exception}")
            raise
        finally:
            self._file_system_helper.close_file(archived_file)
        self._logger.debug(f"Archive file updated: {archive_file_path}")

    def _archive_new_file(self, file, time_of_transfer):
        size = self._file_system_helper.file_size(file.abs_path)
        return {file.file_name: {"file": file.file_name,
                                "size": size,
                                "first transferred": time_of_transfer,
                                "latest update": time_of_transfer,
                                "type of transfer": "new upload"}
                }

    def _archive_file_update(self, file, time_of_transfer):
        size = self._file_system_helper.file_size(file.abs_path)
        return {file.file_name: {"file": file.file_name,
                                "size": size,
                                "first transferred": time_of_transfer,
                                "latest update": time_of_transfer,
                                "type of transfer": "file_update"}
                }

    def _update_archive(self, content, file, time_of_transfer):
        size = self._file_system_helper.file_size(file.abs_path)
        content[file.rel_path]["latest update"] = time_of_transfer
        content[file.rel_path]["type of transfer"] = "update"
        content[file.rel_path]["size"] = size
