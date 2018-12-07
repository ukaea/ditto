from testScenarios.when.base_when_step import BaseWhenStep


class ListPresentWhenSteps(BaseWhenStep):
    def authorised_list_present_called_for_simple_bucket_whole_directory_structure(self):
        handler = 'listpresent'
        body = {'bucket': self._context.standard_bucket_name}
        self._make_authorised_request(handler, body)

    def unauthorised_list_present_called_for_simple_bucket_whole_directory_structure(self):
        handler = 'listpresent'
        body = {'bucket': self._context.standard_bucket_name}
        self._make_unauthorised_request(handler, body)

    def list_present_called_with_no_authorisation_credentials(self):
        handler = 'listpresent'
        body = {'bucket': self._context.standard_bucket_name}
        self._make_request_with_no_user_credentials(handler, body)

    def unauthenticated_list_present_called_for_simple_bucket_whole_directory_structure(self):
        handler = 'listpresent'
        body = {'bucket': self._context.standard_bucket_name}
        self._make_unauthenticated_request(handler, body)

    def authorised_list_present_called_for_directory_up_from_root(self):
        handler = 'listpresent'
        body = {'bucket': self._context.standard_bucket_name, 'directory': '../data2'}
        self._make_authorised_request(handler, body)
