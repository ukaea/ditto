import mock

from DittoWebApi.src.models.file_storage_summary import FilesStorageSummary
from DittoWebApi.src.models.file_information import FileInformation


def build_mock_file_summary(files_in_dir=None, new_files=None, updated_files=None, files_to_be_skipped=None):
    mock_file_summary = mock.create_autospec(FilesStorageSummary)
    mock_file_summary.file_in_directory = files_in_dir if files_in_dir else []
    mock_file_summary.new_files = new_files if new_files else []
    mock_file_summary.updated_files = updated_files if updated_files else None
    mock_file_summary.files_to_be_skipped.return_value = files_to_be_skipped if files_to_be_skipped else None
    return mock_file_summary


def build_mock_file_information(file_name, rel_path, abs_path):
    mock_file_information = mock.create_autospec(FileInformation)
    mock_file_information.file_name = file_name
    mock_file_information.rel_path = rel_path
    mock_file_information.abs_path = abs_path
    return mock_file_information


def build_transfer_return(new, updated, skipped, data, message="Transfer successful"):
    return {"message": message,
            "new_files_uploaded": new,
            "files_updated": updated,
            "files_skipped": skipped,
            "data_transferred": data}
