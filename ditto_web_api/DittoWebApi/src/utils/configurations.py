import os
import configparser

from .parse_strings import str2bool
from .parse_strings import str2non_negative_int


class Configuration:
    def __init__(self, path_to_configuration_file):
        self._path_to_configuration_file = path_to_configuration_file

        if not os.path.exists(self._path_to_configuration_file):
            raise RuntimeError("The configuration file {} does not seem to exist. "
                               "Provide a configuration file".format(self._path_to_configuration_file))

        # Logging
        self._log_folder_location = None
        self._logging_level = "NOTSET"

        # S3 client
        self._s3_host = None
        self._s3_port = None
        self._s3_access_key = None
        self._s3_secret_key = None
        self._s3_use_secure = False

        # Local data
        self._root_dir = None

        self._parse(self._path_to_configuration_file)

    @property
    def log_folder_location(self):
        return self._log_folder_location

    @property
    def logging_level(self):
        return self._logging_level

    @property
    def s3_host(self):
        return self._s3_host

    @property
    def s3_port(self):
        return self._s3_port

    @property
    def s3_access_key(self):
        return self._s3_access_key

    @property
    def s3_secret_key(self):
        return self._s3_secret_key

    @property
    def s3_use_secure(self):
        return self._s3_use_secure

    @property
    def root_dir(self):
        return self._root_dir

    @property
    def bucket_standard(self):
        return self._bucket_standard

    def _parse(self, path):
        config = configparser.ConfigParser()
        config.read(path)
        settings = config["Settings"]

        # Logging
        self._log_folder_location = self.get_directory(settings, "LogFolderLocation")
        self._logging_level = settings["LoggingLevel"]

        # S3 client
        self._s3_host = settings['S3Host']
        self._s3_port = str2non_negative_int(settings['S3Port'])
        self._s3_access_key = settings['S3AccessKey']
        self._s3_secret_key = settings['S3SecretKey']
        self._s3_use_secure = str2bool(settings['S3Secure'])

        # Local data
        self._root_dir = os.path.abspath(settings['RootDirectory'])
        self._bucket_standard = settings['BucketStandardisation']

    @staticmethod
    def get_directory(settings, key):
        directory = settings[key]
        if not os.path.isdir(directory):
            raise ValueError("The directory {} for {} does not seem to exist. "
                             "Make sure to create it".format(directory, key))
        return directory
