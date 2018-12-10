import os
import subprocess
import time

from testScenarios.tools.process_helper import print_port_state


class DittoApiServer:
    def __init__(self, context):
        self._context = context

    def is_started(self):
        self._write_configuration()
        self._write_security()
        self._write_bucket_settings()
        self._start_ditto()

    def is_started_without_bucket_settings(self):
        self._write_configuration()
        self._write_security()
        self._clear_bucket_settings()
        self._start_ditto()

    def is_started_without_configuration(self):
        self._start_ditto()

    def _write_configuration(self):
        file_contents = \
            '[Settings]\n' \
            f'LogFolderLocation = {self._context.log_folder_path}\n' \
            f'LoggingLevel = {self._context.log_level}\n' \
            f'AdminGroups = dittoadmin\n' \
            f'ApplicationPort = {self._context.app_port}\n' \
            f'S3Host = {self._context.host_address}\n' \
            f'S3Port = {self._context.s3port}\n' \
            f'S3AccessKey = {self._context.s3access}\n' \
            f'S3SecretKey = {self._context.s3secret}\n' \
            f'S3Secure = {self._context.s3secure}\n' \
            f'BucketStandardisation = {self._context.bucket_standardisation}\n' \
            f'ArchiveFileName = .ditto_archived\n'

        config_file_path = os.path.join(
            self._context.ditto_web_api_folder_path,
            'DittoWebApi',
            'configuration.ini'
        )

        with open(config_file_path, 'w') as config_file:
            config_file.write(file_contents)

    def _write_security(self):
        file_contents = \
            f'[{self._context.authentication_username}]\n' \
            f'password = {self._context.authentication_password}\n' \
            f'groups = {self._context.authentication_groups}\n' \
            '\n' \
            '[OtherUser]\n' \
            'password = password\n' \
            'groups = othergroup\n' \
            '\n' \
            '[AdminUser]\n' \
            'password = IamAdmin\n' \
            'groups = dittoadmin'

        security_file_path = os.path.join(
            self._context.ditto_web_api_folder_path,
            'DittoWebApi',
            'security_configuration.ini'
        )

        with open(security_file_path, 'w') as security_file:
            security_file.write(file_contents)

    def _write_bucket_settings(self):
        file_contents = \
            f'[{self._context.standard_bucket_name}]\n' \
                f'groups = {self._context.authentication_groups}\n'\
                f'root = {self._context.local_data_folder_path}\n'

        settings_file_path = os.path.join(
            self._context.ditto_web_api_folder_path,
            'DittoWebApi',
            'bucket_settings.ini'
        )

        with open(settings_file_path, 'w') as settings_file:
            settings_file.write(file_contents)

    def _clear_bucket_settings(self):
        settings_file_path = os.path.join(
            self._context.ditto_web_api_folder_path,
            'DittoWebApi',
            'bucket_settings.ini'
        )

        if os.path.exists(settings_file_path):
            os.remove(settings_file_path)

    def _start_ditto(self):
        path_of_file = os.path.dirname(os.path.realpath(__file__))
        web_api_script = os.path.join(path_of_file, 'runDittoWebApi.sh')

        print_port_state(self._context.host_address, self._context.app_port)

        print(f'Starting up DITTO on port {self._context.app_port}')

        self._context.ditto_api_process = subprocess.Popen(
            [web_api_script, self._context.ditto_web_api_folder_path],
            stdout=self._context.console_logger.stdout_log_writer,
            stderr=self._context.console_logger.stderr_log_writer,
            preexec_fn=os.setsid
        )

        timeout_counter = 0
        timeout_step = 0.5
        timeout_limit = 20
        while (not self._context.is_ditto_running()) and timeout_counter < timeout_limit:
            timeout_counter += 1
            time.sleep(timeout_step)
        if timeout_counter >= timeout_limit:
            print(f'Reached timeout of {timeout_step * timeout_limit} seconds waiting for DITTO to start up')
        else:
            print(f'DITTO took {timeout_counter * timeout_step} seconds to start up')
