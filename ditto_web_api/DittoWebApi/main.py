import logging
from logging.handlers import RotatingFileHandler
import os
import tornado

from DittoWebApi.src.handlers.main_handler import MainHandler
from DittoWebApi.src.services.data_replication_service import DataReplicationService
from DittoWebApi.src.services.external_data_service import ExternalDataService
from DittoWebApi.src.services.internal_data_service import InternalDataService
from DittoWebApi.src.utils.configurations import Configuration


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
    configuration_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'configuration.ini'))
    CONFIGURATION = Configuration(configuration_path)

    # Set up logging
    LOGGER = setup_logger(CONFIGURATION.log_folder_location, logging.INFO)
    LOGGER.info("Starting DITTO Web API")

    # Set up services
    external_data_service = ExternalDataService(CONFIGURATION)
    internal_data_service = InternalDataService(CONFIGURATION)
    data_replication_service = DataReplicationService(external_data_service, internal_data_service, LOGGER)

    # Launch app
    app = tornado.web.Application([
        (r"/", MainHandler, dict(data_replication_service=data_replication_service)),
    ])

    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
