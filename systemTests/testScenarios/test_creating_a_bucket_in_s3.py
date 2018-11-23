from testScenarios.context import BaseSystemTest


class TestTemplate(BaseSystemTest):
    def test_template(self):
        self.given.ditto_web_api.is_started()

        response = self.when.create_bucket_called_for_simple_bucket()

        self.then.simple_bucket_exists_in_s3(response)
