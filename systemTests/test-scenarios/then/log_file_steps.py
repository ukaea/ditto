import os
import re

class LogFileSteps:
    def __init__(self, context, log_file_name):
        self._context = context
        self._log_file_name = os.path.join(context.execution_folder_path, 'logs/', log_file_name)

    def contains(self, expected_message):
        with open(self._log_file_name) as f:
          content = f.read()
          matches = re.search(expected_message, content)
          assert matches is not None
