# pylint: disable=R0201
import os
from DittoWebApi.src.utils.file_system.path_helpers import to_posix


class StorageDifferenceProcessor:

    def return_new_files(self, objects_in_bucket, files_in_directory, check_for_updates=False):
        """Returns a tuple of which the first element are the file information objects that are new
        and the second element is a list of the file information elements that need updating.
        When run with check_for_updates=False, doesn't look at if files need updating and thus
         always returns [] for files needing updating"""
        list_of_new_files = []
        files_to_update = []
        if not objects_in_bucket:
            return files_in_directory, files_to_update
        objects_to_check = [s3_obj for s3_obj in objects_in_bucket]
        for file_information in files_in_directory:
            if objects_to_check:
                matches = [self.are_the_same(s3_object, file_information) for s3_object in objects_to_check]
                if not any(matches):
                    list_of_new_files.append(file_information)
                else:
                    if check_for_updates:
                        if self.need_update(objects_to_check[matches.index(True)], file_information):
                            files_to_update.append(file_information)
                    del objects_to_check[matches.index(True)]
                files_in_directory.remove(file_information)
            else:
                list_of_new_files += files_in_directory
                break
        return list_of_new_files, files_to_update

    @staticmethod
    def are_the_same(s3_object, file_information):
        s3_object_name = s3_object.object_name
        return to_posix(file_information.rel_path) == to_posix(s3_object_name)

    @staticmethod
    def need_update(s3_object, file_information):
        return s3_object.last_modified < os.stat(file_information.abs_path).st_mtime
