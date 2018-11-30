from testScenarios.when.base_when_step import BaseWhenStep


class CopyDirWhenSteps(BaseWhenStep):
    def authorised_copy_dir_called_for_whole_directory(self):
        handler = 'copydir'
        body = {'bucket': self._context.standard_bucket_name}
        self._make_authorised_request(handler, body)

    def unauthorised_copy_dir_called_for_whole_directory(self):
        handler = 'copydir'
        body = {'bucket': self._context.standard_bucket_name}
        self._make_unauthorised_request(handler, body)

    def copy_dir_called_with_no_authorisation_credentials(self):
        handler = 'copydir'
        body = {'bucket': self._context.standard_bucket_name}
        self._make_request_with_no_authorisation_credentials(handler, body)

    def authorised_copy_dir_called_for_sub_directory(self):
        handler = 'copydir'
        body = {'bucket': self._context.standard_bucket_name, 'directory': 'sub_dir_A'}
        self._make_authorised_request(handler, body)