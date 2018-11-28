# pylint: disable=R0201
import os
import json


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

    def file_size(self, abs_file_path):
        return os.stat(abs_file_path).st_size

    def create_file(self, file_path, content):
        with open(file_path, "w+") as file:
            json.dump(content, file)

    def does_file_exist(self, file_path):
        return os.path.exists(file_path)

    def load_content(self, file_path):
        with open(file_path, 'rt') as file:
            content = json.loads(file)
        return content
