import logging
from logging.handlers import RotatingFileHandler
import os
import tornado
from DittoWebApi.src.handlers.list_present import ListPresentHandler
from DittoWebApi.src.handlers.copy_dir import CopyDirHandler
from DittoWebApi.src.handlers.create_bucket import CreatBucketHandler
from DittoWebApi.src.handlers.delete_file import DeleteFileHandler
from DittoWebApi.src.services.data_replication_service import DataReplicationService
from DittoWebApi.src.services.external_data_service import ExternalDataService
from DittoWebApi.src.services.internal_data_service import InternalDataService
from DittoWebApi.src.utils.configurations import Configuration
from DittoWebApi.src.utils.file_system.files_system_helpers import FileSystemHelper


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
    EXTERNAL_DATA_SERVICE = ExternalDataService(CONFIGURATION)
    INTERNAL_DATA_SERVICE = InternalDataService(CONFIGURATION, FileSystemHelper())
    DATA_REPLICATION_SERVICE = DataReplicationService(EXTERNAL_DATA_SERVICE, INTERNAL_DATA_SERVICE, LOGGER)

    # Launch app
    APP = tornado.web.Application([
        (r"/listpresent/(.*)", ListPresentHandler, dict(data_replication_service=DATA_REPLICATION_SERVICE)),
        (r"/copydir/(.*)", CopyDirHandler, dict(data_replication_service=DATA_REPLICATION_SERVICE)),
        (r"/createbucket/(.*)", CreatBucketHandler, dict(data_replication_service=DATA_REPLICATION_SERVICE)),
        (r"/deletefile/(.*)", DeleteFileHandler, dict(data_replication_service=DATA_REPLICATION_SERVICE)),
    ])
    APP.listen(8888)
    tornado.ioloop.IOLoop.current().start()
