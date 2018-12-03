import json


class FileReadWriteHelper:
    @staticmethod
    def write_json_to_file(open_file, json_content):
        json.dump(json_content, open_file)

    @staticmethod
    def read_file_as_json(open_file):
        return json.load(open_file)

    @staticmethod
    def clear_file(open_file):
        open_file.seek(0)
        open_file.truncate()
