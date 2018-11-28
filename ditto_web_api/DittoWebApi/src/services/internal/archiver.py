class Archiver:
    def __init__(self, file_system_helper, logger):
        self._logger = logger
        self._file_system_helper = file_system_helper

    # Current placeholder for processing contents of the archive files
    def update_content(self, old_content, new_content):
        return old_content + new_content
