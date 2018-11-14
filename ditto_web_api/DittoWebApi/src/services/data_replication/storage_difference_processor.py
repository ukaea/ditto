# pylint: disable=R0201
import os


class StorageDifferenceProcessor:

    def return_new_files(self, objects_in_bucket, files_in_directory, check_for_updates=False):
        list_of_new_files = []
        files_to_update = []
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
                    if check_for_updates:
                        if self.need_update(objects_to_check[matches.index(True)], file_information):
                            files_to_update.append(file_information)
                    del objects_to_check[matches.index(True)]
        return list_of_new_files, files_to_update

    @staticmethod
    def are_the_same(s3_object, file_information):
        s3_object_name = s3_object.object_name
        return file_information.rel_path == s3_object_name

    def need_update(self, s3_object, file_information):
        return s3_object.last_modified < os.stat(file_information.abs_path).st_mtime
