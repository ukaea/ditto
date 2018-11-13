def new_files(files_in_bucket, files_in_directory):
    names_of_files_in_bucket = [file.file_name for file in files_in_bucket]
    list_of_new_files = [file_information_object
                         for file_information_object
                         in files_in_directory
                         if file_information_object.file_name
                         not in names_of_files_in_bucket]
    return list_of_new_files
