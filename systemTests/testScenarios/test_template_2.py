from testScenarios.context import BaseSystemTest


class TestTemplate2(BaseSystemTest):
    def test_template(self):
        self.given.ditto_web_api.is_started()

        self.when.something_happens()

        self.then.thing_is_true()
