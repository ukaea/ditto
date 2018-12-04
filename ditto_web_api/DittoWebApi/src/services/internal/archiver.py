from DittoWebApi.src.utils.system_helper import current_time_in_utc


class Archiver:
    def __init__(self, file_read_write_helper, file_system_helper, logger):
        self._logger = logger
        self._file_system_helper = file_system_helper
        self._file_read_write_helper = file_read_write_helper

    def write_archive(self, archive_file_path, file_summary):
        try:
            content = {}
            new_archive_file = self._file_system_helper.create_and_open_file_for_writing(archive_file_path)

            self._archive_file_summary(file_summary, content)

            self._file_read_write_helper.write_json_to_file(new_archive_file, content)
        except Exception as exception:
            self._logger.error(f"Exception found here: {exception}")
            raise
        finally:
            self._file_system_helper.close_file(new_archive_file)
        self._logger.debug(f"Archive file created: {archive_file_path}")

    def update_archive(self, archive_file_path, file_summary):
        try:
            archived_file = self._file_system_helper.open_file_for_reading_and_writing(archive_file_path)
            content = self._file_read_write_helper.read_file_as_json(archived_file)
            self._file_read_write_helper.clear_file(archived_file)

            self._archive_file_summary(file_summary, content)

            self._file_read_write_helper.write_json_to_file(archived_file, content)

        except Exception as exception:
            self._logger.error(f"Exception found: {exception}")
            raise
        finally:
            self._file_system_helper.close_file(archived_file)
        self._logger.debug(f"Archive file updated: {archive_file_path}")

    def _archive_file(self, file, time_of_transfer, type_of_transfer):
        size = self._file_system_helper.file_size(file.abs_path)
        return {"file": file.file_name,
                "size": size,
                "latest update": time_of_transfer,
                "type of transfer": type_of_transfer}

    def _archive_file_summary(self, file_summary, content):
        time_of_transfer = str(current_time_in_utc())
        for file in file_summary.new_files:
            content[file.file_name] = self._archive_file(file, time_of_transfer, "new upload")

        for file in file_summary.updated_files:
            content[file.file_name] = self._archive_file(file, time_of_transfer, "file update")
