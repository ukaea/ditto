from tornado_json import schema


class InputSchema:
    def bucket_and_directory(self):
        return {
            "type": "object",
            "properties": {
                "bucket": {"type": "string"},
                "directory": {"type": "string"},
            },
            "required": ["bucket"]
            }

    def bucket(self):
        return {
            "type": "object",
            "properties": {
                "bucket": {"type": "string"},
            },
            "required": ["bucket"]
            }

    def bucket_and_file(self):
        return {
            "type": "object",
            "properties": {
                "bucket": {"type": "string"},
                "file": {"type": "string"},
            },
            "required": ["bucket", "file"]
        }

    def bucket_and_directory_example(self):
        return {
            "bucket": "test-bucket-name",
            "directory": "testdir/testsubdir",
        }

    def bucket_example(self):
        return {
            "bucket": "test-bucket-name",
        }

    def bucket_and_file_example(self):
        return {
            "bucket": "test-bucket-name",
            "file": "path_to_file/file_name",
        }
