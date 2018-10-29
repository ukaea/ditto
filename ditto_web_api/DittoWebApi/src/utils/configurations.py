import os
import configparser

from .parse_strings import str2bool


class Configuration:
    def __init__(self, path_to_configuration_file):
        self._path_to_configuration_file = path_to_configuration_file

        if not os.path.exists(self._path_to_configuration_file):
            raise RuntimeError("The configuration file {} does not seem to exist. "
                               "Provide a configuration file".format(self._path_to_configuration_file))

        # Configurations
        self._s3_url = None
        self._s3_access_key = None
        self._s3_secret_key = None
        self._s3_use_secure = False
        self._parse(self._path_to_configuration_file)

    @property
    def s3_url(self):
        return self._s3_url

    @property
    def s3_access_key(self):
        return self._s3_access_key

    @property
    def s3_secret_key(self):
        return self._s3_secret_key

    @property
    def s3_use_secure(self):
        return self._s3_use_secure

    def _parse(self, path):
        config = configparser.ConfigParser()
        config.read(path)
        settings = config["Settings"]
        # S3
        self._s3_url = settings['S3Address']
        self._s3_access_key = settings['S3AccessKey']
        self._s3_secret_key = settings['S3SecretKey']
        self._s3_use_secure = str2bool(settings['S3Secure'])
