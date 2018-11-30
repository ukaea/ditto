import logging
import os
import tempfile

import mock
import pytest

from DittoWebApi.src.services.bucket_settings_service import BucketSettingsService


class SampleSettingsCreator:
    @staticmethod
    def create_settings(bucket_list):
        content = "\n".join([SampleSettingsCreator.item_as_bucket_setting(item) for item in bucket_list])
        path = SampleSettingsCreator.write_bucket_settings(content)
        return path

    @staticmethod
    def item_as_bucket_setting(item):
        bucket = item[0]
        groups = item[1]
        root_dir = item[2]
        return f'[{bucket}]\ngroups = {groups}\nroot = {root_dir}\n'

    @staticmethod
    def write_bucket_settings(content):
        temp = tempfile.NamedTemporaryFile(mode='w', delete=False)
        temp.write(content)
        path = temp.name
        temp.close()
        return path

    @staticmethod
    def remove_file(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)


def test_settings_raises_when_path_is_not_correct():
    # Arrange
    path = "dummy_path"
    mock_logger = mock.create_autospec(logging.Logger)
    # Act
    with pytest.raises(RuntimeError) as exception_info:
        BucketSettingsService(path, mock_logger)
    # Assert
    assert 'The bucket settings file "dummy_path" does not seem to exist.' in str(exception_info.value)


# pylint: disable=protected-access
def test_settings_loads_empty_file():
    # Arrange
    bucket_settings_path = SampleSettingsCreator.create_settings([])
    mock_logger = mock.create_autospec(logging.Logger)
    # Act
    test_service = BucketSettingsService(bucket_settings_path, mock_logger)
    # Assert
    assert isinstance(test_service._settings, dict)
    assert not test_service._settings


# pylint: disable=protected-access
def test_settings_loads_single_bucket_settings_with_single_group():
    # Arrange
    bucket_settings_path = SampleSettingsCreator.create_settings([('test-bucket', 'group', '/usr/tmp/ditto')])
    mock_logger = mock.create_autospec(logging.Logger)
    # Act
    test_service = BucketSettingsService(bucket_settings_path, mock_logger)
    # Assert
    assert len(test_service._settings) == 1
    assert test_service.is_bucket_recognised('test-bucket')
    assert test_service.bucket_permitted_groups('test-bucket') == ['group']
    assert test_service.bucket_root_directory('test-bucket') == '/usr/tmp/ditto'


# pylint: disable=protected-access
def test_settings_loads_single_bucket_settings_with_multiple_groups():
    # Arrange
    bucket_settings_path = SampleSettingsCreator.create_settings([('test-bucket', 'group1,group2', '/usr/tmp/ditto')])
    mock_logger = mock.create_autospec(logging.Logger)
    # Act
    test_service = BucketSettingsService(bucket_settings_path, mock_logger)
    # Assert
    assert len(test_service._settings) == 1
    assert test_service.is_bucket_recognised('test-bucket')
    assert test_service.bucket_permitted_groups('test-bucket') == ['group1', 'group2']
    assert test_service.bucket_root_directory('test-bucket') == '/usr/tmp/ditto'


# pylint: disable=protected-access
def test_settings_loads_multiple_bucket_settings():
    # Arrange
    bucket_settings_path = SampleSettingsCreator.create_settings([
        ('test-bucket', 'group1,group2', '/usr/tmp/ditto'),
        ('test-other', 'admin', '/usr/tmp/other')
    ])
    mock_logger = mock.create_autospec(logging.Logger)
    # Act
    test_service = BucketSettingsService(bucket_settings_path, mock_logger)
    # Assert
    assert len(test_service._settings) == 2
    assert test_service.is_bucket_recognised('test-bucket')
    assert test_service.bucket_permitted_groups('test-bucket') == ['group1', 'group2']
    assert test_service.bucket_root_directory('test-bucket') == '/usr/tmp/ditto'
    assert test_service.is_bucket_recognised('test-other')
    assert test_service.bucket_permitted_groups('test-other') == ['admin']
    assert test_service.bucket_root_directory('test-other') == '/usr/tmp/other'
