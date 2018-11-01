import mock
import pytest

from DittoWebApi.src.services.external_data_service import ExternalDataService
from DittoWebApi.src.services.data_replication_service import DataReplicationService
from DittoWebApi.src.services.internal_data_service import InternalService



class DataReplicationServiceTest:
    # @pytest.fixture
    @staticmethod
    def setup(self):
        self.mock_external_data_service = mock.create_autospec(ExternalDataService)
        self.mock_internal_data_service = mock.create_autospec(InternalService)


        self.test_service = DataReplicationService(self.mock_external_data_service, self.mock_internal_data_service, self.mock_logger)

    # @pytest.mark.gen_test
    def test_replicate_data_returns_all_folders(self):
        # Arrange
        self.setup()
        self.mock_external_data_service.list_all_objects.return_value = ["foo", "bar"]
        # Act
        output = self.test_service.replicate_data()
        # Assert
        assert output[0] == "foo"