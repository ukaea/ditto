# pylint: disable=R0201
import os


class FileSystemHelper:
    def absolute_file_path(self, file_path):
        return os.path.abspath(file_path)

    def canonical_path(self, path):
        return os.path.realpath(path)

    def close_file(self, open_file):
        if not open_file.closed:
            open_file.close()

    def create_and_open_file_for_writing(self, file_path):
        return open(file_path, "w")

    def does_path_exist(self, path):
        return os.path.exists(path)

    def file_directory(self, file_rel_path):
        return os.path.dirname(file_rel_path)

    def file_name(self, abs_file_path):
        return os.path.basename(abs_file_path)

    def file_size(self, abs_file_path):
        return os.stat(abs_file_path).st_size

    def find_all_files_in_folder(self, directory):
        list_of_files = []
        for path, dummy_subdirs, files in os.walk(directory):
            for name in files:
                list_of_files.append(self.join_paths(path, name))
        return list_of_files

    def is_file(self, path):
        return os.path.isfile(path)

    def join_paths(self, directory, file_name):
        return os.path.join(directory, file_name)

    def last_modified(self, file_path):
        return os.path.getmtime(file_path)

    def make_directory(self, directory_path):
        return os.makedirs(directory_path)

    def open_file_for_reading_and_writing(self, file_path):
        return open(file_path, 'r+')

    def relative_file_path(self, file_path, root_directory):
        return os.path.relpath(self.absolute_file_path(file_path), root_directory)
