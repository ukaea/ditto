from DittoWebApi.src.utils.system_helper import current_time


class Archiver:
    def __init__(self, file_system_helper, logger):
        self._logger = logger
        self._file_system_helper = file_system_helper

    def write_archive(self, archive_file_path, file_summary):
        time_of_transfer = str(current_time())
        try:
            content = {}
            new_archive_file = self._file_system_helper.create_file(archive_file_path)
            for file in file_summary.new_files:
                new_content = self._archive_new_file(file, time_of_transfer)
                content.update(new_content)
            for file in file_summary.updated_files:
                new_content = self._archive_file_update(file, time_of_transfer)
                content.update(new_content)
            self._file_system_helper.write_to_file(new_archive_file, content)
        except Exception as exception:
            self._logger.error(f"Exception found here: {exception}")
            raise
        finally:
            self._file_system_helper.close_file(new_archive_file)
        self._logger.debug(f"Archive file created: {archive_file_path}")

    def update_archive(self, archive_file_path, file_summary):
        time_of_transfer = str(current_time())
        try:
            archived_file = self._file_system_helper.open_file(archive_file_path)
            content = self._convert_old_content_to_json(archived_file)
            self._logger.debug(f"Old archive file content {content}")
            self._file_system_helper.clear_file(archived_file)

            for file in file_summary.new_files:
                content[file.file_name] = self._archive_new_file(file, time_of_transfer)[file.file_name]

            for file in file_summary.updated_files:
                content[file.file_name] = self._archive_file_update(file, time_of_transfer)[file.file_name]

            self._file_system_helper.write_to_file(archived_file, content)

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
                                 "latest update": time_of_transfer,
                                 "type of transfer": "new upload"}
                }

    def _archive_file_update(self, file, time_of_transfer):
        size = self._file_system_helper.file_size(file.abs_path)
        return {file.file_name: {"file": file.file_name,
                                 "size": size,
                                 "latest update": time_of_transfer,
                                 "type of transfer": "file_update"}
                }

    def _convert_old_content_to_json(self, open_file):
        return self._file_system_helper.read_file_as_json(open_file)
