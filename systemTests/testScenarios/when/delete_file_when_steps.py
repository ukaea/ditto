from testScenarios.when.base_when_step import BaseWhenStep


class DeleteFileWhenSteps(BaseWhenStep):
    def authorised_delete_file_is_called_for_simple_file_in_s3(self):
        handler = 'deletefile'
        body = {'bucket': self._context.standard_bucket_name, 'file': 'testA.txt'}
        self._make_authorised_request(handler, body)

    def unauthorised_delete_file_called_for_whole_directory(self):
        handler = 'deletefile'
        body = {'bucket': self._context.standard_bucket_name, 'file': 'testA.txt'}
        self._make_unauthorised_request(handler, body)

    def unauthenticated_delete_file_is_called_for_simple_file_in_s3(self):
        handler = 'deletefile'
        body = {'bucket': self._context.standard_bucket_name, 'file': 'testA.txt'}
        self._make_unauthenticated_request(handler, body)

    def delete_file_called_with_no_authorisation_credentials(self):
        handler = 'deletefile'
        body = {'bucket': self._context.standard_bucket_name, 'file': 'testA.txt'}
        self._make_request_with_no_user_credentials(handler, body)
