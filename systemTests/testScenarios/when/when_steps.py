import requests


class WhenSteps:
    def __init__(self, context):
        self._context = context

    def environment_is_stopped(self):
        self._context.shut_down_ditto_api()

    def something_happens(self):
        print(self.__class__)

    def create_bucket_called_for_simple_bucket(self):
        url = f'http://{self._context.s3host}:{self._context.app_port}/createbucket/'
        body = {'bucket': 'systemtest-textbucket'}
        response = requests.post(url, json=body)
        return response

    def copy_dir_called_for_whole_directory(self):
        url = f'http://{self._context.s3host}:{self._context.app_port}/copydir/'
        body = {'bucket': 'systemtest-textbucket'}
        response = requests.post(url, json=body)
        return response

    def list_present_called_for_simple_bucket_whole_directory_structure(self):
        url = f'http://{self._context.s3host}:{self._context.app_port}/listpresent/'
        body = {'bucket': 'systemtest-textbucket'}
        response = requests.post(url, json=body)
        return response
