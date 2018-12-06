from testScenarios.when.base_when_step import BaseWhenStep


class CopyNewWhenSteps(BaseWhenStep):
    def authorised_copy_new_called_for_whole_directory(self):
        handler = 'copynew'
        body = {'bucket': self._context.standard_bucket_name}
        self._make_authorised_request(handler, body)

    def unauthorised_copy_new_called_for_whole_directory(self):
        handler = 'copynew'
        body = {'bucket': self._context.standard_bucket_name}
        self._make_unauthorised_request(handler, body)

    def unauthenticated_copy_new_called_for_whole_directory(self):
        handler = 'copynew'
        body = {'bucket': self._context.standard_bucket_name}
        self._make_unauthenticated_request(handler, body)

    def copy_new_called_with_no_authorisation_credentials(self):
        handler = 'copynew'
        body = {'bucket': self._context.standard_bucket_name}
        self._make_request_with_no_user_credentials(handler, body)

    def authorised_copy_new_called_for_directory_up_from_root(self):
        handler = 'copynew'
        body = {'bucket': self._context.standard_bucket_name, 'directory': '../data2'}
        self._make_authorised_request(handler, body)
