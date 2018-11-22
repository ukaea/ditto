# pylint: disable=R0913
import os
import tempfile

import pytest

from DittoWebApi.src.utils.configurations import Configuration


class SampleConfigurationCreator:
    @staticmethod
    def create_configuration(log_folder_loc,
                             logging_level,
                             app_port,
                             s3_host,
                             s3_port,
                             s3_access_key,
                             s3_secret_key,
                             s3_use_secure,
                             root_dir,
                             bucket_standard):
        template = "[Settings]\n"
        template = SampleConfigurationCreator.add_element_to_temp_file(template,
                                                                       "LogFolderLocation",
                                                                       log_folder_loc)
        template = SampleConfigurationCreator.add_element_to_temp_file(template,
                                                                       "LoggingLevel",
                                                                       logging_level)
        template = SampleConfigurationCreator.add_element_to_temp_file(template,
                                                                       "ApplicationPort",
                                                                       app_port)
        template = SampleConfigurationCreator.add_element_to_temp_file(template,
                                                                       "S3host",
                                                                       s3_host)
        template = SampleConfigurationCreator.add_element_to_temp_file(template,
                                                                       "S3port",
                                                                       s3_port)
        template = SampleConfigurationCreator.add_element_to_temp_file(template,
                                                                       "S3AccessKey",
                                                                       s3_access_key)
        template = SampleConfigurationCreator.add_element_to_temp_file(template,
                                                                       "S3SecretKey",
                                                                       s3_secret_key)
        template = SampleConfigurationCreator.add_element_to_temp_file(template,
                                                                       "S3Secure",
                                                                       s3_use_secure)
        template = SampleConfigurationCreator.add_element_to_temp_file(template,
                                                                       "RootDirectory",
                                                                       root_dir)
        template = SampleConfigurationCreator.add_element_to_temp_file(template,
                                                                       "BucketStandardisation",
                                                                       bucket_standard)
        return SampleConfigurationCreator.write_sample_configuration_file(template)

    @staticmethod
    def write_sample_configuration_file(file_content):
        temp = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        temp.write(file_content)
        path = temp.name
        temp.close()
        return path

    @staticmethod
    def add_element_to_temp_file(template, key, value):
        if value:
            template += "{} = {}\n".format(key, value)
        return template

    @staticmethod
    def remove_file(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)


def test_configuration_raises_when_path_is_not_correct():
    with pytest.raises(RuntimeError) as exception_info:
        path = "dummy_path"
        Configuration(path)
    assert("The configuration file dummy_path does not seem to exist."
           " Provide a configuration file" in str(exception_info.value))


def test_configuration_can_be_read_when_s3_secure():
    # Arrange
    current = os.getcwd()
    configuration_path = SampleConfigurationCreator.create_configuration(current,
                                                                         "INFO",
                                                                         "8888",
                                                                         "0.0.0.0",
                                                                         "9000",
                                                                         "access",
                                                                         "secret",
                                                                         "true",
                                                                         current,
                                                                         "test")

    # Act
    configuration = Configuration(configuration_path)

    # Assert
    assert configuration.log_folder_location == current
    assert configuration.s3_host == "0.0.0.0"
    assert configuration.s3_port == 9000
    assert configuration.s3_access_key == "access"
    assert configuration.s3_secret_key == "secret"
    assert configuration.s3_use_secure is True
    assert configuration.root_dir == current
    assert configuration.bucket_standard == "test"

    # Clean up
    SampleConfigurationCreator.remove_file(configuration_path)


def test_configuration_can_be_read_when_s3_not_secure():
    # Arrange
    current = os.getcwd()
    configuration_path = SampleConfigurationCreator.create_configuration(current,
                                                                         "INFO",
                                                                         "8888",
                                                                         "0.0.0.0",
                                                                         "9000",
                                                                         "access",
                                                                         "secret",
                                                                         "false",
                                                                         current,
                                                                         "test")

    # Act
    configuration = Configuration(configuration_path)

    # Assert
    assert configuration.log_folder_location == current
    assert configuration.s3_host == "0.0.0.0"
    assert configuration.s3_port == 9000
    assert configuration.s3_access_key == "access"
    assert configuration.s3_secret_key == "secret"
    assert configuration.s3_use_secure is False
    assert configuration.root_dir == current
    assert configuration.bucket_standard == "test"

    # Clean up
    SampleConfigurationCreator.remove_file(configuration_path)
