class Archiver:
    def __init__(self, logger):
        self._logger = logger

    # Current placeholder for processing contents of the archive files
    def update_content(self, old_content, new_content):
        return old_content + new_content
