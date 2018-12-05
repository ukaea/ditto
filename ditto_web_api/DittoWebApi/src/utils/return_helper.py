from DittoWebApi.src.utils.return_status import StatusCodes


def return_transfer_summary(new_files_uploaded=0, files_updated=0, files_skipped=0, data_transferred=0, status=StatusCodes.Okay, message=""):
    return {"message": message,
            "new files uploaded": new_files_uploaded,
            "files updated": files_updated,
            "files skipped": files_skipped,
            "data transferred (bytes)": data_transferred,
            "status": status}


def return_bucket_message(message, bucket_name="", status=StatusCodes.Okay):
    return {"message": message,
            "bucket": bucket_name,
            "status": status}


def return_delete_file_helper(message, file_rel_path, bucket_name, status=StatusCodes.Okay):
    return {"message": message,
            "file": file_rel_path,
            "bucket": bucket_name,
            "status": status}


def return_list_present_helper(message, objects, status=StatusCodes.Okay):
    return {"message": message,
            "objects": objects,
            "status": status}
