import configparser
from tornado_json import exceptions

from DittoWebApi.src.utils.config_helper import config_to_string
from DittoWebApi.src.utils.file_read_write_helper import FileReadWriteHelper
from DittoWebApi.src.utils.file_system.files_system_helpers import FileSystemHelper
from DittoWebApi.src.utils.parse_strings import str2list


class BucketSetting:
    def __init__(self, properties):
        self._groups = str2list(properties['groups']) if isinstance(properties['groups'], str) else properties['groups']
        self._archive_root_dir = properties['archive_root'] if 'archive_root' in properties else properties['data_root']
        self._data_root_dir = properties['data_root']

    @property
    def groups(self):
        return self._groups

    @property
    def data_root_dir(self):
        return self._data_root_dir

    @property
    def archive_root_dir(self):
        return self._archive_root_dir


class BucketSettingsService:
    def __init__(self, bucket_settings_path, configuration, file_read_write_helper, file_system_helper, logger):
        self._bucket_settings_path = bucket_settings_path
        self._file_system_helper = file_system_helper
        self._admin_groups = configuration.admin_groups
        self._file_read_write_helper = file_read_write_helper
        self._logger = logger
        self._settings = {}
        if self._file_system_helper.does_path_exist(self._bucket_settings_path):
            self._parse(self._bucket_settings_path)
        elif self._file_system_helper.does_path_exist(
                self._file_system_helper.file_directory(self._bucket_settings_path)):
            self._logger.info(f'The bucket settings file "{self._bucket_settings_path}" does not seem to exist.'
                              ' Will write settings into that path once buckets are added.')
        else:
            raise RuntimeError(f'Neither the bucket settings file "{self._bucket_settings_path}",'
                               ' nor its directory seem to exist.')

    def _parse(self, bucket_settings_path):
        settings = configparser.ConfigParser()
        text = self._file_read_write_helper.read_file_path_as_text(bucket_settings_path)
        settings.read_string(text)
        self._settings = {bucket_name: BucketSetting(settings[bucket_name]) for bucket_name in settings.sections()}

    def _write_settings(self):
        settings = configparser.ConfigParser()
        for bucket_name, setting in self._settings.items():
            settings[bucket_name] = {}
            groups = ','.join(setting.groups)
            settings[bucket_name]['groups'] = groups
            settings[bucket_name]['archive_root'] = setting.archive_root_dir
            settings[bucket_name]['data_root'] = setting.data_root_dir
        text = config_to_string(settings)
        self._file_read_write_helper.write_text_to_file_path(self._bucket_settings_path, text)

    @property
    def admin_groups(self):
        return self._admin_groups

    def add_bucket(self, bucket_name, groups, archive_root_dir, data_root_dir):
        if self.is_bucket_recognised(bucket_name):
            raise exceptions.APIError(404, f'Bucket "{bucket_name}" already exists')
        self._logger.info(f'Adding new bucket "{bucket_name}" to settings')
        new_setting = BucketSetting({'groups': groups, 'archive_root': archive_root_dir, 'data_root': data_root_dir})
        self._settings[bucket_name] = new_setting
        self._write_settings()

    def bucket_permitted_groups(self, bucket_name):
        if bucket_name in self._settings:
            return self._settings[bucket_name].groups
        self._logger.warning(f'Permitted groups requested for non-existent bucket "{bucket_name}"')
        raise exceptions.APIError(404, f'Bucket "{bucket_name}" does not exist')

    def bucket_data_root_directory(self, bucket_name):
        if bucket_name in self._settings:
            return self._settings[bucket_name].data_root_dir
        self._logger.warning(f'Data root directory requested for non-existent bucket "{bucket_name}"')
        raise exceptions.APIError(404, f'Bucket "{bucket_name}" does not exist')

    def bucket_archive_root_directory(self, bucket_name):
        if bucket_name in self._settings:
            return self._settings[bucket_name].archive_root_dir
        self._logger.warning(f'Archive root directory requested for non-existent bucket "{bucket_name}"')
        raise exceptions.APIError(404, f'Bucket "{bucket_name}" does not exist')

    def is_bucket_recognised(self, bucket_name):
        return bucket_name in self._settings


def build_standard_bucket_settings_service(bucket_settings_path, configuration, logger):
    file_read_write_helper = FileReadWriteHelper()
    file_system_helper = FileSystemHelper()
    service = BucketSettingsService(
        bucket_settings_path,
        configuration,
        file_read_write_helper,
        file_system_helper,
        logger
    )
    return service
