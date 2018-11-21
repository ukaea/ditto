# pylint: disable=R0903
class FilesStorageSummary:
    def __init__(self, files_in_directory):
        self.files_in_directory = files_in_directory
        self.new_files = []
        self.updated_files = []

    def number_files_to_be_skipped(self):
        return len([file for file in self.files_in_directory if file not in self.new_files + self.updated_files])
