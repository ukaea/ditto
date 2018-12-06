import configparser
import os

from tornado_json import exceptions
from DittoWebApi.src.utils.parse_strings import str2list


class BucketSetting:
    def __init__(self, properties):
        self._groups = str2list(properties['groups'])
        self._root_dir = properties['root']

    @property
    def root_dir(self):
        return self._root_dir

    @property
    def groups(self):
        return self._groups


class BucketSettingsService:
    def __init__(self, bucket_settings_path, configuration, logger):
        self._bucket_settings_path = bucket_settings_path
        if not os.path.exists(self._bucket_settings_path):
            raise RuntimeError(f'The bucket settings file "{self._bucket_settings_path}" does not seem to exist.')
        self._admin_groups = configuration.admin_groups
        self._logger = logger
        self._settings = {}
        self._parse(self._bucket_settings_path)

    def _parse(self, bucket_settings_path):
        settings = configparser.ConfigParser()
        settings.read(bucket_settings_path)
        self._settings = {bucket_name: BucketSetting(settings[bucket_name]) for bucket_name in settings.sections()}

    @property
    def admin_groups(self):
        return self._admin_groups

    def is_bucket_recognised(self, bucket_name):
        return bucket_name in self._settings

    def bucket_root_directory(self, bucket_name):
        if bucket_name in self._settings:
            return self._settings[bucket_name].root_dir
        self._logger.warning(f'Root directory requested for non-existent bucket "{bucket_name}"')
        raise exceptions.APIError(404, f'Bucket "{bucket_name}" does not exist')

    def bucket_permitted_groups(self, bucket_name):
        if bucket_name in self._settings:
            return self._settings[bucket_name].groups
        self._logger.warning(f'Permitted groups requested for non-existent bucket "{bucket_name}"')
        raise exceptions.APIError(404, f'Bucket "{bucket_name}" does not exist')