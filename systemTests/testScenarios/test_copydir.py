from testScenarios.context import BaseSystemTest


class TestTemplate(BaseSystemTest):
    def test_copy_dir(self):
        self.given.simple_test_file_is_setup()
        self.given.ditto_web_api.is_started()

        self.when.create_bucket_called_for_simple_bucket()
        self.when.copy_dir_called_for_whole_directory()
        #self.when.list_present_called_for_simple_bucket_whole_directory_structure()

        self.then.simple_bucket_exists_in_s3()
        self.then.new_file_exists_in_s3_bucket()
        #self.then.list_present_body_shows_newly_created_file()
