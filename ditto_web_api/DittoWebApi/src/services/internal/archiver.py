from DittoWebApi.src.utils.system_helper import current_time_in_utc
from DittoWebApi.src.utils.file_read_write_helper import clear_file
from DittoWebApi.src.utils.file_read_write_helper import read_file_as_json
from DittoWebApi.src.utils.file_read_write_helper import write_json_to_file


class Archiver:
    def __init__(self, file_system_helper, logger):
        self._logger = logger
        self._file_system_helper = file_system_helper

    def write_archive(self, archive_file_path, file_summary):
        time_of_transfer = str(current_time_in_utc())
        try:
            content = {}
            new_archive_file = self._file_system_helper.create_and_open_file_for_writing(archive_file_path)

            for file in file_summary.new_files:
                content[file.file_name] = self._archive_file(file, time_of_transfer, "new upload")

            for file in file_summary.updated_files:
                content[file.file_name] = self._archive_file(file, time_of_transfer, "file update")

            write_json_to_file(new_archive_file, content)
        except Exception as exception:
            self._logger.error(f"Exception found here: {exception}")
            raise
        finally:
            self._file_system_helper.close_file(new_archive_file)
        self._logger.debug(f"Archive file created: {archive_file_path}")

    def update_archive(self, archive_file_path, file_summary):
        time_of_transfer = str(current_time_in_utc())
        try:
            archived_file = self._file_system_helper.open_file_for_reading_and_writing(archive_file_path)
            content = read_file_as_json(archived_file)
            clear_file(archived_file)

            for file in file_summary.new_files:
                content[file.file_name] = self._archive_file(file, time_of_transfer, "new upload")[file.file_name]

            for file in file_summary.updated_files:
                content[file.file_name] = self._archive_update(file, time_of_transfer, "file update")[file.file_name]

            write_json_to_file(archived_file, content)

        except Exception as exception:
            self._logger.error(f"Exception found: {exception}")
            raise
        finally:
            self._file_system_helper.close_file(archived_file)
        self._logger.debug(f"Archive file updated: {archive_file_path}")

    def _archive_file(self, file, time_of_transfer, type_of_transfer):
        size = self._file_system_helper.file_size(file.abs_path)
        return {file.file_name: {"file": file.file_name,
                                 "size": size,
                                 "latest update": time_of_transfer,
                                 "type of transfer": type_of_transfer}
                }
