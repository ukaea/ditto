import os
import io


class ProcessLogger:
    def __init__(self, process_name, log_folder_path):
        self._stdout_log_path = os.path.join(log_folder_path, f'{process_name}-stdout.log')
        self._stderr_log_path = os.path.join(log_folder_path, f'{process_name}-stderr.log')
        self.stdout_log_writer = None
        self.stderr_log_writer = None

    def set_up(self):
        self.stdout_log_writer = io.open(self._stdout_log_path, 'wb', 0)
        self.stderr_log_writer = io.open(self._stderr_log_path, 'wb', 0)

    def clean_up(self):
        if self.stdout_log_writer is not None:
            self.stdout_log_writer.close()
        
        if self.stderr_log_writer is not None:
            self.stdout_log_writer.close()
