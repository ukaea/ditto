import json


class FileReadWriteHelper:
    @staticmethod
    def clear_file(open_file):
        open_file.seek(0)
        open_file.truncate()

    @staticmethod
    def read_file_as_json(open_file):
        return json.load(open_file)

    @staticmethod
    def read_file_path_as_text(file_path):
        with open(file_path, 'r') as file:
            text = file.read()
        return text

    @staticmethod
    def write_json_to_file(open_file, json_content):
        json.dump(json_content, open_file)

    @staticmethod
    def write_text_to_file_path(file_path, text):
        with open(file_path, 'w') as file:
            file.write(text)
