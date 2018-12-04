from testScenarios.when.base_when_step import BaseWhenStep


class CreateBucketWhenSteps(BaseWhenStep):
    def authenticated_create_bucket_called_for_simple_bucket(self):
        handler = 'createbucket'
        body = {'bucket': self._context.standard_bucket_name}
        self._make_authorised_request(handler, body)

    def unauthenticated_create_bucket_called_for_simple_bucket(self):
        handler = 'createbucket'
        body = {'bucket': self._context.standard_bucket_name}
        self._make_unauthenticated_request(handler, body)

    def create_bucket_called_for_simple_bucket_with_no_user_credentials(self):
        handler = 'createbucket'
        body = {'bucket': self._context.standard_bucket_name}
        self._make_request_with_no_user_credentials(handler, body)

    def authenticated_create_bucket_called_with_name(self, name):
        handler = 'createbucket'
        body = {'bucket': name}
        self._make_authorised_request(handler, body)
