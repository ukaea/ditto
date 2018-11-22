import requests


class WhenSteps:
    def __init__(self, context):
        self._context = context

    def environment_is_stopped(self):
        self._context.shut_down_ditto_api()

    def something_happens(self):
        print(self.__class__)

    def create_bucket_called_for_simple_bucket(self):
        url = f'http://{self._context.s3host}:{self._context.s3port}/createbucket/'
        body = {'bucket': 'systemtest-textbucket'}
        print(url)
        response = requests.post(url, data=body)
        print(response.status_code)
        return response
