import logging
from logging.handlers import RotatingFileHandler
import os
import tornado
from DittoWebApi.src.handlers.heartbeat import HeartbeatHandler
from DittoWebApi.src.handlers.list_present import ListPresentHandler
from DittoWebApi.src.handlers.copy_dir import CopyDirHandler
from DittoWebApi.src.handlers.create_bucket import CreateBucketHandler
from DittoWebApi.src.handlers.delete_file import DeleteFileHandler
from DittoWebApi.src.handlers.copy_new import CopyNewHandler
from DittoWebApi.src.handlers.copy_update import CopyUpdateHandler
from DittoWebApi.src.services.bucket_settings_service import BucketSettingsService
from DittoWebApi.src.services.data_replication.data_replication_service import build_standard_data_replication_service
from DittoWebApi.src.services.external.external_data_service import ExternalDataService
from DittoWebApi.src.services.external.storage_adapters.boto_adapter import BotoAdapter
from DittoWebApi.src.services.internal.internal_data_service import InternalDataService
from DittoWebApi.src.services.internal.archiver import Archiver
from DittoWebApi.src.services.security.config_security_service import ConfigSecurityService
from DittoWebApi.src.utils.configurations import Configuration
from DittoWebApi.src.utils.file_system.files_system_helpers import FileSystemHelper
from DittoWebApi.src.utils.file_read_write_helper import FileReadWriteHelper
from DittoWebApi.src.utils.route_helper import format_route_specification


def setup_logger(log_file_location, level):
    # Set  up the logger
    logger = logging.getLogger("ditto-web-api")
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    logger.setLevel(level)

    # Set up console logging
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    # Set up file logging
    log_file_name = "ditto-web-api.log"
    full_path = os.path.join(log_file_location, log_file_name)
    file_handler = RotatingFileHandler(full_path, maxBytes=100*1024, backupCount=10)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def launch():
    # Read configuration
    configuration_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'configuration.ini'))
    configuration = Configuration(configuration_path)

    # Set up logging
    logger = setup_logger(configuration.log_folder_location, configuration.logging_level)
    logger.info("Starting DITTO Web API")

    # Bucket settings
    bucket_settings_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'bucket_settings.ini'))
    bucket_settings_service = BucketSettingsService(bucket_settings_path, configuration, logger)

    # Security (PLACEHOLDER CODE)
    security_configuration_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'security_configuration.ini'))
    security_service = ConfigSecurityService(security_configuration_path, logger)

    # Set up services
    s3_adapter = BotoAdapter(configuration, logger)
    file_read_write_helper = FileReadWriteHelper()
    file_system_helper = FileSystemHelper()
    archiver = Archiver(file_read_write_helper, file_system_helper, logger)
    external_data_service = ExternalDataService(configuration, file_system_helper, logger, s3_adapter)
    internal_data_service = InternalDataService(archiver, configuration, file_system_helper, logger)
    data_replication_service = build_standard_data_replication_service(bucket_settings_service,
                                                                       external_data_service,
                                                                       internal_data_service,
                                                                       logger)

    # Launch app
    container = dict(
        bucket_settings_service=bucket_settings_service,
        data_replication_service=data_replication_service,
        security_service=security_service
    )
    app = tornado.web.Application([
        ("(|/)", HeartbeatHandler),
        (format_route_specification("listpresent"), ListPresentHandler, container),
        (format_route_specification("copydir"), CopyDirHandler, container),
        (format_route_specification("createbucket"), CreateBucketHandler, container),
        (format_route_specification("deletefile"), DeleteFileHandler, container),
        (format_route_specification("copynew"), CopyNewHandler, container),
        (format_route_specification("copyupdate"), CopyUpdateHandler, container),
    ])
    logger.info(f'DITTO Web API listening on port {configuration.app_port}')
    app.listen(configuration.app_port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    launch()
