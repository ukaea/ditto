class Archiver:
    def __init__(self, file_system_helper, logger):
        self._logger = logger
        self._file_system_helper = file_system_helper

    def write_archive(self, file_path, file_summary):
        content = "test"
        self._file_system_helper.create_file(file_path, content)
        self._logger.debug("Archive file created")

    def update_archive(self, file_path, file_summary):
        content = "test test"
        try:
            archived_file = self._file_system_helper.open_file(file_path)
            archived_file.write(content)

        except Exception as exception:
            self._logger.debug(f"Exception found: {exception}")
            raise
        finally:
            self._file_system_helper.close_file(archived_file)
        self._logger.debug("Archive file updated")
