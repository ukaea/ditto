from testScenarios.when.base_when_step import BaseWhenStep


class CopyUpdateWhenSteps(BaseWhenStep):
    def authorised_copy_update_called_for_whole_directory(self):
        handler = 'copyupdate'
        body = {'bucket': self._context.standard_bucket_name}
        self._make_authorised_request(handler, body)

    def unauthorised_copy_update_called_for_whole_directory(self):
        handler = 'copyupdate'
        body = {'bucket': self._context.standard_bucket_name}
        self._make_unauthorised_request(handler, body)

    def unauthenticated_copy_update_called_for_whole_directory(self):
        handler = 'copyupdate'
        body = {'bucket': self._context.standard_bucket_name}
        self._make_unauthenticated_request(handler, body)

    def copy_update_called_with_no_authorisation_credentials(self):
        handler = 'copyupdate'
        body = {'bucket': self._context.standard_bucket_name}
        self._make_request_with_no_authorisation_credentials(handler, body)