# pylint: disable=R0201
import os


class FileSystemHelper:
    def join_paths(self, directory, file_name):
        return os.path.join(directory, file_name)

    def find_all_files_in_folder(self, directory):
        list_of_files = []
        for path, dummy_subdirs, files in os.walk(directory):
            for name in files:
                list_of_files.append(self.join_paths(path, name))
        return list_of_files

    def absolute_file_path(self, file_path):
        return os.path.abspath(file_path)

    def relative_file_path(self, file_path, root_directory):
        return os.path.relpath(self.absolute_file_path(file_path), root_directory)

    def file_name(self, abs_file_path):
        return os.path.basename(abs_file_path)

    def last_modified(self, file_path):
        return os.path.getmtime(file_path)
