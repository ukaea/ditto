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

    def create_file(self, file_path):
        return open(file_path, "w")


    def does_file_exist(self, file_path):
        return os.path.exists(file_path)

    def open_file(self, file_path):
        return open(file_path, 'r+')

    def close_file(self, open_file):
        if not open_file.closed:
            open_file.close()

    def write_to_file(self, open_file, content):
        json.dump(content, open_file)


    def file_directory(self, file_rel_path):
        return os.path.dirname(file_rel_path)

    def load_json(self, open_file):
        pass

    def read_file_as_json(self, open_file):
        return json.load(open_file)


    def clear_file(self, open_file):
        open_file.seek(0)
        open_file.truncate()
