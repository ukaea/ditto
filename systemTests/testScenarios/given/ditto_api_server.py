import os
import subprocess
import time


class DittoApiServer:
    def __init__(self, context):
        self._context = context

    def is_started(self):
        self._write_configuration()
        self._start_ditto()

    def is_started_without_configuration(self):
        self._start_ditto()

    def _write_configuration(self):
        file_contents = \
            '[Settings]\n' \
            f'LogFolderLocation = {self._context.log_folder_path}\n'\
            f'LoggingLevel = {self._context.log_level}\n'\
            f'ApplicationPort = {self._context.app_port}\n'\
            f'S3Host = {self._context.s3host}\n'\
            f'S3Port = {self._context.s3port}\n'\
            f'S3AccessKey = {self._context.s3access}\n'\
            f'S3SecretKey = {self._context.s3secret}\n'\
            f'S3Secure = {self._context.s3secure}\n'\
            f'RootDirectory = {self._context.local_data_folder_path}\n'\
            f'BucketStandardisation = {self._context.bucket_standardisation}\n'

        config_file_path = os.path.join(
            self._context.ditto_web_api_folder_path,
            'DittoWebApi',
            'configuration.ini'
        )

        with open(config_file_path, 'w') as config_file:
            config_file.write(file_contents)

    def _start_ditto(self):
        path_of_file = os.path.dirname(os.path.realpath(__file__))
        web_api_script = os.path.join(path_of_file, 'runDittoWebApi.sh')

        self._context.ditto_api_process = subprocess.Popen(
            [web_api_script, self._context.ditto_web_api_folder_path],
            stdout=self._context.console_logger.stdout_log_writer,
            stderr=self._context.console_logger.stderr_log_writer,
            shell=True
        )

        # Let the server start
        time.sleep(2)
