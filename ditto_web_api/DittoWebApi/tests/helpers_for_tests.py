import mock

from DittoWebApi.src.models.file_storage_summary import FilesStorageSummary
from DittoWebApi.src.models.file_information import FileInformation

def build_mock_file_summary():
    mock_file_summary = mock.create_autospec(FilesStorageSummary)
    mock_file_summary.file_in_directory = []
    mock_file_summary.new_files = []
    mock_file_summary.updated_files = []
    mock_file_summary.files_to_be_skipped = []
    return mock_file_summary

def build_mock_file_information(file_name, rel_path, abs_path):
    mock_file_information = mock.create_autospec(FileInformation)
    mock_file_information.file_name = file_name
    mock_file_information.rel_path = rel_path
    mock_file_information.abs_path = abs_path
