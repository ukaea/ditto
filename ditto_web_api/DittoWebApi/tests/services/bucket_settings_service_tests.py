import logging
import mock
import pytest
import unittest

from DittoWebApi.src.services.bucket_settings_service import BucketSettingsService
from DittoWebApi.src.utils.configurations import Configuration
from DittoWebApi.src.utils.file_read_write_helper import FileReadWriteHelper
from DittoWebApi.src.utils.file_system.files_system_helpers import FileSystemHelper


class BucketSettingsServiceTest(unittest.TestCase):
    # pylint: disable=attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_bucket_settings_path = "/path/to/file/bucket_settings.ini"
        self.mock_configuration = mock.create_autospec(Configuration)
        self.mock_file_read_write_helper = mock.create_autospec(FileReadWriteHelper)
        self.mock_file_system_helper = mock.create_autospec(FileSystemHelper)
        self.mock_logger = mock.create_autospec(logging.Logger)

    # pylint: disable=attribute-defined-outside-init
    def initialise_service_with_admin_groups(self, admin_groups):
        self.mock_configuration.admin_groups = admin_groups
        self.test_service = BucketSettingsService(
            self.mock_bucket_settings_path,
            self.mock_configuration,
            self.mock_file_read_write_helper,
            self.mock_file_system_helper,
            self.mock_logger
        )

    def test_settings_raises_when_path_is_not_correct(self):
        # Arrange
        self.mock_file_system_helper.does_file_exist.return_value = False
        # Act
        with pytest.raises(RuntimeError) as exception_info:
            self.initialise_service_with_admin_groups(['admin'])
        # Assert
        self.mock_file_system_helper.does_file_exist.assert_called_once_with(self.mock_bucket_settings_path)
        assert 'The bucket settings file "/path/to/file/bucket_settings.ini" does not seem to exist.' \
               in str(exception_info.value)

    def test_settings_loads_empty_file(self):
        # Arrange
        self.mock_file_system_helper.does_file_exist.return_value = True
        self.mock_file_read_write_helper.read_file_path_as_text.return_value = ''
        # Act
        self.initialise_service_with_admin_groups(['admin'])
        # Assert
        self.mock_file_system_helper.does_file_exist.assert_called_once_with(self.mock_bucket_settings_path)
        self.mock_file_read_write_helper.read_file_path_as_text.assert_called_once_with(self.mock_bucket_settings_path)
        assert isinstance(self.test_service._settings, dict)
        assert not self.test_service._settings

    def test_settings_loads_single_bucket_settings_with_single_group(self):
        # Arrange
        self.mock_file_read_write_helper.read_file_path_as_text.return_value = \
            '[test-bucket]\ngroups = group\nroot = /usr/tmp/ditto\n'
        # Act
        self.initialise_service_with_admin_groups(['admin'])
        # Assert
        assert len(self.test_service._settings) == 1
        assert self.test_service.is_bucket_recognised('test-bucket')
        assert self.test_service.bucket_permitted_groups('test-bucket') == ['group']
        assert self.test_service.bucket_root_directory('test-bucket') == '/usr/tmp/ditto'

    def test_settings_loads_single_bucket_settings_with_multiple_groups(self):
        # Arrange
        self.mock_file_read_write_helper.read_file_path_as_text.return_value = \
            '[test-bucket]\ngroups = group1,group2\nroot = /usr/tmp/ditto\n'
        # Act
        self.initialise_service_with_admin_groups(['admin'])
        # Assert
        assert len(self.test_service._settings) == 1
        assert self.test_service.is_bucket_recognised('test-bucket')
        assert self.test_service.bucket_permitted_groups('test-bucket') == ['group1', 'group2']
        assert self.test_service.bucket_root_directory('test-bucket') == '/usr/tmp/ditto'

    def test_settings_loads_multiple_bucket_settings(self):
        # Arrange
        self.mock_file_read_write_helper.read_file_path_as_text.return_value = \
            '[test-bucket]\ngroups = group1,group2\nroot = /usr/tmp/ditto\n\n' \
            '[test-other]\ngroups = admin\nroot = /usr/tmp/other'
        # Act
        self.initialise_service_with_admin_groups(['admin'])
        # Assert
        assert len(self.test_service._settings) == 2
        assert self.test_service.is_bucket_recognised('test-bucket')
        assert self.test_service.bucket_permitted_groups('test-bucket') == ['group1', 'group2']
        assert self.test_service.bucket_root_directory('test-bucket') == '/usr/tmp/ditto'
        assert self.test_service.is_bucket_recognised('test-other')
        assert self.test_service.bucket_permitted_groups('test-other') == ['admin']
        assert self.test_service.bucket_root_directory('test-other') == '/usr/tmp/other'

    def test_add_bucket_appends_new_settings_to_file(self):
        # Arrange
        self.mock_file_read_write_helper.read_file_path_as_text.return_value = \
            '[test-bucket]\ngroups = group1,group2\nroot = /usr/tmp/ditto\n'
        # Act
        self.initialise_service_with_admin_groups(['admin'])
        self.test_service.add_bucket('test-other', 'admin', '/usr/tmp/other')
        # Assert
        self.mock_file_read_write_helper.write_text_to_file_path.assert_called_once_with(
            '[test-bucket]\ngroups = group\nroot = /usr/tmp/ditto\n\n'
            '[test-other]\ngroups = admin\nroot = /usr/tmp/other\n',
            self.mock_bucket_settings_path
        )
