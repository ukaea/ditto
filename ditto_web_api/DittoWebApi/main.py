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
from DittoWebApi.src.services.data_replication.data_replication_service import DataReplicationService
from DittoWebApi.src.services.data_replication.storage_difference_processor import StorageDifferenceProcessor
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


if __name__ == "__main__":
    # Read configuration
    CONFIGURATION_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'configuration.ini'))
    CONFIGURATION = Configuration(CONFIGURATION_PATH)

    # Set up logging
    LOGGER = setup_logger(CONFIGURATION.log_folder_location, CONFIGURATION.logging_level)
    LOGGER.info("Starting DITTO Web API")

    # Set up services
    S3_ADAPTER = BotoAdapter(CONFIGURATION, LOGGER)
    FILE_READ_WRITE_HELPER = FileReadWriteHelper()
    FILE_SYSTEM_HELPER = FileSystemHelper()
    ARCHIVER = Archiver(FILE_READ_WRITE_HELPER, FILE_SYSTEM_HELPER, LOGGER)
    EXTERNAL_DATA_SERVICE = ExternalDataService(CONFIGURATION, FILE_SYSTEM_HELPER, LOGGER, S3_ADAPTER)
    INTERNAL_DATA_SERVICE = InternalDataService(ARCHIVER, CONFIGURATION, FILE_SYSTEM_HELPER, LOGGER)
    STORAGE_DIFFERENCE_PROCESSOR = StorageDifferenceProcessor(LOGGER)
    DATA_REPLICATION_SERVICE = DataReplicationService(EXTERNAL_DATA_SERVICE,
                                                      INTERNAL_DATA_SERVICE,
                                                      STORAGE_DIFFERENCE_PROCESSOR,
                                                      LOGGER)

    # Security (PLACEHOLDER CODE)
    SECURITY_CONFIGURATION_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'security_configuration.ini'))
    SECURITY_SERVICE = ConfigSecurityService(SECURITY_CONFIGURATION_PATH, LOGGER)

    # Launch app
    CONTAINER = dict(
        data_replication_service=DATA_REPLICATION_SERVICE,
        security_service=SECURITY_SERVICE
    )
    APP = tornado.web.Application([
        ("(|/)", HeartbeatHandler),
        (format_route_specification("listpresent"), ListPresentHandler, CONTAINER),
        (format_route_specification("copydir"), CopyDirHandler, CONTAINER),
        (format_route_specification("createbucket"), CreateBucketHandler, CONTAINER),
        (format_route_specification("deletefile"), DeleteFileHandler, CONTAINER),
        (format_route_specification("copynew"), CopyNewHandler, CONTAINER),
        (format_route_specification("copyupdate"), CopyUpdateHandler, CONTAINER),
    ])
    LOGGER.info(f'DITTO Web API listening on port {CONFIGURATION.app_port}')
    APP.listen(CONFIGURATION.app_port)
    tornado.ioloop.IOLoop.current().start()
