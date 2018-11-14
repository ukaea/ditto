# pylint: disable=R0201
from DittoWebApi.src.utils.file_system.path_helpers import to_posix


class StorageDifferenceProcessor:

    def return_new_files(self, objects_in_bucket, files_in_directory):
        list_of_new_files = []
        if not objects_in_bucket:
            return files_in_directory
        objects_to_check = [s3_obj for s3_obj in objects_in_bucket]
        for file_information in files_in_directory:
            if not objects_to_check:
                list_of_new_files.append(file_information)
            else:
                matches = [self.are_the_same(s3_object, file_information) for s3_object in objects_to_check]
                if not any(matches):
                    list_of_new_files.append(file_information)
                else:
                    del objects_to_check[matches.index(True)]
        return list_of_new_files

    @staticmethod
    def are_the_same(s3_object, file_information):
        s3_object_name = s3_object.object_name
        return to_posix(file_information.rel_path) == to_posix(s3_object_name)
